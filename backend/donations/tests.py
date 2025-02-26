from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from donations.models import Donation, Charity

class DonationTests(TestCase):
    def setUp(self):
        """Set up a test user, charities, and an API client."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.charity1 = Charity.objects.create(name="Charity A", description="Help A")
        self.charity2 = Charity.objects.create(name="Charity B", description="Help B")
        self.client.force_authenticate(user=self.user)  # Simulate login

    def test_create_donation(self):
        """Test if a user can create a donation."""
        data = {"amount": "50.00", "charities": [self.charity1.id, self.charity2.id]}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Donation.objects.count(), 1)

    def test_unauthenticated_donation(self):
        """Test that an unauthenticated user cannot donate."""
        self.client.logout()
        data = {"amount": "50.00", "charities": [self.charity1.id]}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 401)  # Should be unauthorized

    def test_donation_belongs_to_user(self):
        """Test that a donation is correctly linked to a user."""
        donation = Donation.objects.create(user=self.user, amount=100.00)
        self.assertEqual(donation.user.username, "testuser")

    def test_list_donations(self):
        """Test if donations appear in the API."""
        Donation.objects.create(user=self.user, amount=25.00)
        response = self.client.get("/api/donations/")
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(len(response.data), 1)  # Should return at least one

    # ✅ Edge Cases ✅

    def test_negative_donation_amount(self):
        """Test that a donation cannot have a negative amount."""
        data = {"amount": "-10.00", "charities": [self.charity1.id]}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Should fail

    def test_zero_donation_amount(self):
        """Test that a donation cannot be zero."""
        data = {"amount": "0.00", "charities": [self.charity1.id]}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Should fail

    def test_donation_with_invalid_charity(self):
        """Test that a donation fails when given an invalid charity ID."""
        data = {"amount": "50.00", "charities": [9999]}  # Charity ID does not exist
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Should fail

    def test_donation_without_amount(self):
        """Test that a donation cannot be created without an amount."""
        data = {"charities": [self.charity1.id]}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Should fail

    def test_donation_without_charities(self):
        """Test that a donation requires at least one charity."""
        data = {"amount": "50.00", "charities": []}
        response = self.client.post("/api/donations/", data, format="json")
        self.assertEqual(response.status_code, 400)  # Should fail
