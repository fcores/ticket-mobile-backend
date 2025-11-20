import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.users.models import User

print("=== Creando usuarios de soporte ===\n")

# Usuario de Soporte 1
if User.objects.filter(email='maria.garcia@support.com').exists():
    User.objects.filter(email='maria.garcia@support.com').delete()
    print("[INFO] Usuario existente eliminado")

soporte1 = User.objects.create_user(
    username='maria.garcia@support.com',
    email='maria.garcia@support.com',
    password='Soporte123!',
    first_name='Maria',
    last_name='Garcia',
    role='support',
    is_staff=True,
    is_superuser=False
)
print(f"[OK] Soporte creado: maria.garcia@support.com / Soporte123!")

# Usuario de Soporte 2
if User.objects.filter(email='carlos.lopez@support.com').exists():
    User.objects.filter(email='carlos.lopez@support.com').delete()
    print("[INFO] Usuario existente eliminado")

soporte2 = User.objects.create_user(
    username='carlos.lopez@support.com',
    email='carlos.lopez@support.com',
    password='Soporte123!',
    first_name='Carlos',
    last_name='Lopez',
    role='support',
    is_staff=True,
    is_superuser=False
)
print(f"[OK] Soporte creado: carlos.lopez@support.com / Soporte123!")

print("\n¡Listo! Usuarios de soporte creados:")
print("   - maria.garcia@support.com / Soporte123!")
print("   - carlos.lopez@support.com / Soporte123!")

