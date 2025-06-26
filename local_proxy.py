#!/usr/bin/env python

"""
Local Proxy for Railway App
--------------------------
This script creates a local proxy server that forwards requests to your Railway app.
This can help bypass corporate firewalls since it appears as local traffic.

Requirements:
- flask
- requests

Usage:
1. Run this script on your local machine
2. Access your Railway app via http://localhost:8000
3. All requests will be forwarded to your Railway app
"""

import requests
from flask import Flask, request, Response, redirect
import os

app = Flask(__name__)

# Configure target URL - change this to your Railway app URL
TARGET_URL = "https://formulario-rutas.up.railway.app"
RAILWAY_BACKUP_URL = "https://formulario-rutas.lat"

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    """Forward all requests to the target URL"""
    target = f"{TARGET_URL}/{path}"
    
    # Forward request headers
    headers = {key: value for key, value in request.headers.items() 
               if key not in ['Host', 'Content-Length']}
    
    # Add cookie handling
    cookies = request.cookies
    
    try:
        # Forward the request with the same method
        if request.method == 'GET':
            response = requests.get(target, headers=headers, params=request.args, 
                                   cookies=cookies, allow_redirects=False, verify=False)
        elif request.method == 'POST':
            response = requests.post(target, headers=headers, data=request.get_data(), 
                                    cookies=cookies, allow_redirects=False, verify=False)
        elif request.method == 'PUT':
            response = requests.put(target, headers=headers, data=request.get_data(), 
                                   cookies=cookies, allow_redirects=False, verify=False)
        elif request.method == 'DELETE':
            response = requests.delete(target, headers=headers, cookies=cookies,
                                      allow_redirects=False, verify=False)
        else:
            return Response(f"Method {request.method} not supported", status=405)
        
    except requests.RequestException as e:
        print(f"Error connecting to primary URL: {str(e)}")
        print("Trying backup URL...")
        
        # Try backup URL if primary fails
        target = f"{RAILWAY_BACKUP_URL}/{path}"
        try:
            if request.method == 'GET':
                response = requests.get(target, headers=headers, params=request.args, 
                                      cookies=cookies, allow_redirects=False, verify=False)
            elif request.method == 'POST':
                response = requests.post(target, headers=headers, data=request.get_data(),
                                       cookies=cookies, allow_redirects=False, verify=False)
            else:
                return Response("Primary URL unavailable", status=503)
        except:
            return Response("Both primary and backup URLs unavailable", status=503)
        
    # Create response
    resp = Response(response.content, status=response.status_code)
    
    # Forward response headers
    for key, value in response.headers.items():
        if key.lower() not in ['content-encoding', 'content-length', 'transfer-encoding', 'connection']:
            resp.headers[key] = value
    
    # Handle redirects specially
    if response.status_code in [301, 302, 303, 307, 308]:
        # Get the Location header
        if 'Location' in response.headers:
            location = response.headers['Location']
            # Replace the remote domain with local domain in the location
            if TARGET_URL in location:
                new_location = location.replace(TARGET_URL, f"http://localhost:8000")
                resp.headers['Location'] = new_location
            elif RAILWAY_BACKUP_URL in location:
                new_location = location.replace(RAILWAY_BACKUP_URL, f"http://localhost:8000")
                resp.headers['Location'] = new_location
            # If the location is a relative path, keep it as is
    
    # Handle cookies specially
    if 'Set-Cookie' in response.headers:
        # Ensure cookies work with localhost
        resp.headers['Set-Cookie'] = response.headers['Set-Cookie'].replace('Domain='+TARGET_URL.split('//')[1], 'Domain=localhost')
    
    return resp

@app.before_request
def before_request():
    """Log the incoming request for debugging"""
    print(f"{request.method} {request.path}")
    if request.method == 'POST':
        print(f"POST data: {request.form}")
    if request.cookies:
        print(f"Cookies present: {list(request.cookies.keys())}")

if __name__ == '__main__':
    print("🚀 Starting local proxy server for Railway app")
    print(f"⚡ Primary URL: {TARGET_URL}")
    print(f"⚠️ Backup URL: {RAILWAY_BACKUP_URL}")
    print("🌐 Access your Railway app at http://localhost:8000")
    print("📝 Para usar el admin: http://localhost:8000/admin")
    print("🔑 Si hay problemas con el login, elimina las cookies del navegador")
    app.run(host='0.0.0.0', port=8000, debug=True)
