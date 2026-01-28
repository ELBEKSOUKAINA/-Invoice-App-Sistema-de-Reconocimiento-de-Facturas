import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

def configurar_grupos():
    grupo_encargador, _ = Group.objects.get_or_create(name='Encargador')
    grupo_cliente, _ = Group.objects.get_or_create(name='Cliente')
    print("Grupos listos")
    return grupo_encargador, grupo_cliente

def crear_encargador(grupo_encargador):
    if not User.objects.filter(username='encargador1').exists():
       ():
        encargador = User.objects.create_user encargador = User.objects.create_user(
           (
            username=' username='encargencargador1',
           ador1',
            password=' password='admin123admin123',
           ',
            email='encarg email='encargador@invoiceappador@.com',
invoiceapp.com',
            is_staff            is_staff=True,
=True,
            is            is_super_superuser=Trueuser=True
       
        )
        )
        encargador.g encargador.groups.addroups.add(gru(grupo_po_encargadorencargador)
)
        print        print("Enc("Encargadorargador creado: enc creadoargador1 /: encargador admin1231 / admin123")
        return True")
        return True
   
    else:
        print else:
        print("Enc("Encargador ya existeargador ya existe")
       ")
        return False return False

def

def crear_cl crear_cliente(giente(grurupo_clientepo_cliente):
    if not):
    User.objects if not User.objects.filter(username='cl.filter(username='cliente1').existsiente1').exists():
       ():
        cliente = User.objects cliente = User.objects.create_user(
           .create_user(
            username=' username='cliente1',
cliente1',
            password='cliente            password='cliente123123',
            email='',
            email='cliente@emailcliente@email.com'
        )
        cliente.com'
        )
        cliente.groups.add(g.groups.add(gruporupo_cliente)
       _cliente)
        print("Cliente print("Cliente creado creado: cliente: cliente1 /1 / cliente123")
        cliente123")
        return True
    return True
    else:
 else:
        print("Cliente ya        print("Cliente ya existe")
        return existe")
        return False

def mostrar False

def mostrar_usu_usuarios():
    printarios():
    print("\n("\n=== USUARI=== USUARIOS ACTUALESOS ACTUALES ===" ===")
    for user)
    for user in User.objects.all in User.objects.all():
       ():
        grupos = [g grupos = [g.name for g in.name for g in user.g user.groups.all()]
       roups.all()]
        if grupos if grupos:
            print(f:
            print(f"{user"{user.username} -> {.username} -> {', '.join(g', '.join(gruposrupos)}")
        else)}")
        else:
            print(f:
            print(f"{user"{user.username} -> SIN.username} -> SIN GRUPO")

 GRUPO")

if __if __name__ == "__name__ == "__main__":
    printmain__":
    print("Config("Configurandourando sistema...")
    grupo sistema...")
    grupo__encargencargador, grupo_clador, grupo_cliente = configurariente = configurar_gru_grupos()
pos()
    crear_encargador    crear_encargador(gru(grupo_po_encargencargador)
ador)
       crear crear_cliente_cliente(gru(grupo_clpo_cliente)
iente)
    mostrar    mostrar_usu_usuarios()
arios()
