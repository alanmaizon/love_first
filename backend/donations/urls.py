from django.urls import path, include
from rest_framework.routers import DefaultRouter
from donations.views import DonationViewSet

router = DefaultRouter()
router.register(r"donations", DonationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
