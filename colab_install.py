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
    
    # Lista de comandos a ejecutar
    commands = [
        # Actualizar pip
        ("pip install --upgrade pip", "Actualizando pip"),
        
        # Instalar PyTorch con CUDA
        ("pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118", "Instalando PyTorch con CUDA 11.8"),
        
        # Instalar onnxruntime-gpu primero
        ("pip install onnxruntime-gpu==1.15.1", "Instalando ONNX Runtime GPU"),
        
        # Instalar dependencias básicas
        ("pip install numpy==1.24.3", "Instalando NumPy"),
        ("pip install opencv-python==4.8.0.74", "Instalando OpenCV"),
        ("pip install onnx==1.14.0", "Instalando ONNX"),
        ("pip install insightface==0.7.3", "Instalando InsightFace"),
        ("pip install psutil==5.9.5", "Instalando psutil"),
        ("pip install pillow==10.0.0", "Instalando Pillow"),
        ("pip install tensorflow==2.13.0", "Instalando TensorFlow"),
        ("pip install opennsfw2==0.10.2", "Instalando OpenNSFW2"),
        ("pip install protobuf==4.23.4", "Instalando Protobuf"),
        ("pip install tqdm==4.65.0", "Instalando tqdm"),
        ("pip install gfpgan==1.3.8", "Instalando GFPGAN"),
        
        # Dependencias adicionales para análisis automático
        ("pip install moviepy", "Instalando MoviePy para análisis de video"),
        ("pip install matplotlib", "Instalando Matplotlib para gráficos"),
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