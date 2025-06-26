#!/usr/bin/env python3
# Entry point para Railway - Inicializa la base de datos y luego ejecuta la aplicación

import os
import sys
import importlib
from werkzeug.security import generate_password_hash
import sqlite3

# Importar nuestro corrector
try:
    from railway_fix import railway_fix
    print("✅ Módulo railway_fix importado correctamente")
except ImportError:
    print("⚠️ No se pudo importar railway_fix, creándolo en memoria...")

    def railway_fix():
        """Fix para Railway - Asegura que la base de datos exista y tenga la estructura correcta"""
        print("\n🔧 RAILWAY FIX (Memoria): Verificando base de datos y tablas...")
        
        try:
            # Definir ruta de base de datos
            DATABASE = 'sistema_rutas.db'
            
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
            
            conn.commit()
            conn.close()
            print("✅ RAILWAY FIX completado correctamente\n")
            return True
        
        except Exception as e:
            import traceback
            print(f"❌ ERROR en RAILWAY FIX: {e}")
            print(traceback.format_exc())
            return False

# Ejecutar el fix primero
print("🚀 RAILWAY ENTRY: Iniciando...")
if not railway_fix():
    print("❌ ERROR: No se pudo inicializar la base de datos")
    sys.exit(1)

# Importar nuestra aplicación
try:
    print("🚀 Importando aplicación Flask...")
    from app import app
    print("✅ Aplicación importada correctamente")
except ImportError as e:
    print(f"❌ ERROR crítico: No se pudo importar la aplicación: {e}")
    sys.exit(1)

# Para gunicorn
print("✅ app.py importada correctamente, objeto 'app' listo para gunicorn")
