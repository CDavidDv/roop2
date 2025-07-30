#!/usr/bin/env python3
"""
Solución rápida para GPU en Google Colab
Configura GPU para face swap sin modificar código principal
"""

import os
import sys
import subprocess

def setup_colab_gpu():
    """Configurar GPU para Google Colab"""
    print("🚀 Configurando GPU para Google Colab...")
    
    # 1. Instalar dependencias GPU
    print("\n📦 Instalando dependencias GPU...")
    gpu_packages = [
        "onnxruntime-gpu==1.15.1",
        "tensorflow-gpu==2.13.0",
        "nvidia-ml-py3",
        "gputil"
    ]
    
    for package in gpu_packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package}")
        except:
            print(f"⚠️  {package} - puede estar ya instalado")
    
    # 2. Configurar variables de entorno
    print("\n⚙️  Configurando variables de entorno...")
    os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
    os.environ['CUDA_VISIBLE_DEVICES'] = '0'
    
    # 3. Configurar TensorFlow GPU
    print("\n💾 Configurando memoria GPU...")
    try:
        import tensorflow as tf
        
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            # Configurar memoria para Tesla T4 (15GB VRAM)
            # Usar 12GB para dejar espacio al sistema
            memory_limit = 12288  # 12GB en MB
            
            for gpu in gpus:
                tf.config.experimental.set_virtual_device_configuration(
                    gpu,
                    [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=memory_limit)]
                )
            print(f"✅ GPU configurada con {memory_limit}MB")
        else:
            print("⚠️  No se detectaron GPUs")
            
    except Exception as e:
        print(f"⚠️  Error configurando TensorFlow: {e}")
    
    print("\n✅ Configuración GPU completada!")

def create_gpu_patch():
    """Crear parche para forzar uso de GPU"""
    print("\n🔧 Creando parche GPU...")
    
    patch_code = '''
# Parche GPU para Google Colab
import os
import onnxruntime
import tensorflow as tf

# Configurar variables de entorno
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Configurar TensorFlow GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_virtual_device_configuration(
            gpu,
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=12288)]
        )

# Función para obtener providers optimizados
def get_gpu_providers():
    providers = onnxruntime.get_available_providers()
    if 'CUDAExecutionProvider' in providers:
        return ['CUDAExecutionProvider', 'CPUExecutionProvider']
    return ['CPUExecutionProvider']

print("🎯 GPU configurada para face swap")
'''
    
    with open('gpu_patch.py', 'w') as f:
        f.write(patch_code)
    
    print("✅ Archivo gpu_patch.py creado")

def test_gpu_setup():
    """Probar configuración GPU"""
    print("\n🧪 Probando configuración GPU...")
    
    try:
        # Test ONNX Runtime
        import onnxruntime
        providers = onnxruntime.get_available_providers()
        onnx_ok = 'CUDAExecutionProvider' in providers
        
        # Test TensorFlow
        import tensorflow as tf
        gpus = tf.config.experimental.list_physical_devices('GPU')
        tf_ok = len(gpus) > 0
        
        print(f"ONNX CUDA: {'✅' if onnx_ok else '❌'}")
        print(f"TensorFlow GPU: {'✅' if tf_ok else '❌'}")
        
        return onnx_ok and tf_ok
        
    except Exception as e:
        print(f"❌ Error en prueba: {e}")
        return False

def show_usage_instructions():
    """Mostrar instrucciones de uso"""
    print("\n" + "=" * 60)
    print("📋 INSTRUCCIONES DE USO")
    print("=" * 60)
    
    print("""
Para usar GPU en tu face swap:

1. ANTES de ejecutar tu script principal, ejecuta:
   ```python
   from gpu_patch import get_gpu_providers
   ```

2. En tu código, reemplaza las configuraciones de providers:
   ```python
   # En lugar de usar providers por defecto
   providers = get_gpu_providers()
   ```

3. Para verificar que funciona:
   ```python
   python test_colab_gpu.py
   ```

4. Si hay problemas:
   - Reinicia el runtime de Colab
   - Ejecuta: !nvidia-smi
   - Verifica que tengas GPU asignada
   """)

def main():
    """Función principal"""
    print("🎯 CONFIGURACIÓN GPU PARA GOOGLE COLAB")
    print("=" * 50)
    
    # Configurar GPU
    setup_colab_gpu()
    
    # Crear parche
    create_gpu_patch()
    
    # Probar configuración
    gpu_ok = test_gpu_setup()
    
    # Mostrar instrucciones
    show_usage_instructions()
    
    if gpu_ok:
        print("\n🎉 ¡GPU configurada correctamente!")
        print("✅ Puedes usar face swap con GPU")
    else:
        print("\n⚠️  Problemas detectados")
        print("🔧 Revisa las instrucciones de solución")

if __name__ == "__main__":
    main() 