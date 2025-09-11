#!/usr/bin/env python3
"""
Setup optimizado para Google Colab
Configura ROOP con dependencias actualizadas para Python 3.12
"""

import os
import sys
import subprocess
import importlib.util

def check_python_version():
    """Verifica la versión de Python"""
    python_version = sys.version_info
    print(f"🐍 Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 10:
        print("✅ Versión de Python compatible")
        return True
    else:
        print("❌ Se requiere Python 3.10 o superior")
        return False

def install_requirements():
    """Instala requirements optimizados para Colab"""
    print("\n📦 Instalando dependencias optimizadas...")
    
    # Comando de instalación optimizado para Colab
    cmd = """
    pip install --quiet --no-warn-script-location \
        numpy>=1.24.0 \
        opencv-python>=4.8.0 \
        pillow>=10.0.0 \
        psutil>=5.9.0 \
        tqdm>=4.65.0 \
        torch>=2.0.0 \
        torchvision>=0.15.0 \
        tensorflow>=2.13.0 \
        onnx>=1.14.0 \
        "onnxruntime-gpu>=1.17.0" \
        insightface>=0.7.3 \
        gfpgan>=1.3.8 \
        "protobuf>=4.21.0,<5.0.0" \
        opennsfw2>=0.10.2
    """
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        print(f"Salida: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def verify_cuda():
    """Verifica disponibilidad de CUDA"""
    print("\n🚀 Verificando CUDA...")
    
    try:
        import torch
        if torch.cuda.is_available():
            device = torch.cuda.get_device_name(0)
            memory = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ CUDA disponible: {device}")
            print(f"💾 Memoria GPU: {memory:.1f}GB")
            return True
        else:
            print("⚠️ CUDA no disponible, usando CPU")
            return False
    except ImportError:
        print("❌ PyTorch no instalado correctamente")
        return False

def verify_onnxruntime():
    """Verifica ONNX Runtime GPU"""
    print("\n🔧 Verificando ONNX Runtime...")
    
    try:
        import onnxruntime as ort
        providers = ort.get_available_providers()
        print(f"📋 Providers disponibles: {providers}")
        
        if 'CUDAExecutionProvider' in providers:
            print("✅ ONNX Runtime GPU disponible")
            return True
        else:
            print("⚠️ ONNX Runtime GPU no disponible")
            return False
    except ImportError:
        print("❌ ONNX Runtime no instalado")
        return False

def verify_insightface():
    """Verifica InsightFace"""
    print("\n👤 Verificando InsightFace...")
    
    try:
        import insightface
        print("✅ InsightFace importado correctamente")
        return True
    except ImportError as e:
        print(f"❌ Error importando InsightFace: {e}")
        return False

def setup_environment():
    """Configura variables de entorno"""
    print("\n⚙️ Configurando ambiente...")
    
    # Optimizaciones de memoria
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['MKL_NUM_THREADS'] = '1' 
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    
    # Reducir logs de TensorFlow
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    print("✅ Variables de entorno configuradas")

def create_directories():
    """Crea directorios necesarios"""
    print("\n📁 Creando directorios...")
    
    directories = ['source', 'videos_input', 'videos_output', 'models']
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📂 {directory}/")
    
    print("✅ Directorios creados")

def main():
    """Función principal de setup"""
    print("="*60)
    print("🎬 ROOP - Setup para Google Colab (Python 3.12)")
    print("="*60)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependencias
    if not install_requirements():
        return False
    
    # Configurar ambiente
    setup_environment()
    
    # Crear directorios
    create_directories()
    
    # Verificaciones
    cuda_ok = verify_cuda()
    onnx_ok = verify_onnxruntime()
    face_ok = verify_insightface()
    
    print("\n" + "="*60)
    print("🎉 SETUP COMPLETADO")
    print("="*60)
    
    if cuda_ok and onnx_ok and face_ok:
        print("✅ Todo configurado correctamente!")
        print("\n🚀 Listo para usar ROOP:")
        print("   • Coloca imagen fuente en: source/")
        print("   • Coloca videos en: videos_input/")
        print("   • Ejecuta: !python batch_processor.py --auto")
        return True
    else:
        print("⚠️ Algunas verificaciones fallaron")
        print("   El sistema puede funcionar con limitaciones")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ ¡Setup exitoso!")
    else:
        print("\n❌ Setup incompleto, revisa los errores arriba")