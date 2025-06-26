# 🚂 Guía de Despliegue en Railway

## Pasos para subir tu aplicación a Railway:

### 1. Preparar tu código
✅ Ya tienes los archivos necesarios:
- `requirements.txt` - Dependencias de Python
- `Procfile` - Comando de inicio para Railway
- `runtime.txt` - Versión de Python
- `.railway.json` - Configuración específica de Railway
- `config.py` - Configuración optimizada para Railway

### 2. Crear cuenta en Railway
1. Ve a https://railway.app
2. Haz clic en "Login" o "Start a New Project"
3. Conéctate con tu cuenta de GitHub

### 3. Subir tu código a GitHub
```bash
# Si no tienes Git inicializado
git init

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Preparar aplicación para Railway"

# Crear repositorio en GitHub y conectarlo
git remote add origin https://github.com/tu-usuario/rutas-app.git
git branch -M main
git push -u origin main
```

### 4. Desplegar en Railway
1. En Railway, haz clic en "New Project"
2. Selecciona "Deploy from GitHub repo"
3. Autoriza Railway para acceder a tus repositorios
4. Selecciona el repositorio de tu aplicación
5. Railway detectará automáticamente que es una aplicación Python
6. Haz clic en "Deploy"

### 5. Configurar variables de entorno (opcional)
En el dashboard de Railway:
1. Ve a tu proyecto
2. Haz clic en "Variables"
3. Puedes agregar:
   - `SECRET_KEY`: Una clave secreta segura
   - `GOOGLE_MAPS_API_KEY`: Si usas Google Maps
   - `MAPBOX_ACCESS_TOKEN`: Si usas Mapbox

### 6. Acceder a tu aplicación
- Railway te proporcionará una URL automáticamente
- Por ejemplo: `https://tu-app.railway.app`

## Credenciales por defecto:
- **Usuario admin**: `admin` / `admin123`
- **Usuario supervisor**: `supervisor` / `supervisor123`

## Características de la configuración:

### ✅ Optimizado para Railway
- Puerto dinámico automático
- Configuración de host `0.0.0.0`
- Detección automática del entorno Railway
- Headers de seguridad corporativos

### ✅ Base de datos SQLite
- Se crea automáticamente en el primer inicio
- Incluye datos de ejemplo y usuarios por defecto
- Compatible con Railway

### ✅ Manejo de archivos
- Carpeta `uploads` para archivos subidos
- Compatible con el sistema de archivos de Railway

## Troubleshooting:

### Si la aplicación no inicia:
1. Revisa los logs en Railway dashboard
2. Verifica que todas las dependencias estén en `requirements.txt`
3. Asegúrate de que el archivo `app.py` esté en la raíz del proyecto

### Si hay problemas de puerto:
- La configuración ya maneja automáticamente el puerto de Railway
- Los logs mostrarán qué puerto se está usando

### Si la base de datos no funciona:
- Railway reinicia el sistema de archivos en cada deploy
- Los datos se perderán entre deployments
- Para persistencia, considera usar Railway PostgreSQL

## Próximos pasos después del deploy:
1. Cambiar las credenciales por defecto
2. Configurar un dominio personalizado (opcional)
3. Configurar base de datos PostgreSQL para persistencia (opcional)
4. Configurar monitoreo y alertas

¡Tu aplicación estará lista en Railway! 🎉
