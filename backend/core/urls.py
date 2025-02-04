from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import register_user, logout_user, CharityListCreateView, DonationCreateView

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", logout_user, name="logout"),
    path("charities/", CharityListCreateView.as_view(), name="charities"),
    path("donate/", DonationCreateView.as_view(), name="donate"),
]
