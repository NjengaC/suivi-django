import os
import django
from datetime import datetime
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suivi.settings')
django.setup()

from rider.models import Rider
from parcels.models import Parcel
# User and Rider Details
rider_email = 'njengavictor14@gmail.com'
user_contact = '0711470120'
User = get_user_model()

# Get the User instance
try:
    user = User.objects.get(user_contact=user_contact)
except User.DoesNotExist:
    print(f"User with contact {user_contact} does not exist.")
    exit()

# Get the Rider instance
try:
    rider = Rider.objects.get(email=rider_email)
except Rider.DoesNotExist:
    print(f"Rider with email {rider_email} does not exist.")
    exit()

# Parcel Data
parcels_data = [
    {
        'receiver_name': 'John Doe',
        'receiver_contact': '0723000000',
        'pickup_location': 'Westlands, Nairobi',
        'delivery_location': 'Kilimani, Nairobi',
        'description': 'Documents for approval',
        'status': 'in_progress',
        'expected_arrival': datetime(2024, 11, 19),
    },
    {
        'receiver_name': 'Jane Smith',
        'receiver_contact': '0734000000',
        'pickup_location': 'CBD, Nairobi',
        'delivery_location': 'Karen, Nairobi',
        'description': 'Birthday gift',
        'status': 'shipped',
        'expected_arrival': datetime(2024, 11, 20),
    },
    {
        'receiver_name': 'Paul Mwangi',
        'receiver_contact': '0711000000',
        'pickup_location': 'Kilimani, Nairobi',
        'delivery_location': 'Mombasa Road, Nairobi',
        'description': 'Electronics package',
        'status': 'allocated',
        'expected_arrival': datetime(2024, 11, 21),
    },
    {
        'receiver_name': 'Lucy Wanjiru',
        'receiver_contact': '0722000000',
        'pickup_location': 'Langata, Nairobi',
        'delivery_location': 'Ruiru, Nairobi',
        'description': 'Groceries',
        'status': 'pending',
        'expected_arrival': datetime(2024, 11, 22),
    },
    {
        'receiver_name': 'George Kamau',
        'receiver_contact': '0735000000',
        'pickup_location': 'Thika, Nairobi',
        'delivery_location': 'Westlands, Nairobi',
        'description': 'Books',
        'status': 'arrived',
        'expected_arrival': datetime(2024, 11, 17),
    },
    {
        'receiver_name': 'Ann Achieng',
        'receiver_contact': '0713000000',
        'pickup_location': 'Roysambu, Nairobi',
        'delivery_location': 'Parklands, Nairobi',
        'description': 'Household items',
        'status': 'in_progress',
        'expected_arrival': datetime(2024, 11, 18),
    },
    {
        'receiver_name': 'Tom Odhiambo',
        'receiver_contact': '0724000000',
        'pickup_location': 'Kenyatta Market, Nairobi',
        'delivery_location': 'CBD, Nairobi',
        'description': 'Clothing items',
        'status': 'pending',
        'expected_arrival': datetime(2024, 11, 19),
    },
    {
        'receiver_name': 'Faith Njeri',
        'receiver_contact': '0736000000',
        'pickup_location': 'Kasarani, Nairobi',
        'delivery_location': 'Embakasi, Nairobi',
        'description': 'Electronics',
        'status': 'shipped',
        'expected_arrival': datetime(2024, 11, 20),
    },
    {
        'receiver_name': 'James Kariuki',
        'receiver_contact': '0719000000',
        'pickup_location': 'Lavington, Nairobi',
        'delivery_location': 'Kikuyu, Nairobi',
        'description': 'Furniture',
        'status': 'arrived',
        'expected_arrival': datetime(2024, 11, 17),
    },
    {
        'receiver_name': 'Grace Wambui',
        'receiver_contact': '0728000000',
        'pickup_location': 'Gikambura, Nairobi',
        'delivery_location': 'Ngong Road, Nairobi',
        'description': 'Perishables',
        'status': 'allocated',
        'expected_arrival': datetime(2024, 11, 21),
    },
]

# Add Parcels to Database
for idx, data in enumerate(parcels_data, start=1):
    Parcel.objects.create(
        sender=user,  # Use User instance here
        sender_contact=user.user_contact,
        receiver_name=data['receiver_name'],
        receiver_contact=data['receiver_contact'],
        pickup_location=data['pickup_location'],
        delivery_location=data['delivery_location'],
        description=data['description'],
        status=data['status'],
        tracking_number=f"TRK{idx:04d}",
        expected_arrival=data['expected_arrival'],
    )
    print(f"Added parcel {idx} for {data['receiver_name']}")

print("Finished populating parcels.")
