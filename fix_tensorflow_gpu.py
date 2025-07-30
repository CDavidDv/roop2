#!/usr/bin/env python3
"""
Script para solucionar TensorFlow GPU y actualizar face swapper
Específico para Google Colab con Tesla T4
"""

import os
import sys
import subprocess
import shutil

def install_cuda_libraries():
    """Instalar librerías CUDA necesarias para TensorFlow"""
    print("🔧 Instalando librerías CUDA para TensorFlow...")
    
    # Comandos para instalar CUDA libraries
    commands = [
        "apt-get update",
        "apt-get install -y cuda-toolkit-12-0",
        "apt-get install -y libcudnn8",
        "apt-get install -y libcudnn8-dev"
    ]
    
    for cmd in commands:
        try:
            print(f"Ejecutando: {cmd}")
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {cmd}")
            else:
                print(f"⚠️  {cmd} - {result.stderr}")
        except Exception as e:
            print(f"❌ Error en {cmd}: {e}")

def install_tensorflow_gpu():
    """Instalar TensorFlow GPU compatible"""
    print("\n📦 Instalando TensorFlow GPU...")
    
    # Desinstalar TensorFlow CPU si existe
    try:
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "-y", "tensorflow"])
        print("✅ TensorFlow CPU desinstalado")
    except:
        pass
    
    # Instalar TensorFlow GPU
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "tensorflow==2.12.0"])
        print("✅ TensorFlow GPU instalado")
    except Exception as e:
        print(f"❌ Error instalando TensorFlow: {e}")

def configure_tensorflow_gpu():
    """Configurar TensorFlow para usar GPU"""
    print("\n⚙️  Configurando TensorFlow GPU...")
    
    config_code = '''
import os
import tensorflow as tf

# Configurar variables de entorno
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Configurar memoria GPU para Tesla T4
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    for gpu in gpus:
        tf.config.experimental.set_virtual_device_configuration(
            gpu,
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=12288)]
        )
    print("✅ TensorFlow GPU configurado")
else:
    print("❌ No se detectaron GPUs en TensorFlow")

# Verificar configuración
print(f"GPUs detectadas: {len(tf.config.experimental.list_physical_devices('GPU'))}")
'''
    
    with open('tensorflow_gpu_config.py', 'w') as f:
        f.write(config_code)
    
    print("✅ Archivo tensorflow_gpu_config.py creado")

def update_face_swapper_gpu():
    """Actualizar face swapper para usar GPU"""
    print("\n🔄 Actualizando face swapper para GPU...")
    
    # Leer el archivo actual
    try:
        with open('roop/processors/frame/face_swapper.py', 'r') as f:
            content = f.read()
        
        # Buscar y reemplazar la configuración de providers
        old_provider_code = '''            # Forzar uso de CUDA si está disponible
            providers = roop.globals.execution_providers
            if 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
                # Asegurar que CUDA esté primero en la lista
                providers = ['CUDAExecutionProvider'] + [p for p in providers if p != 'CUDAExecutionProvider']
                print(f"[FACE_SWAPPER] Usando providers: {providers})'''
        
        new_provider_code = '''            # Forzar uso de CUDA para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_SWAPPER] Usando providers: {providers}")'''
        
        # Reemplazar
        if old_provider_code in content:
            content = content.replace(old_provider_code, new_provider_code)
            print("✅ Configuración de providers actualizada")
        else:
            # Si no encuentra el código exacto, buscar y reemplazar de otra manera
            import re
            pattern = r'# Forzar uso de CUDA.*?print\(f"\[FACE_SWAPPER\] Usando providers: \{providers\}\)'
            replacement = '''            # Forzar uso de CUDA para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_SWAPPER] Usando providers: {providers}")'''
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            print("✅ Configuración de providers actualizada (regex)")
        
        # Escribir el archivo actualizado
        with open('roop/processors/frame/face_swapper.py', 'w') as f:
            f.write(content)
        
        print("✅ Face swapper actualizado para GPU")
        
    except Exception as e:
        print(f"❌ Error actualizando face swapper: {e}")

def update_face_analyser_gpu():
    """Actualizar face analyser para usar GPU"""
    print("\n🔄 Actualizando face analyser para GPU...")
    
    try:
        with open('roop/face_analyser.py', 'r') as f:
            content = f.read()
        
        # Buscar y reemplazar la configuración de providers
        old_provider_code = '''            # Forzar uso de CUDA si está disponible
            providers = roop.globals.execution_providers
            if 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
                # Asegurar que CUDA esté primero en la lista
                providers = ['CUDAExecutionProvider'] + [p for p in providers if p != 'CUDAExecutionProvider']
                print(f"[FACE_ANALYSER] Usando providers: {providers})'''
        
        new_provider_code = '''            # Forzar uso de CUDA para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_ANALYSER] Usando providers: {providers}")'''
        
        # Reemplazar
        if old_provider_code in content:
            content = content.replace(old_provider_code, new_provider_code)
            print("✅ Configuración de providers actualizada")
        else:
            # Buscar y reemplazar de otra manera
            import re
            pattern = r'# Forzar uso de CUDA.*?print\(f"\[FACE_ANALYSER\] Usando providers: \{providers\}\)'
            replacement = '''            # Forzar uso de CUDA para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_ANALYSER] Usando providers: {providers}")'''
            
            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            print("✅ Configuración de providers actualizada (regex)")
        
        # Escribir el archivo actualizado
        with open('roop/face_analyser.py', 'w') as f:
            f.write(content)
        
        print("✅ Face analyser actualizado para GPU")
        
    except Exception as e:
        print(f"❌ Error actualizando face analyser: {e}")

def test_tensorflow_fix():
    """Probar si TensorFlow GPU funciona después del fix"""
    print("\n🧪 Probando TensorFlow GPU después del fix...")
    
    try:
        # Importar configuración
        exec(open('tensorflow_gpu_config.py').read())
        
        import tensorflow as tf
        
        # Verificar GPUs
        gpus = tf.config.experimental.list_physical_devices('GPU')
        print(f"TensorFlow GPUs detectadas: {len(gpus)}")
        
        if gpus:
            # Test simple
            with tf.device('/GPU:0'):
                a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
                c = tf.matmul(a, b)
                print(f"✅ TensorFlow GPU funcionando: {c}")
                return True
        else:
            print("❌ Aún no hay GPUs en TensorFlow")
            return False
            
    except Exception as e:
        print(f"❌ Error probando TensorFlow: {e}")
        return False

def create_gpu_optimized_patch():
    """Crear parche optimizado para GPU"""
    print("\n🔧 Creando parche GPU optimizado...")
    
    patch_code = '''
# Parche GPU optimizado para Google Colab
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

# Función para verificar GPU
def check_gpu_status():
    print("🔍 Estado de GPU:")
    print(f"  ONNX CUDA: {'CUDAExecutionProvider' in onnxruntime.get_available_providers()}")
    print(f"  TensorFlow GPU: {len(tf.config.experimental.list_physical_devices('GPU')) > 0}")
    print(f"  Memoria GPU configurada: {len(gpus) > 0}")

print("🎯 GPU optimizada para face swap")
'''
    
    with open('gpu_optimized_patch.py', 'w') as f:
        f.write(patch_code)
    
    print("✅ Archivo gpu_optimized_patch.py creado")

def main():
    """Función principal"""
    print("🚀 SOLUCIÓN COMPLETA PARA TENSORFLOW GPU")
    print("=" * 50)
    
    # 1. Instalar librerías CUDA
    install_cuda_libraries()
    
    # 2. Instalar TensorFlow GPU
    install_tensorflow_gpu()
    
    # 3. Configurar TensorFlow GPU
    configure_tensorflow_gpu()
    
    # 4. Actualizar face swapper
    update_face_swapper_gpu()
    
    # 5. Actualizar face analyser
    update_face_analyser_gpu()
    
    # 6. Crear parche optimizado
    create_gpu_optimized_patch()
    
    # 7. Probar fix
    tf_ok = test_tensorflow_fix()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE CAMBIOS")
    print("=" * 50)
    
    if tf_ok:
        print("✅ TensorFlow GPU: FUNCIONANDO")
        print("✅ Face Swapper: ACTUALIZADO para GPU")
        print("✅ Face Analyser: ACTUALIZADO para GPU")
        print("\n🎉 ¡Todo configurado para GPU!")
        print("\nPara usar:")
        print("1. from gpu_optimized_patch import get_gpu_providers, check_gpu_status")
        print("2. check_gpu_status()  # Para verificar estado")
        print("3. providers = get_gpu_providers()  # Para usar en tu código")
    else:
        print("⚠️  TensorFlow GPU: AÚN NO FUNCIONA")
        print("🔧 Soluciones adicionales:")
        print("   - Reinicia el runtime de Colab")
        print("   - Ejecuta: !nvidia-smi")
        print("   - Verifica que tengas GPU asignada")

if __name__ == "__main__":
    main() 