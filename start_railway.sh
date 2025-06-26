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
echo "🔄 Inicializando base de datos antes de arrancar..."
python3 init_database.py

echo "🔄 Verificando tablas de la base de datos..."
python3 -c "
import sqlite3;
conn = sqlite3.connect('sistema_rutas.db');
cursor = conn.cursor();
tables = cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\";').fetchall();
print(f'Tablas encontradas: {[t[0] for t in tables]}');
rutas_count = cursor.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\"table\" AND name=\"rutas\";').fetchone()[0];
if rutas_count == 0:
    print('❌ CRÍTICO: La tabla \"rutas\" NO existe');
else:
    print('✅ Tabla \"rutas\" encontrada');
    count = cursor.execute('SELECT COUNT(*) FROM rutas;').fetchone()[0];
    print(f'📊 Hay {count} rutas en la base de datos');
conn.close();
"

# Para Railway, usamos Gunicorn para servir la aplicación
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120
