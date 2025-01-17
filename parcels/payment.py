import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt


secret_key = settings.STRIPE_SECRET_KEY
publishable_key = settings.STRIPE_PUBLISHABLE_KEY

stripe_keys = {
    "secret_key": secret_key,
    "publishable_key": publishable_key,
}

stripe.api_key = stripe_keys['secret_key']


@csrf_exempt
def payment_success(request):
    """
    Redirect to home after a successful payment.
    """
    messages.success(request, "Payment successful!")
    return redirect("entry:home_authenticated")


def checkout(request):
    """
    Render the checkout page.
    """
    context = {
        "key": settings.STRIPE_PUBLISHABLE_KEY
    }
    return render(request, "checkout.html", context)


@csrf_exempt
def charge(request):
    """
    Handle the charge logic with Stripe.
    """
    if request.method == "POST":
        amount = 1000
        try:
            customer = stripe.Customer.create(
                email="customer@example.com",
                source=request.POST.get("stripeToken")
            )

            # Create a charge for the customer
            charge = stripe.Charge.create(
                customer=customer.id,
                amount=amount,
                currency="usd",
                description="Django Charge"
            )

            # Send payment notification email
            send_payment_notification_email()

            return JsonResponse({"success": True, "charge_id": charge.id})
        except stripe.error.StripeError as e:
            return JsonResponse({"success": False, "error": str(e)})

    return JsonResponse({"success": False, "error": "Invalid request method."})


def send_payment_notification_email():
    """
    Send a payment notification email.
    """
    subject = "New Payment Received"
    message = "A new payment has been received. Please check the dashboard for details."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = ["victorcyrus01@gmai.com"]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception as e:
        print(f"Failed to send email: {e}")
