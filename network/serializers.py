from rest_framework import serializers

from .models import Contacts, Network, Product


class ContactsSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Contacts"""

    class Meta:
        model = Contacts
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Product"""

    class Meta:
        model = Product
        fields = "__all__"


class NetworkSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Network"""

    class Meta:
        model = Network
        fields = "__all__"
        read_only_fields = ("debt",)  # Запрет на редактирование задолженности
