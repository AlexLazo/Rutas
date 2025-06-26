# Configuración del sistema - Sistema de Gestión de Rutas AB InBev
import os

class Config:
    # Configuración de la base de datos
    DATABASE_PATH = 'sistema_rutas.db'
    
    # Configuración del servidor - SOLUCIÓN PARA RAILWAY
    HOST = '0.0.0.0'  # Permitir conexiones desde cualquier IP
    DEBUG = False  # Por defecto producción
    
    def __init__(self):
        self.PORT = self.get_safe_port()  # Puerto dinámico para Railway
    
    # Configuración de Flask
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-rutas-2024')
    
    # Configuración de mapas y geolocalización
    DEFAULT_MAP_CENTER = {
        'lat': 14.6349,  # Guatemala
        'lng': -90.5069,
        'zoom': 13
    }
    
    # Configuración de geocodificación
    GEOCODING_SERVICE = 'nominatim'  # nominatim, google, mapbox
    
    # API Keys (si usas servicios externos)
    GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
    MAPBOX_ACCESS_TOKEN = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
    
    # Configuración de archivos
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB máximo
    
    # Estados permitidos para reportes de rutas
    REPORT_STATUSES = [
        'pendiente',
        'en-proceso', 
        'completado',
        'rechazado'
    ]
    
    # Configuración de exportación
    EXPORT_FORMATS = ['json', 'csv', 'xlsx']
    
    # Configuración de usuarios por defecto
    DEFAULT_USERS = [
        {'username': 'admin', 'password': 'admin123', 'role': 'admin'},
        {'username': 'supervisor', 'password': 'supervisor123', 'role': 'supervisor'}
    ]
    
    # Configuración de zona horaria
    TIMEZONE = os.environ.get('TZ', 'America/Guatemala')
    
    @staticmethod
    def init_app(app):
        """Inicializar configuración en la app Flask"""
        app.config.from_object(Config)
        
        # Crear carpetas necesarias
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Configurar zona horaria
        os.environ.setdefault('TZ', Config.TIMEZONE)

    @staticmethod
    def get_safe_port():
        """Obtener puerto de manera segura para Railway"""
        port_var = os.environ.get('PORT')
        
        print(f"🔍 Variable PORT detectada: '{port_var}'")
        
        # Si PORT no existe, usar puerto por defecto
        if port_var is None:
            print("⚠️ PORT no definida, usando 5000")
            return 5000
        
        # Si PORT es literalmente '$PORT', usar puerto por defecto  
        if port_var == '$PORT':
            print("⚠️ PORT es literalmente '$PORT', usando 5000")
            return 5000
        
        # Si PORT está vacía, usar puerto por defecto
        if str(port_var).strip() == '':
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
        except (ValueError, TypeError):
            print(f"⚠️ No se puede convertir '{port_var}' a número, usando 5000")
            return 5000

# Configuraciones específicas por entorno
class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'
    
    def __init__(self):
        super().__init__()
        self.PORT = 5000

class ProductionConfig(Config):
    DEBUG = False
    HOST = '0.0.0.0'
    
    def __init__(self):
        super().__init__()
        self.PORT = Config.get_safe_port()  # Puerto dinámico seguro para Railway
    
    # Configuración de seguridad para producción
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-producción-2024'

class RailwayConfig(ProductionConfig):
    """Configuración específica para Railway"""
    DEBUG = False
    HOST = '0.0.0.0'
    
    def __init__(self):
        super().__init__()
        self.PORT = self.get_safe_port()
    
    def get_port(self):
        """Método especializado para obtener puerto en Railway"""
        return self.get_safe_port()

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ':memory:'  # Base de datos en memoria para tests
    
    def __init__(self):
        super().__init__()
        self.PORT = 5001

# Detectar entorno automáticamente
def get_config():
    """Detectar y retornar la configuración apropiada"""
    # Detectar Railway
    if os.environ.get('RAILWAY_ENVIRONMENT'):
        print("🚂 Detectado entorno Railway")
        return RailwayConfig
    
    # Detectar Render
    elif os.environ.get('RENDER'):
        print("🌐 Detectado entorno Render")
        return ProductionConfig
    
    # Detectar modo de pruebas
    elif os.environ.get('TESTING') == 'true':
        print("🧪 Detectado entorno de pruebas")
        return TestingConfig
    
    # Detectar desarrollo
    elif os.environ.get('FLASK_ENV') == 'development':
        print("🔧 Detectado entorno de desarrollo")
        return DevelopmentConfig
    
    # Por defecto, usar configuración de desarrollo
    else:
        print("📝 Usando configuración por defecto (desarrollo)")
        return DevelopmentConfig

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'railway': RailwayConfig,
    'testing': TestingConfig,
    'default': get_config()
}
