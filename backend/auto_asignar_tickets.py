"""
Script para asignar automáticamente tickets sin asignar a usuarios de soporte.
Ejecutar periódicamente o cuando se creen nuevos tickets.
"""
import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.tickets.models import Ticket
from apps.users.models import User

def asignar_tickets_automaticamente():
    """Asigna tickets sin asignar a usuarios de soporte de forma aleatoria."""
    
    # Obtener usuarios de soporte activos
    soportes = list(User.objects.filter(role='support', is_active=True))
    
    if not soportes:
        print("[ERROR] No hay usuarios de soporte disponibles")
        return 0
    
    # Obtener tickets sin asignar que estén abiertos o en progreso
    tickets_sin_asignar = Ticket.objects.filter(
        assignee__isnull=True,
        status__in=['open', 'in_progress']
    )
    
    count = 0
    for ticket in tickets_sin_asignar:
        # Asignar a un soporte aleatorio
        soporte = random.choice(soportes)
        ticket.assignee = soporte
        ticket.save()
        count += 1
        print(f"[OK] Ticket #{ticket.id} asignado a {soporte.first_name} {soporte.last_name}")
    
    return count

if __name__ == '__main__':
    print("=== Auto-asignación de Tickets ===\n")
    tickets_asignados = asignar_tickets_automaticamente()
    print(f"\n✓ Total de tickets asignados: {tickets_asignados}")

