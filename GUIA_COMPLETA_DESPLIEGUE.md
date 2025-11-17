# 🚀 Guía Completa: Desplegar Backend y Conectar con Vercel

## 📋 Entendiendo la Arquitectura

Tu aplicación tiene dos partes:

1. **Backend (Servidor Flask)**: `frontend/app.py`
   - Maneja las peticiones de análisis
   - Se conecta a Google Ads API
   - Envía emails
   - **DEBE estar desplegado en Render/Railway** para que Vercel pueda acceder

2. **Frontend (HTML estático)**: `frontend/templates/index.html`
   - Ya está desplegado en Vercel
   - Hace peticiones al backend

**⚠️ IMPORTANTE**: Vercel solo sirve archivos estáticos. No puede ejecutar Python. Por eso necesitas desplegar el backend en otro servicio (Render).

---

## 🎯 Plan de Acción

### Fase 1: Desplegar el Backend en Render (15-20 minutos)
### Fase 2: Conectar Vercel con Render (5 minutos)

---

## 📦 FASE 1: Desplegar Backend en Render

### Paso 1: Verificar que todo está listo

✅ Ya tienes:
- `Procfile` (para Render)
- `requirements.txt` (dependencias)
- `frontend/app.py` (tu backend)
- CORS configurado

### Paso 2: Ir a Render.com

1. Ve a [render.com](https://render.com)
2. Crea cuenta o inicia sesión (puedes usar GitHub)

### Paso 3: Crear Nuevo Web Service

1. Click en **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub:
   - Si no está conectado, autoriza acceso
   - Selecciona el repo `marketingagent`
   - Selecciona branch `main`

### Paso 4: Configurar el Servicio

**Basic Settings:**
- **Name**: `marketingagent-backend` (o el que prefieras)
- **Region**: Elige la más cercana (ej: `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: (déjalo vacío)

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
  (O déjalo vacío, Render usará el `Procfile` automáticamente)

**Plan:**
- **Free** (para empezar, se "duerme" después de 15 min)
- O **Starter** ($7/mes, siempre activo)

### Paso 5: Configurar Variables de Entorno

En la sección **"Environment"**, agrega estas variables:

#### Variables Requeridas:

```bash
# Email
EMAIL_USER=arielsanroj@carmanfe.com.co
EMAIL_PASSWORD=tu-app-password-de-gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LLM (Ollama - pero en Render necesitarás usar OpenAI o similar)
# Si usas Ollama local, necesitarás cambiar a OpenAI para producción
OPENAI_API_KEY=tu-openai-key
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4
# O si tienes Ollama en otro servidor:
# OLLAMA_BASE_URL=https://tu-ollama-servidor.com
# OLLAMA_MODEL=llama3:latest

# Pinecone
PINECONE_API_KEY=pcsk_5F4Kxb_EpxvT1nERpkNoUPo5uNk7UiARTGpB6GRJ5TKSpApKpoYRguLGb89WHvnRupSVh
PINECONE_ENVIRONMENT=us-east-1

# Google Ads (opcional, solo si lanzas campañas reales)
GOOGLE_ADS_DEVELOPER_TOKEN=sbiVN_iPT4c8oDN6dzSQnA
GOOGLE_ADS_CLIENT_ID=YOUR_GOOGLE_ADS_CLIENT_ID
GOOGLE_ADS_CLIENT_SECRET=YOUR_GOOGLE_ADS_CLIENT_SECRET
GOOGLE_ADS_REFRESH_TOKEN=YOUR_GOOGLE_ADS_REFRESH_TOKEN
GOOGLE_ADS_LOGIN_CUSTOMER_ID=7700381649
USE_SIMULATORS=false
```

**⚠️ IMPORTANTE sobre Ollama:**
- Ollama corre en `localhost:11434` en tu computadora
- Render no puede acceder a tu localhost
- **Opciones:**
  1. **Usar OpenAI** (recomendado para producción)
  2. **Desplegar Ollama en otro servidor** y cambiar `OLLAMA_BASE_URL`
  3. **Usar un servicio de Ollama en la nube**

### Paso 6: Deploy

1. Click en **"Create Web Service"**
2. Render comenzará a construir (5-10 minutos)
3. Verás los logs en tiempo real
4. Cuando termine, copia la URL: `https://marketingagent-backend.onrender.com`

### Paso 7: Verificar que Funciona

1. Abre en el navegador: `https://tu-backend-url.onrender.com/health`
2. Deberías ver: `{"status": "healthy"}`

---

## 🔗 FASE 2: Conectar Vercel con Render

### Paso 1: Obtener URL del Backend

Copia la URL de Render (ej: `https://marketingagent-backend.onrender.com`)

### Paso 2: Editar Frontend

1. Abre: `frontend/templates/index.html`
2. Busca la línea **836**:
   ```javascript
   const BACKEND_URL = ''; // 👈 PON AQUÍ TU URL DE RENDER
   ```
3. Reemplaza con tu URL:
   ```javascript
   const BACKEND_URL = 'https://marketingagent-backend.onrender.com'; // 👈 TU URL
   ```

### Paso 3: Subir a Git

```bash
git add frontend/templates/index.html
git commit -m "Conectar frontend Vercel con backend Render"
git push origin main
```

### Paso 4: Esperar Re-deploy

1. Vercel detectará el cambio automáticamente
2. Espera 1-2 minutos
3. Verifica que el deploy terminó en Vercel

### Paso 5: Probar

1. Abre tu sitio en Vercel
2. Abre consola (F12)
3. Intenta hacer un análisis
4. Verifica en Network que las peticiones van a Render

---

## ⚠️ Problema: Ollama en Localhost

Si tu backend usa Ollama (`OLLAMA_BASE_URL=http://localhost:11434`), **NO funcionará en Render** porque Render no puede acceder a tu computadora.

### Soluciones:

#### Opción 1: Usar OpenAI (Recomendado)

1. Obtén una API key de OpenAI: [platform.openai.com](https://platform.openai.com)
2. En Render, agrega estas variables:
   ```bash
   OPENAI_API_KEY=sk-tu-key-aqui
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_MODEL_NAME=gpt-4
   ```
3. El código ya está preparado para usar OpenAI si `OPENAI_API_KEY` está configurado

#### Opción 2: Desplegar Ollama en Otro Servidor

1. Despliega Ollama en otro servicio (Render, Railway, etc.)
2. Cambia `OLLAMA_BASE_URL` a la URL pública de ese servidor

#### Opción 3: Usar Servicio de Ollama en la Nube

- Usa un servicio como [Ollama Cloud](https://ollama.com) o similar

---

## ✅ Checklist Final

- [ ] Backend desplegado en Render
- [ ] Health check responde: `/health`
- [ ] Variables de entorno configuradas
- [ ] Frontend actualizado con URL de Render
- [ ] Cambios subidos a Git
- [ ] Vercel re-desplegado
- [ ] Prueba de análisis funciona end-to-end

---

## 🎉 ¡Listo!

Ahora tienes:
- ✅ Frontend en Vercel (estático, rápido)
- ✅ Backend en Render (Python, siempre disponible)
- ✅ Todo conectado y funcionando

---

## 📝 Resumen Rápido

```
1. Render.com → New Web Service
2. Conecta GitHub repo
3. Configura variables de entorno
4. Deploy (espera 10 min)
5. Copia URL de Render
6. Pégala en frontend/templates/index.html línea 836
7. git push
8. ¡Listo! 🎉
```

---

## 🆘 Ayuda

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica que todas las variables de entorno están configuradas
3. Asegúrate de que CORS está habilitado (ya lo configuramos)
4. Verifica que el backend responde en `/health`

