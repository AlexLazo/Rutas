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
python3 -c "
import sqlite3;
import os;
print('Inicializando base de datos...');
conn = sqlite3.connect('sistema_rutas.db');
conn.executescript('''
CREATE TABLE IF NOT EXISTS rutas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruta TEXT NOT NULL,
    codigo TEXT,
    placa TEXT,
    supervisor TEXT,
    contratista TEXT NOT NULL,
    tipo TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS reportes_rutas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ruta_id INTEGER NOT NULL,
    fecha TEXT, 
    hora TEXT,
    descripcion TEXT,
    estado TEXT,
    usuario_reporte TEXT,
    FOREIGN KEY (ruta_id) REFERENCES rutas (id)
);
''');
conn.commit();
conn.close();
print('✅ Base de datos inicializada correctamente');
"

# Para Railway, usamos Gunicorn para servir la aplicación
exec gunicorn app:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120
