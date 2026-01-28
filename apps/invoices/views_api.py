from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Invoice
from .serializers import InvoiceSerializer

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.groups.filter(name='Encargador').exists():
            return Invoice.objects.all()
        else:
            # Clientes solo ven sus facturas
            return Invoice.objects.filter(cliente__usuario=self.request.user)
