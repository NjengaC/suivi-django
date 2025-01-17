from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Parcel



class ParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ["receiver_name", "receiver_contact", "pickup_location", "delivery_location", "description"]
        widgets = {
            "receiver_name": forms.TextInput(attrs={"placeholder": "Receiver's Name"}),
            "receiver_contact": forms.TextInput(attrs={"placeholder": "Receiver's Contact"}),
            "pickup_location": forms.TextInput(attrs={"placeholder": "Pickup Location"}),
            "delivery_location": forms.TextInput(attrs={"placeholder": "Delivery Location"}),
            "description": forms.Textarea(attrs={"placeholder": "Parcel Description", "rows": 3}),
        }
