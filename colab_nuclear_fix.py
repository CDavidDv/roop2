#!/usr/bin/env python3
"""
Solución nuclear para problemas de NumPy/OpenCV en Colab
Reinstala todo desde cero
"""

import subprocess
import sys
import os

def nuclear_fix():
    """Reinstalación completa y limpia"""
    print("💥 SOLUCIÓN NUCLEAR - Reinstalando todo desde cero")
    print("🚨 Esto puede tomar 2-3 minutos...")
    
    commands = [
        # 1. Limpiar cache pip
        "pip cache purge",
        
        # 2. Desinstalar paquetes problemáticos
        "pip uninstall numpy opencv-python opencv-contrib-python cv2 -y",
        "pip uninstall tensorflow keras -y",
        "pip uninstall onnxruntime onnxruntime-gpu -y",
        
        # 3. Reinstalar en orden específico
        "pip install numpy==1.24.3",
        "pip install opencv-python==4.8.0.74",
        "pip install onnxruntime-gpu==1.15.1",
        
        # 4. Verificar compatibilidad
        "python -c 'import numpy; print(f\"NumPy: {numpy.__version__}\")'",
        "python -c 'import cv2; print(f\"OpenCV: {cv2.__version__}\")'",
        "python -c 'import onnxruntime; print(f\"ONNX: {onnxruntime.__version__}\")'",
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
            if "import" in cmd and result.returncode == 0:
                print(f"✅ {result.stdout.strip()}")
            elif result.returncode == 0:
                print("✅ OK")
            else:
                print(f"⚠️ Warning: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print("⏰ Timeout - continuando...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n💥 Fix nuclear completado")

def install_minimal_deps():
    """Instala solo dependencias mínimas"""
    print("📦 Instalando dependencias mínimas...")
    
    minimal_packages = [
        "insightface==0.7.3",
        "gfpgan==1.3.8", 
        "psutil",
        "tqdm",
    ]
    
    for package in minimal_packages:
        print(f"📦 {package}")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, timeout=120)
            print("✅ OK")
        except:
            print("⚠️ Falló - continuando...")

def test_imports():
    """Prueba los imports críticos"""
    print("\n🧪 Probando imports...")
    
    test_code = '''
try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except Exception as e:
    print(f"❌ NumPy: {e}")

try:
    import cv2
    print(f"✅ OpenCV {cv2.__version__}")
except Exception as e:
    print(f"❌ OpenCV: {e}")

try:
    import onnxruntime
    providers = onnxruntime.get_available_providers()
    print(f"✅ ONNX Runtime - Providers: {providers}")
except Exception as e:
    print(f"❌ ONNX Runtime: {e}")

try:
    import insightface
    print("✅ InsightFace OK")
except Exception as e:
    print(f"❌ InsightFace: {e}")
'''
    
    try:
        result = subprocess.run([sys.executable, "-c", test_code], 
                              capture_output=True, text=True, timeout=30)
        print(result.stdout)
        if result.stderr:
            print(f"Warnings: {result.stderr}")
    except Exception as e:
        print(f"❌ Error testing imports: {e}")

def main():
    print("💥" * 50)
    print("🚨 COLAB NUCLEAR FIX")
    print("💥" * 50)
    
    nuclear_fix()
    install_minimal_deps()
    test_imports()
    
    print("\n💥" * 50)
    print("🎯 INSTRUCCIONES POST-FIX:")
    print("💥" * 50)
    print("1. 🔄 REINICIA EL RUNTIME de Colab")
    print("2. 🚀 Ejecuta: !python colab_simple.py")
    print("💥" * 50)

if __name__ == "__main__":
    main()