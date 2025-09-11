#!/usr/bin/env python3
"""
Instalación ultra-rápida para Google Colab
Solo instala lo esencial que no está preinstalado
"""

import subprocess
import sys

def quick_install():
    """Instalación mínima y rápida para Colab"""
    print("🚀 INSTALACIÓN RÁPIDA PARA COLAB")
    print("=" * 40)
    
    # Solo los paquetes realmente necesarios que no están en Colab
    essential_packages = [
        "onnxruntime-gpu",
        "insightface", 
        "opennsfw2",
        "gfpgan"
    ]
    
    for package in essential_packages:
        print(f"📦 Instalando {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package} instalado")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error instalando {package}: {e}")
    
    print("\n🔍 Verificando instalación...")
    
    # Verificar onnxruntime
    try:
        import onnxruntime
        providers = onnxruntime.get_available_providers()
        print(f"✅ ONNX Runtime OK - Providers: {providers}")
        
        if 'CUDAExecutionProvider' in providers:
            print("🚀 GPU CUDA detectada - ¡Listo para procesar!")
        else:
            print("⚠️ Solo CPU disponible")
            
    except ImportError:
        print("❌ ONNX Runtime falló - prueba instalar manualmente:")
        print("!pip install onnxruntime-gpu")
    
    print("\n✅ Instalación completada")
    print("💡 Ahora puedes ejecutar: !python colab_batch_processor.py")

if __name__ == "__main__":
    quick_install()