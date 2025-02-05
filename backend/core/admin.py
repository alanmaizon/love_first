from django.contrib import admin
from .models import Charity, Donation, DonationAllocation

@admin.register(Charity)
class CharityAdmin(admin.ModelAdmin):
    list_display = ("name", "website")

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "created_at")

@admin.register(DonationAllocation)
class DonationAllocationAdmin(admin.ModelAdmin):
    list_display = ("donation", "charity", "amount")
