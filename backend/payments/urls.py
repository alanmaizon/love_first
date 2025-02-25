from django.urls import path
from .views import create_stripe_checkout, stripe_webhook, create_paypal_payment, paypal_webhook, latest_donation

urlpatterns = [
    path("stripe/checkout/", create_stripe_checkout, name="stripe_checkout"),
    path("stripe/webhook/", stripe_webhook, name="stripe_webhook"),
    path("paypal/payment/", create_paypal_payment, name="paypal_payment"),
    path("paypal/webhook/", paypal_webhook, name="paypal_webhook"),
    path('donations/latest/', latest_donation, name='latest_donation'),
]
