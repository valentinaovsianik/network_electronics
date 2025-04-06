from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from users.permissions import IsActive

from .models import Contacts, Network, Product
from .serializers import ContactsSerializer, NetworkSerializer, ProductSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    """CRUD для модели Network с запретом изменения задолженности"""

    queryset = Network.objects.all()
    serializer_class = NetworkSerializer
    permission_classes = [IsActive]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {"contacts__country": ["exact"]}  # Фильтрация по стране независимо от регистра
    search_fields = ["name", "contacts__city"]  # Поиск по названию и городу


class ContactsViewSet(viewsets.ModelViewSet):
    """CRUD для модели Contacts"""

    queryset = Contacts.objects.all()
    serializer_class = ContactsSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "city", "country"]  # Поиск по email, городу, стране


class ProductViewSet(viewsets.ModelViewSet):
    """CRUD для модели Product"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "model"]  # Поиск по названию и модели
