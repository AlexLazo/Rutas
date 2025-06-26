#!/usr/bin/env python3
"""
Script para verificar el entorno de Railway
y diagnosticar problemas con variables de entorno
"""

import os
import sys
import socket

def check_railway_env():
    """Verificar el entorno de Railway"""
    print("\n🔍 DIAGNÓSTICO DE RAILWAY:")
    
    # Verificar variable PORT
    port_value = os.environ.get('PORT')
    print(f"   PORT = '{port_value}'")
    
    if port_value is None:
        print("   ❌ La variable PORT no está definida")
    elif port_value == '$PORT':
        print("   ❌ La variable PORT es literalmente '$PORT' - ERROR DETECTADO")
    elif port_value.strip() == '':
        print("   ❌ La variable PORT está vacía")
    elif not port_value.strip().isdigit():
        print(f"   ❌ La variable PORT '{port_value}' no es un número")
    else:
        try:
            port_number = int(port_value)
            if 1024 <= port_number <= 65535:
                print(f"   ✅ La variable PORT {port_number} es válida")
            else:
                print(f"   ❌ La variable PORT {port_number} está fuera del rango válido (1024-65535)")
        except (ValueError, TypeError):
            print(f"   ❌ Error al convertir PORT '{port_value}' a número")
    
    # Verificar variables de Railway
    railway_vars = [
        'RAILWAY_ENVIRONMENT', 
        'RAILWAY_PROJECT_ID',
        'RAILWAY_SERVICE_ID',
        'RAILWAY_DEPLOYMENT_ID'
    ]
    
    found_railway = False
    for var in railway_vars:
        value = os.environ.get(var)
        if value:
            found_railway = True
            print(f"   ✅ {var} = '{value[:10]}...' (truncado)")
        else:
            print(f"   ❓ {var} no definida")
    
    if found_railway:
        print("   ✅ DETECTADO ENTORNO RAILWAY")
    else:
        print("   ❌ NO SE DETECTA ENTORNO RAILWAY")
    
    # Verificar Python
    print(f"   🐍 Python: {sys.version}")
    
    # Verificar sistema operativo
    print(f"   💻 Sistema: {sys.platform}")
    
    # Verificar puertos disponibles
    port_var = os.environ.get('PORT', '5000')
    try:
        if port_var == '$PORT' or not port_var.isdigit():
            port_number = 5000
        else:
            port_number = int(port_var)
    except:
        port_number = 5000
    
    check_ports = [port_number, 8080, 3000, 5000]
    print("\n🔌 VERIFICACIÓN DE PUERTOS:")
    for port in check_ports:
        if is_port_available(port):
            print(f"   ✅ Puerto {port} disponible")
        else:
            print(f"   ❌ Puerto {port} no disponible")

def is_port_available(port, host='0.0.0.0'):
    """Verificar si un puerto está disponible"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.close()
        return True
    except:
        return False

if __name__ == "__main__":
    check_railway_env()
    print("\n✅ DIAGNÓSTICO COMPLETADO")
    
    # Intentar iniciar un servidor de prueba
    port = int(os.environ.get('PORT', 5000))
    if port == '$PORT' or not is_port_available(port):
        port = 5000
    
    print(f"\n🔄 Iniciando servidor de prueba en puerto {port}...")
    print("   ℹ️ Presiona Ctrl+C para salir")
    
    try:
        # Servidor mínimo HTTP para pruebas
        import http.server
        import socketserver
        
        class TestHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Railway Test OK!</h1></body></html>")
        
        handler = TestHandler
        httpd = socketserver.TCPServer(("", port), handler)
        print(f"   ✅ Servidor iniciado en puerto {port}")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except Exception as e:
        print(f"\n❌ Error al iniciar servidor: {e}")
