import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

# Crear grupos
grupo_encargador, _ = Group.objects.get_or_create(name='Encargador')
grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')

print("Grupos creados/verificados")

# Crear encargador
if not User.objects.filter(username='encargador1').exists():
    encargador = User.objects.create_user(
        username='encargador1',
        password='admin123',
        email='encargador@invoiceapp.com',
        is_staff=True,
        is_superuser=True
    )
    encargador.groups.add(grupo_encargador)
    print("Encargador creado: encargador1 / admin123")
else:
    print("El usuario encargador1 ya existe")

# Crear cliente de prueba
if not User.objects.filter(username='cliente1').exists():
    cliente = User.objects.create_user(
        username='cliente1',
        password='cliente123',
        email='cliente@email.com'
    )
    cliente.groups.add(grupo_cliente)
    print("Cliente creado: cliente1 / cliente123")
else:
    print("El usuario cliente1 ya existe")
