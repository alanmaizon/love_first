from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Charity, Donation
from decimal import Decimal

class CharityModelTest(TestCase):
    def setUp(self):
        self.charity = Charity.objects.create(name="Operation Smile", description="Helps children with cleft conditions.")

    def test_charity_creation(self):
        self.assertEqual(self.charity.name, "Operation Smile")
        self.assertEqual(str(self.charity), "Operation Smile")

    def test_charity_unique_name(self):
        with self.assertRaises(Exception):
            Charity.objects.create(name="Operation Smile", description="Duplicate charity.")

class DonationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="john_doe", password="secure123")
        self.charity1 = Charity.objects.create(name="Mary's Meals", description="Provides meals to children.")
        self.charity2 = Charity.objects.create(name="Xingu Vivo", description="Protects indigenous Amazon lands.")
        self.donation = Donation.objects.create(user=self.user, amount=Decimal("100.00"))
        self.donation.charities.set([self.charity1, self.charity2])

    def test_donation_creation(self):
        self.assertEqual(self.donation.amount, Decimal("100.00"))
        self.assertEqual(str(self.donation), f"john_doe - €100.00 on {self.donation.date.strftime('%Y-%m-%d')}")

    def test_fund_allocation(self):
        allocation = self.donation.allocate_funds()
        self.assertEqual(allocation["couple"], Decimal("50.00"))
        self.assertEqual(allocation["charities"][self.charity1.name], Decimal("25.00"))
        self.assertEqual(allocation["charities"][self.charity2.name], Decimal("25.00"))
