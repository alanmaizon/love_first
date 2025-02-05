from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CharityViewSet, DonationViewSet

router = DefaultRouter()
router.register(r"charities", CharityViewSet)
router.register(r"donations", DonationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
