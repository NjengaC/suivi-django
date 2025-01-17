from django.urls import path
from . import views
from . import payment

app_name = "parcel"

urlpatterns = [
    path("track_parcel/", views.track_parcel, name="track_parcel"),
    path("charge/", payment.charge, name="charge"),
    path("get_parcel_status/", views.get_parcel_status, name="get_parcel_status"),
    path("request_pickup/", views.request_pickup, name="request_pickup"),
    path('request_pickup/<str:step>/', views.request_pickup, name='request_pickup_step'),
    path("view_parcel_history/", views.view_parcel_history, name="view_parcel_history"),
    path("view_rider_history/", views.view_rider_history, name="view_rider_history"),
]
