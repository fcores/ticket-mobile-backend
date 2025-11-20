# 🚂 Deploy en Railway - Backend Django

## Archivos de Configuración

Este proyecto está preconfigurado para Railway:

### Archivos importantes:
- `Procfile` - Comando para iniciar gunicorn
- `railway.json` - Configuración de build y deploy
- `requirements.txt` - Dependencias Python
- `init_railway_data.py` - Script para crear usuarios y datos iniciales

## Variables de Entorno Necesarias

Configura en Railway → Variables:

```bash
SECRET_KEY=genera-una-clave-secreta-larga-y-aleatoria
DEBUG=False
ALLOWED_HOSTS=.railway.app
```

Railway proporciona automáticamente:
- `DATABASE_URL` - URL de PostgreSQL
- `PORT` - Puerto del servidor
- `RAILWAY_PUBLIC_DOMAIN` - Dominio público

## Después del Deploy

### 1. Verificar que funcione:
```
https://tu-dominio.railway.app/api/health/
```

Debe devolver: `{"status": "healthy"}`

### 2. Inicializar datos:
```bash
railway login
railway link
railway run python init_railway_data.py
```

Esto creará:
- 4 usuarios (admin, 2 soporte, 1 usuario)
- 4 categorías
- 3 tickets de ejemplo

### 3. Acceder al admin de Django:
```
https://tu-dominio.railway.app/admin/
```

Login: `admin@test.com` / `Admin123!`

## Comandos Útiles

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar migraciones
railway run python manage.py migrate

# Crear superusuario
railway run python manage.py createsuperuser

# Abrir shell de Django
railway run python manage.py shell

# Reiniciar servicio
railway restart
```

## Estructura de la Base de Datos

Railway crea automáticamente PostgreSQL con:
- Backups automáticos
- Conexión segura
- Variable `DATABASE_URL` configurada

El código en `settings.py` detecta automáticamente `DATABASE_URL` y usa PostgreSQL en producción.

## Solución de Problemas

### Error: "Application failed to respond"
- Verifica que el `PORT` esté configurado
- Revisa los logs: `railway logs`

### Error: "Database connection failed"
- Asegúrate de que PostgreSQL esté agregado
- Verifica que `DATABASE_URL` exista en Variables

### Error: "Static files not found"
- Whitenoise está configurado automáticamente
- Los archivos estáticos se sirven en `/static/`

## Monitoreo

Railway proporciona:
- Métricas de CPU y RAM
- Logs en tiempo real
- Reinicio automático en caso de fallo

## Costos

**Plan gratuito incluye:**
- 500 horas de ejecución/mes
- $5 de crédito gratis
- PostgreSQL incluido

**Más que suficiente para desarrollo y demos.**

## Seguridad

✅ Configurado:
- HTTPS automático
- CORS configurado
- SECRET_KEY en variable de entorno
- DEBUG=False en producción
- Whitenoise para archivos estáticos

## Endpoints Disponibles

```
GET  /api/health/              - Estado del servidor
POST /api/auth/login/          - Login
POST /api/auth/register/       - Registro
GET  /api/tickets/             - Listar tickets
POST /api/tickets/create/      - Crear ticket
GET  /api/users/               - Listar usuarios (auth)
```

Ver documentación completa: `API-ENDPOINTS.md`

