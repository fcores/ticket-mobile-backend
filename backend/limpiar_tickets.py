import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.tickets.models import Ticket
from apps.users.models import User

print("\n" + "="*80)
print("LIMPIEZA DE TICKETS")
print("="*80 + "\n")

# Contar tickets antes
total_antes = Ticket.objects.count()
print(f"Tickets en la base de datos: {total_antes}")

if total_antes == 0:
    print("\n[INFO] No hay tickets para eliminar.")
else:
    # Eliminar todos los tickets
    confirmacion = input(f"\n¿Estas seguro de eliminar {total_antes} tickets? (si/no): ")
    
    if confirmacion.lower() in ['si', 's', 'yes', 'y']:
        Ticket.objects.all().delete()
        print(f"\n[OK] {total_antes} tickets eliminados exitosamente!")
        
        # Verificar
        total_despues = Ticket.objects.count()
        print(f"Tickets restantes: {total_despues}")
    else:
        print("\n[CANCELADO] No se eliminaron tickets.")

print("\n" + "="*80)
print("USUARIOS EN EL SISTEMA (intactos):")
print("="*80)
for user in User.objects.all():
    print(f"  - {user.email:30} | Role: {user.role}")

print("\n[OK] Base de datos lista para empezar desde cero!")
print("="*80 + "\n")

