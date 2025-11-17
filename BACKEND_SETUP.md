# 🚀 Guía de Inicio del Backend

Esta guía te ayudará a iniciar el servidor Flask y ngrok para el Marketing Agent.

## 📋 Requisitos Previos

1. **Python 3.9+** instalado
2. **ngrok** instalado (`brew install ngrok/ngrok/ngrok`)
3. Dependencias de Python instaladas (`pip install -r requirements.txt`)

## 🎯 Inicio Rápido

### Opción 1: Usar el Script Automático (Recomendado)

```bash
# Iniciar backend
./start_backend.sh

# Detener backend
./stop_backend.sh
```

### Opción 2: Inicio Manual

```bash
# Terminal 1: Iniciar Flask
cd frontend
python3 app.py

# Terminal 2: Iniciar ngrok
ngrok http 15000
```

## 📝 Detalles del Script `start_backend.sh`

El script automático hace lo siguiente:

1. ✅ Verifica y detiene procesos existentes en los puertos
2. ✅ Inicia el servidor Flask en el puerto 15000
3. ✅ Inicia ngrok apuntando al puerto 15000
4. ✅ Muestra las URLs locales y públicas
5. ✅ Guarda los logs en `/tmp/marketingagent/`

## 🔍 Verificación

Después de iniciar, deberías ver:

```
🎉 Backend iniciado correctamente!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📍 URLs:
   Local:  http://localhost:15000
   Public: https://tu-url-ngrok.ngrok-free.dev

📊 Monitoreo:
   Ngrok UI: http://localhost:4040
   Flask Logs: /tmp/marketingagent/flask.log
   Ngrok Logs: /tmp/marketingagent/ngrok.log
```

## 🧪 Probar el Endpoint

```bash
curl -X POST https://tu-url-ngrok.ngrok-free.dev/trial \
  -H "Content-Type: application/json" \
  -H "ngrok-skip-browser-warning: true" \
  -d '{
    "nombre": "Test",
    "apellido": "Test",
    "hotel_nombre": "Test Hotel",
    "web": "https://test.com",
    "correo": "test@test.com",
    "telefono": "1234567890"
  }'
```

## 🛑 Detener los Servicios

### Usando el script:
```bash
./stop_backend.sh
```

### Manualmente:
```bash
# Detener Flask
lsof -ti:15000 | xargs kill -9

# Detener ngrok
lsof -ti:4040 | xargs kill -9
```

## 📊 Monitoreo

- **Logs de Flask**: `/tmp/marketingagent/flask.log`
- **Logs de ngrok**: `/tmp/marketingagent/ngrok.log`
- **Interfaz de ngrok**: http://localhost:4040

## ⚠️ Troubleshooting

### Error: Puerto ya en uso
```bash
# Ver qué está usando el puerto
lsof -i:15000

# Detener el proceso
kill -9 <PID>
```

### Error: ngrok no encontrado
```bash
# Instalar ngrok
brew install ngrok/ngrok/ngrok

# O descargar desde: https://ngrok.com/download
```

### Error: Flask no inicia
```bash
# Ver logs
tail -50 /tmp/marketingagent/flask.log

# Verificar dependencias
pip install -r requirements.txt
```

## 🔄 Actualizar URL en Frontend

Después de iniciar ngrok, copia la URL pública y actualízala en:
`frontend/templates/index.html` línea 908:

```javascript
const BACKEND_URL = 'https://tu-nueva-url-ngrok.ngrok-free.dev';
```

## 📚 Endpoints Disponibles

- `POST /trial` - Guardar datos del formulario de prueba
- `POST /analyze` - Iniciar análisis de hotel
- `GET /status/<request_id>` - Obtener estado del análisis
- `GET /health` - Health check del servidor

## 💡 Tips

1. **Ngrok URL cambia**: Cada vez que reinicias ngrok, obtienes una nueva URL. Actualiza el frontend si es necesario.

2. **Persistencia**: Para mantener la misma URL de ngrok, considera usar ngrok con cuenta premium o configurar un dominio personalizado.

3. **Producción**: En producción, usa un servidor WSGI como Gunicorn y configura un dominio real en lugar de ngrok.

