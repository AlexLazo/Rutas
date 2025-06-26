# Railway - Variables y configuraciones de entorno

import os
import pytz

# Zona horaria para Guatemala
TIMEZONE = pytz.timezone('America/Guatemala')

# Configuración de Railway
IS_RAILWAY = os.environ.get('RAILWAY', False)
RAILWAY_STATIC_URL = os.environ.get('RAILWAY_STATIC_URL', '')

# Configuración de base de datos
DB_PATH = os.environ.get('DB_PATH', 'sistema_rutas.db')

# Configuración de la aplicación
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
PORT = int(os.environ.get('PORT', 5000))
ENV = os.environ.get('ENVIRONMENT', 'production')
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-rutas-2024')

# Configuración de servidor
SERVER_TIMEOUT = int(os.environ.get('SERVER_TIMEOUT', 120))
MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 4))
SERVER_THREADS = int(os.environ.get('SERVER_THREADS', 4))

# Configuraciones para entorno serverless
SERVERLESS = True  # Railway utiliza un modelo serverless
DB_CONNECTION_TIMEOUT = 30
MAX_DB_RETRIES = 3
GRACEFUL_SHUTDOWN_TIMEOUT = 10

# Configuraciones para proxy inverso
PREFERRED_URL_SCHEME = 'https'
SERVER_NAME = None  # Railway asigna automáticamente

# URLs externas permitidas para CORS
ALLOWED_ORIGINS = [
    'https://formulario-rutas.lat',
    'https://*.up.railway.app'
]

# Headers adicionales para seguridad
ADDITIONAL_HEADERS = {
    'X-Enterprise-System': 'Sistema-Gestion-Rutas',
    'X-Company-Domain': 'distribuidora-corporativa.com',
    'X-Corporate-Network': 'INTERNAL',
    'X-System-Environment': 'PRODUCTION-CORPORATE',
    'X-Authentication-Provider': 'ActiveDirectory-Enterprise',
    'X-Corporate-Gateway': 'CORP-DMZ-01',
    'X-Internal-Service': 'Route-Management-System',
    'X-Division': 'Logistica-Distribucion',
    'X-Region': 'CENTROAMERICA',
    'X-System-ID': 'RMS-CORP-2024',
    'X-Corporate-Auth': 'Integrated-Windows-Auth'
}
