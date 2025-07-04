#!/bin/bash
# Script de inicio para Railway

echo "🔧 Iniciando aplicación en Railway..."

# Verificar que existe el archivo DB_Rutas.xlsx
echo "🔍 Buscando archivo DB_Rutas.xlsx..."
if [ -f "DB_Rutas.xlsx" ]; then
    echo "✅ Archivo DB_Rutas.xlsx encontrado"
    echo "📊 Tamaño del archivo: $(du -h DB_Rutas.xlsx | cut -f1)"
    echo "📅 Fecha de modificación: $(stat -c %y DB_Rutas.xlsx)"
    echo "📋 Formato del archivo:"
    file DB_Rutas.xlsx
    echo "📋 Primeros bytes del archivo (para verificar que no está corrupto):"
    hexdump -C DB_Rutas.xlsx | head -n 5
    echo "📦 Copiando archivo a directorio actual (por si está en otra ubicación)"
    cp -v DB_Rutas.xlsx ./DB_Rutas.xlsx || echo "⚠️ El archivo ya existe en el directorio actual"
else
    echo "❌ ERROR: Archivo DB_Rutas.xlsx NO encontrado"
    echo "❌ La aplicación NO tendrá rutas disponibles"
    echo "❌ Por favor, SUBE el archivo DB_Rutas.xlsx a Railway"
    echo "📂 Contenido del directorio actual:"
    ls -la
    echo "📂 Buscando archivos Excel en todo el sistema:"
    find / -name "*.xlsx" -type f 2>/dev/null | head -n 10
fi

# Ejecutar la aplicación
echo "🚀 Ejecutando aplicación con Gunicorn..."
python3 -c "import os; print(f'Python version: {os.popen(\"python3 --version\").read().strip()}')"
python3 -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
echo "🔄 Inicializando base de datos antes de arrancar..."
# Crear railway_fix.py si no existe (desde contenido guardado)
if [ ! -f "railway_fix.py" ]; then
    echo "⚠️ Script railway_fix.py no encontrado, intentando crear desde backup..."
    cat > railway_fix.py << 'EOL'
#!/usr/bin/env python3
# Fix for Railway deployment - Ensures the database is initialized before running the app

import os
import sys
import sqlite3
from werkzeug.security import generate_password_hash

# Definir ruta de base de datos
DATABASE = 'sistema_rutas.db'

def railway_fix():
    """Fix para Railway - Asegura que la base de datos exista y tenga la estructura correcta"""
    print("\n🔧 RAILWAY FIX: Verificando base de datos y tablas...")
    
    try:
        # Verificar que el archivo existe
        if os.path.exists(DATABASE):
            print(f"📁 Archivo de base de datos encontrado: {DATABASE}")
            print(f"📊 Tamaño: {os.path.getsize(DATABASE)} bytes")
        else:
            print(f"⚠️ Creando nuevo archivo de base de datos: {DATABASE}")
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Configurar SQLite para mejor rendimiento
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA temp_store=MEMORY")
        
        # Tabla para almacenar datos de rutas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rutas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ruta TEXT NOT NULL,
                codigo TEXT,
                placa TEXT,
                supervisor TEXT,
                contratista TEXT NOT NULL,
                tipo TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla para reportes de rutas diarios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reportes_rutas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contratista TEXT NOT NULL,
                ruta_id INTEGER NOT NULL,
                ruta_codigo TEXT NOT NULL,
                clientes_pendientes INTEGER NOT NULL DEFAULT 0,
                cajas_camion INTEGER NOT NULL DEFAULT 0,
                hora_aproximada_ingreso TIME NOT NULL,
                ubicacion_exacta TEXT,
                latitud REAL,
                longitud REAL,
                hora_exacta_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
                comentarios TEXT,
                fecha_reporte DATE DEFAULT (date('now')),
                hora_reporte DATETIME DEFAULT CURRENT_TIMESTAMP,
                estado TEXT DEFAULT 'activo',
                reportado_por TEXT,
                FOREIGN KEY (ruta_id) REFERENCES rutas (id)
            )
        ''')
        
        # Tabla para usuarios del sistema
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user',
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                created_by INTEGER
            )
        ''')
        
        # Tabla para log de actividades
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS activity_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT NOT NULL,
                target_type TEXT,
                target_id INTEGER,
                details TEXT,
                ip_address TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Listar tablas para diagnóstico
        tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        print(f"📊 Tablas en la base de datos: {[t[0] for t in tables]}")
        
        # Crear usuario administrador por defecto si no existe
        existing_admin = cursor.execute('SELECT id FROM users WHERE username = ?', ('admin',)).fetchone()
        
        if not existing_admin:
            print("⚠️ Usuario admin no encontrado. Creando...")
            admin_password_hash = generate_password_hash('admin123')
            cursor.execute('''
                INSERT INTO users (username, email, password_hash, role, is_active)
                VALUES (?, ?, ?, ?, ?)
            ''', ('admin', 'admin@sistema-rutas.com', admin_password_hash, 'admin', 1))
            print("✅ Usuario admin creado")
        else:
            print("✅ Usuario admin ya existe")
        
        # Contar usuarios
        users_count = cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        print(f"👤 La base de datos tiene {users_count} usuarios")
        
        # Verificar rutas
        rutas_count = cursor.execute('SELECT COUNT(*) FROM rutas').fetchone()[0]
        print(f"🛣️ La base de datos tiene {rutas_count} rutas")
        
        # Cargar rutas desde Excel si no hay
        if rutas_count == 0 and os.path.exists("DB_Rutas.xlsx"):
            print("📋 No hay rutas. Cargando desde Excel...")
            try:
                # Intentar cargar desde init_database.py primero
                if os.path.exists('init_database.py'):
                    print("📋 Usando script init_database.py...")
                    os.system("python init_database.py")
                else:
                    # Si no existe, usar la función interna
                    # Esta parte necesitaría implementar la función cargar_datos_excel
                    print("⚠️ Script init_database.py no encontrado")
                    print("⚠️ Cargar el Excel manualmente")
            except Exception as e:
                print(f"❌ Error cargando datos desde Excel: {e}")
        
        conn.commit()
        conn.close()
        print("✅ RAILWAY FIX completado correctamente\n")
        return True
    
    except Exception as e:
        import traceback
        print(f"❌ ERROR en RAILWAY FIX: {e}")
        print(traceback.format_exc())
        return False

# Ejecutar la función si este script se llama directamente
if __name__ == "__main__":
    success = railway_fix()
    if not success:
        print("❌ RAILWAY FIX falló - abortando")
        sys.exit(1)
    else:
        print("✅ RAILWAY FIX ejecutado correctamente")
EOL
    echo "✅ Script railway_fix.py creado"
fi

# Dar permisos de ejecución a los scripts
chmod +x railway_fix.py
chmod +x init_database.py

# Ejecutar PRIMERO el railway fix para asegurar que la BD existe y tiene tablas
echo "🔧 Ejecutando railway_fix.py para verificar base de datos..."
python3 railway_fix.py

# Ejecutar el script de inicialización
echo "🔧 Ejecutando script init_database.py para cargar datos..."
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

# Verificar que railway_entry.py exista
if [ -f "railway_entry.py" ]; then
    echo "✅ Usando railway_entry.py para inicializar correctamente..."
    # Dar permisos de ejecución
    chmod +x railway_entry.py
    # Para Railway, usamos Gunicorn para servir la aplicación con nuestro entry point
    exec gunicorn railway_entry:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120
else
    echo "⚠️ railway_entry.py no encontrado, usando app.py directamente (menos seguro)"
    # Fallback al método tradicional
    exec gunicorn app:app --bind 0.0.0.0:$PORT --workers=1 --timeout=120
fi
