# urls.py
from django.urls import path
from rider import views as rider_views

app_name = 'rider'

urlpatterns = [
    path('register_rider/', rider_views.register_rider, name='register_rider'),
    path('login_rider/', rider_views.login_rider, name='login_rider'),
    path('rider_authenticated/', rider_views.rider_authenticated, name='rider_authenticated'),
    path('edit_rider_profile/', rider_views.edit_rider_profile, name='edit_rider_profile'),
    path('view_rider_history/', rider_views.view_rider_history, name='view_rider_history'),
    path('toggle_rider_status/', rider_views.toggle_rider_status, name='toggle_rider_status'),
    path('update_location/', rider_views.update_location, name='update_location'),
]
