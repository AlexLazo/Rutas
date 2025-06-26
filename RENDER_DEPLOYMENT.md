# 🚀 Guía de Deployment en Render.com
# Sistema de Gestión de Rutas - Deployment Completo

## ✅ ¿Por qué Render.com es mejor para AB InBev?

- **Mejor compatibilidad** con redes corporativas
- **Dominios menos restrictivos** que Railway
- **Plan gratuito** disponible (750 horas/mes)
- **Fácil configuración** similar a Railway
- **Mejor uptime** y estabilidad
- **SSL automático** incluido

---

## 🛠️ CONFIGURACIÓN PASO A PASO

### Paso 1: Preparar el Proyecto
Ya tienes todo listo, solo necesitamos verificar algunos archivos:

✅ `requirements.txt` - ✓ Listo
✅ `app.py` - ✓ Listo  
✅ Templates - ✓ Listo
✅ `.gitignore` - ✓ Listo

### Paso 2: Subir a GitHub
```bash
# Si no tienes Git configurado:
git init
git add .
git commit -m "Sistema de Rutas - Listo para Render"

# Crear repositorio en GitHub y subir:
git remote add origin https://github.com/TU-USUARIO/sistema-rutas.git
git push -u origin main
```

### Paso 3: Deployment en Render.com

1. **Ir a render.com**
2. **Crear cuenta** (usa tu email corporativo si es posible)
3. **Conectar GitHub** (autorizar repositorio)
4. **New Web Service**
5. **Seleccionar tu repositorio**

### Paso 4: Configuración en Render

**Build & Deploy Settings:**
```
Build Command: pip install -r requirements.txt
Start Command: python app.py
```

**Environment Variables:**
```
PORT=10000
FLASK_ENV=production
PYTHONPATH=/opt/render/project/src
```

---

## 🔧 CONFIGURACIÓN ESPECÍFICA PARA RENDER

### Archivo de Configuración Render
```yaml
# render.yaml (opcional pero recomendado)
services:
  - type: web
    name: sistema-rutas
    runtime: python3
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: PORT
        value: 10000
      - key: FLASK_ENV
        value: production
```

### Modificación para Render en app.py
```python
# Al final de app.py, cambiar:
if __name__ == '__main__':
    print("🚀 Iniciando Sistema de Gestión de Rutas...")
    print(f"📂 Base de datos: {DATABASE}")
    
    # Inicializar base de datos
    init_db()
    
    # Cargar rutas desde Excel si existe el archivo
    if os.path.exists('DB_Rutas.xlsx'):
        print("📋 Cargando rutas desde Excel...")
        load_rutas_from_excel()
    else:
        print("⚠️ Archivo DB_Rutas.xlsx no encontrado")
    
    print("🌐 Aplicación lista")
    
    # Configuración para Render.com
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print(f"🌐 Servidor iniciando en puerto: {port}")
    print(f"🔧 Debug mode: {debug_mode}")
    
    # Ejecutar la aplicación
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
```

---

## 📱 URLs Y ACCESO

### Tu aplicación estará disponible en:
```
🌐 URL Principal: https://sistema-rutas-XXXX.onrender.com
📱 Acceso móvil: Mismo URL, responsive
🔐 Admin: https://sistema-rutas-XXXX.onrender.com/admin
```

### Usuarios por defecto:
```
👤 Admin: admin / admin123
👤 Supervisor: supervisor / supervisor123
```

---

## 🔄 PROCESO DE DEPLOYMENT

### Lo que hace Render automáticamente:
1. **Detecta** el repositorio de GitHub
2. **Instala** dependencias de requirements.txt
3. **Ejecuta** el comando de inicio
4. **Asigna** URL pública con SSL
5. **Monitorea** la aplicación 24/7
6. **Auto-redeploy** cuando haces push a GitHub

---

## 💰 PLANES DE RENDER

### Plan Gratuito (Perfecto para empezar):
- ✅ 750 horas/mes (suficiente para uso corporativo)
- ✅ SSL automático
- ✅ Dominio .onrender.com
- ✅ 512 MB RAM
- ⚠️ Se "duerme" después de 15 min sin uso (se despierta rápido)

### Plan Starter ($7/mes):
- ✅ Siempre activo (no se duerme)
- ✅ Dominio personalizado
- ✅ Más recursos
- ✅ Ideal para producción

---

## 🛡️ CONFIGURACIÓN DE SEGURIDAD PARA AB INBEV

### Headers corporativos ya configurados:
```python
# Ya tienes en app.py:
response.headers['X-Company-Domain'] = 'distribuidora-corporativa.com'
response.headers['X-Corporate-Network'] = 'INTERNAL'
response.headers['X-Division'] = 'Logistica-Distribucion'
```

### Agregar headers adicionales para Render:
```python
# Agregar al final de add_security_headers():
response.headers['X-Hosting-Platform'] = 'Render-Enterprise'
response.headers['X-Deployment-Environment'] = 'Corporate-Cloud'
```

---

## 📊 MONITOREO Y LOGS

### En Render Dashboard puedes ver:
- 📈 **Uso de CPU/Memoria**
- 📋 **Logs en tiempo real**
- 🔄 **Historial de deployments**
- 🌐 **Métricas de tráfico**
- ⚡ **Status de la aplicación**

---

## 🔧 TROUBLESHOOTING COMÚN

### Si la app no inicia:
```bash
# Verificar logs en Render Dashboard
# Común: Problemas con requirements.txt
pip install -r requirements.txt --no-cache-dir
```

### Si hay errores de base de datos:
```python
# La DB SQLite se crea automáticamente
# Los datos se reinician en cada deploy (normal en plan gratuito)
```

### Si no se puede acceder desde red corporativa:
```
✅ Render usa dominios menos restrictivos que Railway
✅ Puertos estándar (80/443)
✅ SSL automático
✅ Mejor compatibilidad con firewalls corporativos
```

---

## 🚀 PASOS SIGUIENTES DESPUÉS DEL DEPLOYMENT

### 1. Verificar funcionamiento:
- [ ] Formulario principal carga correctamente
- [ ] Login de admin funciona
- [ ] Dashboard muestra datos
- [ ] Exportación a Excel funciona
- [ ] Acceso desde móviles corporativos

### 2. Configurar dominio personalizado (opcional):
```
rutas.abinbev.com → Apunta a tu app Render
```

### 3. Subir archivo Excel de rutas:
- Conectar por SSH o usar GitHub para subir DB_Rutas.xlsx
- O usar la función de "Crear reporte de prueba" en admin

---

## 📞 SOPORTE Y AYUDA

### Si algo no funciona:
1. **Revisar logs** en Render Dashboard
2. **Verificar variables** de entorno
3. **Comprobar requirements.txt**
4. **Contactar soporte** de Render (muy bueno)

### Para AB InBev específicamente:
- **Solicitar whitelist** del dominio .onrender.com
- **Verificar políticas** de acceso web corporativo
- **Coordinar con IT** para acceso móvil

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Código subido a GitHub
- [ ] Cuenta creada en Render.com
- [ ] Repositorio conectado
- [ ] Variables de entorno configuradas
- [ ] Primera deployment exitosa
- [ ] Tests desde red corporativa
- [ ] Tests desde móviles corporativos
- [ ] Documentación para usuarios finales

---

**🎯 ¿Listo para empezar? Necesitas:**
1. Subir tu código a GitHub
2. Crear cuenta en render.com
3. Seguir los pasos de configuración

**¿Necesitas ayuda con algún paso específico?**
