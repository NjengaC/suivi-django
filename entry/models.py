from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from datetime import timedelta, datetime
import random

class UserManager(BaseUserManager):
    def create_user(self, email, username, user_contact, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not username:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            user_contact=user_contact,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, user_contact, password=None):
        user = self.create_user(
            email=email,
            username=username,
            user_contact=user_contact,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    user_contact = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=20, default='user')
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'user_contact']

    def __str__(self):
        return f"{self.username} ({self.email})"

class Rider(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    vehicle_type = models.CharField(max_length=50)
    vehicle_registration = models.CharField(max_length=50, unique=True)
    area_of_operation = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=60)
    role = models.CharField(max_length=20, default='rider')
    status = models.CharField(max_length=20, default='available')

    def __str__(self):
        return f"Rider('{self.name}', '{self.contact_number}')"

class Parcel(models.Model):
    id = models.AutoField(primary_key=True)
    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    sender_contact = models.CharField(max_length=20)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    receiver_contact = models.CharField(max_length=20, blank=True, null=True)
    pickup_location = models.CharField(max_length=255)
    delivery_location = models.CharField(max_length=255)
    description = models.TextField(max_length=400)
    rider = models.ForeignKey(Rider, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')
    tracking_number = models.CharField(max_length=100, unique=True, default=''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10)))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parcel('{self.id}', '{self.sender_name}', '{self.receiver_name}')"

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

