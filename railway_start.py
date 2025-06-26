#!/usr/bin/env python3
"""
Script de inicio robusto para Railway
Maneja variables de entorno y configuración específica
NUEVA VERSIÓN: Solución para el error $PORT
"""

import os
import sys

# Importar nuevo módulo de corrección para $PORT
try:
    from railway_fix import fix_railway_port, print_environment
    RAILWAY_FIX_AVAILABLE = True
    print("✅ Módulo railway_fix importado correctamente")
except ImportError:
    RAILWAY_FIX_AVAILABLE = False
    print("⚠️ Módulo railway_fix no disponible, usando lógica básica")

def setup_railway_environment():
    """Configurar variables de entorno para Railway"""
    
    # SOLUCIÓN MEJORADA para el problema de $PORT
    if RAILWAY_FIX_AVAILABLE:
        # Usar la solución robusta del módulo railway_fix
        print("🛠️ Aplicando corrección avanzada para $PORT")
    else:
        # Lógica básica por si el módulo no está disponible
        port = os.environ.get('PORT', '5000')
        if port == '$PORT' or not port.isdigit():
            print(f"⚠️ PORT era '{port}' (literalmente). Usando 5000 como valor por defecto.")
    
    # Establecer modo producción en Railway
    if 'RAILWAY_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = 'production'
        print("🚂 Detectado Railway - Modo producción activado")
    
    # Configurar zona horaria
    if 'TZ' not in os.environ:
        os.environ['TZ'] = 'America/Guatemala'
    
    print("✅ Variables de entorno configuradas para Railway")

def main():
    """Función principal"""
    print("🚂 Iniciando aplicación en Railway...")
    
    # Configurar entorno
    setup_railway_environment()
    
    # Importar y ejecutar la aplicación
    try:
        from app import app
        
        # SOLUCIÓN DEFINITIVA: Usar el módulo de corrección especializado
        if RAILWAY_FIX_AVAILABLE:
            # Obtener puerto usando la solución robusta
            port = fix_railway_port()
            print(f"🔒 Puerto validado por railway_fix: {port}")
        else:
            # Lógica de respaldo más básica
            port_str = os.environ.get('PORT', '5000')
            if port_str == '$PORT' or not port_str.isdigit():
                port = 5000
                print(f"⚠️ Valor inválido en PORT: '{port_str}'. Usando puerto 5000 por defecto.")
            else:
                port = int(port_str)
        
        debug_mode = os.environ.get('FLASK_ENV') != 'production'
        
        print(f"🌐 Servidor iniciando en puerto: {port}")
        print(f"🔧 Debug mode: {debug_mode}")
        
        # Ejecutar aplicación - CON PUERTO GARANTIZADO
        app.run(
            debug=debug_mode,
            host='0.0.0.0', 
            port=port,
            use_reloader=False  # Evitar problemas en Railway
        )
        
    except Exception as e:
        print(f"❌ Error iniciando aplicación: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
