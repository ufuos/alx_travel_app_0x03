# listings/views.py
import uuid
import requests
from django.conf import settings
from rest_framework import viewsets, status, permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from bookings.models import Booking as BookingModel  # adjust import if needed
from .tasks import send_payment_confirmation_email  # Celery task for email

CHAPA_BASE = "https://api.chapa.co/v1"  # base URL (sandbox & live use same API base)


# ---------------------- CRUD VIEWSETS ----------------------

class ListingViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Listing
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [AllowAny]  # change to IsAuthenticatedOrReadOnly if authentication desired


class BookingViewSet(viewsets.ModelViewSet):
    """
    Provides CRUD for Booking
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [AllowAny]


# ---------------------- CHAPA PAYMENT INTEGRATION ----------------------

class InitiatePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Expects: booking_id, amount, return_url (optional)
        """
        user = request.user
        booking_id = request.data.get('booking_id')
        amount = request.data.get('amount')
        return_url = request.data.get('return_url')  # where chapa redirects after payment

        if not booking_id or not amount:
            return Response({"error": "booking_id and amount required"}, status=status.HTTP_400_BAD_REQUEST)

        # basic booking existence check
        try:
            booking = BookingModel.objects.get(id=booking_id, user=user)
        except BookingModel.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate a tx_ref (unique merchant reference)
        tx_ref = f"booking-{booking.id}-{uuid.uuid4().hex[:8]}"

        payment = Payment.objects.create(
            booking=booking,
            amount=amount,
            currency='ETB',  # change as needed or read from booking
            tx_ref=tx_ref,
            status='PENDING'
        )

        # Prepare payload per Chapa docs
        payload = {
            "amount": float(amount),
            "currency": "ETB",
            "tx_ref": tx_ref,
            "customer_name": f"{user.first_name} {user.last_name}" if user.first_name else user.username,
            "customer_email": user.email,
            "callback_url": request.build_absolute_uri("/api/listings/chapa/verify/"),  # optional
        }
        if return_url:
            payload["return_url"] = return_url

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
            "Content-Type": "application/json"
        }

        try:
            url = f"{CHAPA_BASE}/transaction/initialize"
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            # update payment status
            payment.status = 'FAILED'
            payment.save(update_fields=["status", "updated_at"])
            return Response({"error": "Failed to initialize payment", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        data = resp.json()
        # Chapa returns data with link e.g. data['data']['checkout_url'] or authorization_url — check actual response
        chapa_data = data.get('data') or {}
        checkout_url = chapa_data.get('checkout_url') or chapa_data.get('authorization_url') or chapa_data.get('url')

        # store chapa tx reference if available
        chapa_tx = chapa_data.get('id') or chapa_data.get('tx_ref') or chapa_data.get('reference')
        if chapa_tx:
            payment.chapa_tx = chapa_tx
            payment.save(update_fields=["chapa_tx"])

        return Response({
            "payment_id": payment.id,
            "tx_ref": payment.tx_ref,
            "checkout_url": checkout_url,
            "raw_response": data
        }, status=status.HTTP_200_OK)


class VerifyPaymentAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # Chapa callback might use this; secure appropriately

    def get(self, request, tx_ref=None):
        """
        GET /api/listings/chapa/verify/?tx_ref=booking-1-abcdef12
        or /api/listings/chapa/verify/<tx_ref>/
        """
        if not tx_ref:
            tx_ref = request.query_params.get('tx_ref')

        if not tx_ref:
            return Response({"error": "tx_ref required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = Payment.objects.get(tx_ref=tx_ref)
        except Payment.DoesNotExist:
            return Response({"error": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        }
        verify_url = f"{CHAPA_BASE}/transaction/verify/{tx_ref}"

        try:
            resp = requests.get(verify_url, headers=headers, timeout=15)
            resp.raise_for_status()
        except requests.RequestException as e:
            return Response({"error": "Verification call failed", "details": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        result = resp.json()
        # result['data']['status'] might contain 'success' or 'failed' depending on method
        status_from_chapa = (result.get('data') or {}).get('status')  # check docs for exact field

        if status_from_chapa and status_from_chapa.lower() == 'success':
            payment.status = 'COMPLETED'
            payment.save(update_fields=["status", "updated_at"])
            # enqueue email send (celery)
            send_payment_confirmation_email.delay(payment.id)
            return Response({"status": "COMPLETED", "raw_response": result}, status=status.HTTP_200_OK)
        else:
            payment.status = 'FAILED'
            payment.save(update_fields=["status", "updated_at"])
            return Response({"status": "FAILED", "raw_response": result}, status=status.HTTP_200_OK)
