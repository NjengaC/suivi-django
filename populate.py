import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'suivi.settings')  # Update to 'suivi.settings'

# Initialize Django
django.setup()

from rider.models import Rider
from parcels.models import Parcel
from entry.models import User  # Ensure correct app name and import paths

def populate_parcels():
    try:
        # Fetch the user
        user = User.objects.get(email="njengavictor14@gmail.com")

        # Create sample parcels
        parcels = [
            {
                "sender": user,
                "sender_contact": "0711470120",
                "receiver_name": "John Doe",
                "receiver_contact": "+254712345678",
                "pickup_location": "Nairobi",
                "delivery_location": "Mombasa",
                "description": "Electronics Package",
                "status": "shipped",
                "tracking_number": "TRACK123456",
                "expected_arrival": "2 Days",
            },
            {
                "sender": user,
                "sender_contact": "0711470120",
                "receiver_name": "Jane Smith",
                "receiver_contact": "+254798765432",
                "pickup_location": "Nakuru",
                "delivery_location": "Eldoret",
                "description": "Clothing Package",
                "status": "arrived",
                "tracking_number": "TRACK789101",
                "expected_arrival": "1 Day",
            },
            {
                "sender": user,
                "sender_contact": "0711470120",
                "receiver_name": "Mark Anthony",
                "receiver_contact": "+254701234567",
                "pickup_location": "Kisumu",
                "delivery_location": "Kakamega",
                "description": "Fragile Glassware",
                "status": "in_progress",
                "tracking_number": "TRACK112233",
                "expected_arrival": "3 Days",
            },
        ]

        # Save parcels to the database
        for parcel_data in parcels:
            Parcel.objects.create(**parcel_data)
        print("Parcels added successfully.")

    except User.DoesNotExist:
        print("User with email 'njengavictor14@gmail.com' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    populate_parcels()
