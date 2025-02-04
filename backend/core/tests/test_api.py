from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Charity, Donation
from decimal import Decimal

class CharityAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.charity_data = {"name": "Save the Children", "description": "Helping kids worldwide."}
        self.charity_url = "/api/charities/"

    def test_create_charity(self):
        response = self.client.post(self.charity_url, self.charity_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Charity.objects.count(), 1)

    def test_get_charities(self):
        Charity.objects.create(**self.charity_data)
        response = self.client.get(self.charity_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class DonationAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="john_doe", password="secure123")
        self.client.force_authenticate(user=self.user)
        self.charity = Charity.objects.create(name="Red Cross", description="Disaster relief.")
        self.donation_url = "/api/donate/"

    def test_create_donation(self):
        data = {"amount": "50.00", "charities": [self.charity.id]}
        response = self.client.post(self.donation_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Donation.objects.count(), 1)
        self.assertEqual(Donation.objects.first().amount, Decimal("50.00"))

    def test_create_donation_unauthenticated(self):
        self.client.force_authenticate(user=None)
        response = self.client.post(self.donation_url, {"amount": "50.00"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
