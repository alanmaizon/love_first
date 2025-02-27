from rest_framework import serializers
from donations.models import Donation
from core.models import Charity

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ["id", "user", "amount", "charities", "payment_method", "created_at", "message"]
        read_only_fields = ["user", "created_at"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Donation amount must be greater than zero.")
        return value

    def validate_charities(self, value):
        if not value:
            raise serializers.ValidationError("At least one charity must be selected.")

        # Ensure charities exist
        existing_charities = Charity.objects.filter(id__in=[c.id for c in value])
        if len(existing_charities) != len(value):
            raise serializers.ValidationError("One or more selected charities do not exist.")

        return value
