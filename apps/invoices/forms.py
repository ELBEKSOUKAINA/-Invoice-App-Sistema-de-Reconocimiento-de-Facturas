from django import forms
from django.forms import inlineformset_factory
from .models import Invoice, InvoiceItem
from apps.clients.models import Client
from apps.products.models import Product

# FORMULARIO PRINCIPAL DE FACTURA
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['numero', 'cliente', 'fecha', 'vencimiento', 'estado']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        # Guardamos el usuario que nos pasan desde la vista
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Ponemos la clase 'form-control' a todos los campos para que se vean bonitos con Bootstrap
        for campo in self.fields:
            self.fields[campo].widget.attrs['class'] = 'form-control'
        
        # COMPROBAMOS SI EL USUARIO ES CLIENTE O ENCARGADOR
        if self.user:
            # Si NO es encargador (es cliente)
            if not self.user.groups.filter(name='Encargador').exists():
                try:
                    # Buscamos el cliente asociado a este usuario
                    cliente = Client.objects.get(usuario=self.user)
                    
                    # El campo cliente solo puede ser este cliente
                    self.fields['cliente'].queryset = Client.objects.filter(id=cliente.id)
                    self.fields['cliente'].disabled = True  # No puede cambiarlo
                    
                    # El estado solo puede ser 'borrador' para clientes
                    self.fields['estado'].initial = 'borrador'
                    self.fields['estado'].disabled = True
                    
                except Client.DoesNotExist:
                    # Si el usuario no tiene cliente asociado, no puede crear facturas
                    self.fields['cliente'].queryset = Client.objects.none()
                    self.fields['cliente'].disabled = True

# FORMULARIO PARA CADA LÍNEA DE PRODUCTO DENTRO DE LA FACTURA
class InvoiceItemForm(forms.ModelForm):
    class Meta:
        model = InvoiceItem
        fields = ['producto', 'cantidad', 'precio_unitario']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Solamente mostramos productos que están activos
        self.fields['producto'].queryset = Product.objects.filter(activo=True)
        
        # Aplicamos estilos de Bootstrap a cada campo
        self.fields['producto'].widget.attrs.update({
            'class': 'form-control producto-select'
        })
        self.fields['cantidad'].widget.attrs.update({
            'class': 'form-control cantidad-input',
            'min': 1,
            'value': 1
        })
        self.fields['precio_unitario'].widget.attrs.update({
            'class': 'form-control precio-input',
            'step': '0.01',
            'readonly': True  # El precio se carga automáticamente del producto
        })

# FORMULARIO PARA MANEJAR VARIAS LÍNEAS DE PRODUCTO A LA VEZ
# Esto permite añadir varios productos a una misma factura
InvoiceItemFormSet = inlineformset_factory(
    Invoice,        # Modelo principal (factura)
    InvoiceItem,    # Modelo hijo (líneas de factura)
    form=InvoiceItemForm,  # Usamos el formulario que creamos arriba
    extra=1,        # Mostramos 1 línea vacía para añadir producto
    can_delete=True, # Permitimos eliminar líneas
    min_num=1,      # Mínimo 1 línea (no se puede crear factura sin productos)
    validate_min=True, # Validamos que haya al menos 1 producto
)


# - InvoiceForm: Es el formulario con los datos de la factura (número, cliente, fechas...)
# - InvoiceItemForm: Es el formulario para cada producto (qué producto, cuántos, a qué precio)
# - InvoiceItemFormSet: Es un "pack" de varios InvoiceItemForm para poder añadir varios productos