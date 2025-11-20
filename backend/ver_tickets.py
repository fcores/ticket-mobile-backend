import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.tickets.models import Ticket
from apps.users.models import User

print("\n" + "="*80)
print("TICKETS EN LA BASE DE DATOS")
print("="*80 + "\n")

tickets = Ticket.objects.all().order_by('-created_at')

if not tickets:
    print("No hay tickets en la base de datos.")
else:
    for ticket in tickets:
        print(f"ID: {ticket.id}")
        print(f"Titulo: {ticket.title}")
        print(f"Descripcion: {ticket.description[:50]}..." if len(ticket.description) > 50 else f"Descripcion: {ticket.description}")
        print(f"Estado: {ticket.get_status_display()}")
        print(f"Prioridad: {ticket.get_priority_display()}")
        print(f"Creador: {ticket.creator.email}")
        print(f"Asignado a: {ticket.assignee.email if ticket.assignee else 'Sin asignar'}")
        print(f"Creado: {ticket.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)

print(f"\nTotal de tickets: {tickets.count()}")
print(f"Total de usuarios: {User.objects.count()}\n")

