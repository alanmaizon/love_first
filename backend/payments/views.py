import stripe
import paypalrestsdk
import json
import logging
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from core.models import Donation, Charity
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET  # Add to settings

# Configure PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

# Setup logging
logger = logging.getLogger(__name__)

def generate_donation_receipt(user_name, amount):
    """Generate a PDF receipt for the donation"""
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    p.setFont("Helvetica", 12)

    p.drawString(100, 750, "Donation Receipt")
    p.drawString(100, 730, f"Donor Name: {user_name}")
    p.drawString(100, 710, f"Donation Amount: ${amount}")
    p.drawString(100, 690, "Thank you for your generous support!")

    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

def send_donation_email(user_email, user_name, amount):
    """Send an HTML donation receipt email with a PDF attachment"""
    subject = "🎉 Thank You for Your Donation!"
    html_content = render_to_string("emails/donation_email.html", {
        "name": user_name,
        "amount": amount
    })
    text_content = strip_tags(html_content)  # Fallback for plain-text email clients

    email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [user_email])
    email.attach_alternative(html_content, "text/html")

    # Generate PDF receipt
    pdf_buffer = generate_donation_receipt(user_name, amount)
    email.attach("Donation_Receipt.pdf", pdf_buffer.getvalue(), "application/pdf")

    email.send()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_stripe_checkout(request):
    """Create a Stripe checkout session for donation"""
    amount = request.data.get("amount")
    charity_ids = request.data.get("charities", [])

    if not amount or float(amount) <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    charities = Charity.objects.filter(id__in=charity_ids)
    charity_names = ", ".join([c.name for c in charities])

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "unit_amount": int(float(amount) * 100),
                "product_data": {"name": f"Donation to {charity_names or 'Couple'}"},
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url="http://localhost:3000/success",
        cancel_url="http://localhost:3000/cancel",
    )

    return Response({"session_id": session.id, "stripe_url": session.url})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_paypal_payment(request):
    """Create a PayPal payment link for donation"""
    amount = request.data.get("amount")
    charity_ids = request.data.get("charities", [])

    if not amount or float(amount) <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    charities = Charity.objects.filter(id__in=charity_ids)
    charity_names = ", ".join([c.name for c in charities])

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:3000/success",
            "cancel_url": "http://localhost:3000/cancel",
        },
        "transactions": [{
            "amount": {"total": f"{amount}", "currency": "USD"},
            "description": f"Donation to {charity_names or 'Couple'}",
        }]
    })

    if payment.create():
        return Response({"paypal_url": payment.links[1].href})
    else:
        logger.error(f"PayPal Payment Error: {payment.error}")
        return Response({"error": "Payment failed"}, status=500)


@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook for successful payments"""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        logger.error(f"Stripe Webhook Error: {e}")
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        amount = session["amount_total"] / 100  # Convert from cents
        email = session.get("customer_email", "")

        user = User.objects.filter(email=email).first()
        if user:
            donation = Donation.objects.create(user=user, amount=amount)
            send_donation_email(user.email, user.username, amount)

    return HttpResponse(status=200)


@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhook for successful payments"""
    event = json.loads(request.body)
    
    logger.info(f"Received PayPal Webhook: {event}")

    if event.get("event_type") == "PAYMENT.SALE.COMPLETED":
        amount = event["resource"]["amount"]["total"]
        payer_email = event["resource"]["payer"]["email_address"]

        user = User.objects.filter(email=payer_email).first()
        if user:
            donation = Donation.objects.create(user=user, amount=amount)
            send_donation_email(user.email, user.username, amount)

    return JsonResponse({"message": "Webhook received"}, status=200)
