from rest_framework import serializers
from .models import Charity

class CharitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Charity
        fields = "__all__"

    def validate_name(self, value):
        """Ensure charity name is unique"""
        if Charity.objects.filter(name=value).exists():
            raise serializers.ValidationError("🚨 Charity with this name already exists!")
        return value
