#!/usr/bin/env python3
"""
Instalador específico para Google Colab con Tesla T4
Instala todas las dependencias necesarias para ROOP
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    print("🚀" * 50)
    print("🎬 INSTALADOR ROOP PARA GOOGLE COLAB 🎬")
    print("🚀" * 50)
    print("🎯 Optimizado para Tesla T4")
    print("🚀" * 50)
    
    # Lista de comandos a ejecutar (sin versiones fijas para evitar conflictos)
    commands = [
        # Actualizar pip
        ("pip install --upgrade pip", "Actualizando pip"),
        
        # Instalar onnxruntime-gpu específicamente (lo más importante)
        ("pip install onnxruntime-gpu", "Instalando ONNX Runtime GPU"),
        
        # Instalar dependencias que no están en Colab o versiones muy viejas
        ("pip install opencv-python", "Instalando OpenCV"),
        ("pip install insightface", "Instalando InsightFace"),
        ("pip install opennsfw2", "Instalando OpenNSFW2"),
        ("pip install gfpgan", "Instalando GFPGAN"),
        ("pip install moviepy", "Instalando MoviePy para análisis de video"),
        
        # Solo instalar si realmente no están disponibles
        ("pip install --upgrade psutil", "Actualizando psutil"),
        ("pip install --upgrade tqdm", "Actualizando tqdm"),
    ]
    
    # Ejecutar comandos
    success_count = 0
    total_count = len(commands)
    
    for command, description in commands:
        if run_command(command, description):
            success_count += 1
        print()  # Línea en blanco para separar
    
    print("🚀" * 50)
    print("📊 RESUMEN DE INSTALACIÓN")
    print("🚀" * 50)
    print(f"✅ Comandos exitosos: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("🎉 ¡INSTALACIÓN COMPLETADA EXITOSAMENTE!")
        print("💡 Ahora puedes usar:")
        print("   • python batch_processor.py")
        print("   • python colab_batch_processor.py")
        print("   • python test_cuda.py (para verificar GPU)")
    else:
        print("⚠️  Algunos paquetes fallaron al instalarse")
        print("💡 Prueba ejecutar los comandos fallidos manualmente")
    
    print("🚀" * 50)
    
    # Verificar instalación
    print("🔍 Verificando instalación...")
    try:
        import onnxruntime
        print("✅ onnxruntime instalado correctamente")
        
        providers = onnxruntime.get_available_providers()
        print(f"🎯 Providers disponibles: {providers}")
        
        if 'CUDAExecutionProvider' in providers:
            print("🚀 CUDA disponible - ¡GPU Tesla T4 lista!")
        else:
            print("⚠️  CUDA no disponible - se usará CPU")
            
    except ImportError:
        print("❌ onnxruntime no se pudo importar")
        print("💡 Ejecuta: pip install onnxruntime-gpu==1.15.1")

if __name__ == "__main__":
    main()