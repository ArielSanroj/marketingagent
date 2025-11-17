# 🔗 Pasos para Conectar Vercel con Render

## ⚡ Método Rápido (5 minutos)

### Paso 1: Obtener URL del Backend en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en tu servicio (backend)
3. **Copia la URL** que aparece arriba (ej: `https://marketingagent-backend.onrender.com`)
   - ⚠️ **No incluyas la barra final** `/`

### Paso 2: Editar el Código

1. Abre el archivo: `frontend/templates/index.html`
2. Busca la línea que dice: `const BACKEND_URL = '';` (línea ~833)
3. **Reemplaza** las comillas vacías con tu URL:

```javascript
const BACKEND_URL = 'https://marketingagent-backend.onrender.com'; // 👈 TU URL AQUÍ
```

**Ejemplo completo:**
```javascript
// ============================================
// 🔗 CONFIGURACIÓN DEL BACKEND
// ============================================
const BACKEND_URL = 'https://marketingagent-backend.onrender.com'; // 👈 TU URL
const API_BASE = (BACKEND_URL || window.API_BASE || localStorage.getItem('API_BASE') || '').replace(/\/$/, '');
```

### Paso 3: Guardar y Subir a Git

```bash
# Guarda el archivo, luego ejecuta:
git add frontend/templates/index.html
git commit -m "Configurar URL del backend de Render"
git push origin main
```

### Paso 4: Esperar Re-deploy en Vercel

1. Vercel detectará automáticamente el cambio
2. Espera 1-2 minutos
3. Ve a tu proyecto en Vercel y verifica que el deploy terminó

### Paso 5: Probar

1. Abre tu sitio en Vercel
2. Abre la consola del navegador (F12)
3. Escribe: `console.log(window.API_BASE || 'No configurado')`
4. Deberías ver tu URL del backend
5. Intenta hacer un análisis de prueba

---

## ✅ Verificación

### 1. Backend responde:
Abre en el navegador: `https://tu-backend.onrender.com/health`
Deberías ver: `{"status": "healthy"}`

### 2. Frontend conecta:
- Abre tu sitio en Vercel
- F12 → Network
- Haz un análisis
- Deberías ver peticiones a tu backend de Render

---

## 🆘 Problemas Comunes

**Error: "Failed to fetch"**
→ Verifica que CORS está habilitado en el backend (ya lo configuramos)

**Error: Timeout**
→ El backend puede estar "dormido" (plan Free). Espera 30-60 segundos en la primera petición.

**No se actualiza**
→ Haz hard refresh: Ctrl+Shift+R (Windows) o Cmd+Shift+R (Mac)

---

## 📝 Resumen

1. Copia URL de Render
2. Pégala en `frontend/templates/index.html` línea ~833
3. `git add`, `git commit`, `git push`
4. Espera 2 minutos
5. ¡Listo! 🎉

