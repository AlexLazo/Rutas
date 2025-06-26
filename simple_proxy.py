#!/usr/bin/env python

"""
Simple HTTP Proxy para acceder a tu aplicación Railway
-------------------------------------------------------

Este script crea un proxy HTTP simple que te permite acceder a tu aplicación
en Railway cuando está bloqueada por firewalls corporativos.

Instrucciones:
1. Instala las dependencias: pip install flask requests requests_toolbelt
2. Ejecuta este script: python simple_proxy.py  
3. Accede a tu aplicación en http://localhost:7000
"""

from flask import Flask, request, Response, session
import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = 'proxy-rutas-2024-local'

# Configuración
TARGET_URL = 'https://formulario-rutas.up.railway.app'
LOCAL_PORT = 7000

# Crear sesión persistente para mantener cookies
s = requests.Session()

# Opcional: Usar una dirección IP específica para las conexiones salientes
# s.mount('http://', SourceAddressAdapter(('0.0.0.0', 0)))
# s.mount('https://', SourceAddressAdapter(('0.0.0.0', 0)))

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def proxy(path):
    """Proxy all requests to the target server"""
    # Print request details for debugging
    print(f"\n[{request.method}] {request.url}")
    
    # Build target URL
    target_url = f"{TARGET_URL}/{path}"
    if request.query_string:
        target_url = f"{target_url}?{request.query_string.decode('utf-8')}"
    
    print(f"Forwarding to: {target_url}")
    
    # Copy headers from original request but make some changes
    headers = dict(request.headers)
    if 'Host' in headers:
        headers['Host'] = urllib.parse.urlparse(TARGET_URL).netloc
    
    # Remove problematic headers
    for header in ['Content-Length', 'Transfer-Encoding']:
        if header in headers:
            del headers[header]
    
    try:
        # Forward the request to the target server
        resp = s.request(
            method=request.method,
            url=target_url,
            headers=headers,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,  # We'll handle redirects ourselves
            verify=True  # Set to False if target uses self-signed cert
        )
        
        # Process response
        response_headers = dict(resp.headers)
        
        # Handle redirects - replace remote URLs with localhost
        if resp.status_code in [301, 302, 303, 307, 308]:
            if 'Location' in response_headers:
                location = response_headers['Location']
                if location.startswith(TARGET_URL):
                    response_headers['Location'] = location.replace(
                        TARGET_URL, f"http://localhost:{LOCAL_PORT}")
                elif location.startswith('/'):
                    # Relative URL
                    response_headers['Location'] = f"http://localhost:{LOCAL_PORT}{location}"
        
        # Create response with content from target server
        response = Response(resp.content, resp.status_code)
        
        # Copy response headers from target server
        skip_headers = ['content-encoding', 'transfer-encoding', 'content-length']
        for name, value in response_headers.items():
            if name.lower() not in skip_headers:
                response.headers[name] = value
                
        print(f"Response: {resp.status_code}")
        return response
        
    except requests.RequestException as e:
        print(f"Error: {e}")
        return Response(f"Error accessing target server: {e}", 500)

if __name__ == '__main__':
    print("=" * 70)
    print(f"🚀 Proxy Simple para acceder a Railway")
    print(f"🌐 Destino: {TARGET_URL}")
    print(f"🌐 Local: http://localhost:{LOCAL_PORT}")
    print("=" * 70)
    print("📝 Recomendaciones:")
    print("1. Si tienes problemas, borra las cookies de tu navegador")
    print("2. Para la página de admin usa: http://localhost:7000/admin")
    print("3. Credenciales por defecto: admin / admin123")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=LOCAL_PORT)
