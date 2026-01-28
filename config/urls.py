"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from rest_framework import routers
from apps.clients.views_api import ClientViewSet
from apps.products.views_api import ProductViewSet
from apps.invoices.views_api import InvoiceViewSet

# Vista simple para la página de inicio
def home_view(request):
    return render(request, 'home.html')
    
# Router para la API
router = routers.DefaultRouter()
router.register(r'clientes', ClientViewSet)
router.register(r'productos', ProductViewSet)
router.register(r'facturas', InvoiceViewSet)

urlpatterns = [
    # Página principal (home)
    path('', home_view, name='home'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # LÍNEA PARA AUTENTICACIÓN:
    path('auth/', include('apps.invoice_system.urls')),
    
    # apps con namespaces
    path('clientes/', include('apps.clients.urls', namespace='clients')),
    path('productos/', include('apps.products.urls', namespace='products')),
    path('facturas/', include('apps.invoices.urls',
namespace='invoices')),

# API REST
    path('api/', include(router.urls)),
]
