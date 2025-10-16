# listings/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Payment

@shared_task
def send_payment_confirmation_email(payment_id):
    try:
        payment = Payment.objects.select_related('booking', 'booking__user').get(id=payment_id)
    except Payment.DoesNotExist:
        return False

    user_email = payment.booking.user.email
    subject = f"Payment Confirmation for booking {payment.booking.id}"
    message = render_to_string("emails/payment_confirmation.txt", {"payment": payment, "booking": payment.booking})
    html_message = render_to_string("emails/payment_confirmation.html", {"payment": payment, "booking": payment.booking})

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        html_message=html_message,
        fail_silently=False,
    )
    return True
