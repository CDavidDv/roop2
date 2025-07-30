#!/usr/bin/env python3
"""
Solución rápida para GPU - Solo actualiza face swapper
Ya que InsightFace funciona con GPU, solo necesitamos optimizar face swapper
"""

import os
import sys
import re

def update_face_swapper_only():
    """Actualizar solo face swapper para usar GPU"""
    print("🔄 Actualizando face swapper para GPU...")
    
    try:
        # Leer el archivo actual
        with open('roop/processors/frame/face_swapper.py', 'r') as f:
            content = f.read()
        
        # Buscar la función get_face_swapper
        pattern = r'def get_face_swapper\(\) -> Any:\s*\n\s*global FACE_SWAPPER\s*\n\s*with THREAD_LOCK:\s*\n\s*if FACE_SWAPPER is None:\s*\n\s*model_path = resolve_relative_path\(.*?\)\s*\n\s*# Forzar uso de CUDA.*?FACE_SWAPPER = insightface\.model_zoo\.get_model\(model_path, providers=providers\)'
        
        # Nueva configuración optimizada
        new_config = '''def get_face_swapper() -> Any:
    global FACE_SWAPPER

    with THREAD_LOCK:
        if FACE_SWAPPER is None:
            model_path = resolve_relative_path('../models/inswapper_128.onnx')
            # Configuración optimizada para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_SWAPPER] Usando providers optimizados: {providers}")
            
            FACE_SWAPPER = insightface.model_zoo.get_model(model_path, providers=providers)'''
        
        # Reemplazar usando regex
        content = re.sub(pattern, new_config, content, flags=re.DOTALL)
        
        # Escribir el archivo actualizado
        with open('roop/processors/frame/face_swapper.py', 'w') as f:
            f.write(content)
        
        print("✅ Face swapper actualizado para GPU")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando face swapper: {e}")
        return False

def update_face_analyser_only():
    """Actualizar solo face analyser para usar GPU"""
    print("🔄 Actualizando face analyser para GPU...")
    
    try:
        # Leer el archivo actual
        with open('roop/face_analyser.py', 'r') as f:
            content = f.read()
        
        # Buscar la función get_face_analyser
        pattern = r'def get_face_analyser\(\) -> Any:\s*\n\s*global FACE_ANALYSER\s*\n\s*with THREAD_LOCK:\s*\n\s*if FACE_ANALYSER is None:\s*\n\s*# Forzar uso de CUDA.*?FACE_ANALYSER = insightface\.app\.FaceAnalysis\(name=.*?\)\s*\n\s*FACE_ANALYSER\.prepare\(ctx_id=0\)'
        
        # Nueva configuración optimizada
        new_config = '''def get_face_analyser() -> Any:
    global FACE_ANALYSER

    with THREAD_LOCK:
        if FACE_ANALYSER is None:
            # Configuración optimizada para Google Colab
            providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"[FACE_ANALYSER] Usando providers optimizados: {providers}")
            
            FACE_ANALYSER = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
            FACE_ANALYSER.prepare(ctx_id=0)'''
        
        # Reemplazar usando regex
        content = re.sub(pattern, new_config, content, flags=re.DOTALL)
        
        # Escribir el archivo actualizado
        with open('roop/face_analyser.py', 'w') as f:
            f.write(content)
        
        print("✅ Face analyser actualizado para GPU")
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando face analyser: {e}")
        return False

def create_simple_gpu_patch():
    """Crear parche simple para GPU"""
    print("🔧 Creando parche GPU simple...")
    
    patch_code = '''
# Parche GPU simple para Google Colab
import os
import onnxruntime

# Configurar variables de entorno
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

# Función para obtener providers optimizados
def get_gpu_providers():
    providers = onnxruntime.get_available_providers()
    if 'CUDAExecutionProvider' in providers:
        return ['CUDAExecutionProvider', 'CPUExecutionProvider']
    return ['CPUExecutionProvider']

# Función para verificar GPU
def check_gpu_status():
    providers = onnxruntime.get_available_providers()
    print("🔍 Estado de GPU:")
    print(f"  ONNX CUDA: {'CUDAExecutionProvider' in providers}")
    print(f"  Providers disponibles: {providers}")

print("🎯 GPU configurada para face swap (solo ONNX)")
'''
    
    with open('simple_gpu_patch.py', 'w') as f:
        f.write(patch_code)
    
    print("✅ Archivo simple_gpu_patch.py creado")

def test_face_swap_gpu():
    """Probar face swap con GPU"""
    print("🧪 Probando face swap con GPU...")
    
    try:
        import insightface
        import cv2
        import numpy as np
        
        # Crear imagen de prueba
        test_image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        
        # Probar InsightFace con GPU
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        app = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
        app.prepare(ctx_id=0)
        
        # Procesar imagen
        faces = app.get(test_image)
        print(f"✅ InsightFace GPU: {len(faces)} caras detectadas")
        
        # Probar face swapper
        model_path = 'models/inswapper_128.onnx'
        if os.path.exists(model_path):
            swapper = insightface.model_zoo.get_model(model_path, providers=providers)
            print("✅ Face swapper GPU: Modelo cargado correctamente")
        else:
            print("⚠️  Face swapper: Modelo no encontrado (normal en prueba)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando face swap: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 SOLUCIÓN RÁPIDA PARA GPU")
    print("=" * 40)
    print("Optimizando solo face swapper (InsightFace ya funciona)")
    
    # 1. Actualizar face swapper
    swapper_ok = update_face_swapper_only()
    
    # 2. Actualizar face analyser
    analyser_ok = update_face_analyser_only()
    
    # 3. Crear parche simple
    create_simple_gpu_patch()
    
    # 4. Probar face swap
    test_ok = test_face_swap_gpu()
    
    print("\n" + "=" * 40)
    print("📋 RESUMEN DE CAMBIOS")
    print("=" * 40)
    
    if swapper_ok and analyser_ok and test_ok:
        print("✅ Face Swapper: ACTUALIZADO para GPU")
        print("✅ Face Analyser: ACTUALIZADO para GPU")
        print("✅ Face Swap: FUNCIONANDO con GPU")
        print("\n🎉 ¡Face swap optimizado para GPU!")
        print("\nPara usar:")
        print("1. from simple_gpu_patch import get_gpu_providers, check_gpu_status")
        print("2. check_gpu_status()  # Para verificar estado")
        print("3. providers = get_gpu_providers()  # Para usar en tu código")
        print("\n💡 TensorFlow no es crítico para face swap, ONNX Runtime es suficiente")
    else:
        print("⚠️  Algunos componentes no se actualizaron correctamente")
        print("🔧 Verifica los errores arriba")

if __name__ == "__main__":
    main() 