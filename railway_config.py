# Configuración específica para Railway
# Este archivo ayuda a manejar las variables de entorno de Railway

import os

def get_port():
    """Obtener puerto de manera segura para Railway"""
    port_env = os.environ.get('PORT', '5000')
    
    # CORRECCIÓN: Manejo más estricto de la variable '$PORT'
    if port_env == '$PORT' or not port_env or port_env == '':
        print(f"⚠️ PORT era '{port_env}' - valor inválido literal. Usando puerto 5000.")
        return 5000
    
    # Verificación más estricta de dígitos
    if not port_env.strip().isdigit():
        print(f"⚠️ PORT era '{port_env}' - no es numérico. Usando puerto 5000.")
        return 5000
    
    try:
        port = int(port_env)
        if 1000 <= port <= 65535:  # Rango válido de puertos
            return port
        else:
            print(f"⚠️ PORT era '{port_env}' - fuera de rango. Usando puerto 5000.")
            return 5000
    except (ValueError, TypeError):
        print(f"⚠️ Error convirtiendo PORT '{port_env}' a entero. Usando puerto 5000.")
        return 5000

def get_debug_mode():
    """Determinar si está en modo debug"""
    flask_env = os.environ.get('FLASK_ENV', '').lower()
    railway_env = os.environ.get('RAILWAY_ENVIRONMENT', '').lower()
    
    # En Railway, generalmente queremos production
    if railway_env == 'production' or flask_env == 'production':
        return False
    
    return True  # Por defecto debug para desarrollo

def print_env_info():
    """Imprimir información del entorno para debugging"""
    print("🔍 INFORMACIÓN DEL ENTORNO:")
    print(f"   PORT: '{os.environ.get('PORT', 'NOT_SET')}'")
    print(f"   FLASK_ENV: '{os.environ.get('FLASK_ENV', 'NOT_SET')}'")
    print(f"   RAILWAY_ENVIRONMENT: '{os.environ.get('RAILWAY_ENVIRONMENT', 'NOT_SET')}'")
    print(f"   PYTHON_VERSION: '{os.environ.get('PYTHON_VERSION', 'NOT_SET')}'")
    
    # Variables específicas de Railway
    railway_vars = [
        'RAILWAY_PROJECT_ID', 'RAILWAY_PROJECT_NAME', 'RAILWAY_SERVICE_ID',
        'RAILWAY_SERVICE_NAME', 'RAILWAY_DEPLOYMENT_ID', 'RAILWAY_REPLICA_ID'
    ]
    
    for var in railway_vars:
        value = os.environ.get(var, 'NOT_SET')
        if value != 'NOT_SET':
            print(f"   {var}: '{value[:20]}...' (truncated)")
