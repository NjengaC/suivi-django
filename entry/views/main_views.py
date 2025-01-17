from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from entry.models import FAQ, User
from django.db.models import Q
from django.contrib.auth import logout
from rider.models import Rider


def home(request):
    if request.user.is_authenticated:
        if not isinstance(request.user, Rider):
            return redirect('entry:home_authenticated')
        else:
            return redirect('rider:rider_authenticated')
    else:
        return render(request, 'home.html', {'title': 'Home'})



@login_required
def home_authenticated(request):
    return render(request, 'home_authenticated.html', {'title': 'suivi-User\'s HomePage', 'user': request.user})


def about(request):
    return render(request, 'about.html')


def contacts(request):
    return render(request, 'contact.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('entry:home')


def support(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('comment')

        if not name or not email or not comment:
            messages.error(request, 'Please fill out all fields.')
        else:
            try:
                # Send email to support
                send_mail(
                    'User Comment',
                    f"Name: {name}\nEmail: {email}\nComment: {comment}",
                    'suiviadmn@gmail.com',
                    ['suiviadmn@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, 'Email sent successfully! Our support team will get back to you shortly.')
            except Exception as e:
                messages.error(request, 'Something unexpected happened! Please try again.')

        return redirect('main:support')

    search_query = request.GET.get('search_query', '').strip()
    faqs = []
    if search_query:
        search_words = search_query.split()
        faqs = FAQ.objects.filter(
            Q(question__icontains=search_query) | Q(answer__icontains=search_query)
        )

    return render(request, 'support.html', {'faqs': faqs})
