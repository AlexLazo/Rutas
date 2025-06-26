#!/bin/bash
# Script de instalación de dependencias para Railway

echo "🔧 Instalando dependencias..."
pip install --upgrade pip
pip install Flask==2.3.3 Flask-Login==0.6.3 Werkzeug==2.3.7 gunicorn==21.2.0

# Intentar instalar pandas solo si está configurado
if [ "$INSTALL_PANDAS" = "true" ]; then
    echo "📊 Intentando instalar pandas (opcional)..."
    pip install numpy pandas openpyxl --no-cache-dir || echo "⚠️ No se pudo instalar pandas, pero la aplicación funcionará sin él"
else
    echo "📊 Pandas no instalado (configurado como opcional)"
fi

echo "✅ Dependencias instaladas"
