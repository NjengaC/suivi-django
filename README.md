# SUIVI Parcel Sending Service App

**SUIVI** is an online parcel sending service platform that connects **senders (users)** with **riders** (and/or **parcel service companies**). Users can request pickups, track deliveries, and conveniently complete transactions through integrated payment gateways. Riders (or courier companies) can manage assignments through a central dashboard, update parcel statuses, and communicate with users in real-time. Below is the **Django** implementation of SUIVI:

---

## Table of Contents

1. [Features](#features)  
2. [System Requirements](#system-requirements)  
3. [Django Version](#django-version)  
   - [Key Technologies](#key-technologies---django)  
   - [Project Structure](#project-structure---django)  
   - [Installation](#installation---django)  
   - [Database Setup](#database-setup---django)  
   - [Running the Application](#running-the-application---django)  
   - [Versioning](#versioning---django)  
4. [Legal and Regulatory Considerations](#legal-and-regulatory-considerations)  
5. [License](#license)  
6. [Contact](#contact)  

---

## Features

1. **Homepage**  
   - A straightforward landing page that highlights the core services and functionalities.

2. **User Registration & Login**  
   - Senders (users) can register and log in to request pickups and manage their parcels.

3. **Parcel Sending Request Form**  
   - Users can fill out a form specifying the parcel details (size, weight, pickup/delivery locations).

4. **Riders & Parcel Service Companies Registration & Login**  
   - Riders and companies can manage their profiles, accept/reject deliveries, and track parcels in transit.

5. **Riders Dashboard**  
   - Tools to manage assigned pickups, track deliveries, update parcel status, and communicate with senders.

6. **Parcel Tracking**  
   - Real-time parcel status updates from pickup through to final delivery.

7. **Payment Integration**  
   - Seamless payment workflows using an integrated payment gateway.

8. **Rating and Feedback System**  
   - Users can rate and provide feedback on the services they received, aiding other users in decision-making.

9. **Mobile App Version**  
   - An Android version for on-the-go access to SUIVI's core features.

10. **Admin Panel**  
    - Centralized management of user accounts, company registrations, usage analytics, and issue resolution.

---

## System Requirements

- **Python 3.7+**  
- **PostgreSQL** (recommended)  
- **pip** or **pipenv** for managing Python dependencies  
- A suitable web server (for production deployment)  

---

## Django Version

### Key Technologies - Django

- **Django** (Python web framework)  
- **Django ORM** (database abstraction layer)  
- **PostgreSQL** (production-grade database)  
- **HTML/CSS/JavaScript** (frontend)  

### Project Structure - Django

```bash
suivi-django/
├── db.sqlite3
├── entry
│   ├── __init__.py
│   ├── __pycache__
│   │   ...
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ....
│   ├── models.py
│   ├── static
│   │   ├── images
│   │   │   ...
│   │   ├── scripts
│   │   │   ├── dashboard.js
│   │   │   ...
│   │   ├── site.webmanifest
│   │   └── styles
│   │       ├── about1.css
│   │       ...
│   ├── templates
│   │   ├── about.html
│   │   ....
│   ├── tests.py
│   ├── urls.py
│   └── views
│       ├── __init__.py
│       ├── __pycache__
│       ...
├── faqs.py
├── manage.py
├── parcels
│   ├── __init__.py
│   ├── __pycache__
│   │   ...
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── migrations
│   │   ...
│   ├── models.py
│   ├── payment.py
│   ├── templates
│   │   ├── parcel_history.html
│   │   ├── request_pickup.html
│   │   └── track_parcel.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── populate.py
├── populate_faqs.py
├── populate_rider.py
├── rider
│   ├── __init__.py
│   ├── __pycache__
│   │   ...
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── forms.py
│   ├── migrations
│   │   ...
│   ├── models.py
│   ├── templates
│   │   ├── edit_rider_profile.html
│   │   ...
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── suivi
    ├── __init__.py
    ├── __pycache__
    │   ...
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

## Installation - Django
1. Clone the repository (or download the ZIP):

```bash
git clone https://github.com/NjengaC/suivi-django.git
cd suivi-django
```
2. Create and activate a virtual environment (recommended):

```bash
python3 -m venv venv
source venv/bin/activate      # On macOS/Linux
venv\Scripts\activate.bat     # On Windows
```
3. Install dependencies:

```bash
pip install -r requirements.txt
```
## Database Setup - Django
1. Login into PostgreSQL and create the database:

```bash
sudo -u postgres psql
CREATE DATABASE suivi;
\q
```
(Adjust as needed if you have different user privileges.)

2. Configure environment variables (Optional)
You may need to provide your database URI in an environment variable (e.g., DATABASE_URL):

```bash
export DATABASE_URL="postgresql://postgres:password@localhost/suivi"
```
3. Navigate to your Django project's root directory and update your database settings in suivi/settings.py:

```python

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'suivi',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```
4. Apply migrations to set up the initial database structure:

```bash
python manage.py migrate
```
## Running the Application - Django
1. Start the Django development server:

```bash
python manage.py runserver
```
2. Access the application in your browser:

```bash
http://127.0.0.1:8000
```
(Or whichever host and port you specify.)

## Versioning - Django
Current Version: 0.1 - Django Framework
Future updates will increment version numbers accordingly.

## Legal and Regulatory Considerations
No specific legal and regulatory considerations until deployment. However, please ensure full compliance with data protection laws (e.g., GDPR) and payment standards (e.g., PCI DSS) before going live.

## License
All content in this repository is provided as is. For production deployment, please include an appropriate license (e.g., MIT, Apache 2.0, or proprietary) to clarify usage and distribution rights.

## Contact
Project Maintainer: Victor Njenga
Email: victorcyrus01@gmail.com
Issues/Contributions: Please open an issue or pull request on the GitHub repository.
Thank you for using SUIVI Parcel Sending Service App (Django Version)! Your feedback and contributions are always welcome.
