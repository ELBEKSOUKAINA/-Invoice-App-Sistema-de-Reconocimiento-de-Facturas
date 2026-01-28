from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.clients.views_api import ClientViewSet
from apps.products.views_api import ProductViewSet
from apps.invoices.views_api import InvoiceViewSet

router = DefaultRouter()
router.register(r'clientes', ClientViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'facturas', InvoiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
