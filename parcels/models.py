from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from entry.models import User
from rider.models import Rider
import random
import string
from django.utils.timezone import now, timedelta

class Parcel(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("allocated", "Allocated"),
        ("in_progress", "In Progress"),
        ("shipped", "Shipped"),
        ("arrived", "Arrived"),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_parcels")
    sender_contact = models.CharField(max_length=15, default='+254771178496')
    receiver_name = models.CharField(max_length=100)
    receiver_contact = models.CharField(max_length=15)
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    tracking_number = models.CharField(max_length=50, blank=True, unique=True)
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, related_name="assigned_parcels", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expected_arrival = models.CharField(max_length=50, blank=True)


    def __str__(self):
        return f"Parcel {self.tracking_number} - {self.status}"

    @staticmethod
    def generate_tracking_number():
        """
        Generates a random tracking number consisting of 10 alphanumeric characters.
        """
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def set_expected_arrival(self):
        """
        Sets the expected arrival time to 24 hours from now in a human-readable format.
        """
        expected_time = now() + timedelta(days=1)
        self.expected_arrival = expected_time.strftime('%B %d, %Y, %I:%M %p')

    def save(self, *args, **kwargs):
        """
        Overrides the save method to ensure that the tracking number and expected arrival
        are set when a new Parcel is created.
        """
        if not self.tracking_number:
            self.tracking_number = self.generate_tracking_number()
        if not self.expected_arrival:
            self.set_expected_arrival()
        super().save(*args, **kwargs)
