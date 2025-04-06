from django.contrib import admin
from django.utils.html import format_html

from .models import Contacts, Network, Product


@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ("email", "country", "city", "street", "house_number")
    search_fields = ("email", "city", "country")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "model", "release_date")
    search_fields = ("name", "model")
    list_filter = ("release_date",)


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ("name", "get_supplier_link", "debt", "created_at")
    list_filter = ("contacts__city",)  # Фильтр по городу
    search_fields = ("name", "contacts__city", "supplier__name")
    actions = ["clear_debt"]

    def get_supplier_link(self, obj):
        """Создает кликабельную ссылку на поставщика в админке"""
        if obj.supplier:
            return format_html(
                '<a href="/admin/{}/network/{}/">{}</a>',
                obj._meta.app_label,
                obj.supplier.id,
                obj.supplier.name
            )
        return "Нет"

    get_supplier_link.short_description = "Поставщик"  # Подпись в админке

    @admin.action(description="Очистить задолженность")
    def clear_debt(self, request, queryset):
        """Admin Action: Устанавливает задолженность в 0 у выбранных объектов"""
        queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена у {queryset.count()} объектов.")
