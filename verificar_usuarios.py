import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group

print("=== USUARIOS Y SUS GRUPOS ===")
for user in User.objects.all():
    grupos = [g.name for g in user.groups.all()]
    if grupos:
        print(f"Usuario: {user.username} - Grupos: {', '.join(grupos)}")
    else:
        print(f"Usuario: {user.username} - SIN GRUPO")

print("\n=== MIEMBROS DE CADA GRUPO ===")
for group in Group.objects.all():
    print(f"\nGrupo: {group.name}")
    for user in group.user_set.all():
        print(f"  - {user.username}")
