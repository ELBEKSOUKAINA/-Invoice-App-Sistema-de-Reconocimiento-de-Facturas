from django.contrib import admin
from .models import Product, ProductDetail, ProductCategory

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'tipo', 'precio', 'stock', 'activo']
    list_filter = ['tipo', 'activo']
    search_fields = ['nombre', 'codigo']

@admin.register(ProductDetail)
class ProductDetailAdmin(admin.ModelAdmin):
    list_display = ['producto']

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre']
