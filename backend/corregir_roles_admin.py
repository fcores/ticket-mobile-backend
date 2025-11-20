import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.users.models import User

print("=== Corrigiendo roles de administradores ===\n")

# Actualizar admin@test.com
admin1 = User.objects.get(email='admin@test.com')
admin1.role = 'sysAdmin'
admin1.save()
print(f"[OK] {admin1.email} -> role: sysAdmin")

# Actualizar facundo.cores@gmail.com
admin2 = User.objects.get(email='facundo.cores@gmail.com')
admin2.role = 'sysAdmin'
admin2.save()
print(f"[OK] {admin2.email} -> role: sysAdmin")

print("\nVerificando roles actualizados:")
print("-" * 80)
for user in User.objects.all():
    print(f"{user.email:30} | Role: {user.role:10} | Staff: {user.is_staff} | Superuser: {user.is_superuser}")

print("\n[OK] Roles corregidos exitosamente!")

