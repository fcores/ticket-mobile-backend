import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.users.models import User
from apps.tickets.models import Ticket
from django.db.models import Q

print("\n" + "="*80)
print("VERIFICACION DE PERMISOS DE VISUALIZACION DE TICKETS")
print("="*80 + "\n")

total_tickets = Ticket.objects.count()
print(f"TOTAL DE TICKETS EN LA BD: {total_tickets}\n")
print("-" * 80)

# Admin 1
admin1 = User.objects.get(email='admin@test.com')
tickets_admin1 = Ticket.objects.all()  # Admin ve TODOS
print(f"ADMIN: {admin1.email}")
print(f"  Role: {admin1.role}")
print(f"  Puede ver: {tickets_admin1.count()} tickets")
print(f"  -> [OK] Ve TODOS los tickets" if tickets_admin1.count() == total_tickets else f"  -> [ERROR] Deberia ver {total_tickets}")
print()

# Admin 2
admin2 = User.objects.get(email='facundo.cores@gmail.com')
tickets_admin2 = Ticket.objects.all()  # Admin ve TODOS
print(f"ADMIN: {admin2.email}")
print(f"  Role: {admin2.role}")
print(f"  Puede ver: {tickets_admin2.count()} tickets")
print(f"  -> [OK] Ve TODOS los tickets" if tickets_admin2.count() == total_tickets else f"  -> [ERROR] Deberia ver {total_tickets}")
print()

# Soporte Maria
maria = User.objects.get(email='maria.garcia@support.com')
tickets_maria = Ticket.objects.filter(Q(assignee=maria) | Q(assignee__isnull=True))
print(f"SOPORTE: {maria.email}")
print(f"  Role: {maria.role}")
print(f"  Puede ver: {tickets_maria.count()} tickets")
print(f"  - Asignados a ella: {Ticket.objects.filter(assignee=maria).count()}")
print(f"  - Sin asignar: {Ticket.objects.filter(assignee__isnull=True).count()}")
print()

# Soporte Carlos
carlos = User.objects.get(email='carlos.lopez@support.com')
tickets_carlos = Ticket.objects.filter(Q(assignee=carlos) | Q(assignee__isnull=True))
print(f"SOPORTE: {carlos.email}")
print(f"  Role: {carlos.role}")
print(f"  Puede ver: {tickets_carlos.count()} tickets")
print(f"  - Asignados a el: {Ticket.objects.filter(assignee=carlos).count()}")
print(f"  - Sin asignar: {Ticket.objects.filter(assignee__isnull=True).count()}")
print()

# Usuario normal
usuario = User.objects.get(email='usuario@test.com')
tickets_usuario = Ticket.objects.filter(creator=usuario)
print(f"USUARIO: {usuario.email}")
print(f"  Role: {usuario.role}")
print(f"  Puede ver: {tickets_usuario.count()} tickets (solo creados por el)")
print()

print("="*80)
print("RESUMEN:")
print("  - Admins ven TODOS los tickets independientemente de asignacion")
print("  - Soporte ve tickets asignados a el + sin asignar")
print("  - Usuarios solo ven tickets que crearon")
print("="*80 + "\n")

