import stripe
import paypalrestsdk
import json
import logging
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


from core.models import Donation, Charity
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
import stripe
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from core.models import Donation  # Adjust based on your app structure
from django.contrib.auth import get_user_model
from payments.utils import send_donation_email, generate_donation_receipt  # Adjust import based on your structure

logger = logging.getLogger(__name__)
User = get_user_model()

# Configure Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
STRIPE_WEBHOOK_SECRET = settings.STRIPE_WEBHOOK_SECRET  # Store in settings

# Configure PayPal
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

# Setup logging
logger = logging.getLogger(__name__)

# Use Django settings for success/cancel URLs
SUCCESS_URL = settings.FRONTEND_URL + "/success"
CANCEL_URL = settings.FRONTEND_URL + "/donate"

@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_stripe_checkout(request):
    """Create a Stripe checkout session for donation."""
    try:
        amount = request.data.get("amount")
        charity_ids = request.data.get("charities", [])

        if not amount or float(amount) <= 0:
            return Response({"error": "Invalid amount"}, status=400)

        charities = Charity.objects.filter(id__in=charity_ids)
        charity_names = ", ".join([c.name for c in charities]) or "Couple"

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "unit_amount": int(float(amount) * 100),
                    "product_data": {"name": f"Donation to {charity_names}"},
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=SUCCESS_URL,
            cancel_url=CANCEL_URL,
            metadata={
                "charity_ids": json.dumps(charity_ids),  # Store charity IDs
                "user_email": request.user.email,  # Track user
            },
        )

        return Response({"session_id": session.id, "stripe_url": session.url})

    except Exception as e:
        logger.error(f"Stripe Checkout Error: {e}")
        return Response({"error": "Failed to create Stripe session"}, status=500)


@api_view(["POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_paypal_payment(request):
    """Create a PayPal payment link for donation."""
    try:
        amount = request.data.get("amount")
        charity_ids = request.data.get("charities", [])

        if not amount or float(amount) <= 0:
            return Response({"error": "Invalid amount"}, status=400)

        charities = Charity.objects.filter(id__in=charity_ids)
        charity_names = ", ".join([c.name for c in charities]) or "Couple"

        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {"payment_method": "paypal"},
            "redirect_urls": {
                "return_url": SUCCESS_URL,
                "cancel_url": CANCEL_URL,
            },
            "transactions": [{
                "amount": {"total": f"{amount}", "currency": "USD"},
                "description": f"Donation to {charity_names}",
            }]
        })

        if payment.create():
            return Response({"paypal_url": payment.links[1].href})
        else:
            logger.error(f"PayPal Payment Error: {payment.error}")
            return Response({"error": "Payment failed"}, status=500)

    except Exception as e:
        logger.error(f"PayPal Payment Creation Error: {e}")
        return Response({"error": "Something went wrong"}, status=500)
    
@csrf_exempt
def stripe_webhook(request):
    """Handle Stripe webhook for successful payments."""
    payload = request.body
    sig_header = request.headers.get("Stripe-Signature")

    if not sig_header:
        logger.error("Missing Stripe-Signature header")
        return HttpResponse("Missing Stripe-Signature", status=400)

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            email = session.get("customer_email", "")
            amount = session["amount_total"] / 100  # Convert from cents
            metadata = session.get("metadata", {})

            user = User.objects.filter(email=email).first()
            if not user:
                logger.error(f"User with email {email} not found")
                return HttpResponse(status=400)

            # Retrieve charity IDs from metadata
            charity_ids = json.loads(metadata.get("charity_ids", "[]"))
            charities = Charity.objects.filter(id__in=charity_ids)

            # ✅ Create the Donation record (Triggers `post_save` signal)
            donation = Donation.objects.create(user=user, amount=amount)
            donation.charities.set(charities)

            logger.info(f"Donation created: {amount} by {user.username}")

        return HttpResponse(status=200)

    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Invalid signature: {e}")
        return HttpResponse("Invalid signature", status=400)

    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        return HttpResponse("Webhook processing error", status=500)

@csrf_exempt
def paypal_webhook(request):
    """Handle PayPal webhook for successful payments."""
    try:
        event = json.loads(request.body)
        logger.info(f"Received PayPal Webhook: {event}")

        if event.get("event_type") == "PAYMENT.SALE.COMPLETED":
            amount = event["resource"]["amount"]["total"]
            payer_email = event["resource"]["payer"]["email_address"]
            metadata = event.get("resource", {}).get("custom", "{}")  # Extract metadata

            user = User.objects.filter(email=payer_email).first()
            if not user:
                logger.error(f"User with email {payer_email} not found")
                return JsonResponse({"error": "User not found"}, status=400)

            charity_ids = json.loads(metadata.get("charity_ids", "[]"))
            charities = Charity.objects.filter(id__in=charity_ids)

            # ✅ Create the Donation record (Triggers `post_save` signal)
            donation = Donation.objects.create(user=user, amount=amount)
            donation.charities.set(charities)

            logger.info(f"Donation created: {amount} by {user.username}")

        return JsonResponse({"message": "Webhook received"}, status=200)

    except json.JSONDecodeError as e:
        logger.error(f"PayPal Webhook JSON Error: {e}")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        logger.error(f"Unexpected PayPal Webhook Error: {e}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def latest_donation(request):
    donation = Donation.objects.filter(user=request.user).order_by('-created_at').first()
    if donation:
        return Response({
            'amount': donation.amount,
            'created_at': donation.created_at
        })
    return Response({'error': 'No donations found'}, status=404)