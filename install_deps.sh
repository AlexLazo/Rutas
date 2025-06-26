#!/bin/bash
# Script de instalación de dependencias para Railway

echo "🔧 Instalando dependencias..."
pip install --upgrade pip
pip install Flask==2.3.3 Flask-Login==0.6.3 Werkzeug==2.3.7 gunicorn==21.2.0

echo "📊 Instalando pandas y dependencias para Excel..."
pip install numpy==1.21.6 pandas==1.3.5 openpyxl==3.0.10 --no-cache-dir

echo "✅ Dependencias instaladas"
