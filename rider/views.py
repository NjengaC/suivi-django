from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, get_backends
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from .forms import RiderRegistrationForm, RiderUpdateAccountForm, LoginRiderForm
from .models import Rider
from entry.models import Parcel
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Rider

@csrf_protect
def register_rider(request):
    if request.user.is_authenticated:
        return redirect('rider:rider_authenticated')

    form = RiderRegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        try:
            rider = form.save(commit=False)
            rider.password = make_password(form.cleaned_data['password'])
            rider.save()
            
#            backend = get_backends()[0]
#            login(request, rider, backend=backend)
            login(request, rider, backend='rider.backends.RiderBackend')
            welcome_msg = render(request, 'welcome_rider_mail.html', {'rider': rider}).content.decode()
            send_mail(
                'Welcome to Suivi!',
                '',  # Empty text content
                'from@example.com',
                [rider.email],
                fail_silently=False,
                html_message=welcome_msg,
            )

            messages.success(request, 'Rider registration successful!')
            return redirect('rider:rider_authenticated')
        
        except IntegrityError:
            messages.error(request, 'A rider with these details already exists.')

    return render(request, 'register_rider.html', {'form': form})



def login_rider(request):
    if request.user.is_authenticated:
        return redirect('rider:rider_authenticated')

    form = LoginRiderForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        
        rider = authenticate(request, email=email, password=password)
        
        if rider:
            login(request, rider, backend='rider.backends.RiderBackend')  # Specify backend
            messages.success(request, 'Rider login successful!')
            return redirect('rider:rider_authenticated')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'login_rider.html', {'form': form})


def rider_authenticated(request):
#    if not isinstance(request.user, Rider):
#        return redirect('entry:home')
    pending_assignments = Parcel.objects.filter(
        rider_id=request.user.id, status__in=['allocated', 'shipped', 'in_progress']
    ).first()
    return render(request, 'rider_authenticated.html', {'user': request.user, 'assignment': pending_assignments})


@login_required
def edit_rider_profile(request):
    if not isinstance(request.user, Rider):
        return redirect('home')

    form = RiderUpdateAccountForm(request.POST or None, instance=request.user)
    if form.is_valid():
        rider = form.save(commit=False)
        if form.cleaned_data['password']:
            rider.password = make_password(form.cleaned_data['password'])
        rider.save()
        messages.success(request, 'Your account has been updated successfully!')
        return redirect('rider:rider_authenticated')
    return render(request, 'edit_rider_profile.html', {'form': form})



@login_required
def view_rider_history(request):
    open_orders = Parcel.objects.filter(rider_id=request.user.id, status__in=["pending", "allocated", "in_progress"])
    closed_orders = Parcel.objects.filter(rider_id=request.user.id, status="arrived")

    return render(request, 'view_rider_history.html', {
        'open_orders': open_orders,
        'closed_orders': closed_orders,
    })

@require_POST
def toggle_rider_status(request):
    try:
        rider = Rider.objects.get(id=request.user.id, email=request.user.email)
    except Rider.DoesNotExist:
        return JsonResponse({'error': 'Rider not found or unauthorized'}, status=404)

    rider.status = 'unavailable' if rider.status == 'available' else 'available'
    rider.save()

    return JsonResponse({'status': rider.status})


@require_POST
def update_location(request):
    data = json.loads(request.body)
    rider_id = data.get('rider_id')
    new_location = data.get('current_location')

    if not rider_id or not new_location:
        return JsonResponse({"error": "Missing rider_id or current_location"}, status=400)

    try:
        rider = Rider.objects.get(id=rider_id)
        rider.current_location = new_location
        rider.save()
        return JsonResponse({"success": "Location updated successfully"})
    except Rider.DoesNotExist:
        return JsonResponse({"error": "Rider not found"}, status=404)

