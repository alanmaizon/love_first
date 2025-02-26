from rest_framework import viewsets, permissions, filters
from .models import Charity
from .serializers import CharitySerializer
from rest_framework.pagination import PageNumberPagination

class CharityPagination(PageNumberPagination):
    page_size = 5  # Override default page size if needed
    page_size_query_param = "page_size"
    max_page_size = 50

class CharityViewSet(viewsets.ModelViewSet):
    queryset = Charity.objects.only("id", "name").order_by('name')  # Fetch only needed fields
    serializer_class = CharitySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    pagination_class = CharityPagination

    def get_permissions(self):
        """Allow anyone to GET, but only admins can POST"""
        if self.request.method in permissions.SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [permissions.AllowAny()]
        return [permissions.IsAdminUser()]  # Only admins can POST, PUT, DELETE


