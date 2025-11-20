# 📊 Guía de Uso de Métricas - Ticket Mobile API

## 🎯 Endpoints Disponibles

### 1. Overview de Tickets
**Endpoint:** `GET /api/metrics/tickets/overview/`  
**Permisos:** Support o Admin  
**Descripción:** Vista general de tickets por estado y prioridad

**Respuesta:**
```json
{
  "statusMetrics": {
    "total": 1,
    "open": 1,
    "inProgress": 0,
    "resolved": 0,
    "closed": 0,
    "canceled": 0,
    "unassigned": 1
  },
  "priorityMetrics": {
    "low": 0,
    "medium": 0,
    "high": 1,
    "urgent": 0
  }
}
```

---

### 2. Performance de Tickets
**Endpoint:** `GET /api/metrics/tickets/performance/`  
**Permisos:** Support o Admin  
**Descripción:** Métricas de rendimiento y resolución

**Respuesta:**
```json
{
  "averageResolutionTime": 24.5,
  "totalResolved": 15,
  "totalCreatedToday": 3,
  "totalCreatedThisWeek": 12,
  "totalCreatedThisMonth": 45,
  "resolutionRate": 75.5
}
```

---

### 3. Actividad de Usuarios
**Endpoint:** `GET /api/metrics/users/activity/`  
**Permisos:** Solo Admin (sysAdmin)  
**Descripción:** Actividad detallada de cada usuario

**Respuesta:**
```json
{
  "count": 2,
  "users": [
    {
      "userId": 1,
      "userName": "Admin System",
      "email": "admin@ticketmobile.com",
      "role": "sysAdmin",
      "ticketsCreated": 10,
      "ticketsAssigned": 5,
      "ticketsResolved": 3,
      "commentsPosted": 15,
      "lastActivity": "2025-11-19T12:57:46.088169-03:00"
    }
  ]
}
```

---

### 4. Salud del Sistema
**Endpoint:** `GET /api/metrics/system/health/`  
**Permisos:** Support o Admin  
**Descripción:** Estado general del sistema

**Respuesta:**
```json
{
  "status": "healthy",
  "totalUsers": 25,
  "activeUsers": 23,
  "totalTickets": 100,
  "openTickets": 15,
  "urgentTickets": 2,
  "unassignedTickets": 5,
  "averageResponseTime": 2.5
}
```

---

## 🔑 Requisitos de Permisos

| Endpoint | Permiso Requerido | Roles Permitidos |
|----------|-------------------|------------------|
| `tickets/overview/` | Support o Admin | `support`, `sysAdmin` |
| `tickets/performance/` | Support o Admin | `support`, `sysAdmin` |
| `users/activity/` | Solo Admin | `sysAdmin` |
| `system/health/` | Support o Admin | `support`, `sysAdmin` |

---

## 📱 Cómo Acceder desde Android

### 1. Agregar el servicio en `ApiService.kt`:

```kotlin
interface ApiService {
    // ... otros endpoints ...
    
    // Metrics
    @GET("metrics/tickets/overview/")
    suspend fun getTicketsOverview(
        @Header("Authorization") token: String
    ): Response<TicketsOverviewResponse>
    
    @GET("metrics/tickets/performance/")
    suspend fun getTicketsPerformance(
        @Header("Authorization") token: String
    ): Response<TicketsPerformanceResponse>
    
    @GET("metrics/users/activity/")
    suspend fun getUsersActivity(
        @Header("Authorization") token: String
    ): Response<UsersActivityResponse>
    
    @GET("metrics/system/health/")
    suspend fun getSystemHealth(
        @Header("Authorization") token: String
    ): Response<SystemHealthResponse>
}
```

### 2. Crear los modelos de datos:

```kotlin
// En data/models/Metrics.kt
data class TicketsOverviewResponse(
    val statusMetrics: StatusMetrics,
    val priorityMetrics: PriorityMetrics
)

data class StatusMetrics(
    val total: Int,
    val open: Int,
    val inProgress: Int,
    val resolved: Int,
    val closed: Int,
    val canceled: Int,
    val unassigned: Int
)

data class PriorityMetrics(
    val low: Int,
    val medium: Int,
    val high: Int,
    val urgent: Int
)

data class TicketsPerformanceResponse(
    val averageResolutionTime: Float,
    val totalResolved: Int,
    val totalCreatedToday: Int,
    val totalCreatedThisWeek: Int,
    val totalCreatedThisMonth: Int,
    val resolutionRate: Float
)

data class UsersActivityResponse(
    val count: Int,
    val users: List<UserActivity>
)

data class UserActivity(
    val userId: Int,
    val userName: String,
    val email: String,
    val role: String,
    val ticketsCreated: Int,
    val ticketsAssigned: Int,
    val ticketsResolved: Int,
    val commentsPosted: Int,
    val lastActivity: String
)

data class SystemHealthResponse(
    val status: String,
    val totalUsers: Int,
    val activeUsers: Int,
    val totalTickets: Int,
    val openTickets: Int,
    val urgentTickets: Int,
    val unassignedTickets: Int,
    val averageResponseTime: Float
)
```

### 3. Usar en el ViewModel:

```kotlin
class MetricsViewModel : ViewModel() {
    private val repository = TicketRepository()
    
    private val _ticketsOverview = MutableStateFlow<TicketsOverviewResponse?>(null)
    val ticketsOverview: StateFlow<TicketsOverviewResponse?> = _ticketsOverview.asStateFlow()
    
    fun loadTicketsOverview(token: String) {
        viewModelScope.launch {
            try {
                val response = repository.getTicketsOverview(token)
                if (response.isSuccessful) {
                    _ticketsOverview.value = response.body()
                }
            } catch (e: Exception) {
                // Manejar error
            }
        }
    }
}
```

### 4. Mostrar en la UI (Compose):

```kotlin
@Composable
fun MetricsScreen(viewModel: MetricsViewModel) {
    val overview by viewModel.ticketsOverview.collectAsState()
    
    overview?.let { data ->
        Column {
            Text("Total Tickets: ${data.statusMetrics.total}")
            Text("Abiertos: ${data.statusMetrics.open}")
            Text("En Progreso: ${data.statusMetrics.inProgress}")
            
            // Gráfico de torta con las prioridades
            PieChart(
                data = listOf(
                    data.priorityMetrics.low,
                    data.priorityMetrics.medium,
                    data.priorityMetrics.high,
                    data.priorityMetrics.urgent
                )
            )
        }
    }
}
```

---

## 🖥️ Cómo Acceder desde Terminal/Postman

### 1. Obtener Token JWT

```bash
# Hacer Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@ticketmobile.com",
    "password": "tu_password"
  }'

# Respuesta:
{
  "accessToken": "eyJhbGciOiJIUzI1...",
  "refreshToken": "eyJhbGciOiJIUzI1...",
  "user": { ... }
}
```

### 2. Usar el Token para Obtener Métricas

```bash
# PowerShell
$token = "TU_TOKEN_AQUI"
$headers = @{ "Authorization" = "Bearer $token" }

# 1. Overview
Invoke-WebRequest -Uri "http://localhost:8000/api/metrics/tickets/overview/" `
  -Method GET -Headers $headers | Select-Object -ExpandProperty Content

# 2. Performance
Invoke-WebRequest -Uri "http://localhost:8000/api/metrics/tickets/performance/" `
  -Method GET -Headers $headers | Select-Object -ExpandProperty Content

# 3. Actividad de Usuarios
Invoke-WebRequest -Uri "http://localhost:8000/api/metrics/users/activity/" `
  -Method GET -Headers $headers | Select-Object -ExpandProperty Content

# 4. Salud del Sistema
Invoke-WebRequest -Uri "http://localhost:8000/api/metrics/system/health/" `
  -Method GET -Headers $headers | Select-Object -ExpandProperty Content
```

### 3. Usando Postman

1. **Crear nueva request GET**
2. **URL:** `http://localhost:8000/api/metrics/tickets/overview/`
3. **Headers:**
   - Key: `Authorization`
   - Value: `Bearer TU_TOKEN_AQUI`
4. **Send**

---

## 📊 Ejemplo de Pantalla de Métricas en Android

```kotlin
@Composable
fun StatisticsScreen(viewModel: MetricsViewModel) {
    val overview by viewModel.ticketsOverview.collectAsState()
    val performance by viewModel.ticketsPerformance.collectAsState()
    val systemHealth by viewModel.systemHealth.collectAsState()
    
    LazyColumn {
        // Header
        item {
            Text(
                text = "Dashboard de Métricas",
                style = MaterialTheme.typography.headlineMedium
            )
        }
        
        // Estado del Sistema
        item {
            Card {
                systemHealth?.let {
                    Row {
                        Icon(
                            imageVector = when(it.status) {
                                "healthy" -> Icons.Default.CheckCircle
                                "warning" -> Icons.Default.Warning
                                else -> Icons.Default.Error
                            },
                            contentDescription = null
                        )
                        Column {
                            Text("Estado: ${it.status}")
                            Text("Usuarios Activos: ${it.activeUsers}/${it.totalUsers}")
                            Text("Tickets Urgentes: ${it.urgentTickets}")
                        }
                    }
                }
            }
        }
        
        // Gráfico de Estado de Tickets
        item {
            Card {
                overview?.let {
                    BarChart(
                        data = listOf(
                            "Abiertos" to it.statusMetrics.open,
                            "En Progreso" to it.statusMetrics.inProgress,
                            "Resueltos" to it.statusMetrics.resolved
                        )
                    )
                }
            }
        }
        
        // Métricas de Performance
        item {
            Card {
                performance?.let {
                    Column {
                        MetricItem(
                            label = "Tiempo Promedio Resolución",
                            value = "${it.averageResolutionTime} hrs"
                        )
                        MetricItem(
                            label = "Tasa de Resolución",
                            value = "${it.resolutionRate}%"
                        )
                        MetricItem(
                            label = "Creados Hoy",
                            value = "${it.totalCreatedToday}"
                        )
                    }
                }
            }
        }
    }
}
```

---

## 🔧 Casos de Uso

### 1. Dashboard Principal (Admin)
- Mostrar estado general del sistema
- Tickets sin asignar
- Tickets urgentes

### 2. Reportes de Performance
- Gráficos de resolución por semana/mes
- Tiempo promedio de respuesta
- Tasa de resolución

### 3. Gestión de Equipo
- Actividad de cada agente
- Tickets asignados vs resueltos
- Productividad del equipo

### 4. Alertas y Monitoreo
- Sistema en estado "warning" o "critical"
- Tickets urgentes sin asignar
- Usuarios inactivos

---

## 🚀 Tips de Implementación

### 1. **Actualización en Tiempo Real**
```kotlin
LaunchedEffect(Unit) {
    while(true) {
        viewModel.loadMetrics()
        delay(30_000) // Actualizar cada 30 segundos
    }
}
```

### 2. **Caché Local**
```kotlin
// Guardar en DataStore para acceso offline
dataStore.data.map { preferences ->
    preferences[LAST_METRICS]?.let { json ->
        Json.decodeFromString<MetricsData>(json)
    }
}
```

### 3. **Gráficos Recomendados**
- **Overview:** Gráfico de torta (PieChart)
- **Performance:** Gráfico de líneas (LineChart)
- **Actividad:** Tabla o lista
- **Salud:** Cards con iconos de estado

---

## ❓ Troubleshooting

### Error 403 (Forbidden)
**Causa:** Usuario sin permisos suficientes  
**Solución:** Asegurarse que el usuario tenga rol `support` o `sysAdmin`

### Error 401 (Unauthorized)
**Causa:** Token inválido o expirado  
**Solución:** Hacer login nuevamente para obtener nuevo token

### Datos vacíos
**Causa:** No hay tickets/usuarios en el sistema  
**Solución:** Crear datos de prueba primero

---

## 📚 Referencias

- Documentación completa: `backend/IMPLEMENTATION.md`
- Guía rápida: `backend/QUICKSTART.md`
- Modelos de datos: `backend/apps/*/models.py`
- Serializers: `backend/apps/metrics/serializers.py`

---

**Desarrollado para Ticket Mobile - Sistema de Gestión de Tickets**

