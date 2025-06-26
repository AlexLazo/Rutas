# Script de deployment para Sistema de Rutas
# PowerShell script para facilitar la subida del proyecto

Write-Host "🚀 Sistema de Gestión de Rutas - Script de Deployment" -ForegroundColor Green
Write-Host "=================================================" -ForegroundColor Green

# Función para verificar dependencias
function Test-Dependencies {
    Write-Host "`n📋 Verificando dependencias..." -ForegroundColor Yellow
    
    # Verificar Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Host "✅ Python encontrado: $pythonVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ Python no encontrado. Por favor instala Python 3.8+" -ForegroundColor Red
        return $false
    }
    
    # Verificar pip
    try {
        $pipVersion = pip --version 2>&1
        Write-Host "✅ pip encontrado: $pipVersion" -ForegroundColor Green
    } catch {
        Write-Host "❌ pip no encontrado. Por favor instala pip" -ForegroundColor Red
        return $false
    }
    
    return $true
}

# Función para instalar dependencias Python
function Install-PythonDependencies {
    Write-Host "`n📦 Instalando dependencias de Python..." -ForegroundColor Yellow
    
    $requirements = @(
        "Flask==2.3.3",
        "Flask-Login==0.6.2",
        "Werkzeug==2.3.7",
        "pandas==2.0.3",
        "openpyxl==3.1.2"
    )
    
    foreach ($package in $requirements) {
        Write-Host "Instalando $package..." -ForegroundColor Cyan
        pip install $package
        if ($LASTEXITCODE -ne 0) {
            Write-Host "❌ Error instalando $package" -ForegroundColor Red
            return $false
        }
    }
    
    Write-Host "✅ Todas las dependencias instaladas correctamente" -ForegroundColor Green
    return $true
}

# Función para verificar archivos del proyecto
function Test-ProjectFiles {
    Write-Host "`n📁 Verificando archivos del proyecto..." -ForegroundColor Yellow
    
    $requiredFiles = @(
        "app.py",
        "templates/base.html",
        "templates/index.html",
        "templates/admin.html",
        "templates/login.html"
    )
    
    $missing = @()
    foreach ($file in $requiredFiles) {
        if (-not (Test-Path $file)) {
            $missing += $file
        } else {
            Write-Host "✅ $file" -ForegroundColor Green
        }
    }
    
    if ($missing.Count -gt 0) {
        Write-Host "❌ Archivos faltantes:" -ForegroundColor Red
        foreach ($file in $missing) {
            Write-Host "   - $file" -ForegroundColor Red
        }
        return $false
    }
    
    # Verificar archivo Excel opcional
    if (Test-Path "DB_Rutas.xlsx") {
        Write-Host "✅ DB_Rutas.xlsx (archivo de rutas encontrado)" -ForegroundColor Green
    } else {
        Write-Host "⚠️ DB_Rutas.xlsx no encontrado (se puede agregar después)" -ForegroundColor Yellow
    }
    
    return $true
}

# Función para configurar el proyecto
function Initialize-Project {
    Write-Host "`n⚙️ Inicializando proyecto..." -ForegroundColor Yellow
    
    # Crear base de datos si no existe
    if (-not (Test-Path "sistema_rutas.db")) {
        Write-Host "📊 Creando base de datos..." -ForegroundColor Cyan
        python -c "
from app import init_db
init_db()
print('Base de datos creada correctamente')
"
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Base de datos creada" -ForegroundColor Green
        } else {
            Write-Host "❌ Error creando base de datos" -ForegroundColor Red
            return $false
        }
    } else {
        Write-Host "✅ Base de datos ya existe" -ForegroundColor Green
    }
    
    return $true
}

# Función para crear archivos de configuración
function Create-ConfigFiles {
    Write-Host "`n📝 Creando archivos de configuración..." -ForegroundColor Yellow
    
    # requirements.txt
    $requirementsTxt = @"
Flask==2.3.3
Flask-Login==0.6.2
Werkzeug==2.3.7
pandas==2.0.3
openpyxl==3.1.2
"@
    $requirementsTxt | Out-File -FilePath "requirements.txt" -Encoding UTF8
    Write-Host "✅ requirements.txt creado" -ForegroundColor Green
    
    # .gitignore
    $gitignore = @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Flask
instance/
.webassets-cache

# Database
*.db
*.sqlite
*.sqlite3

# Environment variables
.env
.venv
env/
venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary files
*.tmp
*.temp
"@
    $gitignore | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore creado" -ForegroundColor Green
    
    # Archivo de inicio start.bat
    $startBat = @"
@echo off
echo 🚀 Iniciando Sistema de Gestión de Rutas...
python app.py
pause
"@
    $startBat | Out-File -FilePath "start.bat" -Encoding ASCII
    Write-Host "✅ start.bat creado" -ForegroundColor Green
    
    return $true
}

# Función para mostrar información de deployment
function Show-DeploymentInfo {
    Write-Host "`n🌐 Información de Deployment" -ForegroundColor Green
    Write-Host "================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "📁 Directorio del proyecto: $(Get-Location)" -ForegroundColor Cyan
    Write-Host "🌐 URL local: http://127.0.0.1:5000" -ForegroundColor Cyan
    Write-Host "👤 Usuario admin: admin / admin123" -ForegroundColor Cyan
    Write-Host "👤 Usuario supervisor: supervisor / supervisor123" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🚀 Para iniciar el servidor:" -ForegroundColor Yellow
    Write-Host "   • Ejecuta: python app.py" -ForegroundColor White
    Write-Host "   • O usa: start.bat" -ForegroundColor White
    Write-Host ""
    Write-Host "📋 Para cargar rutas desde Excel:" -ForegroundColor Yellow
    Write-Host "   • Copia tu archivo Excel como 'DB_Rutas.xlsx'" -ForegroundColor White
    Write-Host "   • El archivo debe tener columnas: RUTA, CODIGO, PLACA, SUPERVISOR, CONTRATISTA, TIPO" -ForegroundColor White
    Write-Host "   • Las rutas se cargarán automáticamente al iniciar" -ForegroundColor White
    Write-Host ""
}

# Función principal
function Main {
    $currentDir = Get-Location
    Write-Host "📁 Directorio actual: $currentDir" -ForegroundColor Cyan
    
    # Verificar dependencias
    if (-not (Test-Dependencies)) {
        Write-Host "`n❌ Error en las dependencias. Abortando deployment." -ForegroundColor Red
        return
    }
    
    # Verificar archivos del proyecto
    if (-not (Test-ProjectFiles)) {
        Write-Host "`n❌ Archivos del proyecto faltantes. Abortando deployment." -ForegroundColor Red
        return
    }
    
    # Instalar dependencias Python
    if (-not (Install-PythonDependencies)) {
        Write-Host "`n❌ Error instalando dependencias Python. Abortando deployment." -ForegroundColor Red
        return
    }
    
    # Crear archivos de configuración
    if (-not (Create-ConfigFiles)) {
        Write-Host "`n❌ Error creando archivos de configuración. Abortando deployment." -ForegroundColor Red
        return
    }
    
    # Inicializar proyecto
    if (-not (Initialize-Project)) {
        Write-Host "`n❌ Error inicializando proyecto. Abortando deployment." -ForegroundColor Red
        return
    }
    
    Write-Host "`n✅ ¡Deployment completado exitosamente!" -ForegroundColor Green
    Show-DeploymentInfo
    
    # Preguntar si quiere iniciar el servidor
    $response = Read-Host "`n¿Deseas iniciar el servidor ahora? (s/n)"
    if ($response -eq 's' -or $response -eq 'S' -or $response -eq 'si' -or $response -eq 'Si') {
        Write-Host "`n🚀 Iniciando servidor..." -ForegroundColor Green
        python app.py
    } else {
        Write-Host "`n👍 Puedes iniciar el servidor más tarde ejecutando: python app.py" -ForegroundColor Yellow
    }
}

# Ejecutar función principal
Main
