# 🔗 Opciones para Conectar Backend con Vercel

Tienes **2 opciones** dependiendo de si quieres probar rápido o tener una solución permanente.

---

## 🚀 Opción 1: Túnel Temporal (Para Pruebas Rápidas)

**Cuándo usar:** Para probar que todo funciona antes de desplegar en Render.

**Ventajas:**
- ✅ Rápido (5 minutos)
- ✅ No necesitas desplegar nada
- ✅ Pruebas inmediatas

**Desventajas:**
- ❌ Tu PC debe estar encendido
- ❌ La URL cambia cada vez que reinicias el túnel
- ❌ No es para producción
- ❌ Puede ser lento

---

### Paso a Paso con ngrok

#### 1. Instalar ngrok

**Mac:**
```bash
brew install ngrok
```

**Windows/Linux:**
- Descarga de [ngrok.com](https://ngrok.com/download)
- O usa: `choco install ngrok` (Windows) / `snap install ngrok` (Linux)

#### 2. Iniciar tu Backend Local

En una terminal:
```bash
cd /Users/arielsanroj/marketingagent
PYTHONPATH=/Users/arielsanroj/marketingagent python3 frontend/app.py
```

Deberías ver:
```
🚀 Starting tphagent Frontend Server...
🌐 Server: http://127.0.0.1:15000
```

#### 3. Crear Túnel Público

En **otra terminal** (deja la anterior corriendo):
```bash
ngrok http 15000
```

Verás algo como:
```
Forwarding  https://abc123.ngrok-free.app -> http://localhost:15000
```

**Copia la URL HTTPS** (ej: `https://abc123.ngrok-free.app`)

#### 4. Configurar en Vercel

1. Abre tu sitio en Vercel (ej: `https://tu-proyecto.vercel.app`)
2. Abre la consola del navegador (F12 → Console)
3. Pega y ejecuta:
```javascript
localStorage.setItem('API_BASE', 'https://abc123.ngrok-free.app');
location.reload();
```

**⚠️ IMPORTANTE:** Reemplaza `abc123.ngrok-free.app` con tu URL real de ngrok.

#### 5. Probar

- Intenta hacer un análisis
- Verifica en Network que las peticiones van a tu túnel de ngrok

**⚠️ Nota:** Cada vez que reinicies ngrok, obtendrás una URL nueva y tendrás que actualizar `localStorage` de nuevo.

---

### Paso a Paso con cloudflared (Alternativa)

#### 1. Instalar cloudflared

**Mac:**
```bash
brew install cloudflared
```

**O descarga de:** [developers.cloudflare.com](https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation)

#### 2. Iniciar tu Backend Local

Igual que con ngrok:
```bash
cd /Users/arielsanroj/marketingagent
PYTHONPATH=/Users/arielsanroj/marketingagent python3 frontend/app.py
```

#### 3. Crear Túnel

En otra terminal:
```bash
cloudflared tunnel --url http://localhost:15000
```

Verás:
```
+--------------------------------------------------------------------------------------------+
|  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):
|  https://random-words-1234.trycloudflare.com
+--------------------------------------------------------------------------------------------+
```

**Copia la URL HTTPS**

#### 4. Configurar en Vercel

Igual que con ngrok:
```javascript
localStorage.setItem('API_BASE', 'https://random-words-1234.trycloudflare.com');
location.reload();
```

---

## 🏭 Opción 2: Desplegar en Render (Para Producción)

**Cuándo usar:** Para tener tu aplicación funcionando 24/7 sin depender de tu PC.

**Ventajas:**
- ✅ Funciona 24/7 (o casi, si usas plan Free)
- ✅ URL permanente
- ✅ No necesitas tener tu PC encendido
- ✅ Mejor para usuarios reales

**Desventajas:**
- ⏱️ Toma 15-20 minutos configurar
- 💰 Plan Free se "duerme" después de 15 min (Starter $7/mes siempre activo)

---

### Paso a Paso con Render

#### 1. Ve a Render.com

1. Crea cuenta o inicia sesión: [render.com](https://render.com)
2. Click en **"New +"** → **"Web Service"**

#### 2. Conectar Repositorio

1. Conecta tu repositorio de GitHub
2. Selecciona `marketingagent`
3. Branch: `main`

#### 3. Configurar Servicio

**Basic Settings:**
- Name: `marketingagent-backend`
- Region: Elige la más cercana
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command: `pip install -r requirements.txt`
- Start Command: (déjalo vacío, usa Procfile)

**Plan:** Free (para empezar)

#### 4. Variables de Entorno

Agrega en **Environment**:

```bash
EMAIL_USER=arielsanroj@carmanfe.com.co
EMAIL_PASSWORD=tu-app-password-gmail
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# IMPORTANTE: Ollama no funciona en Render (está en localhost)
# Usa OpenAI o despliega Ollama en otro servidor
OPENAI_API_KEY=sk-tu-key-aqui
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL_NAME=gpt-4

PINECONE_API_KEY=pcsk_5F4Kxb_EpxvT1nERpkNoUPo5uNk7UiARTGpB6GRJ5TKSpApKpoYRguLGb89WHvnRupSVh
PINECONE_ENVIRONMENT=us-east-1

GOOGLE_ADS_DEVELOPER_TOKEN=sbiVN_iPT4c8oDN6dzSQnA
GOOGLE_ADS_CLIENT_ID=YOUR_GOOGLE_ADS_CLIENT_ID
GOOGLE_ADS_CLIENT_SECRET=YOUR_GOOGLE_ADS_CLIENT_SECRET
GOOGLE_ADS_REFRESH_TOKEN=YOUR_GOOGLE_ADS_REFRESH_TOKEN
GOOGLE_ADS_LOGIN_CUSTOMER_ID=7700381649
```

#### 5. Deploy

1. Click **"Create Web Service"**
2. Espera 5-10 minutos
3. Copia la URL: `https://marketingagent-backend.onrender.com`

#### 6. Conectar con Vercel

Edita `frontend/templates/index.html` línea **836**:

```javascript
const BACKEND_URL = 'https://marketingagent-backend.onrender.com'; // 👈 TU URL
```

Luego:
```bash
git add frontend/templates/index.html
git commit -m "Conectar con backend de Render"
git push origin main
```

Espera 2 minutos y ¡listo!

---

## 🤔 ¿Cuál Opción Elegir?

### Usa Túnel (Opción 1) si:
- ✅ Solo quieres probar rápido
- ✅ Estás desarrollando y probando cambios
- ✅ No necesitas que funcione 24/7
- ✅ Tu PC puede estar encendida

### Usa Render (Opción 2) si:
- ✅ Quieres que funcione para usuarios reales
- ✅ No quieres depender de tu PC
- ✅ Necesitas una solución permanente
- ✅ Quieres una URL estable

---

## ⚠️ Problema Común: Ollama en Localhost

**Tu backend usa Ollama** (`OLLAMA_BASE_URL=http://localhost:11434`), que está en tu PC.

**Esto NO funcionará en Render** porque Render no puede acceder a tu localhost.

### Soluciones:

#### Solución 1: Usar OpenAI (Recomendado para Render)

1. Obtén API key: [platform.openai.com](https://platform.openai.com)
2. En Render, agrega:
   ```bash
   OPENAI_API_KEY=sk-tu-key
   OPENAI_API_BASE=https://api.openai.com/v1
   OPENAI_MODEL_NAME=gpt-4
   ```
3. El código ya detecta automáticamente si usar OpenAI u Ollama

#### Solución 2: Desplegar Ollama en Otro Servidor

1. Despliega Ollama en Render/Railway/Fly.io
2. Cambia `OLLAMA_BASE_URL` a la URL pública de ese servidor

#### Solución 3: Usar Túnel para Ollama también

1. Crea un túnel para Ollama: `ngrok http 11434`
2. Usa esa URL en `OLLAMA_BASE_URL`

---

## 📝 Resumen Rápido

**Opción Rápida (Túnel):**
```bash
# Terminal 1: Backend
python3 frontend/app.py

# Terminal 2: Túnel
ngrok http 15000

# En Vercel (consola):
localStorage.setItem('API_BASE', 'https://tu-url-ngrok');
location.reload();
```

**Opción Producción (Render):**
1. Render.com → New Web Service
2. Configura variables
3. Deploy (10 min)
4. Pega URL en `index.html` línea 836
5. `git push`

---

## ✅ Checklist

**Para Túnel:**
- [ ] Backend corriendo en localhost:15000
- [ ] Túnel activo (ngrok o cloudflared)
- [ ] URL copiada
- [ ] `localStorage` configurado en Vercel
- [ ] Prueba funcionando

**Para Render:**
- [ ] Backend desplegado en Render
- [ ] Health check funciona: `/health`
- [ ] Variables de entorno configuradas
- [ ] URL pegada en `index.html`
- [ ] Cambios en Git
- [ ] Vercel re-desplegado
- [ ] Prueba funcionando

---

¿Cuál opción prefieres usar? Te guío paso a paso con la que elijas.

