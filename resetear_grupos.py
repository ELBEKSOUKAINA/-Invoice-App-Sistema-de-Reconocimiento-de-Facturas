import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

def asignar_grupo(username, nombre_grupo):
    try:
        user = User.objects.get(username=username)
        grupo, _ = Group.objects.get_or_create(name=nombre_grupo)
        
        # Quitar todos los grupos actuales
        user.groups.clear()
        
        # Asignar el nuevo grupo
        user.groups.add(grupo)
        
        # Configurar permisos de admin según el grupo
        if nombre_grupo == 'Encargador':
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        
        user.save()
        print(f"Usuario {username} ahora es {nombre_grupo}")
        return True
    except User.DoesNotExist:
        print(f"ERROR: Usuario {username} no existe")
        return False

def listar_usuarios():
    print("\n=== USUARIOS DISPONIBLES ===")
    usuarios = User.objects.all()
    if not usuarios:
        print("No hay usuarios en el sistema")
    else:
        for user in usuarios:
            grupos = [g.name for g in user.groups.all()]
            if grupos:
                print(f"  - {user.username} ({', '.join(grupos)})")
            else:
                print(f"  - {user.username} (sin grupo)")

def resetear_todos():
    print("\n=== RESETEANDO GRUPOS ===")
    asignar_grupo('encargador1', 'Encargador')
    asignar_grupo('cliente1', 'Cliente')
    
    # Si tienes usuario admin, descomenta la siguiente línea:
    # asignar_grupo('admin', 'Encargador')

if __name__ == "__main__":
    print("SCRIPT: Resetear Grupos")
    print("=" * 50)
    
    # Mostrar usuarios actuales
    listar_usuarios()
    
    # Preguntar qué hacer
    print("\nOpciones:")
    print("  1. Resetear usuarios por defecto (encargador1, cliente1)")
    print("  2. Resetear un usuario específico")
    print("  3. Salir")
    
    opcion = input("\nSelecciona una opción (1, 2 o 3): ")
    
    if opcion == '1':
        resetear_todos()
    elif opcion == '2':
        username = input("Nombre de usuario a resetear: ")
        print("Grupos disponibles: Cliente, Encargador")
        grupo = input("Asignar grupo: ")
        asignar_grupo(username, grupo)
    else:
        print("Saliendo...")
    
    # Mostrar resultado final
    print("\n=== RESULTADO FINAL ===")
    listar_usuarios()
