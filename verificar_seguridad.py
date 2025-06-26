#!/usr/bin/env python

"""
Verificador de Seguridad de Headers para Railway
------------------------------------------------

Este script verifica los headers de seguridad de tu aplicación desplegada 
en Railway y genera un informe que puedes presentar al equipo de seguridad.

Requisitos:
- requests
- colorama (opcional, para salida en color)

Uso:
python verificar_seguridad.py
"""

import requests
import json
from datetime import datetime
try:
    from colorama import init, Fore, Style
    init()
    COLOR_ENABLED = True
except ImportError:
    COLOR_ENABLED = False

# Configuración
URL_TO_CHECK = "https://formulario-rutas.up.railway.app"
OUTPUT_FILE = "informe_seguridad.txt"

def color_print(text, color, bold=False):
    """Print colored text if colorama is available"""
    if COLOR_ENABLED:
        if bold:
            print(f"{color}{Style.BRIGHT}{text}{Style.RESET_ALL}")
        else:
            print(f"{color}{text}{Style.RESET_ALL}")
    else:
        print(text)

def check_security_headers(url):
    """Check security headers for a given URL"""
    print(f"Verificando headers de seguridad para: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers
        
        # Headers de seguridad esperados
        security_headers = {
            "Content-Security-Policy": {
                "present": "Content-Security-Policy" in headers,
                "value": headers.get("Content-Security-Policy", "No definido"),
                "importance": "Alta"
            },
            "Strict-Transport-Security": {
                "present": "Strict-Transport-Security" in headers,
                "value": headers.get("Strict-Transport-Security", "No definido"),
                "importance": "Alta"
            },
            "X-Content-Type-Options": {
                "present": "X-Content-Type-Options" in headers,
                "value": headers.get("X-Content-Type-Options", "No definido"),
                "importance": "Media"
            },
            "X-Frame-Options": {
                "present": "X-Frame-Options" in headers,
                "value": headers.get("X-Frame-Options", "No definido"),
                "importance": "Media"
            },
            "X-XSS-Protection": {
                "present": "X-XSS-Protection" in headers,
                "value": headers.get("X-XSS-Protection", "No definido"),
                "importance": "Media"
            },
            "Referrer-Policy": {
                "present": "Referrer-Policy" in headers,
                "value": headers.get("Referrer-Policy", "No definido"),
                "importance": "Media"
            },
            "Permissions-Policy": {
                "present": "Permissions-Policy" in headers,
                "value": headers.get("Permissions-Policy", "No definido"),
                "importance": "Baja"
            },
            "Cache-Control": {
                "present": "Cache-Control" in headers,
                "value": headers.get("Cache-Control", "No definido"),
                "importance": "Baja"
            }
        }
        
        # Verificar HTTPS
        https_enabled = url.startswith("https://")
        
        # Calcular puntuación
        score = 0
        max_score = 0
        
        for header, info in security_headers.items():
            weight = 3 if info["importance"] == "Alta" else 2 if info["importance"] == "Media" else 1
            max_score += weight
            if info["present"]:
                score += weight
        
        # Añadir HTTPS a la puntuación
        if https_enabled:
            score += 3
            max_score += 3
            
        # Calcular porcentaje
        percentage = (score / max_score) * 100
        
        # Determinar calificación
        grade = "A" if percentage >= 90 else "B" if percentage >= 70 else "C" if percentage >= 50 else "D" if percentage >= 30 else "F"
        
        return {
            "url": url,
            "https_enabled": https_enabled,
            "headers": security_headers,
            "score": score,
            "max_score": max_score,
            "percentage": percentage,
            "grade": grade,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    except requests.RequestException as e:
        return {
            "url": url,
            "error": str(e),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

def generate_report(results):
    """Generate a report based on the security check results"""
    with open(OUTPUT_FILE, "w") as f:
        f.write("==================================================\n")
        f.write("       INFORME DE SEGURIDAD PARA RAILWAY APP\n")
        f.write("==================================================\n\n")
        
        f.write(f"URL verificada: {results['url']}\n")
        f.write(f"Fecha y hora: {results['timestamp']}\n\n")
        
        if "error" in results:
            f.write(f"ERROR: {results['error']}\n")
            return
        
        f.write(f"Calificación de Seguridad: {results['grade']} ({results['percentage']:.1f}%)\n")
        f.write(f"Puntuación: {results['score']}/{results['max_score']}\n")
        f.write(f"HTTPS habilitado: {'SÍ' if results['https_enabled'] else 'NO'}\n\n")
        
        f.write("HEADERS DE SEGURIDAD\n")
        f.write("-----------------\n\n")
        
        for header, info in results["headers"].items():
            f.write(f"{header} (Importancia: {info['importance']})\n")
            f.write(f"  Presente: {'SÍ' if info['present'] else 'NO'}\n")
            f.write(f"  Valor: {info['value']}\n\n")
        
        f.write("==================================================\n")
        f.write("RECOMENDACIONES\n")
        f.write("==================================================\n\n")
        
        if not results["https_enabled"]:
            f.write("* CRÍTICO: Habilitar HTTPS para la aplicación\n")
        
        for header, info in results["headers"].items():
            if not info["present"] and info["importance"] == "Alta":
                f.write(f"* IMPORTANTE: Implementar el header {header}\n")
            elif not info["present"] and info["importance"] == "Media":
                f.write(f"* RECOMENDADO: Considerar implementar el header {header}\n")
        
        f.write("\n")
        f.write("Este informe puede ser presentado al equipo de seguridad\n")
        f.write("como parte de la justificación para la excepción de firewall.\n")

def print_results(results):
    """Print results to console"""
    if "error" in results:
        color_print(f"ERROR: {results['error']}", Fore.RED, bold=True)
        return
    
    color_print("\n===== RESULTADOS DEL ANÁLISIS DE SEGURIDAD =====", Fore.CYAN, bold=True)
    
    # Mostrar calificación
    grade_color = Fore.GREEN if results["grade"] in ["A", "B"] else Fore.YELLOW if results["grade"] == "C" else Fore.RED
    color_print(f"Calificación: {results['grade']} ({results['percentage']:.1f}%)", grade_color, bold=True)
    color_print(f"Puntuación: {results['score']}/{results['max_score']}", Fore.CYAN)
    
    # Mostrar HTTPS
    https_color = Fore.GREEN if results["https_enabled"] else Fore.RED
    https_text = "SÍ" if results["https_enabled"] else "NO"
    color_print(f"HTTPS habilitado: {https_text}", https_color)
    
    # Mostrar headers
    color_print("\nHeaders de seguridad:", Fore.CYAN, bold=True)
    for header, info in results["headers"].items():
        importance_color = Fore.RED if info["importance"] == "Alta" else Fore.YELLOW if info["importance"] == "Media" else Fore.WHITE
        color_print(f"{header} (Importancia: {info['importance']})", importance_color)
        
        present_color = Fore.GREEN if info["present"] else Fore.RED
        present_text = "SÍ" if info["present"] else "NO"
        color_print(f"  Presente: {present_text}", present_color)
        
        if info["present"]:
            color_print(f"  Valor: {info['value']}", Fore.WHITE)
        
        print()
    
    # Mostrar ruta del informe
    color_print(f"\nEl informe detallado se ha generado en: {OUTPUT_FILE}", Fore.CYAN)

if __name__ == "__main__":
    print("Verificador de Seguridad para Railway App")
    print("----------------------------------------")
    
    results = check_security_headers(URL_TO_CHECK)
    print_results(results)
    generate_report(results)
