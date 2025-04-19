from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .forms import RegistrationForm, LoginForm, UpdateAccountForm
from entry.models import User
import logging
from django.views.decorators.csrf import csrf_protect

logger = logging.getLogger(__name__)

def register(request):
    if request.user.is_authenticated:
        return redirect('entry:home')

    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Check for existing user
            existing_user = User.objects.filter(
                username=form.cleaned_data['username']
            ).first() or User.objects.filter(
                email=form.cleaned_data['email']
            ).first() or User.objects.filter(
                user_contact=form.cleaned_data['user_contact']
            ).first()

            if existing_user:
                messages.error(request, 'Username, email, or contact already exists.')
                return redirect('entry:register')

            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                user_contact=form.cleaned_data['user_contact'],
                password=form.cleaned_data['password1'],
            )

            # Send welcome email
            welcome_msg = render_to_string('welcome_user_mail.html', {'user': user, 'login_url': request.build_absolute_uri('entry:login')})
            send_mail(
                'Welcome to Suivi!',
                '',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                html_message=welcome_msg,
                fail_silently=False
            )
            messages.success(request, 'Account created successfully. Please log in.')
            return redirect('entry:login')
    return render(request, 'register.html', {'title': 'Register', 'form': form})
@csrf_protect
def login_view(request):
    if request.user.is_authenticated:
        return redirect('entry:home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        # Authenticate user by email
        user = User.objects.filter(email=email).first()
        if user and user.check_password(password):
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('entry:home_authenticated')
        else:
            messages.error(request, 'Login unsuccessful. Please check your email and password.')

    return render(request, 'login.html', {'title': 'Login', 'form': form})

@login_required
def edit_profile(request):
    form = UpdateAccountForm(instance=request.user)
    if request.method == 'POST':
        form = UpdateAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Account updated successfully!')
            return redirect('entry:home_authenticated')
    return render(request, 'edit_profile.html', {'title': 'Edit Profile', 'form': form, 'user': request.user})
