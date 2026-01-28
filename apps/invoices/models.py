from django.db import models
from django.db.models import Sum, F
from decimal import Decimal


class Invoice(models.Model):
    ESTADOS_FACTURA = [
        ('borrador', ' Borrador'),
        ('enviada', ' Enviada'),
        ('pagada', ' Pagada'),
    ]

    numero = models.CharField(max_length=20, unique=True, verbose_name=" Número")
    cliente = models.ForeignKey(
        'clients.Client',
        on_delete=models.CASCADE,
        verbose_name=" Cliente"
    )
    fecha = models.DateField(verbose_name=" Fecha")
    vencimiento = models.DateField(verbose_name=" Vencimiento")

    subtotal = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=" Subtotal"
    )
    iva = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=" IVA"
    )
    total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name=" Total"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_FACTURA,
        default='borrador',
        verbose_name=" Estado"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name=" Fecha de creación"
    )

    class Meta:
        verbose_name = " Factura"
        verbose_name_plural = " Facturas"

    def __str__(self):
        return f" Factura {self.numero}"

    def calcular_totales(self):
        resultado = self.items.aggregate(
            total=Sum(F('cantidad') * F('precio_unitario'))
        )

        # CORREGIDO ↓
        subtotal = resultado['total'] if resultado['total'] is not None else Decimal('0')
        
        self.subtotal = subtotal
        self.iva = self.subtotal * Decimal('0.21')
        self.total = self.subtotal + self.iva

        self.save(update_fields=['subtotal', 'iva', 'total'])


class InvoiceItem(models.Model):
    factura = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=" Factura"
    )
    producto = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        verbose_name=" Producto"
    )
    cantidad = models.IntegerField(default=1, verbose_name=" Cantidad")
    precio_unitario = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=" Precio unitario"
    )

    class Meta:
        verbose_name = " Item de Factura"
        verbose_name_plural = " Items de Factura"

    def __str__(self):
        return f" {self.producto.nombre} x{self.cantidad}"

    @property
    def total_item(self):
        return self.cantidad * self.precio_unitario

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.factura.calcular_totales()

    def delete(self, *args, **kwargs):
        factura = self.factura
        super().delete(*args, **kwargs)
        factura.calcular_totales()


class InvoicePayment(models.Model):
    factura = models.OneToOneField(
        Invoice,
        on_delete=models.CASCADE,
        related_name='pago'
    )
    fecha_pago = models.DateField(verbose_name=" Fecha de pago")
    metodo_pago = models.CharField(max_length=50, verbose_name=" Método de pago")
    referencia = models.CharField(
        max_length=100, blank=True, verbose_name=" Referencia"
    )

    def __str__(self):
        return f" Pago de {self.factura.numero}"