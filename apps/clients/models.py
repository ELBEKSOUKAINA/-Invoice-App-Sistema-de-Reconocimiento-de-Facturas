from django.db import models
from django.contrib.auth.models import User 

class Client(models.Model):
    TIPOS_CLIENTE = [
        ('individual', ' Persona'),
        ('empresa', ' Empresa'),
    ]
    

    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        verbose_name=" Usuario Django"
    )
    es_encargado = models.BooleanField(
        default=False, 
        verbose_name=" Es encargado"
    )

    
    nombre = models.CharField(max_length=100, verbose_name=" Nombre")
    email = models.EmailField(verbose_name=" Correo electrónico")
    telefono = models.CharField(max_length=15, blank=True, verbose_name=" Teléfono")
    direccion = models.TextField(blank=True, verbose_name=" Dirección")
    tipo = models.CharField(max_length=20, choices=TIPOS_CLIENTE, default='individual', verbose_name=" Tipo")
    activo = models.BooleanField(default=True, verbose_name=" Activo")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name=" Fecha de creación")

    class Meta:
        verbose_name = " Cliente"
        verbose_name_plural = " Clientes"

    def __str__(self):
        return f" {self.nombre}"

# ONEtoONE RELATION
class ClientProfile(models.Model):
    cliente = models.OneToOneField(Client, on_delete=models.CASCADE, related_name='perfil')
    notas_internas = models.TextField(blank=True, verbose_name=" Notas internas")
    preferencias = models.TextField(blank=True, verbose_name=" Preferencias")
    fecha_registro = models.DateField(auto_now_add=True, verbose_name=" Fecha de registro")

    def __str__(self):
        return f" Perfil de {self.cliente.nombre}"

# MANYtoMANY RELATION
class ClientCategory(models.Model):
    nombre = models.CharField(max_length=50, verbose_name=" Categoría")
    descripcion = models.TextField(blank=True, verbose_name=" Descripción")
    clientes = models.ManyToManyField(
        Client, 
        related_name='categorias', 
        blank=True, 
        verbose_name=" Clientes"
    )
    
    class Meta:
        verbose_name = " Categoría de Cliente"
        verbose_name_plural = " Categorías de Clientes"

    def __str__(self):
        return f" {self.nombre}"