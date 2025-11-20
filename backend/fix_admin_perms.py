#!/usr/bin/env python
"""Script para corregir permisos del admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

print('=' * 60)
print('ACTUALIZANDO PERMISOS DE ADMIN')
print('=' * 60)

# Actualizar o crear admin
email = 'admin@test.com'
try:
    user = User.objects.get(email=email)
    user.is_staff = True
    user.is_superuser = True
    user.set_password('Admin123!')  # Resetear contraseña por si acaso
    user.role = 'sysAdmin'
    user.save()
    print(f'✓ Admin actualizado: {email}')
    print(f'  - is_staff: {user.is_staff}')
    print(f'  - is_superuser: {user.is_superuser}')
    print(f'  - role: {user.role}')
except User.DoesNotExist:
    user = User.objects.create_superuser(
        username=email,
        email=email,
        password='Admin123!',
        first_name='Admin',
        last_name='Sistema',
        role='sysAdmin'
    )
    print(f'✓ Admin creado: {email}')

print('=' * 60)
print('✓ PERMISOS ACTUALIZADOS CORRECTAMENTE')
print('=' * 60)
print(f'\nCredenciales:')
print(f'  Email: {email}')
print(f'  Contraseña: Admin123!')
print('=' * 60)

