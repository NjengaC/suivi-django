from django.db import models
from datetime import timedelta, datetime
import random
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import uuid

class RiderManager(BaseUserManager):
    def create_rider(self, email, contact_number, password=None, **extra_fields):
        if not email:
            raise ValueError("Riders must have an email address")
        if not contact_number:
            raise ValueError("Riders must have a contact number")

        email = self.normalize_email(email)
        rider = self.model(email=email, contact_number=contact_number, **extra_fields)
        rider.set_password(password)
        rider.save(using=self._db)
        return rider

    def create_superuser(self, email, contact_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_rider(email, contact_number, password, **extra_fields)


class Rider(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=20, unique=True)
    vehicle_type = models.CharField(max_length=50)
    vehicle_registration = models.CharField(max_length=50, unique=True)
    area_of_operation = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, default='available')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = RiderManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['contact_number', 'name']

    def __str__(self):
        return f"{self.name} ({self.contact_number})"
