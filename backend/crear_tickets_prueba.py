import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.tickets.models import Ticket
from apps.users.models import User

print("\n" + "="*80)
print("CREACION DE TICKETS DE PRUEBA")
print("="*80 + "\n")

# Obtener usuarios
usuario = User.objects.get(email='usuario@test.com')
admin = User.objects.get(email='admin@test.com')
maria = User.objects.get(email='maria.garcia@support.com')
carlos = User.objects.get(email='carlos.lopez@support.com')

# Tickets de ejemplo
tickets_ejemplos = [
    {
        'title': 'Problema con el sistema de login',
        'description': 'No puedo acceder al sistema con mis credenciales habituales',
        'priority': 'high',
        'creator': usuario,
        'assignee': maria
    },
    {
        'title': 'Error en generación de reportes',
        'description': 'El sistema arroja error 500 al intentar generar reportes mensuales',
        'priority': 'urgent',
        'creator': usuario,
        'assignee': carlos
    },
    {
        'title': 'Solicitud de acceso a módulo de ventas',
        'description': 'Necesito acceso al módulo de ventas para poder consultar el histórico',
        'priority': 'medium',
        'creator': usuario,
        'assignee': None  # Sin asignar
    },
    {
        'title': 'Actualización de información personal',
        'description': 'Necesito actualizar mi número de teléfono y dirección en el sistema',
        'priority': 'low',
        'creator': usuario,
        'assignee': None  # Sin asignar
    },
    {
        'title': 'Impresora de oficina no funciona',
        'description': 'La impresora del segundo piso no responde y necesitamos imprimir documentos urgentes',
        'priority': 'medium',
        'creator': usuario,
        'assignee': maria
    },
    {
        'title': 'Solicitud de vacaciones',
        'description': 'Quiero solicitar vacaciones para la primera quincena de diciembre',
        'priority': 'low',
        'creator': usuario,
        'assignee': carlos
    }
]

print("Creando tickets de prueba...\n")

for idx, ticket_data in enumerate(tickets_ejemplos, 1):
    ticket = Ticket.objects.create(
        title=ticket_data['title'],
        description=ticket_data['description'],
        priority=ticket_data['priority'],
        creator=ticket_data['creator'],
        assignee=ticket_data['assignee'],
        status='open'
    )
    
    asignado = f"Asignado a: {ticket.assignee.first_name} {ticket.assignee.last_name}" if ticket.assignee else "Sin asignar"
    print(f"[{idx}] {ticket.title}")
    print(f"    Prioridad: {ticket.priority.upper()} | {asignado}")

print(f"\n[OK] {len(tickets_ejemplos)} tickets de prueba creados!")

print("\n" + "="*80)
print("RESUMEN:")
print("="*80)
print(f"Total de tickets: {Ticket.objects.count()}")
print(f"Sin asignar: {Ticket.objects.filter(assignee__isnull=True).count()}")
print(f"Asignados a Maria: {Ticket.objects.filter(assignee=maria).count()}")
print(f"Asignados a Carlos: {Ticket.objects.filter(assignee=carlos).count()}")
print("="*80 + "\n")

