import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.tickets.models import Ticket
from apps.users.models import User

print("=== Asignando tickets a usuarios de soporte ===\n")

# Obtener usuarios de soporte
soportes = User.objects.filter(role='support', is_active=True)

if soportes.count() == 0:
    print("[ERROR] No hay usuarios de soporte disponibles")
    exit(1)

print(f"Usuarios de soporte disponibles: {soportes.count()}")
for soporte in soportes:
    print(f"  - {soporte.first_name} {soporte.last_name} ({soporte.email})")

print("\n" + "="*80)

# Obtener tickets abiertos o en progreso sin asignar
tickets_sin_asignar = Ticket.objects.filter(
    assignee__isnull=True,
    status__in=['open', 'in_progress']
)

print(f"\nTickets sin asignar: {tickets_sin_asignar.count()}")

if tickets_sin_asignar.count() == 0:
    print("No hay tickets para asignar")
else:
    # Asignar cada ticket a un usuario aleatorio
    for ticket in tickets_sin_asignar:
        soporte_asignado = random.choice(soportes)
        ticket.assignee = soporte_asignado
        ticket.save()
        
        print(f"[OK] Ticket #{ticket.id} '{ticket.title[:30]}...' asignado a {soporte_asignado.first_name} {soporte_asignado.last_name}")

print(f"\n¡Completado! {tickets_sin_asignar.count()} tickets asignados aleatoriamente.")

