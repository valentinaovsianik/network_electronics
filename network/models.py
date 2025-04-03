from django.db import models

NULLABLE = {"blank": True, "null": True}


class Contacts(models.Model):
    """Модель для хранения контактной информации"""

    email = models.EmailField(verbose_name="Электронная почта")
    country = models.CharField(max_length=100, verbose_name="Cтрана")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=20, verbose_name="Номер дома")

    class Meta:
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"

    def __str__(self):
        return f"{self.email} {self.country} {self.city} {self.street} {self.house_number}"


class Product(models.Model):
    """Модель для хранения информации о продукте"""

    name = models.CharField(max_length=100, verbose_name="Название")
    model = models.CharField(max_length=100, verbose_name="Модель")
    release_date = models.DateField(verbose_name="Дата выхода продукта на рынок")

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        return f"{self.name} {self.model} {self.release_date}"


class Network(models.Model):
    """Модель сети по продаже электроники"""

    LEVEL_CHOICES = (
        (0, "Завод"),
        (1, "Розничная сеть"),
        (2, "ИП"),
    )

    name = models.CharField(max_length=100, verbose_name="Название")
    contacts = models.OneToOneField(Contacts, on_delete=models.CASCADE, verbose_name="Контакты", **NULLABLE)
    products = models.ManyToManyField(Product, verbose_name="Продукты", blank=True)
    supplier = models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name="Поставщик", **NULLABLE)
    debt = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Задолженность перед поставщиком",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    level = models.IntegerField(choices=LEVEL_CHOICES, verbose_name="Уровень иерархии", editable=False)

    class Meta:
        verbose_name = "Сеть"
        verbose_name_plural = "Сети"


    def save(self, *args, **kwargs):
        """Автоматически устанавливает уровень иерархии перед сохранением"""
        if self.supplier:
            self.level = self.supplier.level + 1
        else:
            self.level = 0  # Завод (верхний уровень)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} (Уровень: {self.get_level_display()}), Поставщик: {self.supplier.name if self.supplier else 'Нет'}"
