from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from .models import Contacts, Product, Network


class NetworkAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Создаём пользователя и аутентифицируем
        self.user = User.objects.create(
            email="test2@example.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)

        self.contacts_data = {
            "email": "contact@example.com",
            "country": "Россия",
            "city": "Москва",
            "street": "Арбат",
            "house_number": "15",
        }

        self.product_data = {
            "name": "Смартфон",
            "model": "Samsung Galaxy",
            "release_date": "2024-01-01",
        }

    def test_create_contact(self):
        response = self.client.post("/network/contacts/", self.contacts_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contacts.objects.count(), 1)
        self.assertEqual(Contacts.objects.first().email, self.contacts_data["email"])

    def test_create_product(self):
        response = self.client.post("/network/products/", self.product_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, self.product_data["name"])

    def test_create_network(self):
        contact = Contacts.objects.create(**self.contacts_data)
        product = Product.objects.create(**self.product_data)

        network_data = {
            "name": "Магазин электроники",
            "contacts": contact.id,
            "products": [product.id],
            "supplier": None
        }

        response = self.client.post("/network/networks/", network_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Network.objects.count(), 1)
        network = Network.objects.first()
        self.assertEqual(network.name, "Магазин электроники")
        self.assertEqual(network.level, 0)

    def test_list_contacts(self):
        Contacts.objects.create(**self.contacts_data)
        response = self.client.get("/network/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_products(self):
        Product.objects.create(**self.product_data)
        response = self.client.get("/network/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_network_with_supplier(self):
        # Создаем контакты для поставщика и розничной сети
        supplier_contact = Contacts.objects.create(
            email="supplier@example.com",
            country="Россия",
            city="Москва",
            street="Тверская",
            house_number="1"
        )

        retailer_contact = Contacts.objects.create(
            email="retailer@example.com",
            country="Россия",
            city="Москва",
            street="Арбат",
            house_number="15"
        )

        product = Product.objects.create(
            name="Ноутбук",
            model="XYZ-2000",
            release_date="2023-01-01"
        )

        # Создаем поставщика (уровень 0 - завод)
        supplier_data = {
            "name": "Завод Электроник",
            "contacts": supplier_contact.id,
            "products": [product.id],
            "supplier": None,
            "debt": "0.00"
        }
        supplier_response = self.client.post(
            "/network/networks/",
            supplier_data,
            format="json"
        )
        self.assertEqual(supplier_response.status_code, status.HTTP_201_CREATED)
        supplier_id = supplier_response.data["id"]

        # Создаем розничную сеть с поставщиком
        network_data = {
            "name": "Розничная сеть 1",
            "contacts": retailer_contact.id,
            "products": [product.id],
            "supplier": supplier_id,
            "debt": "0.00"
        }

        response = self.client.post(
            "/network/networks/",
            network_data,
            format="json"
        )

        # Вывод ошибок
        if response.status_code == 400:
            print(response.json())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем созданный объект
        network = Network.objects.get(name="Розничная сеть 1")
        self.assertEqual(network.level, 1)
        self.assertEqual(network.supplier.id, supplier_id)
