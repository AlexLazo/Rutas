#!/usr/bin/env python3
"""
Inicio HÍBRIDO para Railway - Intenta usar PORT pero con respaldo
"""

import os
import sys
from app import app

# SOLUCIÓN HÍBRIDA: Intentar Railway PORT, si falla usar puerto fijo
def get_safe_port():
    # Obtener la variable PORT
    port_var = os.environ.get('PORT')
    
    print(f"� Variable PORT detectada: '{port_var}'")
    
    # Si PORT no existe, usar puerto por defecto
    if port_var is None:
        print("⚠️ PORT no definida, usando 5000")
        return 5000
    
    # Si PORT es literalmente '$PORT', usar puerto por defecto  
    if port_var == '$PORT':
        print("⚠️ PORT es literalmente '$PORT', usando 5000")
        return 5000
    
    # Si PORT está vacía, usar puerto por defecto
    if port_var.strip() == '':
        print("⚠️ PORT está vacía, usando 5000")
        return 5000
    
    # Intentar convertir PORT a número
    try:
        port_num = int(port_var)
        if 1000 <= port_num <= 65535:
            print(f"✅ Usando puerto Railway: {port_num}")
            return port_num
        else:
            print(f"⚠️ Puerto {port_num} fuera de rango, usando 5000")
            return 5000
    except:
        print(f"⚠️ No se puede convertir '{port_var}' a número, usando 5000")
        return 5000

# Obtener puerto seguro
PORT = get_safe_port()

print(f"🚀 Iniciando app en puerto: {PORT}")

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT, debug=False)
