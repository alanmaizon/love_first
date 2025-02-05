from django.db import models
from django.contrib.auth.models import User

class Charity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Charities"

    def __str__(self):
        return self.name


class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    charities = models.ManyToManyField(Charity, through="DonationAllocation")

    def __str__(self):
        return f"${self.amount} by {self.user.username}"


class DonationAllocation(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"${self.amount} to {self.charity.name}"
