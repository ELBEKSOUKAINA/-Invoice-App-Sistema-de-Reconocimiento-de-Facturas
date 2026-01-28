from django.db import models

class Product(models.Model):
    TIPOS_PRODUCTO = [
        ('sanitario', ' Sanitario'),
        ('griferia', ' Grifería'),
        ('accesorio', ' Accesorio'),
    ]
    
    nombre = models.CharField(max_length=100, verbose_name=" Nombre")
    descripcion = models.TextField(blank=True, verbose_name=" Descripción")
    codigo = models.CharField(max_length=50, unique=True, verbose_name=" Código")
    tipo = models.CharField(max_length=20, choices=TIPOS_PRODUCTO, default='sanitario', verbose_name=" Tipo")
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=" Precio")
    stock = models.IntegerField(default=0, verbose_name=" Stock")
    activo = models.BooleanField(default=True, verbose_name=" Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name=" Fecha de creación")
    

    visible_para_clientes = models.ManyToManyField(
        'clients.Client',
        blank=True,
        verbose_name=" Visible para clientes"
    )
 

    class Meta:
        verbose_name = " Producto"
        verbose_name_plural = " Productos"

    def __str__(self):
        return f" {self.nombre}"

#ONEtoONE RELATION
class ProductDetail(models.Model):
    producto = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='detalle')
    especificaciones = models.TextField(blank=True, verbose_name=" Especificaciones")
    instrucciones = models.TextField(blank=True, verbose_name=" Instrucciones de uso")
    garantia = models.IntegerField(default=12, verbose_name=" Meses de garantía")

    def __str__(self):
        return f" Detalles de {self.producto.nombre}"

#MANYtoMANY RELATION
class ProductCategory(models.Model):
    nombre = models.CharField(max_length=50, verbose_name=" Categoría")
    productos = models.ManyToManyField(Product, related_name='categorias', blank=True, verbose_name=" Productos")
    
    class Meta:
        verbose_name = " Categoría de Producto"
        verbose_name_plural = " Categorías de Productos"

    def __str__(self):
        return f" {self.nombre}"