
from .models import Donation
from .serializers import DonationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.select_related("user").prefetch_related("charities").order_by("-created_at")
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username"]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            charities = self.request.data.get("charities", [])
            donation = serializer.save(user=self.request.user)  # Save first
            donation.charities.set(charities)  # Set charities after saving
        except Exception as e:
            print(f"❌ Donation Creation Error: {e}")
            return Response({"error": str(e)}, status=500)


    @action(detail=False, methods=["get"])
    def latest(self, request):
        """Return the latest donation for the authenticated user."""
        latest_donation = Donation.objects.filter(user=request.user).order_by("-created_at").first()
        if not latest_donation:
            return Response({"detail": "No donations found."}, status=404)
        return Response(DonationSerializer(latest_donation).data)
