#!/usr/bin/env python
"""Script simple para crear usuario admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helpdesk.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Crear admin si no existe
email = 'admin@test.com'
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(
        username=email,
        email=email,
        password='Admin123!',
        first_name='Admin',
        last_name='Sistema',
        role='sysAdmin'
    )
    print(f'✓ Admin creado: {email}')
else:
    print(f'- Admin ya existe: {email}')

