from django.db import models
from django.contrib.auth.models import User
from core.models import Charity


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    charities = models.ManyToManyField(Charity)
    
    def __str__(self):
        return f"${self.amount} by {self.user.username}"