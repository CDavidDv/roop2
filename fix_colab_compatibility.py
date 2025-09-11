#!/usr/bin/env python3
"""
Script para solucionar problemas de compatibilidad en Google Colab
"""

import subprocess
import sys
import os

def fix_numpy_compatibility():
    """Arregla el problema de NumPy 2.x"""
    print("🔧 Solucionando compatibilidad de NumPy...")
    
    commands = [
        # Downgrade a NumPy 1.x para compatibilidad
        "pip install 'numpy<2.0'",
        
        # Reinstalar OpenCV con NumPy correcto
        "pip uninstall opencv-python -y",
        "pip install opencv-python",
        
        # Asegurar TensorFlow compatible
        "pip install 'tensorflow>=2.13.0,<2.16.0'",
    ]
    
    for cmd in commands:
        print(f"📦 Ejecutando: {cmd}")
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True)
            print("✅ Comando exitoso")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning en: {cmd}")
    
    print("✅ NumPy compatibility fix aplicado")

def install_missing_packages():
    """Instala paquetes faltantes específicos para Colab"""
    print("📦 Instalando paquetes faltantes...")
    
    packages = [
        "onnxruntime-gpu",
        "insightface", 
        "opennsfw2",
        "gfpgan",
        # NO instalar customtkinter (GUI no necesario en Colab)
    ]
    
    for package in packages:
        print(f"📦 Instalando {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning instalando {package}")

def verify_installation():
    """Verifica que todo esté funcionando"""
    print("🔍 Verificando instalación...")
    
    # Test NumPy
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} OK")
    except Exception as e:
        print(f"❌ NumPy error: {e}")
    
    # Test OpenCV
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} OK")
    except Exception as e:
        print(f"❌ OpenCV error: {e}")
    
    # Test ONNX Runtime
    try:
        import onnxruntime
        providers = onnxruntime.get_available_providers()
        print(f"✅ ONNX Runtime OK - Providers: {providers}")
    except Exception as e:
        print(f"❌ ONNX Runtime error: {e}")
    
    # Test TensorFlow
    try:
        import tensorflow as tf
        print(f"✅ TensorFlow {tf.__version__} OK")
    except Exception as e:
        print(f"❌ TensorFlow error: {e}")

def main():
    print("🚀" * 50)
    print("🔧 SOLUCIONADOR DE COMPATIBILIDAD COLAB")
    print("🚀" * 50)
    
    fix_numpy_compatibility()
    print()
    
    install_missing_packages()
    print()
    
    verify_installation()
    print()
    
    print("✅ Fix de compatibilidad completado")
    print("💡 Ahora ejecuta: !python colab_batch_processor.py")

if __name__ == "__main__":
    main()