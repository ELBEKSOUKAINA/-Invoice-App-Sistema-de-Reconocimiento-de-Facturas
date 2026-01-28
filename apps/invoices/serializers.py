from rest_framework import serializers
from .models import Invoice
from apps.clients.serializers import ClientSerializer
from apps.products.serializers import ProductSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    # incluir datos completos del cliente y productos
    cliente_detalle = ClientSerializer(source='cliente', read_only=True)
    
    class Meta:
        model = Invoice
        fields = '__all__'
