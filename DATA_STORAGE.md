# 📊 Sistema de Almacenamiento de Datos

Este documento explica dónde y cómo se almacenan los datos en el Marketing Agent.

## 🗂️ Ubicación de los Datos

### 1. Datos del Formulario de Prueba (`/trial`)

**Ubicación:** `outputs/trials/`

**Formato:** Archivos JSON individuales

**Estructura del nombre:** `trial_{email}_{timestamp}.json`

**Ejemplo:**
```json
{
  "nombre": "Ariel",
  "apellido": "Sanchez",
  "hotel_nombre": "TPH Hotel",
  "instagram": "https://instagram.com/tphj",
  "web": "https://estanciahacienda.lovable.app/",
  "correo": "ariel@gmail.com",
  "telefono": "1234567890",
  "timestamp": "2025-11-17T12:43:05.409553"
}
```

**Persistencia:** ✅ **Permanente** - Los datos se guardan en disco y persisten después de reiniciar el servidor.

### 2. Estado del Análisis (`/status`)

**Ubicación:** Memoria del servidor (`processing_status`)

**Formato:** Diccionario en memoria de Python

**Estructura:**
```python
{
  'request_id': {
    'status': 'processing' | 'completed' | 'error',
    'message': 'Starting analysis...',
    'progress': 10-100,
    'start_time': timestamp,
    'elapsed_time': segundos
  }
}
```

**Persistencia:** ❌ **Temporal** - Se pierde cuando el servidor se reinicia.

### 3. Resultados del Análisis

**Ubicación:** Memoria del servidor (`processing_results`)

**Formato:** Diccionario en memoria de Python

**Persistencia:** ❌ **Temporal** - Se pierde cuando el servidor se reinicia.

**Nota:** Los resultados también se pueden descargar como JSON usando `/download/<request_id>`

### 4. Archivos de Análisis Generados

**Ubicación:** `outputs/`

**Tipos de archivos:**
- `{hotel_name}_analysis.json` - Análisis completo del hotel
- `{hotel_name}_google_ads.md` - Campañas de Google Ads
- `{hotel_name}_market_research.md` - Investigación de mercado
- `{hotel_name}_optimization.md` - Optimizaciones recomendadas
- `workflow_results.json` - Resultados del workflow completo

**Persistencia:** ✅ **Permanente** - Se guardan en disco.

## 🔄 Flujo de Datos

```
1. Usuario completa formulario → POST /trial
   ↓
2. Datos guardados en: outputs/trials/trial_{email}_{timestamp}.json
   ↓
3. Análisis iniciado → request_id generado
   ↓
4. Estado guardado en: processing_status[request_id] (memoria)
   ↓
5. Análisis completado → Resultados en: processing_results[request_id] (memoria)
   ↓
6. Archivos generados en: outputs/{hotel_name}_*.{json,md}
```

## ⚠️ Limitaciones Actuales

### Datos en Memoria
- **Estado del análisis** (`processing_status`) se pierde al reiniciar el servidor
- **Resultados** (`processing_results`) se pierden al reiniciar el servidor
- **Solución temporal:** Los datos del trial se guardan en archivos JSON

### Recomendaciones para Producción

1. **Base de Datos:** Implementar PostgreSQL o MongoDB para:
   - Estados de análisis persistentes
   - Resultados almacenados permanentemente
   - Historial de análisis por usuario

2. **Cache Redis:** Para estados temporales de análisis en progreso

3. **Almacenamiento de Archivos:** Considerar S3 o similar para archivos generados

## 📁 Estructura de Directorios

```
marketingagent/
├── outputs/
│   ├── trials/                    # Datos del formulario de prueba
│   │   └── trial_*.json
│   ├── approvals/                 # Aprobaciones de estrategias
│   ├── strategies/                # Estrategias guardadas
│   ├── {hotel_name}_*.json       # Análisis completos
│   └── {hotel_name}_*.md          # Reportes en markdown
├── logs/                          # Logs del sistema
└── memory_data.json              # Memoria del sistema (si se usa)
```

## 🔍 Verificar Datos Guardados

### Ver datos del trial:
```bash
ls -la outputs/trials/
cat outputs/trials/trial_*.json
```

### Ver análisis completados:
```bash
ls -la outputs/*.json
ls -la outputs/*.md
```

### Ver logs:
```bash
tail -f logs/marketing-agent.log
```

## 💾 Migración a Base de Datos

Para migrar a una base de datos real, necesitarías:

1. **Modelo de Datos:**
   - Tabla `trials` - Datos del formulario
   - Tabla `analyses` - Estados y resultados de análisis
   - Tabla `hotels` - Información de hoteles

2. **Cambios en el código:**
   - Reemplazar `processing_status` con consultas a BD
   - Reemplazar `processing_results` con consultas a BD
   - Actualizar endpoint `/trial` para guardar en BD

3. **Ventajas:**
   - Persistencia permanente
   - Búsqueda y filtrado
   - Historial completo
   - Escalabilidad

## 📝 Notas Importantes

- Los datos del trial **SÍ se guardan permanentemente** en archivos JSON
- El estado del análisis **NO persiste** si el servidor se reinicia
- Los resultados finales **NO persisten** si el servidor se reinicia
- Los archivos generados (JSON, MD) **SÍ persisten** en disco

