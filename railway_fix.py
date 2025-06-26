#!/usr/bin/env python3
"""
CORRECCIÓN PARA EL ERROR '$PORT' EN RAILWAY
Este módulo soluciona el problema específico de la variable de entorno PORT
cuando viene como '$PORT' (string literal) en Railway.
"""

import os
import sys
import time
import socket

def get_valid_port():
    """
    Obtiene un puerto válido o usa 5000 como valor por defecto.
    Esta función es extremadamente defensiva contra el error '$PORT'.
    """
    port_value = os.environ.get('PORT')
    
    # Caso 1: PORT no está definido
    if port_value is None:
        print("⚠️ Variable PORT no definida. Usando puerto 5000.")
        return 5000
    
    # Caso 2: PORT es la cadena literal '$PORT'
    if port_value == '$PORT':
        print("⚠️ La variable PORT es literalmente '$PORT'. Usando puerto 5000.")
        return 5000
    
    # Caso 3: PORT está vacío
    if port_value.strip() == '':
        print("⚠️ La variable PORT está vacía. Usando puerto 5000.")
        return 5000
    
    # Caso 4: PORT no es un número
    if not port_value.strip().isdigit():
        print(f"⚠️ La variable PORT '{port_value}' no es un número. Usando puerto 5000.")
        return 5000
    
    # Caso 5: PORT está fuera del rango válido
    try:
        port_number = int(port_value)
        if not (1024 <= port_number <= 65535):
            print(f"⚠️ La variable PORT {port_number} está fuera del rango válido. Usando puerto 5000.")
            return 5000
        return port_number
    except (ValueError, TypeError):
        print(f"⚠️ Error al convertir PORT '{port_value}' a número. Usando puerto 5000.")
        return 5000

def print_environment():
    """
    Imprime información sobre el entorno para debugging.
    """
    print("\n🔍 INFORMACIÓN DEL ENTORNO RAILWAY:")
    print(f"   PORT: '{os.environ.get('PORT', 'NOT_SET')}'")
    print(f"   RAILWAY_ENVIRONMENT: '{os.environ.get('RAILWAY_ENVIRONMENT', 'NOT_SET')}'")
    print(f"   RAILWAY_PROJECT_ID: '{os.environ.get('RAILWAY_PROJECT_ID', 'NOT_SET')}'")
    print(f"   RAILWAY_SERVICE_ID: '{os.environ.get('RAILWAY_SERVICE_ID', 'NOT_SET')}'")
    print(f"   PYTHON_VERSION: '{sys.version}'")
    print("\n")

def is_port_available(port, host='0.0.0.0'):
    """
    Verifica si un puerto está disponible para usar.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind((host, port))
        available = True
    except:
        available = False
    sock.close()
    return available

def fix_railway_port():
    """
    Corrige problemas de puerto en Railway.
    Retorna el puerto correcto a usar.
    """
    print("\n🚂 INICIANDO CORRECCIÓN DE PUERTO PARA RAILWAY...")
    print_environment()
    
    # Obtener puerto válido
    port = get_valid_port()
    
    # Verificar disponibilidad
    if not is_port_available(port):
        print(f"⚠️ El puerto {port} no está disponible. Buscando alternativa...")
        # Probar puertos alternativos
        for alt_port in [8080, 8000, 3000, 5000, 5001]:
            if is_port_available(alt_port):
                print(f"✅ Puerto alternativo encontrado: {alt_port}")
                port = alt_port
                break
    
    print(f"🔄 Puerto final seleccionado: {port}")
    return port

if __name__ == "__main__":
    # Solo para pruebas
    print_environment()
    port = fix_railway_port()
    print(f"Puerto a usar: {port}")
