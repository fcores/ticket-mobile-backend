# 🚀 Quick Start - API REST Tickets

## Pasos para ejecutar la API

### 1. Instalar dependencias (si no lo has hecho)

```bash
cd backend
pip install -r requirements.txt
```

### 2. Ejecutar migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario (admin)

```bash
python manage.py createsuperuser
```

Ingresa:
- Email: admin@example.com
- Username: admin
- First name: Admin
- Last name: User
- Password: (tu contraseña segura)

### 4. Ejecutar el servidor

```bash
python manage.py runserver
```

El servidor estará disponible en: **http://localhost:8000**

---

## 🧪 Probar los endpoints

### Opción 1: Usar el Admin de Django

Ve a: http://localhost:8000/admin/

Puedes ver y gestionar:
- Usuarios
- Tickets
- Comentarios
- Attachments
- Categorías

### Opción 2: Usar Postman o curl

#### 1. Registrar un usuario

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "firstName": "Juan",
    "lastName": "Pérez",
    "email": "juan@example.com",
    "password": "MyPass123!",
    "confirmPassword": "MyPass123!"
  }'
```

#### 2. Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "juan@example.com",
    "password": "MyPass123!"
  }'
```

Respuesta:
```json
{
  "accessToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refreshToken": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "juan@example.com",
    "firstName": "Juan",
    "lastName": "Pérez",
    "role": "user"
  }
}
```

**Guarda el `accessToken` para usarlo en las siguientes requests.**

#### 3. Crear un ticket

```bash
curl -X POST http://localhost:8000/api/tickets/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI" \
  -d '{
    "title": "Problema con la aplicación",
    "description": "La aplicación no carga correctamente en la pantalla principal",
    "priority": "high"
  }'
```

#### 4. Listar mis tickets

```bash
curl -X GET http://localhost:8000/api/tickets/my-tickets/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

#### 5. Ver un ticket específico

```bash
curl -X GET http://localhost:8000/api/tickets/1/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

#### 6. Agregar un comentario

```bash
curl -X POST http://localhost:8000/api/tickets/1/comments/create/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI" \
  -d '{
    "text": "Este es mi primer comentario en el ticket"
  }'
```

#### 7. Ver métricas del sistema (requiere rol support o admin)

```bash
curl -X GET http://localhost:8000/api/metrics/tickets/overview/ \
  -H "Authorization: Bearer TU_ACCESS_TOKEN_AQUI"
```

#### 8. Health check (sin autenticación)

```bash
curl -X GET http://localhost:8000/api/health/
```

---

## 📚 Endpoints Principales

### Autenticación
- `POST /api/auth/register/` - Registro
- `POST /api/auth/login/` - Login
- `POST /api/auth/refresh/` - Renovar token
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Info del usuario actual

### Tickets
- `GET /api/tickets/` - Listar tickets
- `POST /api/tickets/create/` - Crear ticket
- `GET /api/tickets/my-tickets/` - Mis tickets
- `GET /api/tickets/{id}/` - Ver ticket
- `PUT /api/tickets/{id}/update/` - Actualizar ticket

### Comentarios
- `GET /api/tickets/{id}/comments/` - Listar comentarios
- `POST /api/tickets/{id}/comments/create/` - Crear comentario

### Usuarios (admin)
- `GET /api/users/` - Listar usuarios
- `GET /api/users/profile/` - Mi perfil
- `PUT /api/users/profile/update/` - Actualizar perfil

### Métricas (support/admin)
- `GET /api/metrics/tickets/overview/` - Resumen de tickets
- `GET /api/metrics/tickets/performance/` - Rendimiento
- `GET /api/metrics/system/health/` - Estado del sistema

### Sistema
- `GET /api/health/` - Health check
- `GET /api/info/` - Info de la API

---

## 🔑 Roles de Usuario

1. **user** (por defecto)
   - Puede crear tickets
   - Ver sus propios tickets
   - Comentar en sus tickets

2. **support**
   - Ver tickets asignados y sin asignar
   - Asignar tickets
   - Cambiar estado de tickets
   - Comentarios privados

3. **sysAdmin**
   - Acceso completo
   - Gestionar usuarios
   - Ver todas las métricas

---

## 📖 Documentación Completa

Ver `IMPLEMENTATION.md` para:
- Lista completa de endpoints
- Validaciones implementadas
- Sistema de permisos
- Manejo de errores
- Y mucho más

---

## ❓ Troubleshooting

### Error: "No module named 'rest_framework'"
```bash
pip install djangorestframework
```

### Error: "No module named 'rest_framework_simplejwt'"
```bash
pip install djangorestframework-simplejwt
```

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate --run-syncdb
```

### Token expirado
Usa el refresh token para obtener un nuevo access token:
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refreshToken": "TU_REFRESH_TOKEN"
  }'
```

---

¡Listo! La API está completamente funcional y lista para usar. 🎉

