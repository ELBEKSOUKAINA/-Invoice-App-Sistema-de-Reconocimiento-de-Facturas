from django.contrib import admin
from .models import Client, ClientProfile, ClientCategory

class CategoriaInline(admin.TabularInline):
    model = ClientCategory.clientes.through
    extra = 1

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'tipo', 'activo']
    list_filter = ['tipo', 'activo', 'categorias']
    search_fields = ['nombre', 'email']
    inlines = [CategoriaInline]
    exclude = ('categorias',)

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'fecha_registro']

@admin.register(ClientCategory)
class ClientCategoryAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    filter_horizontal = ['clientes']