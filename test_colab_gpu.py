#!/usr/bin/env python3
"""
Script de prueba GPU para Google Colab
Verifica si la GPU está disponible y funcionando
"""

import os
import sys
import time
import numpy as np

def test_basic_gpu():
    """Prueba básica de GPU"""
    print("🔍 Prueba básica de GPU...")
    
    try:
        import onnxruntime
        providers = onnxruntime.get_available_providers()
        print(f"ONNX Providers: {providers}")
        
        if 'CUDAExecutionProvider' in providers:
            print("✅ CUDA disponible en ONNX")
            return True
        else:
            print("❌ CUDA no disponible en ONNX")
            return False
    except Exception as e:
        print(f"❌ Error ONNX: {e}")
        return False

def test_tensorflow_gpu():
    """Prueba TensorFlow GPU"""
    print("\n🔍 Prueba TensorFlow GPU...")
    
    try:
        import tensorflow as tf
        
        # Verificar GPUs
        gpus = tf.config.experimental.list_physical_devices('GPU')
        print(f"TensorFlow GPUs: {len(gpus)}")
        
        if gpus:
            # Test simple
            with tf.device('/GPU:0'):
                a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
                b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
                c = tf.matmul(a, b)
                print(f"✅ TensorFlow GPU: {c}")
                return True
        else:
            print("❌ No hay GPUs en TensorFlow")
            return False
            
    except Exception as e:
        print(f"❌ Error TensorFlow: {e}")
        return False

def test_insightface_gpu():
    """Prueba InsightFace con GPU"""
    print("\n🔍 Prueba InsightFace GPU...")
    
    try:
        import insightface
        import cv2
        
        # Crear imagen de prueba
        test_image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        
        # Configurar InsightFace con CUDA
        providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        app = insightface.app.FaceAnalysis(name='buffalo_l', providers=providers)
        app.prepare(ctx_id=0)
        
        # Procesar imagen
        faces = app.get(test_image)
        print(f"✅ InsightFace GPU: {len(faces)} caras detectadas")
        return True
        
    except Exception as e:
        print(f"❌ Error InsightFace: {e}")
        return False

def get_gpu_memory():
    """Obtener información de memoria GPU"""
    print("\n💾 Información de memoria GPU...")
    
    try:
        import nvidia_ml_py3 as nvml
        nvml.nvmlInit()
        
        handle = nvml.nvmlDeviceGetHandleByIndex(0)
        memory_info = nvml.nvmlDeviceGetMemoryInfo(handle)
        
        total_gb = memory_info.total // (1024**3)
        free_gb = memory_info.free // (1024**3)
        used_gb = memory_info.used // (1024**3)
        
        print(f"Memoria total: {total_gb}GB")
        print(f"Memoria libre: {free_gb}GB")
        print(f"Memoria usada: {used_gb}GB")
        
        return free_gb >= 8  # Necesitamos al menos 8GB libres
        
    except Exception as e:
        print(f"⚠️  No se pudo obtener info memoria: {e}")
        return False

def run_complete_test():
    """Ejecutar prueba completa"""
    print("🚀 PRUEBA COMPLETA DE GPU PARA FACE SWAP")
    print("=" * 50)
    
    results = {
        'onnx': test_basic_gpu(),
        'tensorflow': test_tensorflow_gpu(),
        'insightface': test_insightface_gpu(),
        'memory': get_gpu_memory()
    }
    
    print("\n" + "=" * 50)
    print("📋 RESULTADOS DE LA PRUEBA")
    print("=" * 50)
    
    for test, result in results.items():
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test.upper()}: {status}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 ¡TU GPU ESTÁ LISTA PARA FACE SWAP!")
        print("✅ Todas las pruebas pasaron")
        print("✅ Puedes usar face swap con GPU")
    else:
        print("\n⚠️  PROBLEMAS DETECTADOS:")
        failed_tests = [test for test, result in results.items() if not result]
        for test in failed_tests:
            print(f"   - {test.upper()}")
        
        print("\n🔧 SOLUCIONES:")
        print("   1. Reinicia el runtime de Colab")
        print("   2. Verifica que tengas GPU asignada")
        print("   3. Ejecuta: !nvidia-smi")
        print("   4. Asegúrate de tener suficiente memoria libre")
    
    return all_passed

if __name__ == "__main__":
    run_complete_test() 