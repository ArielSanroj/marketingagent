# 🎯 Pasos desde Vercel.com - Configurar Conexión con Backend

## 📍 Situación Actual

Estás en tu proyecto en Vercel. Vamos a configurar el frontend para que se conecte al backend.

**⚠️ IMPORTANTE:** Necesitas tener el backend corriendo ANTES. Tienes 2 opciones:

### Opción A: Backend con Túnel (Rápido para Probar)
- Tu backend local corriendo
- Un túnel (ngrok o cloudflared) activo
- URL del túnel copiada

### Opción B: Backend en Render (Producción)
- Backend desplegado en Render
- URL de Render copiada

---

## 🚀 PASO A PASO DESDE VERCEL

### Paso 1: Obtener URL del Backend

**Si usas Túnel (Opción A):**
1. Abre una terminal en tu PC
2. Ejecuta: `ngrok http 15000` (o `cloudflared tunnel --url http://localhost:15000`)
3. Copia la URL HTTPS que aparece (ej: `https://abc123.ngrok-free.app`)

**Si usas Render (Opción B):**
1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en tu servicio (backend)
3. Copia la URL que aparece arriba (ej: `https://marketingagent-backend.onrender.com`)

**Anota la URL aquí:** `___________________________`

---

### Paso 2: Editar el Código Localmente

**NO puedes editar directamente desde Vercel.** Necesitas editar el archivo en tu computadora y subirlo a Git.

1. Abre tu editor de código (VS Code, etc.)
2. Abre el archivo: `frontend/templates/index.html`
3. Busca la línea **836** que dice:
   ```javascript
   const BACKEND_URL = ''; // 👈 PON AQUÍ TU URL DE RENDER
   ```
4. Reemplaza las comillas vacías con tu URL:
   ```javascript
   const BACKEND_URL = 'https://tu-url-aqui.com'; // 👈 TU URL
   ```

**Ejemplo con ngrok:**
```javascript
const BACKEND_URL = 'https://abc123.ngrok-free.app';
```

**Ejemplo con Render:**
```javascript
const BACKEND_URL = 'https://marketingagent-backend.onrender.com';
```

5. **Guarda el archivo**

---

### Paso 3: Subir Cambios a Git

Abre una terminal y ejecuta:

```bash
cd /Users/arielsanroj/marketingagent
git add frontend/templates/index.html
git commit -m "Configurar URL del backend"
git push origin main
```

---

### Paso 4: Esperar Re-deploy en Vercel

1. **Vuelve a Vercel.com** (donde estás ahora)
2. Ve a la pestaña **"Deployments"** (o "Deploys")
3. Verás que Vercel detectó el cambio automáticamente
4. Aparecerá un nuevo deploy en progreso
5. Espera 1-2 minutos hasta que veas ✅ "Ready"

---

### Paso 5: Probar la Conexión

1. Haz clic en el botón **"Visit"** o abre tu URL de Vercel
2. Abre la consola del navegador:
   - **Chrome/Edge:** F12 → pestaña "Console"
   - **Safari:** Cmd+Option+I → Console
   - **Firefox:** F12 → Console
3. Escribe y presiona Enter:
   ```javascript
   console.log('Backend URL:', window.API_BASE || 'Configurado en código');
   ```
4. Deberías ver tu URL del backend
5. Intenta hacer un análisis de prueba
6. Ve a la pestaña **"Network"** y verifica que las peticiones van a tu backend

---

## 🔄 ALTERNATIVA: Configuración Temporal sin Git

Si quieres probar **SIN hacer commit** (solo para pruebas):

### Desde la Consola del Navegador en Vercel

1. Abre tu sitio en Vercel
2. Abre la consola (F12 → Console)
3. Pega y ejecuta:
   ```javascript
   localStorage.setItem('API_BASE', 'https://tu-url-backend.com');
   location.reload();
   ```

**⚠️ Esta configuración se pierde si el usuario limpia caché o usa modo incógnito.**

---

## ✅ Verificación Final

### 1. Verificar que el Backend Responde

Abre en tu navegador:
```
https://tu-url-backend.com/health
```

Deberías ver:
```json
{"status": "healthy"}
```

### 2. Verificar en el Frontend

1. Abre tu sitio en Vercel
2. F12 → Network
3. Haz un análisis
4. Deberías ver peticiones a tu backend

---

## 🆘 Problemas Comunes

**Error: "Failed to fetch"**
- Verifica que el backend está corriendo
- Si usas túnel, verifica que ngrok/cloudflared está activo
- Verifica que la URL es correcta (sin barra final `/`)

**No se actualiza en Vercel**
- Espera 2-3 minutos después del push
- Haz hard refresh: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)
- Verifica que el deploy terminó en Vercel

**CORS Error**
- Ya está configurado en el backend
- Si persiste, verifica que CORS está habilitado en `frontend/app.py`

---

## 📝 Resumen Visual

```
1. Obtener URL del backend (túnel o Render)
   ↓
2. Editar frontend/templates/index.html línea 836
   const BACKEND_URL = 'https://tu-url.com';
   ↓
3. git add, commit, push
   ↓
4. Esperar en Vercel (1-2 min)
   ↓
5. Probar en tu sitio
   ↓
✅ ¡Listo!
```

---

¿Ya tienes el backend corriendo (túnel o Render)? Si no, te guío para configurarlo primero.

