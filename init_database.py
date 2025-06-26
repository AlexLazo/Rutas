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
    
    # Crear supervisor de ejemplo si no existe
    existing_supervisor = cursor.execute(
        'SELECT id FROM users WHERE username = ?', ('supervisor',)
    ).fetchone()
    
    if not existing_supervisor:
        supervisor_password_hash = generate_password_hash('supervisor123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, role, is_active)
            VALUES (?, ?, ?, ?, ?)
        ''', ('supervisor', 'supervisor@sistema-rutas.com', supervisor_password_hash, 'supervisor', 1))
    
    print("✅ Usuarios por defecto creados:")
    print("\n   Admin: admin / admin123")
    print("\n   Supervisor: supervisor / supervisor123")
    
    # Verificar si hay rutas
    rutas_count = cursor.execute('SELECT COUNT(*) FROM rutas').fetchone()[0]
    print(f"📊 La base de datos tiene {rutas_count} rutas registradas")
    
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente")

def cargar_datos_excel():
    """Cargar datos desde el archivo Excel"""
    try:
        # Verificar si existe pandas
        try:
            import pandas as pd
            PANDAS_AVAILABLE = True
            print("✅ Pandas importado correctamente")
        except ImportError as e:
            print(f"❌ Error importando pandas: {e}")
            print("❌ No se pueden cargar datos desde Excel")
            return False
        
        # Verificar si existe el archivo Excel
        excel_path = 'DB_Rutas.xlsx'
        if not os.path.exists(excel_path):
            print(f"❌ No se encontró el archivo {excel_path}")
            return False
        
        print(f"📊 Cargando datos desde {excel_path}...")
        df = pd.read_excel(excel_path)
        
        print(f"📋 Excel leído correctamente. Encontradas {len(df)} filas")
        print(f"📋 Columnas en el Excel: {', '.join(df.columns.tolist())}")
        
        # Verificar columnas requeridas
        required_columns = ['RUTA', 'CODIGO', 'CONTRATISTA']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            print(f"❌ Error: Faltan columnas requeridas en el Excel: {', '.join(missing_columns)}")
            return False
        
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        
        # Limpiar tabla de rutas existente
        rutas_count = cursor.execute('SELECT COUNT(*) FROM rutas').fetchone()[0]
        print(f"🔄 Eliminando {rutas_count} rutas existentes...")
        cursor.execute('DELETE FROM rutas')
        
        # Insertar datos desde Excel
        loaded_count = 0
        for idx, row in df.iterrows():
            try:
                ruta = str(row['RUTA']) if pd.notna(row['RUTA']) else ''
                codigo = str(row['CODIGO']) if pd.notna(row['CODIGO']) else ''
                placa = str(row['PLACA']) if pd.notna(row['PLACA']) else ''
                supervisor = str(row['SUPERVISOR']) if pd.notna(row['SUPERVISOR']) else ''
                contratista = str(row['CONTRATISTA']) if pd.notna(row['CONTRATISTA']) else ''
                tipo = str(row['TIPO']) if pd.notna(row['TIPO']) else ''
                
                # Verificar que contratista no sea vacío (es NOT NULL)
                if not contratista:
                    print(f"⚠️ Fila {idx+2}: Saltando ruta sin contratista: {ruta}")
                    continue
                
                cursor.execute('''
                    INSERT INTO rutas (ruta, codigo, placa, supervisor, contratista, tipo)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (ruta, codigo, placa, supervisor, contratista, tipo))
                
                loaded_count += 1
                if loaded_count % 50 == 0:
                    print(f"🔄 {loaded_count} rutas procesadas...")
            except Exception as row_error:
                print(f"⚠️ Error en fila {idx+2}: {row_error}")
                continue
        
        conn.commit()
        conn.close()
        
        print(f"✅ {loaded_count} rutas cargadas desde Excel correctamente")
        return True
        
    except Exception as e:
        import traceback
        print(f"❌ Error cargando datos desde Excel: {e}")
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    # Ejecutar inicialización de forma independiente
    init_db()
    
    # Cargar datos desde Excel si existe
    print("\n🔄 Verificando archivo Excel para cargar datos...")
    if os.path.exists("DB_Rutas.xlsx"):
        print("📋 Archivo DB_Rutas.xlsx encontrado")
        cargar_datos_excel()
    else:
        print("⚠️ No se encontró el archivo DB_Rutas.xlsx")
        print("⚠️ La aplicación no tendrá rutas disponibles")
