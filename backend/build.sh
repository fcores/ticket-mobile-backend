#!/usr/bin/env bash
# Script de build para Railway

set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Crear superusuario si no existe (opcional)
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(email='admin@test.com').exists():
    User.objects.create_superuser('admin@test.com', 'admin@test.com', 'Admin123!', first_name='Admin', last_name='Sistema', role='sysAdmin')
"

echo "Build completado exitosamente!"

