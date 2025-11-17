# 🚀 Guía Paso a Paso: Desplegar Backend en Render

Esta guía te llevará paso a paso para desplegar el backend Flask en Render y conectarlo con tu frontend en Vercel.

---

## 📋 Paso 1: Preparar el Repositorio

### 1.1 Verificar que no hay credenciales en Git

```bash
# Asegúrate de que .env está en .gitignore
git status
git check-ignore .env
```

Si `.env` no está ignorado, agrégalo:
```bash
echo ".env" >> .gitignore
echo ".env.*" >> .gitignore
git add .gitignore
git commit -m "Asegurar que .env está ignorado"
```

### 1.2 Verificar archivos importantes

Asegúrate de que estos archivos existen:
- ✅ `Procfile` (ya creado)
- ✅ `requirements.txt` (ya existe)
- ✅ `frontend/app.py` (ya existe)

---

## 📋 Paso 2: Crear Cuenta en Render

1. Ve a [render.com](https://render.com)
2. Crea una cuenta (puedes usar GitHub para login rápido)
3. Verifica tu email si es necesario

---

## 📋 Paso 3: Crear Nuevo Web Service en Render

### 3.1 Iniciar creación

1. En el dashboard de Render, haz clic en **"New +"**
2. Selecciona **"Web Service"**
3. Conecta tu repositorio de GitHub:
   - Si no está conectado, Render te pedirá autorizar acceso a GitHub
   - Selecciona el repositorio `marketingagent`
   - Selecciona la rama `main`

### 3.2 Configurar el servicio

Completa estos campos:

**Basic Settings:**
- **Name**: `marketingagent-backend` (o el nombre que prefieras)
- **Region**: Elige la región más cercana a tus usuarios (ej: `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: (déjalo vacío, Render usará la raíz)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```bash
  PYTHONPATH=/app python3 frontend/app.py
  ```
  (O simplemente deja el Procfile que ya creamos)

**Plan:**
- Para empezar, usa el plan **Free** (puedes actualizar después)
- ⚠️ **Nota**: El plan free "duerme" después de 15 minutos de inactividad. Para producción, considera el plan Starter ($7/mes)

---

## 📋 Paso 4: Configurar Variables de Entorno

En la sección **"Environment"** de tu servicio en Render, agrega estas variables:

### Variables Requeridas (Mínimas para funcionar):

```bash
# Email (para enviar reportes)
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LLM (Ollama o OpenAI)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest
# O si usas OpenAI:
# OPENAI_API_KEY=sk-...
# OPENAI_API_BASE=https://api.openai.com/v1
# OPENAI_MODEL_NAME=gpt-4

# Pinecone (opcional, pero recomendado)
PINECONE_API_KEY=tu-pinecone-key
PINECONE_ENVIRONMENT=us-east-1
```

### Variables Opcionales (para Google Ads real):

```bash
# Solo si quieres lanzar campañas reales
GOOGLE_ADS_DEVELOPER_TOKEN=tu-developer-token
GOOGLE_ADS_CLIENT_ID=tu-client-id
GOOGLE_ADS_CLIENT_SECRET=tu-client-secret
GOOGLE_ADS_REFRESH_TOKEN=tu-refresh-token
GOOGLE_ADS_LOGIN_CUSTOMER_ID=tu-customer-id
USE_SIMULATORS=false
```

### Variables de Sistema (Render las configura automáticamente):

- `PORT` - Render lo configura automáticamente
- `HOST` - Render lo configura automáticamente

**⚠️ IMPORTANTE**: 
- No agregues `PORT` ni `HOST` manualmente, Render los configura automáticamente
- Para cada variable, haz clic en **"Add Environment Variable"** y pega el nombre y valor

---

## 📋 Paso 5: Desplegar

1. Haz clic en **"Create Web Service"**
2. Render comenzará a construir y desplegar tu aplicación
3. Esto puede tomar 5-10 minutos la primera vez
4. Verás los logs en tiempo real

### 5.1 Verificar el despliegue

Una vez completado, verás:
- ✅ **Status**: Live
- 🌐 **URL**: `https://marketingagent-backend.onrender.com` (o similar)

Prueba que funciona:
```bash
curl https://tu-backend-url.onrender.com/health
```

Deberías recibir: `{"status": "healthy"}`

---

## 📋 Paso 6: Configurar CORS (si es necesario)

Si tu frontend en Vercel tiene un dominio específico, actualiza CORS en `frontend/app.py`:

```python
# En frontend/app.py, línea ~40, cambia:
CORS(app, resources={
    r"/*": {
        "origins": ["https://tu-frontend.vercel.app"],  # Tu dominio de Vercel
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

O déjalo con `"origins": ["*"]` si quieres permitir cualquier origen (menos seguro pero más flexible para desarrollo).

---

## 📋 Paso 7: Conectar Frontend de Vercel con Backend de Render

### Opción A: Configurar en Vercel (Recomendado)

1. Ve a tu proyecto en Vercel
2. Ve a **Settings** → **Environment Variables**
3. Agrega:
   ```
   API_BASE=https://tu-backend-url.onrender.com
   ```
4. En `frontend/templates/index.html`, agrega al inicio del `<script>`:
   ```javascript
   window.API_BASE = 'https://tu-backend-url.onrender.com';
   ```

### Opción B: Usar localStorage (Temporal)

Abre la consola del navegador en tu sitio de Vercel y ejecuta:
```javascript
localStorage.setItem('API_BASE', 'https://tu-backend-url.onrender.com');
location.reload();
```

---

## 📋 Paso 8: Probar la Conexión

1. Abre tu frontend en Vercel
2. Abre la consola del navegador (F12)
3. Intenta hacer un análisis
4. Verifica que las peticiones van a `https://tu-backend-url.onrender.com`
5. Revisa los logs en Render para ver si hay errores

---

## 🔧 Troubleshooting

### Error: "Module not found"
- Verifica que `requirements.txt` tiene todas las dependencias
- Revisa los logs de build en Render

### Error: "Port already in use"
- Render configura `PORT` automáticamente, no lo definas manualmente

### Error: CORS
- Verifica que `flask-cors` está en `requirements.txt`
- Asegúrate de que los orígenes en CORS incluyen tu dominio de Vercel

### El servicio se "duerme" (plan Free)
- El plan Free de Render duerme después de 15 min de inactividad
- La primera petición después de dormir puede tardar 30-60 segundos
- Considera actualizar al plan Starter ($7/mes) para producción

### Error: "Email not sent"
- Verifica que `EMAIL_USER` y `EMAIL_PASSWORD` están correctos
- Si usas Gmail, necesitas una "App Password", no tu contraseña normal

---

## ✅ Checklist Final

- [ ] Backend desplegado en Render y funcionando
- [ ] Variables de entorno configuradas
- [ ] Health check responde correctamente
- [ ] Frontend en Vercel configurado con `API_BASE`
- [ ] Prueba de análisis funciona end-to-end
- [ ] Logs en Render muestran actividad correcta

---

## 🎉 ¡Listo!

Tu backend está desplegado y conectado. Los usuarios pueden usar tu frontend en Vercel y todas las peticiones irán a tu backend en Render.

**Próximos pasos opcionales:**
- Configurar un dominio personalizado en Render
- Habilitar auto-deploy en cada push a `main`
- Configurar alertas de monitoreo
- Actualizar al plan Starter para evitar el "sleep mode"

