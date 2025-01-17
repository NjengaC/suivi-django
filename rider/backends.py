from django.contrib.auth.backends import BaseBackend
from .models import Rider

class RiderBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            rider = Rider.objects.get(email=email)
            if rider.check_password(password):
                return rider
        except Rider.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Rider.objects.get(pk=user_id)
        except Rider.DoesNotExist:
            return None
