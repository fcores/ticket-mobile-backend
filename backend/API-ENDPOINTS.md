# 📡 Documentación de Endpoints API - Sistema de Tickets

**Versión:** 1.0  
**Base URL:** `http://localhost:8000/api`  
**Autenticación:** JWT Bearer Token  
**Formato:** JSON

---

## 📋 Índice

1. [Introducción](#introducción)
2. [Autenticación](#autenticación)
3. [Usuarios](#usuarios)
4. [Tickets](#tickets)
5. [Comentarios](#comentarios)
6. [Attachments](#attachments)
7. [Categorías](#categorías)
8. [Métricas](#métricas)
9. [Sistema](#sistema)
10. [Códigos de Error](#códigos-de-error)

---

## 🎯 Introducción

### Base URL

```
Desarrollo: http://localhost:8000/api
Producción: https://api.ticketmobile.com/api
```

### Formato de Respuesta

Todas las respuestas están en formato JSON.

#### Respuesta Exitosa:
```json
{
  "msg": "Operación exitosa",
  "data": { ... }
}
```

#### Respuesta con Error:
```json
{
  "error": "Mensaje de error",
  "details": { ... },
  "timestamp": "2024-11-19T12:00:00Z"
}
```

### Autenticación

La mayoría de los endpoints requieren autenticación mediante JWT Bearer Token.

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 🔐 Autenticación

### 1. Registro de Usuario

Registra un nuevo usuario en el sistema.

**Endpoint:** `POST /auth/register/`  
**Autenticación:** No requerida

#### Request Body:
```json
{
  "firstName": "Juan",
  "lastName": "Pérez",
  "email": "juan.perez@example.com",
  "password": "MiPassword123!",
  "confirmPassword": "MiPassword123!"
}
```

#### Validaciones:
- `firstName`: 2-50 caracteres
- `lastName`: 2-50 caracteres
- `email`: Formato email válido, único
- `password`: Mínimo 8 caracteres, debe incluir:
  - Al menos una mayúscula
  - Al menos una minúscula
  - Al menos un número
  - Al menos un símbolo especial
- `confirmPassword`: Debe coincidir con password

#### Response 201 Created:
```json
{
  "msg": "Usuario registrado exitosamente",
  "user": {
    "id": 1,
    "email": "juan.perez@example.com",
    "firstName": "Juan",
    "lastName": "Pérez",
    "fullName": "Juan Pérez",
    "role": "user",
    "displayRole": "Usuario",
    "createdAt": "2024-11-19T12:00:00Z"
  },
  "accessToken": "eyJhbGc...",
  "refreshToken": "eyJhbGc..."
}
```

#### Errores Posibles:
- `400` - Datos inválidos
- `400` - Email ya registrado
- `400` - Contraseñas no coinciden

---

### 2. Login

Inicia sesión y obtiene tokens JWT.

**Endpoint:** `POST /auth/login/`  
**Autenticación:** No requerida

#### Request Body:
```json
{
  "email": "juan.perez@example.com",
  "password": "MiPassword123!"
}
```

#### Response 200 OK:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": 1,
    "email": "juan.perez@example.com",
    "firstName": "Juan",
    "lastName": "Pérez",
    "role": "user",
    "lastLogin": "2024-11-19T12:00:00Z"
  }
}
```

#### Errores Posibles:
- `401` - Credenciales inválidas
- `401` - Usuario inactivo

---

### 3. Refresh Token

Renueva el access token usando el refresh token.

**Endpoint:** `POST /auth/refresh/`  
**Autenticación:** No requerida (requiere refresh token válido)

#### Request Body:
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response 200 OK:
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

### 4. Logout

Cierra sesión e invalida el refresh token.

**Endpoint:** `POST /auth/logout/`  
**Autenticación:** Requerida

#### Request Body:
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### Response 200 OK:
```json
{
  "msg": "Logout exitoso"
}
```

---

### 5. Usuario Actual

Obtiene información del usuario autenticado.

**Endpoint:** `GET /auth/me/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "id": 1,
  "email": "juan.perez@example.com",
  "firstName": "Juan",
  "lastName": "Pérez",
  "fullName": "Juan Pérez",
  "role": "user",
  "displayRole": "Usuario",
  "profilePicture": null,
  "createdAt": "2024-11-19T12:00:00Z",
  "lastLogin": "2024-11-19T12:00:00Z",
  "isActive": true
}
```

---

### 6. Cambiar Contraseña

Cambia la contraseña del usuario autenticado.

**Endpoint:** `POST /auth/change-password/`  
**Autenticación:** Requerida

#### Request Body:
```json
{
  "currentPassword": "MiPassword123!",
  "newPassword": "NuevaPassword456!",
  "confirmPassword": "NuevaPassword456!"
}
```

#### Response 200 OK:
```json
{
  "msg": "Contraseña actualizada exitosamente"
}
```

#### Errores Posibles:
- `400` - Contraseña actual incorrecta
- `400` - Nueva contraseña no cumple requisitos
- `400` - Contraseñas no coinciden

---

### 7. Solicitar Reset de Contraseña

Solicita un reset de contraseña (envía email).

**Endpoint:** `POST /auth/password-reset/`  
**Autenticación:** No requerida

#### Request Body:
```json
{
  "email": "juan.perez@example.com"
}
```

#### Response 200 OK:
```json
{
  "msg": "Si el email existe, recibirás instrucciones para restablecer tu contraseña"
}
```

---

## 👥 Usuarios

### 1. Listar Usuarios (Admin)

Lista todos los usuarios del sistema.

**Endpoint:** `GET /users/`  
**Autenticación:** Requerida (sysAdmin)  
**Paginación:** Sí (20 items por página)

#### Query Parameters:
- `page` (opcional) - Número de página
- `page_size` (opcional) - Items por página (max 100)
- `role` (opcional) - Filtrar por rol (user, support, sysAdmin)
- `is_active` (opcional) - Filtrar por activos (true/false)
- `search` (opcional) - Buscar en nombre o email

#### Ejemplo:
```http
GET /users/?page=1&role=support&search=juan
```

#### Response 200 OK:
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "juan.perez@example.com",
      "firstName": "Juan",
      "lastName": "Pérez",
      "fullName": "Juan Pérez",
      "role": "support",
      "displayRole": "Soporte",
      "createdAt": "2024-11-19T12:00:00Z",
      "lastLogin": "2024-11-19T12:00:00Z",
      "isActive": true
    }
  ]
}
```

---

### 2. Ver Perfil

Obtiene el perfil del usuario autenticado.

**Endpoint:** `GET /users/profile/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "id": 1,
  "email": "juan.perez@example.com",
  "firstName": "Juan",
  "lastName": "Pérez",
  "role": "user",
  "profilePicture": "http://localhost:8000/media/profiles/juan.jpg",
  "createdAt": "2024-11-19T12:00:00Z"
}
```

---

### 3. Actualizar Perfil

Actualiza el perfil del usuario autenticado.

**Endpoint:** `PUT /users/profile/update/`  
**Autenticación:** Requerida  
**Content-Type:** `multipart/form-data` (si incluye imagen)

#### Request Body:
```json
{
  "firstName": "Juan Carlos",
  "lastName": "Pérez González"
}
```

O con imagen:
```
firstName: Juan Carlos
lastName: Pérez González
profilePicture: [archivo]
```

#### Response 200 OK:
```json
{
  "msg": "Perfil actualizado exitosamente",
  "user": { ... }
}
```

---

### 4. Ver Usuario por ID (Admin)

Obtiene detalles de un usuario específico.

**Endpoint:** `GET /users/{id}/`  
**Autenticación:** Requerida (sysAdmin)

#### Response 200 OK:
```json
{
  "id": 5,
  "email": "usuario@example.com",
  "firstName": "Usuario",
  "lastName": "Ejemplo",
  "role": "user",
  "createdAt": "2024-11-19T12:00:00Z"
}
```

---

### 5. Actualizar Rol (Admin)

Actualiza el rol de un usuario.

**Endpoint:** `PUT /users/{id}/role/`  
**Autenticación:** Requerida (sysAdmin)

#### Request Body:
```json
{
  "role": "support"
}
```

#### Roles válidos:
- `user` - Usuario regular
- `support` - Agente de soporte
- `observer` - Observador (solo lectura)
- `sysAdmin` - Administrador del sistema

#### Response 200 OK:
```json
{
  "msg": "Rol actualizado exitosamente",
  "user": { ... }
}
```

#### Errores Posibles:
- `403` - No puedes cambiar tu propio rol

---

### 6. Activar/Desactivar Usuario (Admin)

Activa o desactiva un usuario.

**Endpoint:** `PATCH /users/{id}/activation/`  
**Autenticación:** Requerida (sysAdmin)

#### Request Body:
```json
{
  "isActive": false
}
```

#### Response 200 OK:
```json
{
  "msg": "Usuario desactivado exitosamente",
  "user": { ... }
}
```

---

### 7. Eliminar Usuario (Admin)

Elimina un usuario del sistema.

**Endpoint:** `DELETE /users/{id}/delete/`  
**Autenticación:** Requerida (sysAdmin)

#### Response 200 OK:
```json
{
  "msg": "Usuario juan@example.com eliminado exitosamente"
}
```

#### Errores Posibles:
- `403` - No puedes eliminar tu propia cuenta

---

## 🎫 Tickets

### 1. Listar Tickets

Lista tickets según el rol del usuario.

**Endpoint:** `GET /tickets/`  
**Autenticación:** Requerida  
**Paginación:** Sí

#### Filtros por Rol:
- **user:** Solo tickets propios
- **support:** Tickets asignados + sin asignar
- **sysAdmin:** Todos los tickets

#### Query Parameters:
- `status` - Filtrar por estado (open, in_progress, resolved, closed, canceled)
- `priority` - Filtrar por prioridad (low, medium, high, urgent)
- `search` - Buscar en título y descripción
- `page` - Número de página
- `page_size` - Items por página

#### Ejemplo:
```http
GET /tickets/?status=open&priority=high&search=servidor
```

#### Response 200 OK:
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/tickets/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Problema con el servidor",
      "status": "open",
      "displayStatus": "Abierto",
      "priority": "high",
      "displayPriority": "Alta",
      "creator": {
        "id": 2,
        "email": "user@example.com",
        "fullName": "Usuario Ejemplo"
      },
      "assignee": null,
      "createdAt": "2024-11-19T12:00:00Z",
      "updatedAt": "2024-11-19T12:00:00Z",
      "resolvedAt": null,
      "commentsCount": 3,
      "attachmentsCount": 1
    }
  ]
}
```

---

### 2. Crear Ticket

Crea un nuevo ticket.

**Endpoint:** `POST /tickets/create/`  
**Autenticación:** Requerida

#### Request Body:
```json
{
  "title": "Problema con la aplicación móvil",
  "description": "La aplicación se cierra inesperadamente al intentar subir archivos grandes. El error ocurre específicamente cuando el archivo supera los 5MB.",
  "priority": "high"
}
```

#### Validaciones:
- `title`: 5-200 caracteres
- `description`: mínimo 10 caracteres
- `priority`: low, medium, high, urgent (default: medium)

#### Response 201 Created:
```json
{
  "msg": "Ticket creado exitosamente",
  "ticket": {
    "id": 15,
    "title": "Problema con la aplicación móvil",
    "description": "La aplicación se cierra inesperadamente...",
    "status": "open",
    "priority": "high",
    "creator": { ... },
    "assignee": null,
    "createdAt": "2024-11-19T12:00:00Z"
  }
}
```

---

### 3. Ver Ticket

Obtiene detalles de un ticket específico.

**Endpoint:** `GET /tickets/{id}/`  
**Autenticación:** Requerida

#### Permisos:
- **user:** Solo propios tickets
- **support:** Asignados o sin asignar
- **sysAdmin:** Cualquier ticket

#### Response 200 OK:
```json
{
  "id": 1,
  "title": "Problema con el servidor",
  "description": "Descripción completa del problema...",
  "status": "open",
  "displayStatus": "Abierto",
  "priority": "high",
  "displayPriority": "Alta",
  "creator": {
    "id": 2,
    "email": "user@example.com",
    "fullName": "Usuario Ejemplo",
    "role": "user"
  },
  "assignee": null,
  "createdAt": "2024-11-19T12:00:00Z",
  "updatedAt": "2024-11-19T12:00:00Z",
  "resolvedAt": null
}
```

---

### 4. Actualizar Ticket

Actualiza un ticket existente.

**Endpoint:** `PUT /tickets/{id}/update/`  
**Autenticación:** Requerida

#### Permisos:
- **user:** Solo propios tickets en estado "open" (solo title/description)
- **support:** Tickets asignados o sin asignar (todos los campos)
- **sysAdmin:** Cualquier ticket (todos los campos)

#### Request Body:
```json
{
  "title": "Título actualizado",
  "description": "Descripción actualizada",
  "status": "in_progress",
  "priority": "urgent",
  "assigneeId": 5
}
```

#### Campos opcionales:
- `title` (5-200 chars)
- `description` (min 10 chars)
- `status` (open, in_progress, resolved, closed, canceled)
- `priority` (low, medium, high, urgent)
- `assigneeId` (ID de usuario support o admin, null para desasignar)

#### Response 200 OK:
```json
{
  "msg": "Ticket actualizado exitosamente",
  "ticket": { ... }
}
```

#### Errores Posibles:
- `403` - No tienes permiso para actualizar este ticket
- `400` - Usuario asignado debe ser support o admin

---

### 5. Actualizar Estado (Support/Admin)

Actualiza solo el estado de un ticket.

**Endpoint:** `PATCH /tickets/{id}/status/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Request Body:
```json
{
  "status": "resolved"
}
```

#### Estados válidos:
- `open` - Abierto (inicial)
- `in_progress` - En progreso
- `resolved` - Resuelto
- `closed` - Cerrado (final)
- `canceled` - Cancelado

#### Validaciones de Transición:
- No se puede reabrir un ticket cerrado
- Solo se puede resolver si está asignado

#### Response 200 OK:
```json
{
  "msg": "Estado actualizado exitosamente",
  "ticket": { ... }
}
```

---

### 6. Asignar Ticket (Support/Admin)

Asigna un ticket a un usuario de soporte.

**Endpoint:** `PATCH /tickets/{id}/assign/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Request Body:
```json
{
  "assigneeId": 5
}
```

O para desasignar:
```json
{
  "assigneeId": null
}
```

#### Validaciones:
- Usuario debe existir
- Usuario debe ser support o sysAdmin
- Usuario debe estar activo

#### Response 200 OK:
```json
{
  "msg": "Ticket asignado a Juan Pérez exitosamente",
  "ticket": { ... }
}
```

---

### 7. Mis Tickets

Lista tickets creados por el usuario autenticado.

**Endpoint:** `GET /tickets/my-tickets/`  
**Autenticación:** Requerida

#### Query Parameters:
- `status` - Filtrar por estado

#### Response 200 OK:
```json
{
  "count": 10,
  "results": [ ... ]
}
```

---

### 8. Tickets Asignados (Support/Admin)

Lista tickets asignados al usuario autenticado.

**Endpoint:** `GET /tickets/assigned/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Response 200 OK:
```json
{
  "count": 5,
  "results": [ ... ]
}
```

---

### 9. Tickets Sin Asignar (Support/Admin)

Lista tickets que no tienen usuario asignado.

**Endpoint:** `GET /tickets/unassigned/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Response 200 OK:
```json
{
  "count": 15,
  "results": [ ... ]
}
```

---

### 10. Eliminar Ticket (Admin)

Elimina un ticket del sistema.

**Endpoint:** `DELETE /tickets/{id}/delete/`  
**Autenticación:** Requerida (sysAdmin)

#### Response 200 OK:
```json
{
  "msg": "Ticket \"Problema con el servidor\" eliminado exitosamente"
}
```

---

## 💬 Comentarios

### 1. Listar Comentarios

Lista comentarios de un ticket.

**Endpoint:** `GET /tickets/{ticket_id}/comments/`  
**Autenticación:** Requerida

#### Permisos:
- **user:** Solo comentarios públicos de sus tickets
- **support/admin:** Todos los comentarios (incluidos privados)

#### Response 200 OK:
```json
{
  "count": 5,
  "comments": [
    {
      "id": 1,
      "text": "Estoy investigando el problema...",
      "author": {
        "id": 3,
        "fullName": "Agente Soporte",
        "role": "support"
      },
      "ticketId": 1,
      "createdAt": "2024-11-19T12:00:00Z",
      "isPrivate": false
    }
  ]
}
```

---

### 2. Crear Comentario

Agrega un comentario a un ticket.

**Endpoint:** `POST /tickets/{ticket_id}/comments/create/`  
**Autenticación:** Requerida

#### Request Body:
```json
{
  "text": "He revisado el servidor y encontré el problema...",
  "isPrivate": false
}
```

#### Validaciones:
- `text`: 1-2000 caracteres, no vacío
- `isPrivate`: Solo support/admin pueden crear privados (default: false)

#### Response 201 Created:
```json
{
  "msg": "Comentario creado exitosamente",
  "comment": { ... }
}
```

---

### 3. Ver Comentario

Obtiene detalles de un comentario.

**Endpoint:** `GET /tickets/{ticket_id}/comments/{comment_id}/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "id": 1,
  "text": "Comentario completo...",
  "author": { ... },
  "createdAt": "2024-11-19T12:00:00Z"
}
```

---

### 4. Actualizar Comentario

Actualiza un comentario existente.

**Endpoint:** `PUT /tickets/{ticket_id}/comments/{comment_id}/update/`  
**Autenticación:** Requerida

#### Permisos:
- Solo el autor o sysAdmin

#### Request Body:
```json
{
  "text": "Texto actualizado del comentario..."
}
```

#### Response 200 OK:
```json
{
  "msg": "Comentario actualizado exitosamente",
  "comment": { ... }
}
```

---

### 5. Eliminar Comentario

Elimina un comentario.

**Endpoint:** `DELETE /tickets/{ticket_id}/comments/{comment_id}/delete/`  
**Autenticación:** Requerida

#### Permisos:
- Solo el autor o sysAdmin

#### Response 200 OK:
```json
{
  "msg": "Comentario eliminado exitosamente"
}
```

---

## 📎 Attachments

### 1. Listar Archivos

Lista archivos adjuntos de un ticket.

**Endpoint:** `GET /tickets/{ticket_id}/attachments/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "count": 2,
  "attachments": [
    {
      "id": 1,
      "originalFilename": "screenshot.png",
      "fileUrl": "http://localhost:8000/media/attachments/1/screenshot.png",
      "fileSize": 245678,
      "mimeType": "image/png",
      "uploadedBy": {
        "id": 2,
        "fullName": "Usuario Ejemplo"
      },
      "createdAt": "2024-11-19T12:00:00Z",
      "isPrivate": false
    }
  ]
}
```

---

### 2. Subir Archivo

Sube un archivo adjunto a un ticket.

**Endpoint:** `POST /tickets/{ticket_id}/attachments/upload/`  
**Autenticación:** Requerida  
**Content-Type:** `multipart/form-data`

#### Request Body (form-data):
```
file: [archivo]
isPrivate: false
```

#### Validaciones:
- Tamaño máximo: 10MB
- Tipos permitidos: .pdf, .doc, .docx, .txt, .xlsx, .xls, .jpg, .jpeg, .png, .gif, .bmp, .zip, .rar, .7z
- `isPrivate`: Solo support/admin pueden subir privados

#### Response 201 Created:
```json
{
  "msg": "Archivo subido exitosamente",
  "attachment": { ... }
}
```

#### Errores Posibles:
- `400` - Archivo excede 10MB
- `400` - Tipo de archivo no permitido

---

### 3. Ver Archivo

Obtiene detalles de un archivo.

**Endpoint:** `GET /tickets/{ticket_id}/attachments/{attachment_id}/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "id": 1,
  "originalFilename": "documento.pdf",
  "fileUrl": "http://localhost:8000/media/...",
  "fileSize": 1234567,
  "mimeType": "application/pdf"
}
```

---

### 4. Eliminar Archivo

Elimina un archivo adjunto.

**Endpoint:** `DELETE /tickets/{ticket_id}/attachments/{attachment_id}/delete/`  
**Autenticación:** Requerida

#### Permisos:
- Solo quien subió el archivo o sysAdmin

#### Response 200 OK:
```json
{
  "msg": "Archivo \"documento.pdf\" eliminado exitosamente"
}
```

---

## 🏷️ Categorías

### 1. Listar Categorías

Lista todas las categorías.

**Endpoint:** `GET /categories/`  
**Autenticación:** Requerida

#### Query Parameters:
- `search` - Buscar por nombre

#### Response 200 OK:
```json
{
  "count": 5,
  "categories": [
    {
      "id": 1,
      "name": "Hardware",
      "description": "Problemas relacionados con hardware",
      "createdAt": "2024-11-19T12:00:00Z",
      "ticketCount": 15
    }
  ]
}
```

---

### 2. Crear Categoría (Admin)

Crea una nueva categoría.

**Endpoint:** `POST /categories/create/`  
**Autenticación:** Requerida (sysAdmin)

#### Request Body:
```json
{
  "name": "Software",
  "description": "Problemas de software y aplicaciones"
}
```

#### Validaciones:
- `name`: 2-100 caracteres, único
- `description`: Opcional

#### Response 201 Created:
```json
{
  "msg": "Categoría creada exitosamente",
  "category": { ... }
}
```

---

### 3. Ver Categoría

Obtiene detalles de una categoría.

**Endpoint:** `GET /categories/{id}/`  
**Autenticación:** Requerida

#### Response 200 OK:
```json
{
  "id": 1,
  "name": "Hardware",
  "description": "Problemas relacionados con hardware",
  "ticketCount": 15
}
```

---

### 4. Actualizar Categoría (Admin)

Actualiza una categoría existente.

**Endpoint:** `PUT /categories/{id}/update/`  
**Autenticación:** Requerida (sysAdmin)

#### Request Body:
```json
{
  "name": "Hardware y Equipos",
  "description": "Descripción actualizada"
}
```

#### Response 200 OK:
```json
{
  "msg": "Categoría actualizada exitosamente",
  "category": { ... }
}
```

---

### 5. Eliminar Categoría (Admin)

Elimina una categoría.

**Endpoint:** `DELETE /categories/{id}/delete/`  
**Autenticación:** Requerida (sysAdmin)

#### Response 200 OK:
```json
{
  "msg": "Categoría \"Hardware\" eliminada exitosamente"
}
```

#### Errores Posibles:
- `400` - No se puede eliminar una categoría con tickets asociados

---

## 📊 Métricas

### 1. Overview de Tickets

Resumen de tickets por estado y prioridad.

**Endpoint:** `GET /metrics/tickets/overview/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Response 200 OK:
```json
{
  "statusMetrics": {
    "total": 150,
    "open": 45,
    "inProgress": 30,
    "resolved": 50,
    "closed": 20,
    "canceled": 5,
    "unassigned": 15
  },
  "priorityMetrics": {
    "low": 30,
    "medium": 70,
    "high": 40,
    "urgent": 10
  }
}
```

---

### 2. Performance de Tickets

Métricas de rendimiento del sistema.

**Endpoint:** `GET /metrics/tickets/performance/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Response 200 OK:
```json
{
  "averageResolutionTime": 24.5,
  "totalResolved": 50,
  "totalCreatedToday": 5,
  "totalCreatedThisWeek": 25,
  "totalCreatedThisMonth": 90,
  "resolutionRate": 33.33
}
```

#### Campos:
- `averageResolutionTime`: Horas promedio de resolución
- `resolutionRate`: Porcentaje de tickets resueltos

---

### 3. Actividad de Usuarios (Admin)

Métricas de actividad por usuario.

**Endpoint:** `GET /metrics/users/activity/`  
**Autenticación:** Requerida (sysAdmin)

#### Response 200 OK:
```json
{
  "count": 20,
  "users": [
    {
      "userId": 3,
      "userName": "Agente Soporte",
      "email": "agente@example.com",
      "role": "support",
      "ticketsCreated": 5,
      "ticketsAssigned": 30,
      "ticketsResolved": 25,
      "commentsPosted": 120,
      "lastActivity": "2024-11-19T12:00:00Z"
    }
  ]
}
```

---

### 4. Health del Sistema

Estado general del sistema.

**Endpoint:** `GET /metrics/system/health/`  
**Autenticación:** Requerida (support o sysAdmin)

#### Response 200 OK:
```json
{
  "status": "healthy",
  "totalUsers": 150,
  "activeUsers": 145,
  "totalTickets": 200,
  "openTickets": 45,
  "urgentTickets": 10,
  "unassignedTickets": 15,
  "averageResponseTime": 2.5
}
```

#### Estados posibles:
- `healthy` - Sistema normal
- `warning` - >10 tickets sin asignar
- `critical` - >5 urgentes o >20 sin asignar

---

## 🔧 Sistema

### 1. Health Check

Verifica el estado del sistema.

**Endpoint:** `GET /health/`  
**Autenticación:** No requerida

#### Response 200 OK:
```json
{
  "status": "healthy",
  "message": "Sistema de tickets funcionando correctamente",
  "timestamp": "2024-11-19T12:00:00Z",
  "version": "1.0.0",
  "database": "healthy",
  "services": {
    "database": "healthy",
    "api": "healthy"
  }
}
```

---

### 2. Información de la API

Información general de la API.

**Endpoint:** `GET /info/`  
**Autenticación:** No requerida

#### Response 200 OK:
```json
{
  "name": "Sistema de Tickets API",
  "version": "1.0.0",
  "description": "API REST para sistema de gestión de tickets de soporte",
  "documentation": {
    "swagger": "http://localhost:8000/api/schema/swagger-ui/",
    "redoc": "http://localhost:8000/api/schema/redoc/"
  },
  "endpoints": {
    "authentication": "/api/auth/",
    "users": "/api/users/",
    "tickets": "/api/tickets/",
    "comments": "/api/tickets/{id}/comments/",
    "attachments": "/api/tickets/{id}/attachments/",
    "categories": "/api/categories/",
    "metrics": "/api/metrics/",
    "health": "/api/health/"
  },
  "contact": {
    "team": "Equipo de Desarrollo",
    "productOwner": "Lautaro Cavallo"
  }
}
```

---

### 3. Versión de la API

Versión actual de la API.

**Endpoint:** `GET /version/`  
**Autenticación:** No requerida

#### Response 200 OK:
```json
{
  "version": "1.0.0",
  "releaseDate": "2024-01-01",
  "environment": "development"
}
```

---

## ❌ Códigos de Error

### Códigos HTTP

| Código | Significado | Cuándo ocurre |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado |
| 400 | Bad Request | Datos inválidos |
| 401 | Unauthorized | Sin autenticación o token inválido |
| 403 | Forbidden | Sin permisos para la operación |
| 404 | Not Found | Recurso no encontrado |
| 500 | Internal Server Error | Error del servidor |

### Formato de Error

```json
{
  "error": "Mensaje de error legible",
  "details": {
    "campo": ["Detalle específico del error"]
  },
  "timestamp": "2024-11-19T12:00:00Z",
  "status_code": 400
}
```

### Errores Comunes

#### 401 - No Autenticado
```json
{
  "error": "Debe iniciar sesión para acceder a este recurso",
  "timestamp": "2024-11-19T12:00:00Z"
}
```

#### 403 - Sin Permisos
```json
{
  "error": "No tiene permiso para realizar esta acción",
  "timestamp": "2024-11-19T12:00:00Z"
}
```

#### 400 - Validación
```json
{
  "error": "Datos inválidos",
  "details": {
    "title": ["Asegúrese de que este campo tenga al menos 5 caracteres."],
    "email": ["Ya existe un usuario registrado con este email."]
  },
  "timestamp": "2024-11-19T12:00:00Z"
}
```

---

## 📚 Ejemplos de Uso

### Flujo Completo: Crear y Resolver un Ticket

#### 1. Login
```bash
POST /api/auth/login/
{
  "email": "soporte@example.com",
  "password": "Password123!"
}
```

#### 2. Crear Ticket (como usuario)
```bash
POST /api/tickets/create/
Authorization: Bearer {accessToken}
{
  "title": "Error en la aplicación",
  "description": "La app se cierra al subir archivos",
  "priority": "high"
}
```

#### 3. Asignar Ticket (como support)
```bash
PATCH /api/tickets/1/assign/
Authorization: Bearer {accessToken}
{
  "assigneeId": 5
}
```

#### 4. Agregar Comentario
```bash
POST /api/tickets/1/comments/create/
Authorization: Bearer {accessToken}
{
  "text": "Estoy revisando el problema..."
}
```

#### 5. Actualizar Estado
```bash
PATCH /api/tickets/1/status/
Authorization: Bearer {accessToken}
{
  "status": "resolved"
}
```

---

## 🔗 Recursos Adicionales

- **Swagger UI:** http://localhost:8000/api/schema/swagger-ui/
- **ReDoc:** http://localhost:8000/api/schema/redoc/
- **Manual del Desarrollador:** `MANUAL-DESARROLLADOR.md`
- **Guía Rápida:** `QUICKSTART.md`

---

**Versión:** 1.0  
**Última Actualización:** Noviembre 2025  
**Mantenido por:** Equipo de Desarrollo

