# 🚚 Sistema de Gestión de Rutas

Sistema web para la gestión y seguimiento de rutas de distribución, desarrollado con Flask.

## 📋 Características

- ✅ **Dashboard administrativo** con paginación y filtros
- ✅ **Reportes de rutas** en tiempo real
- ✅ **Gestión de usuarios** con roles (admin/supervisor)
- ✅ **Exportación a Excel** de reportes
- ✅ **Carga masiva** desde archivos Excel
- ✅ **Interface responsive** con Bootstrap
- ✅ **Base de datos SQLite** integrada
- ✅ **Sistema de autenticación** seguro

## 🚀 Instalación Rápida

### Opción 1: Script Automático (Recomendado)
```powershell
# En PowerShell como administrador:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\deploy.ps1
```

### Opción 2: Instalación Manual
```bash
# 1. Instalar dependencias
pip install Flask==2.3.3 Flask-Login==0.6.2 Werkzeug==2.3.7 pandas==2.0.3 openpyxl==3.1.2

# 2. Iniciar el servidor
python app.py
```

## 📁 Estructura del Proyecto

```
Rutas/
├── app.py                 # Aplicación principal Flask
├── sistema_rutas.db       # Base de datos SQLite (se crea automáticamente)
├── DB_Rutas.xlsx         # Archivo Excel con rutas (opcional)
├── templates/
│   ├── base.html         # Template base
│   ├── index.html        # Página principal (formulario)
│   ├── admin.html        # Panel administrativo
│   └── login.html        # Página de login
├── deploy.ps1            # Script de deployment automático
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## 👤 Usuarios por Defecto

| Usuario     | Contraseña    | Rol          |
|-------------|---------------|--------------|
| admin       | admin123      | super_admin  |
| supervisor  | supervisor123 | supervisor   |

## 🌐 URLs del Sistema

- **Formulario público**: `http://127.0.0.1:5000/`
- **Panel admin**: `http://127.0.0.1:5000/admin`
- **Login**: `http://127.0.0.1:5000/login`

## 📊 Configuración del Excel

Para cargar rutas masivamente, crea un archivo `DB_Rutas.xlsx` con las siguientes columnas:

| Columna     | Descripción                    | Requerido |
|-------------|--------------------------------|-----------|
| RUTA        | Nombre de la ruta             | ✅        |
| CODIGO      | Código de la ruta             | ❌        |
| PLACA       | Placa del vehículo            | ❌        |
| SUPERVISOR  | Nombre del supervisor         | ❌        |
| CONTRATISTA | Nombre del contratista        | ✅        |
| TIPO        | Tipo de ruta                  | ❌        |

## 🔧 Configuración Avanzada

### Variables de Entorno
```bash
# Puerto del servidor (por defecto: 5000)
export PORT=8080

# Modo debug (por defecto: True en desarrollo)
export FLASK_DEBUG=False
```

### Base de Datos
- El sistema usa SQLite por defecto
- La base de datos se crea automáticamente en `sistema_rutas.db`
- Incluye tablas para: rutas, reportes, usuarios, logs de actividad

## 📱 Funcionalidades del Dashboard

### 📊 Estadísticas en Tiempo Real
- Total de reportes del día
- Contratistas activos
- Rutas activas
- Total de cajas reportadas

### 🔍 Filtros Avanzados
- Filtro por fecha
- Filtro por contratista
- Paginación configurable (10, 25, 50 registros)

### 📈 Reportes y Exportación
- Exportación a Excel con formato profesional
- Filtros aplicables a las exportaciones
- Logs de actividad de usuarios

## 🛡️ Seguridad

- Autenticación con Flask-Login
- Contraseñas hasheadas con Werkzeug
- Headers de seguridad configurados
- Simulación de entorno corporativo en headers
- Control de acceso por roles

## 🔄 Flujo de Trabajo

1. **Usuario reporta ruta**: Formulario público → Base de datos
2. **Admin revisa**: Dashboard con filtros y paginación
3. **Gestión de estados**: Activo → Completado
4. **Exportación**: Reportes en Excel para análisis
5. **Seguimiento**: Logs de actividad y auditoría

## ⚡ Comandos Útiles

```bash
# Iniciar servidor
python app.py

# Crear backup de base de datos
copy sistema_rutas.db sistema_rutas_backup.db

# Ver logs en tiempo real (si se habilita logging a archivo)
tail -f sistema_rutas.log

# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

## 🐛 Troubleshooting

### Error: ModuleNotFoundError
```bash
pip install -r requirements.txt
```

### Error: Base de datos bloqueada
```bash
# Cerrar todas las instancias de la aplicación
# Reiniciar el servidor
python app.py
```

### Error: Puerto ocupado
```bash
# Cambiar puerto en app.py línea final:
app.run(debug=True, host='0.0.0.0', port=8080)
```

## 🚀 Deployment en Producción

### Para Railway/Heroku:
1. Crear `Procfile`:
   ```
   web: python app.py
   ```

2. Configurar variables de entorno:
   ```
   PORT=5000
   FLASK_DEBUG=False
   ```

### Para servidor local:
```bash
# Usar gunicorn para producción
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📝 Changelog

### v1.0.0 (2025-06-25)
- ✅ Sistema completo funcionando
- ✅ Dashboard con paginación
- ✅ Exportación a Excel
- ✅ Sistema de usuarios
- ✅ Carga desde Excel
- ✅ Scripts de deployment

## 👨‍💻 Desarrollo

Para contribuir al proyecto:

1. Clonar el repositorio
2. Crear un virtual environment
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar tests (si existen)
5. Hacer cambios y probar
6. Crear pull request

## 📞 Soporte

- **Documentación**: Este README
- **Issues**: Reportar en el repositorio
- **Email**: sistema-rutas@empresa.com

---

### 🏆 Sistema desarrollado para optimizar la gestión logística de rutas de distribución

**Tecnologías**: Python 3.8+, Flask 2.3+, SQLite, Bootstrap 5, jQuery

---

*© 2025 Sistema de Gestión de Rutas - Todos los derechos reservados*
