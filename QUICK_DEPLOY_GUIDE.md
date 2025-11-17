# ⚡ Guía Rápida: Desplegar Backend en Render

## 🎯 Resumen

Esta es una guía rápida. Para detalles completos, ve a [docs/DEPLOY_BACKEND_RENDER.md](docs/DEPLOY_BACKEND_RENDER.md)

---

## 📝 Checklist Pre-Deploy

- [x] ✅ `Procfile` creado
- [x] ✅ CORS configurado en `frontend/app.py`
- [x] ✅ Puerto dinámico configurado (usa `PORT` de Render)
- [x] ✅ `flask-cors` en `requirements.txt`
- [x] ✅ `.env` en `.gitignore`

---

## 🚀 Pasos Rápidos

### 1. Ir a Render.com
- Crea cuenta o inicia sesión
- Click en **"New +"** → **"Web Service"**

### 2. Conectar Repositorio
- Conecta tu repo de GitHub
- Selecciona `marketingagent`
- Branch: `main`

### 3. Configurar Servicio

**Settings básicos:**
- Name: `marketingagent-backend`
- Region: Elige la más cercana
- Runtime: `Python 3`

**Build & Deploy:**
- Build Command: `pip install -r requirements.txt`
- Start Command: (deja vacío, usa Procfile)

**Plan:** Free (para empezar)

### 4. Variables de Entorno

Agrega estas variables en **Environment**:

```bash
# Email (requerido)
EMAIL_USER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# LLM (requerido)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3:latest

# Pinecone (opcional)
PINECONE_API_KEY=tu-key
PINECONE_ENVIRONMENT=us-east-1

# Google Ads (opcional, solo si lanzas campañas reales)
GOOGLE_ADS_DEVELOPER_TOKEN=...
GOOGLE_ADS_CLIENT_ID=...
GOOGLE_ADS_CLIENT_SECRET=...
GOOGLE_ADS_REFRESH_TOKEN=...
GOOGLE_ADS_LOGIN_CUSTOMER_ID=...
```

### 5. Deploy
- Click **"Create Web Service"**
- Espera 5-10 minutos
- Copia la URL: `https://tu-backend.onrender.com`

### 6. Conectar con Vercel

**Opción A (Recomendada):**
Edita `frontend/templates/index.html` y agrega al inicio del `<script>`:
```javascript
window.API_BASE = 'https://tu-backend.onrender.com';
```

**Opción B (Temporal):**
En la consola del navegador en Vercel:
```javascript
localStorage.setItem('API_BASE', 'https://tu-backend.onrender.com');
location.reload();
```

### 7. Probar
- Abre tu frontend en Vercel
- Haz un análisis de prueba
- Verifica logs en Render

---

## 🔗 URLs Importantes

- **Render Dashboard**: https://dashboard.render.com
- **Tu Backend**: `https://tu-backend.onrender.com`
- **Health Check**: `https://tu-backend.onrender.com/health`

---

## ⚠️ Notas Importantes

1. **Plan Free**: Se "duerme" después de 15 min de inactividad. Primera petición puede tardar 30-60 seg.
2. **Gmail App Password**: No uses tu contraseña normal, crea una "App Password" en Google Account
3. **CORS**: Ya está configurado para permitir cualquier origen. En producción, restringe a tu dominio de Vercel.

---

## 🆘 Problemas Comunes

**Error: Module not found**
→ Verifica `requirements.txt` tiene todas las dependencias

**Error: CORS**
→ Ya está configurado, pero verifica que `flask-cors` está instalado

**El servicio se duerme**
→ Es normal en plan Free. Considera actualizar a Starter ($7/mes)

**Email no se envía**
→ Verifica que `EMAIL_USER` y `EMAIL_PASSWORD` son correctos (usa App Password para Gmail)

---

## ✅ Listo!

Una vez desplegado, tu backend estará disponible 24/7 (o con sleep mode en plan Free) y tu frontend en Vercel podrá conectarse a él.

**Siguiente paso:** Actualiza `API_BASE` en tu frontend de Vercel con la URL de tu backend en Render.

