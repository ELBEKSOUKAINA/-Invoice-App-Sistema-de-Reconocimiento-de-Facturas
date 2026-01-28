from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados
    
    def get_queryset(self):
        # Si es cliente, solo ve su propio cliente? 
        if self.request.user.groups.filter(name='Encargador').exists():
            return Client.objects.all()
        else:
            # Clientes solo ven su propio perfil
            return Client.objects.filter(usuario=self.request.user)
