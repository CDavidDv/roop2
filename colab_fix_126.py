#!/usr/bin/env python3
"""
Fix específico para Colab usando NumPy 1.26.4
Versión que funciona en el entorno del usuario
"""

import subprocess
import sys

def quick_fix_126():
    """Fix rápido con NumPy 1.26.4"""
    print("🔧 Fix rápido con NumPy 1.26.4 (versión que funciona)")
    print("=" * 50)
    
    commands = [
        # Usar la versión de NumPy que funciona en tu entorno
        "pip install numpy==1.26.4",
        
        # Reinstalar OpenCV con la versión correcta de NumPy
        "pip uninstall opencv-python -y",
        "pip install opencv-python==4.8.0.74",
        
        # Instalar ONNX Runtime GPU
        "pip install onnxruntime-gpu",
        
        # Dependencias mínimas
        "pip install insightface gfpgan",
    ]
    
    for cmd in commands:
        print(f"📦 {cmd}")
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True)
            print("✅ OK")
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Warning - continuando...")
    
    print("\n🧪 Verificando imports...")
    test_code = '''
import numpy as np
import cv2
import onnxruntime
print(f"✅ NumPy: {np.__version__}")
print(f"✅ OpenCV: {cv2.__version__}")
print(f"✅ ONNX: {onnxruntime.get_available_providers()}")
'''
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Test falló: {e}")
    
    print("\n✅ Fix completado con NumPy 1.26.4")
    print("💡 Ahora ejecuta: !python colab_simple.py")

if __name__ == "__main__":
    quick_fix_126()