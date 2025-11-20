# 📘 Manual del Desarrollador - Sistema de Tickets

**Versión:** 1.0  
**Fecha:** Noviembre 2025  
**Estado:** Producción

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Requisitos del Sistema](#requisitos-del-sistema)
3. [Instalación](#instalación)
4. [Configuración](#configuración)
5. [Estructura del Proyecto](#estructura-del-proyecto)
6. [Base de Datos](#base-de-datos)
7. [Desarrollo](#desarrollo)
8. [Testing](#testing)
9. [Despliegue](#despliegue)
10. [Troubleshooting](#troubleshooting)

---

## 🎯 Introducción

Este manual proporciona información técnica completa para desarrolladores que trabajen con el backend del Sistema de Gestión de Tickets.

### Tecnologías Principales

- **Framework:** Django 4.2.7
- **API:** Django REST Framework 3.14.0
- **Autenticación:** JWT (Simple JWT 5.3.0)
- **Base de Datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Python:** 3.8+ (testeado con 3.13)

---

## 💻 Requisitos del Sistema

### Software Requerido

```
✅ Python 3.8 o superior
✅ pip (gestor de paquetes Python)
✅ Git
✅ Editor de código (VS Code, PyCharm, etc.)
```

### Software Opcional

```
⭐ virtualenv / venv (entornos virtuales)
⭐ PostgreSQL 14+ (para producción)
⭐ Docker (para containerización)
⭐ Postman / Insomnia (testing de API)
```

### Conocimientos Previos

- Python básico/intermedio
- Django fundamentals
- REST API concepts
- SQL básico
- Git workflow

---

## 🔧 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/LautaroCavallo/Ticket-Mobile.git
cd Ticket-Mobile
```

### 2. Checkout de la Branch de Backend

```bash
git checkout epic-22-backend-completo
```

### 3. Navegar al Directorio Backend

```bash
cd backend
```

### 4. Crear Entorno Virtual (Recomendado)

#### Linux / macOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 5. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Dependencias instaladas:**
```txt
Django==4.2.7                      # Framework web
djangorestframework==3.14.0        # API REST
djangorestframework-simplejwt==5.3.0  # Autenticación JWT
django-cors-headers==4.3.1         # CORS para mobile
Pillow>=10.4.0                     # Manejo de imágenes
python-decouple==3.8               # Variables de entorno
setuptools                         # Utilidades Python
```

### 6. Aplicar Migraciones

```bash
python manage.py migrate
```

**Resultado esperado:**
```
Operations to perform:
  Apply all migrations: admin, attachments, auth, categories, 
                       comments, contenttypes, sessions, tickets, users
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying users.0001_initial... OK
  Applying tickets.0001_initial... OK
  ... (27 migraciones totales)
```

### 7. Crear Superusuario

```bash
python manage.py createsuperuser
```

**Datos requeridos:**
- Email (usado como username)
- First name
- Last name
- Password (mínimo 8 caracteres)

### 8. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

**Servidor disponible en:** `http://localhost:8000`

---

## ⚙️ Configuración

### Variables de Entorno

Crear archivo `.env` en el directorio `backend/`:

```bash
# Desarrollo
DEBUG=True
SECRET_KEY=tu-secret-key-aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos (Producción)
DATABASE_URL=postgresql://user:password@localhost:5432/tickets_db

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://10.0.2.2:3000

# JWT
JWT_ACCESS_TOKEN_LIFETIME=60  # minutos
JWT_REFRESH_TOKEN_LIFETIME=30 # días

# Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

### Configuración de Base de Datos

#### SQLite (Desarrollo - Default)

Ya configurado en `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Producción)

Actualizar `settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
```

Instalar driver:
```bash
pip install psycopg2-binary
```

### Configuración de CORS

Editar `backend/helpdesk/settings.py`:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",      # Web dev
    "http://127.0.0.1:3000",
    "http://10.0.2.2:3000",       # Android emulator
    "http://10.0.2.2:8000",
]

# Para desarrollo más permisivo:
CORS_ALLOW_ALL_ORIGINS = DEBUG
```

### Configuración de JWT

Ya configurado en `settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

---

## 📁 Estructura del Proyecto

```
backend/
├── helpdesk/                    # Proyecto Django principal
│   ├── __init__.py
│   ├── settings.py             # Configuración global
│   ├── urls.py                 # URLs principales
│   ├── wsgi.py                 # WSGI para producción
│   └── asgi.py                 # ASGI para async
│
├── apps/                        # Apps Django modulares
│   ├── authentication/          # Autenticación JWT
│   │   ├── serializers.py      # Validación de auth
│   │   ├── views.py            # Login, registro, etc.
│   │   └── urls.py
│   │
│   ├── users/                   # Gestión de usuarios
│   │   ├── models.py           # Modelo User custom
│   │   ├── serializers.py      # Serializers de User
│   │   ├── views.py            # CRUD usuarios
│   │   ├── permissions.py      # Permisos custom
│   │   ├── urls.py
│   │   └── migrations/         # Migraciones BD
│   │
│   ├── tickets/                 # Core del negocio
│   │   ├── models.py           # Modelo Ticket
│   │   ├── serializers.py      # 6 serializers
│   │   ├── views.py            # 10 endpoints
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── comments/                # Comentarios
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── attachments/             # Archivos adjuntos
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── categories/              # Categorías
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── migrations/
│   │
│   ├── metrics/                 # Métricas y analytics
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   │
│   └── common/                  # Utilidades comunes
│       ├── serializers.py
│       ├── views.py
│       ├── urls.py
│       ├── exceptions.py       # Manejo de errores
│       └── responses.py        # Respuestas helpers
│
├── media/                       # Archivos subidos (usuarios)
├── staticfiles/                 # Archivos estáticos (producción)
├── db.sqlite3                   # Base de datos (desarrollo)
├── manage.py                    # CLI de Django
├── requirements.txt             # Dependencias Python
│
└── Documentación:
    ├── IMPLEMENTATION.md        # Doc técnica API
    ├── QUICKSTART.md           # Guía rápida
    ├── MANUAL-DESARROLLADOR.md # Este archivo
    ├── API-ENDPOINTS.md        # Endpoints detallados
    └── EPIC-22-COMPLETADO.md  # Resumen de épica
```

---

## 🗄️ Base de Datos

### Modelos Principales

#### User (apps/users/models.py)

```python
class User(AbstractUser):
    email = EmailField(unique=True)
    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    role = CharField(choices=ROLE_CHOICES, default='user')
    profile_picture = ImageField(upload_to='uploads/profiles/')
    created_at = DateTimeField(default=timezone.now)
    last_login = DateTimeField(null=True)
    is_active = BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
```

**Roles disponibles:**
- `user` - Usuario regular
- `support` - Agente de soporte
- `observer` - Observador (solo lectura)
- `sysAdmin` - Administrador del sistema

#### Ticket (apps/tickets/models.py)

```python
class Ticket(Model):
    title = CharField(max_length=200)
    description = TextField()
    status = CharField(choices=STATUS_CHOICES, default='open')
    priority = CharField(choices=PRIORITY_CHOICES, default='medium')
    creator = ForeignKey(User, related_name='created_tickets')
    assignee = ForeignKey(User, related_name='assigned_tickets', null=True)
    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(auto_now=True)
    resolved_at = DateTimeField(null=True)
```

**Estados:** open, in_progress, resolved, closed, canceled  
**Prioridades:** low, medium, high, urgent

#### Comment (apps/comments/models.py)

```python
class Comment(Model):
    text = TextField()
    author = ForeignKey(User, related_name='comments')
    ticket = ForeignKey(Ticket, related_name='comments')
    created_at = DateTimeField(default=timezone.now)
    is_private = BooleanField(default=False)
```

#### Attachment (apps/attachments/models.py)

```python
class Attachment(Model):
    ticket = ForeignKey(Ticket, related_name='attachments')
    uploaded_by = ForeignKey(User, related_name='uploaded_attachments')
    file = FileField(upload_to=upload_attachment_to)
    original_filename = CharField(max_length=255)
    file_size = PositiveIntegerField()
    mime_type = CharField(max_length=100)
    created_at = DateTimeField(default=timezone.now)
    is_private = BooleanField(default=False)
```

#### Category (apps/categories/models.py)

```python
class Category(Model):
    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
```

### Diagrama ER

```
┌─────────────┐
│    User     │
│  (Custom)   │
└──────┬──────┘
       │
       │ creator/assignee
       │
┌──────▼──────┐
│   Ticket    │◄─────┐
│  (Core)     │      │
└──────┬──────┘      │
       │             │
       │             │ ticket
       │             │
┌──────▼──────┐ ┌────┴─────┐ ┌───────────┐
│  Comment    │ │Attachment│ │ Category  │
└─────────────┘ └──────────┘ └───────────┘
```

### Migraciones

#### Crear Nueva Migración

Después de modificar un modelo:

```bash
python manage.py makemigrations app_name
```

Ejemplo:
```bash
python manage.py makemigrations users
```

#### Aplicar Migraciones

```bash
python manage.py migrate
```

#### Ver Migraciones Pendientes

```bash
python manage.py showmigrations
```

#### Revertir Migración

```bash
python manage.py migrate app_name 0001
```

#### SQL de una Migración

```bash
python manage.py sqlmigrate app_name 0001
```

---

## 👨‍💻 Desarrollo

### Crear Nueva App

```bash
python manage.py startapp nombre_app
```

Agregar a `INSTALLED_APPS` en `settings.py`:
```python
INSTALLED_APPS = [
    # ...
    'apps.nombre_app',
]
```

### Crear Nuevo Endpoint

1. **Definir Serializer** (`serializers.py`):

```python
from rest_framework import serializers

class MiModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = MiModelo
        fields = ['id', 'campo1', 'campo2']
    
    def validate_campo1(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Muy corto")
        return value
```

2. **Crear View** (`views.py`):

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def mi_endpoint_view(request):
    if request.method == 'GET':
        # Lógica GET
        serializer = MiModeloSerializer(objetos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = MiModeloSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

3. **Mapear URL** (`urls.py`):

```python
from django.urls import path
from . import views

urlpatterns = [
    path('mi-recurso/', views.mi_endpoint_view, name='mi-recurso'),
]
```

4. **Incluir en URLs principales** (`helpdesk/urls.py`):

```python
urlpatterns = [
    # ...
    path('api/', include('apps.mi_app.urls')),
]
```

### Permisos Personalizados

Crear en `permissions.py`:

```python
from rest_framework import permissions

class MiPermiso(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'
    
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
```

Usar en views:

```python
from .permissions import MiPermiso

@permission_classes([IsAuthenticated, MiPermiso])
def mi_view(request):
    # ...
```

### Validaciones Custom

```python
from rest_framework import serializers
import re

class MiSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Mínimo 8 caracteres")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("Debe contener mayúsculas")
        return value
    
    def validate(self, attrs):
        # Validación de múltiples campos
        if attrs['email'] == attrs.get('username'):
            raise serializers.ValidationError("Email y username deben ser diferentes")
        return attrs
```

### Manejo de Errores

Ya implementado en `apps/common/exceptions.py`:

```python
from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        response.data = {
            'error': get_error_message(exc),
            'details': response.data,
            'timestamp': timezone.now().isoformat(),
            'status_code': response.status_code
        }
    
    return response
```

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de una app
python manage.py test apps.users

# Tests específicos
python manage.py test apps.users.tests.TestUserModel

# Con coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Crear Tests

Crear `tests.py` en cada app:

```python
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.users.models import User

class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='test@example.com',
            email='test@example.com',
            password='Test123!',
            first_name='Test',
            last_name='User'
        )
    
    def test_login(self):
        response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'Test123!'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', response.data)
    
    def test_create_ticket_authenticated(self):
        # Login
        login_response = self.client.post('/api/auth/login/', {
            'email': 'test@example.com',
            'password': 'Test123!'
        })
        token = login_response.data['accessToken']
        
        # Create ticket
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post('/api/tickets/create/', {
            'title': 'Test Ticket',
            'description': 'This is a test ticket description',
            'priority': 'high'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
```

### Testing con Postman/Insomnia

1. Importar colección desde `api/swagger.yaml`
2. Configurar environment:
   - `base_url`: http://localhost:8000
   - `access_token`: (obtenido del login)

---

## 🚀 Despliegue

### Preparación para Producción

1. **Actualizar settings.py:**

```python
DEBUG = False
ALLOWED_HOSTS = ['tudominio.com', 'www.tudominio.com']

# Secret key from environment
SECRET_KEY = config('SECRET_KEY')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# Static files
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'

# Media files
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

2. **Recolectar archivos estáticos:**

```bash
python manage.py collectstatic --noinput
```

3. **Crear requirements.txt de producción:**

```bash
pip freeze > requirements-prod.txt
```

Agregar:
```txt
gunicorn==21.2.0
psycopg2-binary==2.9.9
dj-database-url==2.1.0
whitenoise==6.6.0  # Para servir static files
```

### Despliegue con Heroku

1. **Instalar Heroku CLI y login:**

```bash
heroku login
heroku create tu-app-tickets
```

2. **Crear Procfile:**

```
web: gunicorn helpdesk.wsgi --log-file -
```

3. **Crear runtime.txt:**

```
python-3.11.5
```

4. **Configurar variables de entorno:**

```bash
heroku config:set SECRET_KEY=tu-secret-key
heroku config:set DEBUG=False
heroku config:set DATABASE_URL=postgresql://...
```

5. **Deploy:**

```bash
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Despliegue con Docker

1. **Crear Dockerfile:**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "helpdesk.wsgi:application", "--bind", "0.0.0.0:8000"]
```

2. **Crear docker-compose.yml:**

```yaml
version: '3.8'

services:
  db:
    image: postgres:14
    environment:
      POSTGRES_DB: tickets_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  web:
    build: .
    command: gunicorn helpdesk.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/tickets_db
    depends_on:
      - db

volumes:
  postgres_data:
```

3. **Ejecutar:**

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

### Despliegue con AWS/Azure

Ver documentación específica de cada proveedor en:
- AWS: Elastic Beanstalk / EC2 + RDS
- Azure: App Service + PostgreSQL
- GCP: Cloud Run + Cloud SQL

---

## 🔍 Troubleshooting

### Error: "No module named 'django'"

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "No such table: users"

**Solución:**
```bash
python manage.py migrate
```

### Error: "Port 8000 already in use"

**Solución:**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# O usar otro puerto
python manage.py runserver 8001
```

### Error: "CORS header 'Access-Control-Allow-Origin' missing"

**Solución:**
Agregar origen en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://tu-frontend-url:3000",
]
```

### Error: "Token invalid or expired"

**Solución:**
Usar refresh token para obtener nuevo access token:
```bash
POST /api/auth/refresh/
{
  "refreshToken": "tu-refresh-token"
}
```

### Migraciones Conflictivas

**Solución:**
```bash
# Resetear migraciones (¡CUIDADO! Pierdes datos)
python manage.py migrate --fake-initial
# O eliminar db.sqlite3 y volver a migrar
rm db.sqlite3
python manage.py migrate
```

---

## 📚 Referencias

### Documentación Oficial

- Django: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Simple JWT: https://django-rest-framework-simplejwt.readthedocs.io/

### Documentación del Proyecto

- `IMPLEMENTATION.md` - Documentación técnica de la API
- `API-ENDPOINTS.md` - Endpoints detallados
- `QUICKSTART.md` - Guía rápida de inicio
- `../docs/arquitectura-final.md` - Arquitectura del sistema

### Recursos Adicionales

- Python: https://docs.python.org/3/
- PostgreSQL: https://www.postgresql.org/docs/
- Git: https://git-scm.com/doc

---

## 👥 Soporte

### Contacto del Equipo

- **Product Owner / API REST:** Lautaro Cavallo
- **Backend:** Tomás Liñeiro
- **UX/UI:** Ivo Rubino
- **QA / DevOps:** Facundo Cores

### Reportar Issues

GitHub: https://github.com/LautaroCavallo/Ticket-Mobile/issues

---

**Versión del Manual:** 1.0  
**Última Actualización:** Noviembre 2025  
**Mantenido por:** Equipo de Desarrollo

