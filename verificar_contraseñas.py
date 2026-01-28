from django.contrib.auth.models import User

try:
    user = User.objects.get(username='cliente1')
    user.set_password('cliente123')
    user.save()
    print("Contraseña de cliente1 cambiada a: cliente123")
except:
    print("El usuario cliente1 no existe, creándolo...")
    user = User.objects.create_user('cliente1', 'cliente@email.com', 'cliente123')
    print("Usuario cliente1 creado con contraseña: cliente123")

from django.contrib.auth.models import Group
grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')
user.groups.add(grupo_cliente)
print(f"Usuario {user.username} asignado al grupo Cliente")

print(f"\nUsuario: {user.username}")
print(f"Contraseña: cliente123")
print(f"Grupos: {[g.name for g in user.groups.all()]}")

exit()