#!/usr/bin/env python
"""
Script para inicializar datos en Railway después del deploy
Ejecutar: python init_railway_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.categories.models import Category
from apps.tickets.models import Ticket

User = get_user_model()

print('=' * 70)
print('INICIALIZANDO DATOS EN RAILWAY')
print('=' * 70)

# 1. Crear usuarios
print('\n1. Creando usuarios...')
users_data = [
    {
        'email': 'admin@test.com',
        'password': 'Admin123!',
        'first_name': 'Admin',
        'last_name': 'Sistema',
        'role': 'sysAdmin'
    },
    {
        'email': 'maria.garcia@support.com',
        'password': 'Soporte123!',
        'first_name': 'Maria',
        'last_name': 'Garcia',
        'role': 'support'
    },
    {
        'email': 'carlos.lopez@support.com',
        'password': 'Soporte123!',
        'first_name': 'Carlos',
        'last_name': 'Lopez',
        'role': 'support'
    },
    {
        'email': 'usuario@test.com',
        'password': 'Usuario123!',
        'first_name': 'Usuario',
        'last_name': 'Prueba',
        'role': 'user'
    },
]

for user_data in users_data:
    if not User.objects.filter(email=user_data['email']).exists():
        # Usar create_superuser para admin, create_user para los demás
        if user_data['role'] == 'sysAdmin':
            User.objects.create_superuser(
                username=user_data['email'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
        else:
            User.objects.create_user(
                username=user_data['email'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                role=user_data['role']
            )
        print(f'   ✓ Usuario creado: {user_data["email"]}')
    else:
        # Actualizar usuario existente si es admin para asegurar permisos
        if user_data['role'] == 'sysAdmin':
            user = User.objects.get(email=user_data['email'])
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f'   ✓ Admin actualizado: {user_data["email"]}')
        else:
            print(f'   - Usuario ya existe: {user_data["email"]}')

# 2. Crear categorías
print('\n2. Creando categorías...')
categories = [
    {'name': 'Técnico', 'description': 'Problemas técnicos y de software'},
    {'name': 'Hardware', 'description': 'Problemas de equipamiento físico'},
    {'name': 'Acceso', 'description': 'Problemas de permisos y accesos'},
    {'name': 'General', 'description': 'Consultas generales'},
]

for cat_data in categories:
    if not Category.objects.filter(name=cat_data['name']).exists():
        Category.objects.create(**cat_data)
        print(f'   ✓ Categoría creada: {cat_data["name"]}')
    else:
        print(f'   - Categoría ya existe: {cat_data["name"]}')

# 3. Crear tickets de ejemplo
print('\n3. Creando tickets de ejemplo...')
usuario = User.objects.get(email='usuario@test.com')
support1 = User.objects.get(email='maria.garcia@support.com')
support2 = User.objects.get(email='carlos.lopez@support.com')

tickets_data = [
    {
        'title': 'Problema con el sistema de login',
        'description': 'No puedo acceder al sistema con mis credenciales habituales',
        'priority': 'high',
        'creator': usuario,
        'assignee': support1
    },
    {
        'title': 'Error en generación de reportes',
        'description': 'El sistema arroja error 500 al intentar generar reportes mensuales',
        'priority': 'urgent',
        'creator': usuario,
        'assignee': support2
    },
    {
        'title': 'Solicitud de vacaciones',
        'description': 'Quiero solicitar vacaciones para la primera quincena de diciembre',
        'priority': 'low',
        'creator': usuario,
        'assignee': support2
    },
]

for ticket_data in tickets_data:
    if not Ticket.objects.filter(title=ticket_data['title']).exists():
        Ticket.objects.create(**ticket_data)
        print(f'   ✓ Ticket creado: {ticket_data["title"]}')
    else:
        print(f'   - Ticket ya existe: {ticket_data["title"]}')

print('\n' + '=' * 70)
print('✓ INICIALIZACIÓN COMPLETADA')
print('=' * 70)
print(f'\nUsuarios totales: {User.objects.count()}')
print(f'Categorías totales: {Category.objects.count()}')
print(f'Tickets totales: {Ticket.objects.count()}')
print('\nCredenciales de acceso:')
print('  Admin: admin@test.com / Admin123!')
print('  Soporte: maria.garcia@support.com / Soporte123!')
print('  Usuario: usuario@test.com / Usuario123!')
print('=' * 70)

