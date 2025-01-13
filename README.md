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
├── README.md
├── __pycache__/
├── manage.py
├── suivi/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
├── core/
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── admin_routes.py
│   │   ├── auth_routes.py
│   │   ├── main_routes.py
│   │   ├── parcels.py
│   │   ├── password.py
│   │   ├── payment.py
│   │   └── rider_routes.py
│   ├── static/
│   │   ├── images/
│   │   ├── main.css
│   │   ├── profiles.css
│   │   ├── scripts/
│   │   │   ├── dashboard.js
│   │   │   ├── home.js
│   │   │   ├── ...
│   │   └── styles/
│   │       ├── about1.css
│   │       ├── ...
│   └── templates/
│       ├── about.html
│       ├── admin_dashboard.html
│       ├── ...
├── requirements.txt
└── tailwind.config.js
