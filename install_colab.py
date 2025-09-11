#!/usr/bin/env python3
"""
Script de instalación automática para Google Colab
Instala todas las dependencias actualizadas para Python 3.12
"""

import subprocess
import sys

def install_dependencies():
    """Instala dependencias compatibles con Python 3.12"""
    
    print("🚀 Instalando dependencias actualizadas para Python 3.12...")
    
    # Lista de paquetes actualizados
    packages = [
        "numpy>=1.24.0",
        "opencv-python>=4.8.0", 
        "pillow>=10.0.0",
        "psutil>=5.9.0",
        "tqdm>=4.65.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "tensorflow>=2.13.0",
        "onnx>=1.14.0",
        "onnxruntime-gpu>=1.17.0",
        "insightface>=0.7.3",
        "gfpgan>=1.3.8",
        "protobuf>=4.21.0,<5.0.0",
        "opennsfw2>=0.10.2"
    ]
    
    # Instalar con pip
    cmd = [sys.executable, "-m", "pip", "install"] + packages
    
    try:
        print("📦 Ejecutando instalación...")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Dependencias instaladas exitosamente!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante la instalación: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def verify_installation():
    """Verifica que las dependencias se instalaron correctamente"""
    
    print("\n🔍 Verificando instalación...")
    
    critical_packages = [
        "numpy", "cv2", "torch", "tensorflow", 
        "onnxruntime", "insightface", "PIL"
    ]
    
    failed = []
    
    for package in critical_packages:
        try:
            if package == "cv2":
                import cv2
            elif package == "PIL":
                from PIL import Image
            else:
                __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️ Falló la importación de: {', '.join(failed)}")
        return False
    else:
        print("\n🎉 Todas las dependencias se importaron correctamente!")
        return True

if __name__ == "__main__":
    print("="*60)
    print("🎬 ROOP - Instalación automática para Colab")
    print("="*60)
    
    # Instalar dependencias
    if install_dependencies():
        # Verificar instalación
        verify_installation()
        print("\n🚀 ¡Listo para usar ROOP en Colab!")
    else:
        print("\n❌ Instalación fallida. Revisa los errores arriba.")