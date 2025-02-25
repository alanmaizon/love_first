from rest_framework import serializers
from .models import Charity, Donation, DonationAllocation

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = "__all__"

    def validate_name(self, value):
        """Ensure charity name is unique"""
        if Charity.objects.filter(name=value).exists():
            raise serializers.ValidationError("🚨 Charity with this name already exists!")
        return value


class DonationAllocationSerializer(serializers.ModelSerializer):
    charity = CharitySerializer(read_only=True)

    class Meta:
        model = DonationAllocation
        fields = ["charity", "amount"]


class DonationSerializer(serializers.ModelSerializer):
    charities = serializers.PrimaryKeyRelatedField(queryset=Charity.objects.all(), many=True)
    allocations = DonationAllocationSerializer(many=True, source="donationallocation_set", read_only=True)

    class Meta:
        model = Donation
        fields = ["id", "user", "amount", "charities", "allocations", "created_at"]
        read_only_fields = ["user", "created_at"]

    def create(self, validated_data):
        charities = validated_data.pop("charities", [])
        donation = Donation.objects.create(**validated_data)
        donation.charities.set(charities)

        # ✅ Auto-create DonationAllocation entries
        if charities:
            charity_share = donation.amount * 0.5
            per_charity = charity_share / len(charities)

            for charity in charities:
                DonationAllocation.objects.create(
                    donation=donation,
                    charity=charity,
                    amount=per_charity
                )

        return donation
