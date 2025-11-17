# 🔗 Guía Paso a Paso: Conectar Frontend Vercel con Backend Render

Esta guía te mostrará exactamente cómo conectar tu frontend desplegado en Vercel con tu backend desplegado en Render.

---

## 📋 Prerrequisitos

Antes de empezar, asegúrate de tener:
- ✅ Frontend desplegado en Vercel (ya lo tienes)
- ✅ Backend desplegado en Render (o la URL donde estará)
- ✅ URL del backend de Render (ej: `https://marketingagent-backend.onrender.com`)

---

## 🎯 Opción 1: Configuración Permanente (Recomendada)

Esta opción configura la URL del backend directamente en el código, así siempre funcionará sin depender de localStorage.

### Paso 1: Obtener la URL de tu Backend en Render

1. Ve a [dashboard.render.com](https://dashboard.render.com)
2. Haz clic en tu servicio web (backend)
3. Copia la URL que aparece en la parte superior (ej: `https://marketingagent-backend.onrender.com`)
4. **Importante**: No incluyas la barra final `/`

### Paso 2: Editar el Frontend Localmente

1. Abre el archivo `frontend/templates/index.html` en tu editor
2. Busca la línea que dice:
   ```javascript
   const API_BASE = (window.API_BASE || localStorage.getItem('API_BASE') || '').replace(/\/$/, '');
   ```
   (Está alrededor de la línea 831)

3. **Reemplázala** con:
   ```javascript
   // Configuración del backend
   window.API_BASE = 'https://tu-backend-url.onrender.com'; // 👈 REEMPLAZA CON TU URL
   const API_BASE = (window.API_BASE || localStorage.getItem('API_BASE') || '').replace(/\/$/, '');
   ```

   **Ejemplo real:**
   ```javascript
   // Configuración del backend
   window.API_BASE = 'https://marketingagent-backend.onrender.com';
   const API_BASE = (window.API_BASE || localStorage.getItem('API_BASE') || '').replace(/\/$/, '');
   ```

### Paso 3: Guardar y Hacer Commit

```bash
git add frontend/templates/index.html
git commit -m "Configurar API_BASE para conectar con backend de Render"
git push origin main
```

### Paso 4: Esperar el Re-deploy en Vercel

1. Vercel detectará automáticamente el cambio en `main`
2. Espera 1-2 minutos mientras Vercel re-despliega
3. Ve a tu proyecto en Vercel y verifica que el deploy se completó

### Paso 5: Probar la Conexión

1. Abre tu sitio en Vercel (ej: `https://tu-proyecto.vercel.app`)
2. Abre la consola del navegador (F12 → Console)
3. Escribe:
   ```javascript
   console.log(window.API_BASE);
   ```
4. Deberías ver tu URL del backend
5. Intenta hacer un análisis de prueba
6. Verifica en la pestaña "Network" que las peticiones van a tu backend de Render

---

## 🎯 Opción 2: Usar Variable de Entorno en Vercel

Esta opción es más flexible y permite cambiar la URL sin modificar código.

### Paso 1: Obtener la URL del Backend

Igual que en la Opción 1, copia la URL de tu backend en Render.

### Paso 2: Agregar Variable de Entorno en Vercel

1. Ve a tu proyecto en [vercel.com](https://vercel.com)
2. Haz clic en **Settings**
3. En el menú lateral, haz clic en **Environment Variables**
4. Haz clic en **Add New**
5. Completa:
   - **Key**: `API_BASE`
   - **Value**: `https://tu-backend-url.onrender.com` (tu URL de Render)
   - **Environment**: Selecciona **Production**, **Preview**, y **Development**
6. Haz clic en **Save**

### Paso 3: Modificar el Código para Usar la Variable

Edita `frontend/templates/index.html` y busca la línea 831. Reemplázala con:

```javascript
// Configuración del backend desde variable de entorno de Vercel
// Vercel inyecta las variables como window.API_BASE en el build
const API_BASE = (window.API_BASE || localStorage.getItem('API_BASE') || '').replace(/\/$/, '');
```

**Nota**: Vercel no inyecta automáticamente las variables en archivos estáticos HTML. Necesitarás usar un script de build o inyectar la variable manualmente.

### Alternativa: Usar un Script de Build

Crea un archivo `vercel.json` en la raíz del proyecto:

```json
{
  "buildCommand": "node scripts/inject-env.js",
  "outputDirectory": "frontend/templates"
}
```

Y crea `scripts/inject-env.js`:

```javascript
const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, '../frontend/templates/index.html');
let html = fs.readFileSync(htmlPath, 'utf8');

// Inyectar API_BASE desde variable de entorno
const apiBase = process.env.API_BASE || '';
html = html.replace(
  /const API_BASE = .*?;/,
  `const API_BASE = '${apiBase}'.replace(/\\/$/, '');`
);

fs.writeFileSync(htmlPath, html);
console.log('✅ API_BASE inyectado:', apiBase);
```

**⚠️ Esta opción es más compleja. Recomiendo la Opción 1 para simplicidad.**

---

## 🎯 Opción 3: Configuración Temporal (Solo para Pruebas)

Si solo quieres probar rápidamente sin hacer cambios en el código:

### Paso 1: Obtener la URL del Backend

Copia la URL de tu backend en Render.

### Paso 2: Configurar en el Navegador

1. Abre tu sitio en Vercel
2. Abre la consola del navegador (F12 → Console)
3. Ejecuta:
   ```javascript
   localStorage.setItem('API_BASE', 'https://tu-backend-url.onrender.com');
   location.reload();
   ```

### Paso 3: Verificar

Después de recargar, verifica:
```javascript
console.log(localStorage.getItem('API_BASE'));
```

**⚠️ Esta configuración se pierde si el usuario limpia su caché o usa modo incógnito.**

---

## ✅ Verificación Final

### 1. Verificar que el Backend Responde

Abre en tu navegador:
```
https://tu-backend-url.onrender.com/health
```

Deberías ver:
```json
{"status": "healthy"}
```

### 2. Verificar en el Frontend

1. Abre tu sitio en Vercel
2. Abre la consola del navegador (F12)
3. Ve a la pestaña **Network**
4. Intenta hacer un análisis
5. Deberías ver peticiones a `https://tu-backend-url.onrender.com/analyze`

### 3. Verificar Logs

1. Ve a Render Dashboard
2. Haz clic en tu servicio
3. Ve a la pestaña **Logs**
4. Deberías ver las peticiones entrantes cuando uses el frontend

---

## 🔧 Troubleshooting

### Error: "Failed to fetch" o CORS

**Problema**: El backend no permite peticiones desde tu dominio de Vercel.

**Solución**: 
1. Verifica que `flask-cors` está instalado en el backend
2. En `frontend/app.py`, verifica que CORS está configurado:
   ```python
   CORS(app, resources={
       r"/*": {
           "origins": ["*"],  # O tu dominio específico de Vercel
           "methods": ["GET", "POST", "OPTIONS"],
           "allow_headers": ["Content-Type", "Authorization"]
       }
   })
   ```
3. Reinicia el servicio en Render

### Error: "Network Error" o Timeout

**Problema**: El backend está "dormido" (plan Free de Render).

**Solución**: 
- La primera petición puede tardar 30-60 segundos
- Considera actualizar al plan Starter ($7/mes) para evitar el sleep mode

### Error: "404 Not Found"

**Problema**: La URL del backend es incorrecta o falta la ruta.

**Solución**:
1. Verifica que la URL no tiene barra final: `https://backend.onrender.com` (no `https://backend.onrender.com/`)
2. Verifica que las rutas en el frontend coinciden con las del backend:
   - `/analyze`
   - `/status/{request_id}`
   - `/start-campaign`
   - `/send-report`

### La URL no se actualiza en Vercel

**Problema**: Los cambios no se reflejan después del deploy.

**Solución**:
1. Verifica que hiciste commit y push a `main`
2. Espera 2-3 minutos para que Vercel complete el deploy
3. Haz un "hard refresh" en el navegador (Ctrl+Shift+R o Cmd+Shift+R)
4. Limpia la caché del navegador si es necesario

---

## 📝 Resumen Rápido

**Método Recomendado (Opción 1):**

1. Copia la URL de tu backend en Render
2. Edita `frontend/templates/index.html` línea ~831
3. Agrega: `window.API_BASE = 'https://tu-backend-url.onrender.com';`
4. Guarda, commit, push
5. Espera el re-deploy en Vercel
6. ¡Listo!

---

## 🎉 ¡Listo!

Una vez configurado, tu frontend en Vercel se comunicará automáticamente con tu backend en Render. Todas las peticiones de análisis, campañas y reportes irán a tu backend desplegado.

**Próximos pasos:**
- Prueba hacer un análisis completo
- Verifica que los emails se envían correctamente
- Monitorea los logs en Render para detectar errores

