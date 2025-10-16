
# listings/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, BookingViewSet, InitiatePaymentAPIView, VerifyPaymentAPIView

router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    path('', include(router.urls)),
    # Chapa payment endpoints
    path('chapa/initiate/', InitiatePaymentAPIView.as_view(), name='chapa-initiate'),
    path('chapa/verify/', VerifyPaymentAPIView.as_view(), name='chapa-verify'),  # accepts ?tx_ref=...
    path('chapa/verify/<str:tx_ref>/', VerifyPaymentAPIView.as_view(), name='chapa-verify-tx'),
]
