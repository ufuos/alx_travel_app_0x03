from django.core.management.base import BaseCommand
from listings.models import Listing
from django.contrib.auth.models import User
import random


class Command(BaseCommand):
    help = "Seed the database with sample listings"

    def handle(self, *args, **kwargs):
        if Listing.objects.exists():
            self.stdout.write(self.style.WARNING("Listings already seeded."))
            return

        # Ensure at least one user exists
        user, created = User.objects.get_or_create(username="testuser")
        if created:
            user.set_password("password123")
            user.save()

        listings_data = [
            {"title": "Beachside Villa", "description": "Beautiful villa with sea view.", "price_per_night": 250.00, "location": "Lagos"},
            {"title": "City Apartment", "description": "Modern apartment in city center.", "price_per_night": 100.00, "location": "Abuja"},
            {"title": "Mountain Cabin", "description": "Cozy cabin near the mountains.", "price_per_night": 80.00, "location": "Jos"},
        ]

        for data in listings_data:
            Listing.objects.create(**data)

        self.stdout.write(self.style.SUCCESS("Successfully seeded listings data!"))
