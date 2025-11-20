# TicketMobile Backend - Django REST API

## Descripción
Backend del sistema de gestión de tickets desarrollado con Django REST Framework. Proporciona una API REST completa para la aplicación móvil Android.

## Tecnologías Utilizadas

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Autenticación**: JWT con Simple JWT
- **Base de Datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **CORS**: django-cors-headers
- **Imágenes**: Pillow

## Estructura del Proyecto

```
backend/
├── helpdesk/
│   ├── settings.py          # Configuración principal
│   ├── urls.py             # URLs principales
│   ├── wsgi.py             # Configuración WSGI
│   └── asgi.py             # Configuración ASGI
├── apps/
│   ├── authentication/     # Autenticación y JWT
│   ├── users/             # Gestión de usuarios
│   ├── tickets/           # Gestión de tickets
│   ├── comments/          # Comentarios en tickets
│   ├── attachments/       # Archivos adjuntos
│   ├── categories/        # Categorías de tickets
│   ├── metrics/           # Métricas del sistema
│   └── common/            # Utilidades comunes
├── manage.py              # Script de gestión Django
├── requirements.txt       # Dependencias Python
└── README.md             # Este archivo
```

## Configuración e Instalación

### Requisitos
- Python 3.8+
- pip
- virtualenv (recomendado)

### Instalación

1. **Crear entorno virtual**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Configurar base de datos**:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. **Crear superusuario**:
```bash
python manage.py createsuperuser
```

5. **Ejecutar servidor**:
```bash
python manage.py runserver
```

El servidor estará disponible en `http://localhost:8000`

## API Endpoints

### Autenticación
- `POST /api/auth/register/` - Registro de usuarios
- `POST /api/auth/login/` - Inicio de sesión
- `POST /api/auth/refresh/` - Renovar token
- `POST /api/auth/logout/` - Cerrar sesión
- `GET /api/auth/me/` - Información del usuario actual

### Tickets
- `GET /api/tickets/` - Listar tickets
- `POST /api/tickets/` - Crear ticket
- `GET /api/tickets/{id}/` - Detalles del ticket
- `PUT /api/tickets/{id}/` - Actualizar ticket

### Comentarios
- `GET /api/tickets/{id}/comments/` - Listar comentarios
- `POST /api/tickets/{id}/comments/` - Agregar comentario
- `DELETE /api/tickets/{id}/comments/{id}/` - Eliminar comentario

### Usuarios
- `GET /api/users/` - Listar usuarios (admin)
- `GET /api/users/profile/` - Perfil del usuario
- `PUT /api/users/profile/` - Actualizar perfil
- `DELETE /api/users/{id}/` - Eliminar usuario (admin)

### Categorías
- `GET /api/categorias/` - Listar categorías
- `POST /api/categorias/` - Crear categoría
- `PUT /api/categorias/{id}/` - Actualizar categoría
- `DELETE /api/categorias/{id}/` - Eliminar categoría

### Métricas
- `GET /api/metrics/tickets/overview/` - Resumen de tickets
- `GET /api/metrics/tickets/performance/` - Métricas de rendimiento
- `GET /api/metrics/users/activity/` - Actividad de usuarios

### Sistema
- `GET /api/health/` - Estado del sistema

## Modelos de Datos

### User
- `id`: ID único
- `email`: Email único (username)
- `first_name`: Nombre
- `last_name`: Apellido
- `role`: Rol del usuario (user, support, observer, sysAdmin)
- `profile_picture`: Foto de perfil
- `created_at`: Fecha de creación
- `last_login`: Último acceso

### Ticket
- `id`: ID único
- `title`: Título del ticket
- `description`: Descripción detallada
- `status`: Estado (open, in_progress, resolved, closed, canceled)
- `priority`: Prioridad (low, medium, high, urgent)
- `creator`: Usuario creador
- `assignee`: Usuario asignado
- `created_at`: Fecha de creación
- `updated_at`: Fecha de actualización
- `resolved_at`: Fecha de resolución

### Comment
- `id`: ID único
- `text`: Contenido del comentario
- `author`: Autor del comentario
- `ticket`: Ticket relacionado
- `created_at`: Fecha de creación
- `is_private`: Comentario privado (solo admin)

### Attachment
- `id`: ID único
- `ticket`: Ticket relacionado
- `uploaded_by`: Usuario que subió el archivo
- `file`: Archivo
- `original_filename`: Nombre original
- `file_size`: Tamaño del archivo
- `mime_type`: Tipo MIME
- `created_at`: Fecha de subida
- `is_private`: Archivo privado (solo admin)

## Autenticación JWT

### Configuración
- **Access Token**: 1 hora de duración
- **Refresh Token**: 30 días de duración
- **Header**: `Authorization: Bearer <token>`

### Flujo de Autenticación
1. Usuario se registra/inicia sesión
2. Servidor devuelve access_token y refresh_token
3. Cliente incluye access_token en header Authorization
4. Cuando el token expira, usar refresh_token para renovar

## Permisos y Roles

### Roles de Usuario
- **user**: Usuario regular, puede crear tickets y comentarios
- **support**: Agente de soporte, puede ver tickets asignados y cambiar estados
- **observer**: Observador, solo lectura
- **sysAdmin**: Administrador del sistema, acceso completo

### Permisos por Endpoint
- **Tickets**: Los usuarios pueden ver sus propios tickets, los de soporte pueden ver asignados
- **Comentarios**: Todos pueden crear, solo autor/admin puede eliminar
- **Usuarios**: Solo admin puede listar/eliminar usuarios
- **Métricas**: Solo admin puede acceder

## CORS Configuration

Configurado para permitir conexiones desde:
- `http://localhost:3000` (desarrollo web)
- `http://10.0.2.2:3000` (emulador Android)
- `http://10.0.2.2:8000` (emulador Android)

## Base de Datos

### Desarrollo
- SQLite (archivo `db.sqlite3`)
- Migraciones automáticas con `makemigrations` y `migrate`

### Producción
- PostgreSQL recomendado
- Configurar variables de entorno para conexión

## Archivos Estáticos y Media

### Desarrollo
- Archivos estáticos servidos automáticamente
- Archivos media en carpeta `media/`

### Producción
- Usar servicio como AWS S3 o similar
- Configurar `STATIC_ROOT` y `MEDIA_ROOT`

## Logging

Configuración básica de logging en consola:
- Nivel INFO para Django
- Logs de requests y errores

## Testing

```bash
# Ejecutar todos los tests
python manage.py test

# Tests específicos
python manage.py test apps.users
python manage.py test apps.tickets
```

## Deployment

### Variables de Entorno
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host:port/dbname
ALLOWED_HOSTS=yourdomain.com,api.yourdomain.com
```

### Comandos de Deployment
```bash
python manage.py collectstatic
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

## API Documentation

La documentación completa de la API está disponible en:
- **Swagger**: `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://localhost:8000/api/schema/redoc/`

## Troubleshooting

### Errores Comunes

1. **CORS Error**: Verificar configuración en `settings.py`
2. **JWT Error**: Verificar secret key y configuración de tokens
3. **Database Error**: Ejecutar migraciones con `python manage.py migrate`
4. **Media Files**: Verificar permisos de carpeta `media/`

### Logs
```bash
# Ver logs en tiempo real
tail -f logs/django.log

# Logs de errores
grep ERROR logs/django.log
```

## Contribución

Para contribuir al backend:

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Implementar cambios
4. Ejecutar tests: `python manage.py test`
5. Commit: `git commit -m 'Agregar nueva funcionalidad'`
6. Push: `git push origin feature/nueva-funcionalidad`
7. Crear Pull Request

---

**Equipo de Desarrollo:**
- **Product Owner / API Rest:** Lautaro Cavallo
- **Backend:** Tomás Liñeiro
- **UX/UI:** Ivo Rubino
- **QA / DevOps:** Facundo Cores
