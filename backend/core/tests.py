from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Charity, Donation
from .serializers import UserSerializer, CharitySerializer, DonationSerializer
from django.urls import reverse
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken

class CharityModelTest(TestCase):
    def setUp(self):
        self.charity = Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")

    def test_charity_creation(self):
        self.assertEqual(self.charity.name, "Charity1")
        self.assertEqual(self.charity.description, "Description1")
        self.assertEqual(self.charity.website, "http://example.com")

class DonationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.charity = Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")
        self.donation = Donation.objects.create(user=self.user, amount=Decimal("100.00"))
        self.donation.charities.add(self.charity)

    def test_donation_creation(self):
        self.assertEqual(self.donation.user.username, "testuser")
        self.assertEqual(self.donation.amount, Decimal("100.00"))
        self.assertIn(self.charity, self.donation.charities.all())

    def test_allocate_funds(self):
        allocation = self.donation.allocate_funds()
        self.assertEqual(allocation["couple"], Decimal("50.00"))
        self.assertEqual(allocation["charities"]["Charity1"], Decimal("50.00"))

class UserSerializerTest(TestCase):
    def test_user_serializer(self):
        user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass"}
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")

class CharitySerializerTest(TestCase):
    def setUp(self):
        self.charity = Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")

    def test_charity_serializer(self):
        serializer = CharitySerializer(self.charity)
        data = serializer.data
        self.assertEqual(data["name"], "Charity1")
        self.assertEqual(data["description"], "Description1")
        self.assertEqual(data["website"], "http://example.com")

class DonationSerializerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.charity = Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")
        self.donation_data = {"user": self.user.id, "amount": Decimal("100.00"), "charities": [self.charity.id]}

    def test_donation_serializer(self):
        serializer = DonationSerializer(data=self.donation_data)
        self.assertTrue(serializer.is_valid())
        donation = serializer.save()
        self.assertEqual(donation.user.username, "testuser")
        self.assertEqual(donation.amount, Decimal("100.00"))
        self.assertIn(self.charity, donation.charities.all())

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse("register")

    def test_register_user(self):
        user_data = {"username": "testuser", "email": "test@example.com", "password": "testpass"}
        response = self.client.post(self.register_url, user_data, format="json")
        print("\nDEBUG RESPONSE:", response.status_code, response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

class UserLogoutTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.logout_url = reverse("logout")

    def test_logout_user(self):
        refresh = RefreshToken.for_user(self.user)
        response = self.client.post(self.logout_url, {"refresh": str(refresh)}, format="json")
        print("\nDEBUG RESPONSE:", response.status_code, response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logged out successfully")


class CharityListCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.charity_url = reverse("charities")

    def test_list_charities(self):
        Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")
        response = self.client.get(self.charity_url, follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_charity(self):
        charity_data = {"name": "Charity2", "description": "Description2", "website": "http://example.com"}
        response = self.client.post(self.charity_url, charity_data, format="json", follow=True)
        print("\nDEBUG URL:", reverse("charities"))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Charity2")

class DonationCreateViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)  # ✅ Authenticate user
        self.charity = Charity.objects.create(name="Charity1", description="Description1", website="http://example.com")
        self.donation_url = reverse("donate")

    def test_create_donation(self):
        donation_data = {"amount": "100.00", "charities": [self.charity.id]}
        response = self.client.post(self.donation_url, donation_data, format="json")
        print("\nDEBUG RESPONSE:", response.status_code, response.data)  # Debug
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)