from rest_framework import serializers
from donations.models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ["id", "user", "amount", "charities", "created_at"]
        read_only_fields = ["user", "created_at"]

    def validate_amount(self, value):
        """Ensure amount is positive and greater than zero."""
        if value <= 0:
            raise serializers.ValidationError("Donation amount must be greater than zero.")
        return value

    def validate_charities(self, value):
        """Ensure at least one charity is selected."""
        if not value:
            raise serializers.ValidationError("At least one charity must be selected.")
        return value
