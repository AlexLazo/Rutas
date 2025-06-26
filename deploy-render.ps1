# 🚀 Script de Deployment para Render.com
# Sistema de Gestión de Rutas - AB InBev

Write-Host "🚀 Preparando deployment para Render.com" -ForegroundColor Green
Write-Host "===========================================" -ForegroundColor Green

# Función para verificar Git
function Test-Git {
    Write-Host "`n📋 Verificando Git..." -ForegroundColor Yellow
    
    try {
        $gitVersion = git --version 2>&1
        Write-Host "✅ Git encontrado: $gitVersion" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Git no encontrado. Por favor instala Git desde https://git-scm.com/" -ForegroundColor Red
        return $false
    }
}

# Función para verificar archivos del proyecto
function Test-RenderFiles {
    Write-Host "`n📁 Verificando archivos para Render..." -ForegroundColor Yellow
    
    $requiredFiles = @(
        "app.py",
        "requirements.txt",
        "templates/base.html",
        "templates/index.html",
        "templates/admin.html",
        "templates/login.html",
        "render.yaml"
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
    
    return $true
}

# Función para inicializar Git si no existe
function Initialize-Git {
    Write-Host "`n🔧 Configurando Git..." -ForegroundColor Yellow
    
    if (-not (Test-Path ".git")) {
        Write-Host "📦 Inicializando repositorio Git..." -ForegroundColor Cyan
        git init
        git branch -M main
    } else {
        Write-Host "✅ Repositorio Git ya existe" -ForegroundColor Green
    }
    
    # Verificar .gitignore
    if (-not (Test-Path ".gitignore")) {
        Write-Host "📝 Creando .gitignore..." -ForegroundColor Cyan
        @"
# Python
__pycache__/
*.pyc
*.pyo
*.db
*.sqlite3

# Flask
instance/
.webassets-cache

# Environment
.env
.venv
venv/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    }
    
    return $true
}

# Función para preparar commit
function Prepare-Commit {
    Write-Host "`n📝 Preparando archivos para commit..." -ForegroundColor Yellow
    
    git add .
    
    $status = git status --porcelain
    if ($status) {
        Write-Host "📋 Archivos a subir:" -ForegroundColor Cyan
        git status --short
        
        $message = "Sistema de Rutas - Deployment para Render.com"
        git commit -m $message
        Write-Host "✅ Commit creado: $message" -ForegroundColor Green
        return $true
    } else {
        Write-Host "✅ No hay cambios para hacer commit" -ForegroundColor Green
        return $true
    }
}

# Función para mostrar instrucciones de GitHub
function Show-GitHubInstructions {
    Write-Host "`n🌐 PASOS PARA SUBIR A GITHUB:" -ForegroundColor Green
    Write-Host "==============================" -ForegroundColor Green
    Write-Host ""
    Write-Host "1. 📱 Ve a github.com y crea una cuenta (si no tienes)" -ForegroundColor Yellow
    Write-Host "2. ➕ Crea un nuevo repositorio:" -ForegroundColor Yellow
    Write-Host "   • Nombre: sistema-rutas-abinbev" -ForegroundColor White
    Write-Host "   • Descripción: Sistema de Gestión de Rutas para AB InBev" -ForegroundColor White
    Write-Host "   • Público o Privado (tu elección)" -ForegroundColor White
    Write-Host "   • NO marques README, .gitignore, license (ya los tienes)" -ForegroundColor White
    Write-Host ""
    Write-Host "3. 🔗 Después de crear el repo, ejecuta estos comandos aquí:" -ForegroundColor Yellow
    Write-Host "   git remote add origin https://github.com/TU-USUARIO/sistema-rutas-abinbev.git" -ForegroundColor Cyan
    Write-Host "   git push -u origin main" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "4. 🚀 Una vez en GitHub, ve a render.com para el deployment" -ForegroundColor Yellow
    Write-Host ""
}

# Función para mostrar instrucciones de Render
function Show-RenderInstructions {
    Write-Host "`n🚀 PASOS PARA DEPLOYMENT EN RENDER.COM:" -ForegroundColor Green
    Write-Host "=======================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "1. 🌐 Ve a render.com" -ForegroundColor Yellow
    Write-Host "2. 📧 Crea cuenta (usa tu email corporativo si es posible)" -ForegroundColor Yellow
    Write-Host "3. 🔗 Conecta tu cuenta de GitHub" -ForegroundColor Yellow
    Write-Host "4. ➕ Clic en 'New +' → 'Web Service'" -ForegroundColor Yellow
    Write-Host "5. 📦 Selecciona tu repositorio: sistema-rutas-abinbev" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "6. ⚙️ Configuración del servicio:" -ForegroundColor Yellow
    Write-Host "   • Name: sistema-rutas-abinbev" -ForegroundColor Cyan
    Write-Host "   • Region: Oregon (US West) - mejor para LATAM" -ForegroundColor Cyan
    Write-Host "   • Branch: main" -ForegroundColor Cyan
    Write-Host "   • Runtime: Python 3" -ForegroundColor Cyan
    Write-Host "   • Build Command: pip install -r requirements.txt" -ForegroundColor Cyan
    Write-Host "   • Start Command: python app.py" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "7. 🔧 Variables de entorno (Environment Variables):" -ForegroundColor Yellow
    Write-Host "   • FLASK_ENV = production" -ForegroundColor Cyan
    Write-Host "   • TZ = America/Guatemala" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "8. 💰 Plan: Free (0$/mes)" -ForegroundColor Yellow
    Write-Host "9. 🚀 Clic en 'Create Web Service'" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "⏱️ El deployment toma 2-5 minutos..." -ForegroundColor Green
    Write-Host ""
}

# Función para mostrar información post-deployment
function Show-PostDeployment {
    Write-Host "`n✅ DESPUÉS DEL DEPLOYMENT:" -ForegroundColor Green
    Write-Host "=========================" -ForegroundColor Green
    Write-Host ""
    Write-Host "🌐 Tu aplicación estará en:" -ForegroundColor Yellow
    Write-Host "   https://sistema-rutas-abinbev-XXXX.onrender.com" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "👤 Usuarios por defecto:" -ForegroundColor Yellow
    Write-Host "   Admin: admin / admin123" -ForegroundColor Cyan
    Write-Host "   Supervisor: supervisor / supervisor123" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📱 Pruebas recomendadas:" -ForegroundColor Yellow
    Write-Host "   ✅ Acceso desde PC corporativo" -ForegroundColor White
    Write-Host "   ✅ Acceso desde teléfono corporativo" -ForegroundColor White
    Write-Host "   ✅ Formulario de reportes" -ForegroundColor White
    Write-Host "   ✅ Login de administrador" -ForegroundColor White
    Write-Host "   ✅ Dashboard y filtros" -ForegroundColor White
    Write-Host "   ✅ Exportar a Excel" -ForegroundColor White
    Write-Host ""
    Write-Host "🔄 Auto-deploy:" -ForegroundColor Yellow
    Write-Host "   Cada vez que hagas 'git push', Render actualiza automáticamente" -ForegroundColor White
    Write-Host ""
}

# Función principal
function Main {
    $currentDir = Get-Location
    Write-Host "📁 Directorio: $currentDir" -ForegroundColor Cyan
    
    # Verificar Git
    if (-not (Test-Git)) {
        Write-Host "`n❌ Error: Git requerido. Abortando." -ForegroundColor Red
        return
    }
    
    # Verificar archivos del proyecto
    if (-not (Test-RenderFiles)) {
        Write-Host "`n❌ Error: Archivos del proyecto faltantes. Abortando." -ForegroundColor Red
        return
    }
    
    # Inicializar Git
    if (-not (Initialize-Git)) {
        Write-Host "`n❌ Error configurando Git. Abortando." -ForegroundColor Red
        return
    }
    
    # Preparar commit
    if (-not (Prepare-Commit)) {
        Write-Host "`n❌ Error preparando commit. Abortando." -ForegroundColor Red
        return
    }
    
    Write-Host "`n✅ ¡Proyecto listo para Render.com!" -ForegroundColor Green
    
    # Mostrar instrucciones
    Show-GitHubInstructions
    Show-RenderInstructions
    Show-PostDeployment
    
    Write-Host "`n🎯 SIGUIENTE PASO:" -ForegroundColor Green
    Write-Host "Sube tu código a GitHub y luego configura en Render.com" -ForegroundColor Yellow
    Write-Host ""
    
    # Preguntar si quiere abrir los sitios web
    $response = Read-Host "¿Deseas abrir GitHub y Render.com en el navegador? (s/n)"
    if ($response -eq 's' -or $response -eq 'S') {
        Start-Process "https://github.com/new"
        Start-Sleep -Seconds 2
        Start-Process "https://render.com"
        Write-Host "🌐 Sitios web abiertos en el navegador" -ForegroundColor Green
    }
}

# Ejecutar función principal
Main
