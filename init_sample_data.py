"""
Script para inicializar datos de ejemplo sin necesidad de Excel
"""
import sqlite3
from datetime import datetime

def create_sample_data():
    """Crear datos de ejemplo para la aplicación"""
    conn = sqlite3.connect('sistema_rutas.db')
    cursor = conn.cursor()
    
    # Datos de ejemplo para rutas
    sample_routes = [
        ("Ruta 01", "GT001", "ABC-123", "Juan Pérez", "Transportes Guatemala", "Urbana"),
        ("Ruta 02", "GT002", "DEF-456", "María López", "Logística Central", "Interurbana"),
        ("Ruta 03", "GT003", "GHI-789", "Carlos Rodríguez", "Transportes Guatemala", "Urbana"),
        ("Ruta 04", "GT004", "JKL-012", "Ana Martínez", "Distribución Norte", "Rural"),
        ("Ruta 05", "GT005", "MNO-345", "Pedro Gómez", "Logística Central", "Interurbana"),
    ]
    
    print("📦 Insertando rutas de ejemplo...")
    for ruta_data in sample_routes:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO rutas (ruta, codigo, placa, supervisor, contratista, tipo)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ruta_data)
        except Exception as e:
            print(f"Error insertando ruta {ruta_data[0]}: {e}")
    
    # Datos de ejemplo para reportes
    sample_reports = [
        (1, "2024-01-15", "08:30", "Entrega completada sin problemas", "completado", "admin"),
        (2, "2024-01-15", "10:15", "Retraso por tráfico", "en-proceso", "supervisor"),
        (3, "2024-01-15", "14:20", "Ruta iniciada correctamente", "en-proceso", "admin"),
        (1, "2024-01-14", "09:00", "Entrega exitosa", "completado", "supervisor"),
        (4, "2024-01-15", "11:30", "Pendiente de confirmación", "pendiente", "admin"),
    ]
    
    print("📋 Insertando reportes de ejemplo...")
    for report_data in sample_reports:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO reportes_rutas 
                (ruta_id, fecha, hora, descripcion, estado, usuario_reporte)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', report_data)
        except Exception as e:
            print(f"Error insertando reporte: {e}")
    
    conn.commit()
    conn.close()
    print("✅ Datos de ejemplo creados correctamente")

if __name__ == "__main__":
    create_sample_data()
