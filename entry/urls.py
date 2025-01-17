from django.urls import path
from .views import main_views, auth_views, password_views

app_name = 'entry'

urlpatterns = [
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login_view, name='login'),
    path('edit_profile/', auth_views.edit_profile, name='edit_profile'),
    path('home_authenticated/', main_views.home_authenticated, name='home_authenticated'),
    path('', main_views.home, name='home'),
    path('home', main_views.home, name='home'),
    path('about/', main_views.about, name='about'),
    path('contacts/', main_views.contacts, name='contacts'),
    path('logout/', main_views.logout_view, name='logout'),
    path('support/', main_views.support, name='support'),
    path('forgot_password/', password_views.PasswordResetView.as_view(), name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', password_views.PasswordResetConfirmView.as_view(), name='reset_password'),
]
