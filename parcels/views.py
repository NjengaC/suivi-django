from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import ParcelForm
from .models import Parcel
from rider.models import Rider
from django.db.models import Q
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import stripe
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

secret_key = settings.STRIPE_SECRET_KEY
publishable_key = settings.STRIPE_PUBLISHABLE_KEY

stripe_keys = {
    "secret_key": secret_key,
    "publishable_key": publishable_key,
}

stripe.api_key = stripe_keys['secret_key']

def track_parcel(request):
    return render(request, "track_parcel.html")


def get_parcel_status(request):
    tracking_number = request.GET.get("tracking_number")
    if tracking_number:
        try:
            parcel = Parcel.objects.get(tracking_number=tracking_number)
            pickup_lat, pickup_lng = get_lat_lng(parcel.pickup_location)
            delivery_lat, delivery_lng = get_lat_lng(parcel.delivery_location)

            return JsonResponse({
                "status": parcel.status,
                "expected_arrival": parcel.expected_arrival,
                "pickup_location": parcel.pickup_location,
                "delivery_location": parcel.delivery_location,
                "pickup_coords": {"lat": pickup_lat, "lng": pickup_lng},
                "delivery_coords": {"lat": delivery_lat, "lng": delivery_lng},
            })
        except Parcel.DoesNotExist:
            return JsonResponse({"error": "Parcel not found"}, status=404)
    else:
        return JsonResponse({"error": "Tracking number not provided"}, status=400)



@login_required
def request_pickup(request, step="1"):
    print("Checking route response")
    form = ParcelForm(request.POST or None)  # Initialize form with POST data if any
    step = str(step)  # Ensure step is a string for consistency
    form.fields["delivery_location"].required = False
    form.fields["pickup_location"].required = False
    form.fields["receiver_name"].required = False
    form.fields["receiver_contact"].required = False

    if request.method == "POST" and form.is_valid():
        print(f"Form is valid for step {step}.")
        if step == "1":
            form.fields["delivery_location"].required = True
            form.fields["pickup_location"].required = False
            form.fields["receiver_name"].required = False
            form.fields["receiver_contact"].required = False
            request.session["delivery_location"] = form.cleaned_data.get("delivery_location")
            print(f"Delivery location saved: {request.session['delivery_location']}")
            return redirect(reverse("parcel:request_pickup_step", args=["2"]))

        elif step == "2":
            form.fields["delivery_location"].required = True
            form.fields["pickup_location"].required = True
            form.fields["receiver_name"].required = False
            form.fields["receiver_contact"].required = False 
            request.session["pickup_location"] = form.cleaned_data.get("pickup_location")
            return redirect(reverse("parcel:request_pickup_step", args=["3"]))

        elif step == "3":
            form.fields["delivery_location"].required = True
            form.fields["pickup_location"].required = True
            form.fields["receiver_name"].required = False
            form.fields["receiver_contact"].required = False
            pickup_location = request.session.get("pickup_location")
            delivery_location = request.session.get("delivery_location")

            # Get coordinates
            pickup_lat, pickup_lng = get_lat_lng(pickup_location)
            delivery_lat, delivery_lng = get_lat_lng(delivery_location)

            if not all([pickup_lat, pickup_lng, delivery_lat, delivery_lng]):
                messages.error(request, "Unable to get coordinates. Please try again.")
                return redirect(reverse("parcel:request_pickup_step", args=["2"]))

            # Save coordinates in session
            request.session["pickup_coords"] = {"lat": pickup_lat, "lng": pickup_lng}
            request.session["delivery_coords"] = {"lat": delivery_lat, "lng": delivery_lng}
            return redirect(reverse("parcel:request_pickup_step", args=["4"]))

        elif step == "4":
            form.fields["receiver_name"].required = True
            form.fields["receiver_contact"].required = True 
            parcel = Parcel(
                sender=request.user,
#                sender_email=request.user.email,
                sender_contact=request.user.user_contact,
                receiver_name=form.cleaned_data.get("receiver_name"),
                receiver_contact=form.cleaned_data.get("receiver_contact"),
                pickup_location=request.session.get("pickup_location"),
                delivery_location=request.session.get("delivery_location"),
                description="Testing Parcel",
            )
            parcel.save()

            closest_rider = allocate_parcel(parcel)
            if closest_rider:
                messages.success(request, "Rider Allocated. Check your email for more details.")
            else:
                messages.success(request, "Allocation in progress. Please wait for a rider to be assigned.")

    return render(request, "request_pickup.html", {"form": form, "step": step, "key": stripe_keys['publishable_key']})



def get_lat_lng(location):
    geolocator = Nominatim(user_agent="MyGeocodingApp")
    try:
        loc = geolocator.geocode(location)
        return loc.latitude, loc.longitude
    except:
        return None, None


def allocate_parcel(parcel):
    available_riders = Rider.objects.filter(status="available")
    if not available_riders.exists():
        return None

    closest_rider = None
    min_distance = float("inf")
    for rider in available_riders:
        distance = calculate_distance(parcel.pickup_location, rider.current_location)
        if distance < min_distance:
            closest_rider = rider
            min_distance = distance

    if closest_rider:
        parcel.status = "allocated"
        parcel.rider = closest_rider
        closest_rider.status = "unavailable"
        parcel.save()
        closest_rider.save()
        return closest_rider
    return None


def calculate_distance(location1, location2):
    geolocator = Nominatim(user_agent="MyGeocodingApp")
    loc1 = geolocator.geocode(location1)
    loc2 = geolocator.geocode(location2)
    if loc1 and loc2:
        return geodesic((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).kilometers
    return float("inf")


@login_required
def view_parcel_history(request):
    user_parcels = Parcel.objects.filter(sender_contact=request.user.user_contact).order_by('updated_at')
    return render(request, 'parcel_history.html', {'parcels': user_parcels})

@login_required
def view_rider_history(request):
    parcels = Parcel.objects.filter(rider=request.user)
    return render(request, "view_rider_history.html", {"parcels": parcels})
