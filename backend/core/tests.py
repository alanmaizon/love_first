from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken  # Import JWT tokens
from .models import Charity

class CharityAPITestCase(APITestCase):

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.admin_user = User.objects.create_superuser(username="admin", password="adminpass")
        self.charity = Charity.objects.create(name="Save the Children", description="Helping kids worldwide")

        # Get admin authentication token
        refresh = RefreshToken.for_user(self.admin_user)
        self.admin_token = str(refresh.access_token)

    def authenticate_admin(self):
        """Helper function to authenticate admin"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")

    def test_create_charity_invalid_data(self):
        """🚫 Test creating a charity with missing fields"""
        self.authenticate_admin()
        
        # Missing 'name' field
        response = self.client.post("/api/charities/", {"description": "No name provided"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # Ensure error message is for 'name'

    def test_create_duplicate_charity(self):
        """🚫 Test creating a duplicate charity (should fail)"""
        self.authenticate_admin()
        
        data = {"name": "Save the Children", "description": "Duplicate charity"}
        response = self.client.post("/api/charities/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)  # Ensure error message is for 'name'

    def test_list_charities(self):
        """✅ Test retrieving the list of charities (now checking pagination results)"""
        response = self.client.get("/api/charities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)  # Ensure response is paginated
        self.assertEqual(len(response.data["results"]), 1)  # ✅ Fix: check paginated data

    def test_get_single_charity(self):
        """✅ Test retrieving a single charity"""
        response = self.client.get(f"/api/charities/{self.charity.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Save the Children")

    def test_create_charity_unauthorized(self):
        """🚫 Unauthorized users cannot create charities"""
        data = {"name": "New Charity", "description": "A test charity"}
        response = self.client.post("/api/charities/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Expecting 401 Unauthorized

    def test_create_charity_authorized(self):
        """✅ Admin users can create charities"""
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.admin_token}")  # Use JWT auth
        data = {"name": "New Charity", "description": "A test charity"}
        response = self.client.post("/api/charities/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Charity.objects.count(), 2)

    def test_filter_charities_by_name(self):
        """✅ Test filtering charities by name (checking paginated results)"""
        Charity.objects.create(name="Education First", description="A charity for education")
        Charity.objects.create(name="Education for All", description="Another charity")
        Charity.objects.create(name="Health First", description="A health charity")
    
        response = self.client.get("/api/charities/?search=Education")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # ✅ Fix: Check paginated response inside "results"
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 2)  # Expect 2 Education-related charities

    def test_charity_pagination(self):
        """✅ Ensure pagination works correctly"""
        # Create 10 charities
        for i in range(10):
            Charity.objects.create(name=f"Charity {i}", description="Test")

        response = self.client.get("/api/charities/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("next", response.data)  # Pagination should include 'next' URL
        self.assertEqual(len(response.data["results"]), 5)  # Ensure page size = 5
