from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Charity: This model represents a charity organization. It includes the fields name, description, and website. The name field is unique, meaning that each charity must have a unique name.

class Charity(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

# Donation: This model represents a donation made by a user. It includes the fields user, amount, date, and charities. The user field is a foreign key that references the User model. The amount field is a decimal field that stores the donation amount. The date field stores the date and time of the donation. The charities field is a many-to-many field that references the Charity model.

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    charities = models.ManyToManyField(Charity, related_name="donations")

    def allocate_funds(self):
        selected_charities = self.charities.all()
        couple_share = self.amount * Decimal("0.50")
        charity_share_total = self.amount * Decimal("0.50")

        if selected_charities.count() > 0:
            per_charity_share = charity_share_total / selected_charities.count()
        else:
            per_charity_share = Decimal("0.00")

        return {
            "couple": couple_share,
            "charities": {charity.name: per_charity_share for charity in selected_charities},
        }
