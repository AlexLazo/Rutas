#!/usr/bin/env python3
# Script para inicializar la base de datos de forma explícita antes de iniciar la aplicación

import sqlite3
import os
from werkzeug.security import generate_password_hash

# Definir ruta de base de datos
DATABASE = 'sistema_rutas.db'

def init_db():
    """Inicializar la base de datos"""
    print(f"🔄 Inicializando base de datos en: {DATABASE}")
    
    # Verificar que el archivo existe
    if os.path.exists(DATABASE):
        print(f"📁 Archivo de base de datos encontrado: {DATABASE}")
    else:
        print(f"⚠️ Creando nuevo archivo de base de datos: {DATABASE}")
        
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Configurar SQLite para mejor rendimiento
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.execute("PRAGMA synchronous=NORMAL")
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA temp_store=MEMORY")
    
    # Tabla para almacenar datos de rutas (cargados desde Excel)
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
    
    # Crear usuario administrador por defecto si no existe
    existing_admin = cursor.execute(
        'SELECT id FROM users WHERE username = ?', ('admin',)
    ).fetchone()
    
    if not existing_admin:
        admin_password_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@sistema-rutas.com', admin_password_hash, 'admin', 1))
        print("✅ Usuario admin creado")
    
    # Verificar si hay rutas
    rutas_count = cursor.execute('SELECT COUNT(*) FROM rutas').fetchone()[0]
    print(f"📊 La base de datos tiene {rutas_count} rutas registradas")
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    # Ejecutar inicialización de forma independiente
    init_db()
