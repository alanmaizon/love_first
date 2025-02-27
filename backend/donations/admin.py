from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "payment_method", "created_at", "message")
    search_fields = ("user__username", "amount", "payment_method", "message")

