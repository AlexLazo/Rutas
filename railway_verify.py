#!/usr/bin/env python3
"""
Script para verificar localmente que la aplicación está lista
para Railway y que maneja correctamente el error $PORT
"""

import os
import subprocess
import sys
import time
import requests

def test_port_error():
    """Probar el manejo del error $PORT"""
    print("\n🔍 PRUEBA DE ERROR $PORT:")
    
    # Guardar el valor original de PORT si existe
    original_port = os.environ.get('PORT')
    
    try:
        # Establecer PORT a $PORT para simular el error
        os.environ['PORT'] = '$PORT'
        print("   ✅ Establecida variable PORT='$PORT'")
        
        # Ejecutar railway_check.py para diagnóstico
        print("\n   🔄 Ejecutando diagnóstico railway_check.py...")
        subprocess.run([sys.executable, 'railway_check.py'], check=False)
        
        # Probar railway_fix.py
        print("\n   🔄 Probando railway_fix.py...")
        subprocess.run([sys.executable, 'railway_fix.py'], check=False)
        
        # Iniciar aplicación en segundo plano para prueba
        print("\n   🔄 Probando railway_start.py (por 5 segundos)...")
        proc = subprocess.Popen(
            [sys.executable, 'railway_start.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Esperar un poco para que la aplicación arranque
        time.sleep(5)
        
        # Verificar si la aplicación está respondiendo
        try:
            response = requests.get('http://localhost:5000')
            print(f"   ✅ La aplicación respondió con código: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️ No se pudo conectar a la aplicación: {e}")
        
        # Terminar el proceso
        proc.terminate()
        stdout, stderr = proc.communicate()
        
        # Mostrar la salida
        print("\n   📋 SALIDA DEL PROCESO:")
        for line in stdout.split('\n')[:20]:  # Mostrar solo las primeras 20 líneas
            if line.strip():
                print(f"   {line}")
        
        if "❌" in stdout or "error" in stdout.lower():
            print("\n   ❌ Se encontraron errores en la salida")
        else:
            print("\n   ✅ No se encontraron errores en la salida")
            
    finally:
        # Restaurar PORT original si existía
        if original_port is not None:
            os.environ['PORT'] = original_port
        else:
            os.environ.pop('PORT', None)

def check_files():
    """Verificar que todos los archivos necesarios existen"""
    print("\n📋 VERIFICANDO ARCHIVOS:")
    
    required_files = [
        'railway_start.py',
        'railway_config.py',
        'railway_fix.py',
        'railway_check.py',
        'Procfile',
        'runtime.txt',
        'requirements.txt'
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - NO ENCONTRADO")

def check_procfile():
    """Verificar el contenido del Procfile"""
    print("\n📄 VERIFICANDO PROCFILE:")
    
    try:
        with open('Procfile', 'r') as f:
            content = f.read().strip()
            
        if content == 'web: python railway_start.py':
            print("   ✅ Procfile tiene el contenido correcto")
        else:
            print(f"   ❌ Procfile incorrecto: '{content}'")
            print("      Debería ser: 'web: python railway_start.py'")
            
            # Corregir Procfile automáticamente
            print("   🔄 Corrigiendo Procfile...")
            with open('Procfile', 'w') as f:
                f.write('web: python railway_start.py\n')
            print("   ✅ Procfile corregido")
    except Exception as e:
        print(f"   ❌ Error al verificar Procfile: {e}")

if __name__ == "__main__":
    print("🚂 VERIFICACIÓN LOCAL PARA RAILWAY")
    check_files()
    check_procfile()
    test_port_error()
    print("\n✅ VERIFICACIÓN COMPLETADA")
    
    print("\n📋 RECOMENDACIONES:")
    print("   1. Ejecutar 'git add .' para incluir todos los archivos nuevos")
    print("   2. Ejecutar 'git commit -m \"Fix: Solución definitiva para error $PORT\"'")
    print("   3. Ejecutar 'git push' para subir los cambios a GitHub")
    print("   4. En Railway: forzar un redeploy completo")
