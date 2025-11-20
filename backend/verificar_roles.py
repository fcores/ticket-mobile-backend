import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from apps.users.models import User
from apps.tickets.models import Ticket

print("\n" + "="*80)
print("VERIFICACIÓN DE ROLES Y PERMISOS")
print("="*80 + "\n")

print("USUARIOS EN EL SISTEMA:")
print("-" * 80)
users = User.objects.all()
for user in users:
    print(f"Email: {user.email}")
    print(f"  Role: {user.role}")
    print(f"  Is Staff: {user.is_staff}")
    print(f"  Is Superuser: {user.is_superuser}")
    print()

print("\n" + "="*80)
print("TICKETS POR USUARIO")
print("="*80 + "\n")

for user in users:
    if user.role == 'sysAdmin':
        # Admin debe ver TODOS los tickets
        tickets_admin = Ticket.objects.all()
        print(f"🔐 ADMIN ({user.email}):")
        print(f"   Puede ver: {tickets_admin.count()} tickets (TODOS)")
        print()
    elif user.role == 'support':
        # Support ve tickets asignados a él O sin asignar
        from django.db.models import Q
        tickets_support = Ticket.objects.filter(
            Q(assignee=user) | Q(assignee__isnull=True)
        )
        print(f"👷 SOPORTE ({user.email}):")
        print(f"   Puede ver: {tickets_support.count()} tickets")
        print(f"   - Asignados a él: {Ticket.objects.filter(assignee=user).count()}")
        print(f"   - Sin asignar: {Ticket.objects.filter(assignee__isnull=True).count()}")
        print()
    else:
        # Usuario normal solo ve sus propios tickets
        tickets_user = Ticket.objects.filter(creator=user)
        print(f"👤 USUARIO ({user.email}):")
        print(f"   Puede ver: {tickets_user.count()} tickets (solo propios)")
        print()

print("\n" + "="*80)
print("RESUMEN DE TICKETS")
print("="*80)
print(f"Total de tickets: {Ticket.objects.count()}")
print(f"Tickets sin asignar: {Ticket.objects.filter(assignee__isnull=True).count()}")
print(f"Tickets asignados a Maria Garcia: {Ticket.objects.filter(assignee__first_name='Maria').count()}")
print(f"Tickets asignados a Carlos Lopez: {Ticket.objects.filter(assignee__first_name='Carlos').count()}")
print()

