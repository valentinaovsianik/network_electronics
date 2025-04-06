from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import ContactsViewSet, NetworkViewSet, ProductViewSet

app_name = "network"

router = SimpleRouter()

router.register(r"contacts", ContactsViewSet)
router.register(r"products", ProductViewSet)
router.register(r"networks", NetworkViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
