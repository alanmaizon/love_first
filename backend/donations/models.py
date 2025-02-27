from django.db import models
from django.contrib.auth.models import User
from core.models import Charity

class Donation(models.Model):
    PAYMENT_CHOICES = [
        ("manual", "Manual Transfer"),
        ("stripe", "Stripe"),
        ("paypal", "PayPal"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    charities = models.ManyToManyField(Charity)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="manual")
    message = models.TextField(blank=True, null=True)  # <-- New field for personalized messages

    def __str__(self):
        return f"${self.amount} by {self.user.username} via {self.payment_method}"
