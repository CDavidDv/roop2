#!/usr/bin/env python3
"""
Script para instalar dependencias necesarias para el análisis automático de videos
"""

import subprocess
import sys
import os

def install_package(package):
    """Instala un paquete usando pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package):
    """Verifica si un paquete está instalado"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

def main():
    print("🔧 INSTALANDO DEPENDENCIAS PARA ANÁLISIS AUTOMÁTICO")
    print("=" * 60)
    
    # Lista de paquetes necesarios
    packages = [
        ("opencv-python", "cv2", "Análisis de video y detección de rostros"),
        ("numpy", "numpy", "Procesamiento numérico"),
    ]
    
    print("📦 Verificando paquetes necesarios...")
    print()
    
    all_installed = True
    
    for package_name, import_name, description in packages:
        print(f"🔍 Verificando {package_name}...")
        
        if check_package(import_name):
            print(f"   ✅ {package_name} ya está instalado")
        else:
            print(f"   📦 Instalando {package_name}...")
            if install_package(package_name):
                print(f"   ✅ {package_name} instalado correctamente")
            else:
                print(f"   ❌ Error instalando {package_name}")
                all_installed = False
    
    print()
    
    if all_installed:
        print("✅ TODAS LAS DEPENDENCIAS INSTALADAS")
        print("=" * 60)
        print("🎉 El análisis automático está listo para usar!")
        print()
        print("📊 COMANDOS DISPONIBLES:")
        print("  python batch_processor.py          - Procesar videos con análisis automático")
        print("  python face_config.py analyze      - Analizar todos los videos")
        print("  python video_analyzer.py <video>   - Analizar un video específico")
        print("  python show_config.py              - Ver configuración actual")
        print()
        print("💡 El sistema ahora detectará automáticamente:")
        print("   • Número de rostros en el video")
        print("   • Tamaño de los rostros")
        print("   • Calidad del video")
        print("   • Duración del video")
        print("   • Y configurará los parámetros óptimos")
    else:
        print("❌ ALGUNAS DEPENDENCIAS NO SE PUDIERON INSTALAR")
        print("=" * 60)
        print("💡 Puedes instalar manualmente:")
        print("   pip install opencv-python numpy")
        print()
        print("⚠️  El análisis automático no estará disponible")
        print("   Pero el procesamiento manual seguirá funcionando")

if __name__ == "__main__":
    main() 