#!/usr/bin/env python3
"""
Script de inicio robusto para Railway
Maneja variables de entorno y configuración específica
"""

import os
import sys

def setup_railway_environment():
    """Configurar variables de entorno para Railway"""
    
    # Si PORT no está definida o es '$PORT', usar 5000
    port = os.environ.get('PORT', '5000')
    if port == '$PORT' or not port.isdigit():
        os.environ['PORT'] = '5000'
        print(f"⚠️ PORT era '{port}', establecida a 5000")
    
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
        
        port = int(os.environ.get('PORT', 5000))
        debug_mode = os.environ.get('FLASK_ENV') != 'production'
        
        print(f"🌐 Servidor iniciando en puerto: {port}")
        print(f"🔧 Debug mode: {debug_mode}")
        
        # Ejecutar aplicación
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
