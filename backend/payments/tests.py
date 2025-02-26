# from django.contrib.auth.models import User
# from rest_framework.test import APITestCase
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken
# from core.models import Charity
# 
# class PaymentAPITestCase(APITestCase):
# 
#     def setUp(self):
#         """Create a user and get a JWT token for authentication"""
#         self.user = User.objects.create_user(username="testuser", password="testpass", email="testuser@example.com")
#         self.client.force_authenticate(user=self.user)
# 
#         self.charity = Charity.objects.create(name="Education Fund", description="Supporting education")
# 
#     def test_stripe_payment(self):
#         """✅ Test creating a Stripe checkout session"""
#         response = self.client.post("/api/stripe/checkout/", {
#             "amount": 50,
#             "charities": [self.charity.id]
#         })
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("stripe_url", response.data)
# 
#     def test_paypal_payment(self):
#         """✅ Test creating a PayPal payment link"""
#         response = self.client.post("/api/paypal/payment/", {
#             "amount": 50,
#             "charities": [self.charity.id]
#         })
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn("paypal_url", response.data)
