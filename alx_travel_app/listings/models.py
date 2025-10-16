
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Payment(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    )

    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # currency units
    currency = models.CharField(max_length=10, default='ETB')  # or 'USD' etc.
    tx_ref = models.CharField(max_length=255, unique=True)  # merchant reference (our side)
    chapa_tx = models.CharField(max_length=255, blank=True, null=True)  # chapa transaction id / reference
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking} - {self.tx_ref} - {self.status}"


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    listing = models.ForeignKey(Listing, related_name="bookings", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="bookings", on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(check_in__lt=models.F("check_out")),
                name="check_in_before_check_out"
            )
        ]

    def __str__(self):
        return f"Booking by {self.user.username} for {self.listing.title}"


class Review(models.Model):
    listing = models.ForeignKey(Listing, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rating__gte=1) & models.Q(rating__lte=5),
                                   name="valid_rating_range")
        ]

    def __str__(self):
        return f"Review {self.rating}★ by {self.user.username} on {self.listing.title}"
