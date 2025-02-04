from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Charity, Donation

# UserSerializer: This serializer is used to serialize the User model. It includes the fields id, username, email, and password. The password field is write-only, meaning that it can be used to create a new user but will not be included in the response.

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

# CharitySerializer: This serializer is used to serialize the Charity model. It includes all fields from the model. The Meta class specifies the model and fields to include in the serialization.

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = "__all__"

# DonationSerializer: This serializer is used to serialize the Donation model. It includes the fields id, user, amount, date, and charities. The charities field is a ManyToManyField that references the Charity model. The create method is overridden to handle the creation of a new donation with the associated charities.

class DonationSerializer(serializers.ModelSerializer):
    charities = serializers.PrimaryKeyRelatedField(many=True, queryset=Charity.objects.all())

    class Meta:
        model = Donation
        fields = ["id", "user", "amount", "date", "charities"]

    def create(self, validated_data):
        charities = validated_data.pop("charities")
        donation = Donation.objects.create(**validated_data)
        donation.charities.set(charities)
        return donation