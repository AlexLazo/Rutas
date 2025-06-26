#!/bin/bash
# Script de inicio para Railway

echo "🔧 Iniciando aplicación en Railway..."

# Verificar que existe el archivo DB_Rutas.xlsx
if [ -f "DB_Rutas.xlsx" ]; then
    echo "✅ Archivo DB_Rutas.xlsx encontrado"
    echo "📊 Tamaño del archivo: $(du -h DB_Rutas.xlsx | cut -f1)"
    echo "📅 Fecha de modificación: $(stat -c %y DB_Rutas.xlsx)"
    echo "📋 Contenido del Excel (primeras 5 filas):"
    head -n 5 DB_Rutas.xlsx || echo "  (No se puede mostrar contenido binario)"
else
    echo "❌ ERROR: Archivo DB_Rutas.xlsx NO encontrado"
    echo "❌ La aplicación NO tendrá rutas disponibles"
    echo "❌ Por favor, SUBE el archivo DB_Rutas.xlsx a Railway"
    echo "📂 Contenido del directorio actual:"
    ls -la
fi

# Ejecutar la aplicación
echo "🚀 Ejecutando aplicación con Gunicorn..."
python3 -c "import os; print(f'Python version: {os.popen(\"python3 --version\").read().strip()}')"
python3 -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
echo "🔄 Iniciando app.py directamente para asegurar carga de datos..."

# Para Railway, usamos Gunicorn para servir la aplicación
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120 --preload
