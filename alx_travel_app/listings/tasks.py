from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Payment


@shared_task
def send_payment_confirmation_email(payment_id):
    """
    Task to send payment confirmation email asynchronously.
    """
    try:
        payment = Payment.objects.select_related('booking', 'booking__user').get(id=payment_id)
    except Payment.DoesNotExist:
        return False

    user_email = payment.booking.user.email
    subject = f"Payment Confirmation for booking {payment.booking.id}"
    message = render_to_string(
        "emails/payment_confirmation.txt",
        {"payment": payment, "booking": payment.booking}
    )
    html_message = render_to_string(
        "emails/payment_confirmation.html",
        {"payment": payment, "booking": payment.booking}
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )
    return True


@shared_task
def send_booking_confirmation_email(user_email, booking_details):
    """
    Task to send booking confirmation email asynchronously.
    """
    subject = "Booking Confirmation - ALX Travel"
    message = f"""
    Dear Customer,

    Your booking has been confirmed successfully!

    Booking Details:
    {booking_details}

    Thank you for choosing ALX Travel!
    """
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )
    return "Email sent successfully"
