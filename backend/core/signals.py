from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Donation, DonationAllocation

@receiver(post_save, sender=Donation)
def allocate_donation(sender, instance, created, **kwargs):
    if created:
        charities = instance.charities.all()
        if charities.exists():
            charity_share = instance.amount * 0.5
            per_charity = charity_share / charities.count()
            
            for charity in charities:
                DonationAllocation.objects.create(
                    donation=instance,
                    charity=charity,
                    amount=per_charity
                )
