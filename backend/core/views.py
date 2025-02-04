from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import UserSerializer
from rest_framework import generics
from .models import Charity, Donation
from .serializers import CharitySerializer, DonationSerializer
from rest_framework.permissions import IsAuthenticated

# CharityListCreateView: This view class is used to list all charities and create a new charity. It extends the ListCreateAPIView class provided by Django REST framework and specifies the queryset and serializer class to use.

class CharityListCreateView(generics.ListCreateAPIView):
    queryset = Charity.objects.all()
    serializer_class = CharitySerializer

# DonationCreateView: This view class is used to create a new donation. It extends the CreateAPIView class provided by Django REST framework and specifies the queryset and serializer class to use. It also sets the permission_classes attribute to [IsAuthenticated] to require authentication for creating donations.

class DonationCreateView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# register_user: This view function is used to register a new user. It takes a POST request with user data, validates the data using the UserSerializer, and creates a new user if the data is valid. It returns a response with the user's access and refresh tokens if the user is created successfully.

@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# login_user: This view function is used to log in a user. It takes a POST request with user credentials, validates the credentials, and returns the user's access and refresh tokens if the credentials are valid.

@api_view(["POST"])
def logout_user(request):
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

