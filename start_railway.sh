#!/bin/bash
# Script de inicio para Railway

echo "🔧 Iniciando aplicación en Railway..."

# Verificar que existe el archivo DB_Rutas.xlsx
if [ -f "DB_Rutas.xlsx" ]; then
    echo "✅ Archivo DB_Rutas.xlsx encontrado"
    echo "📊 Tamaño del archivo: $(du -h DB_Rutas.xlsx | cut -f1)"
    echo "📅 Fecha de modificación: $(stat -c %y DB_Rutas.xlsx)"
else
    echo "❌ ERROR: Archivo DB_Rutas.xlsx NO encontrado"
    echo "❌ La aplicación NO tendrá rutas disponibles"
    echo "❌ Por favor, SUBE el archivo DB_Rutas.xlsx a Railway"
    echo "📂 Contenido del directorio actual:"
    ls -la
fi

# Ejecutar la aplicación
echo "🚀 Ejecutando aplicación..."
python3 app.py
