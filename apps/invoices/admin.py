from django.contrib import admin
from .models import Invoice, InvoiceItem, InvoicePayment

class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['numero', 'cliente', 'fecha', 'total', 'estado']
    list_filter = ['estado', 'fecha']
    search_fields = ['numero', 'cliente__nombre']
    inlines = [InvoiceItemInline]

@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ['factura', 'producto', 'cantidad', 'precio_unitario', 'total_item']

@admin.register(InvoicePayment)
class InvoicePaymentAdmin(admin.ModelAdmin):
    list_display = ['factura', 'fecha_pago', 'metodo_pago']