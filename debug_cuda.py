#!/usr/bin/env python3

import onnxruntime
import tensorflow as tf
import numpy as np
import insightface
import os

def debug_cuda_usage():
    print("🔍 Diagnóstico de uso de CUDA")
    print("=" * 50)
    
    # 1. Verificar providers disponibles
    providers = onnxruntime.get_available_providers()
    print(f"1. Providers disponibles: {providers}")
    
    # 2. Verificar configuración de InsightFace
    print("\n2. Probando InsightFace con CUDA...")
    try:
        # Forzar uso de CUDA
        cuda_providers = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        face_analyser = insightface.app.FaceAnalysis(name='buffalo_l', providers=cuda_providers)
        face_analyser.prepare(ctx_id=0)
        print("✅ InsightFace configurado con CUDA")
        
        # Verificar qué provider realmente está usando
        print(f"   Providers configurados: {face_analyser.providers}")
        
    except Exception as e:
        print(f"❌ Error con InsightFace: {e}")
    
    # 3. Verificar TensorFlow GPU
    print("\n3. Verificando TensorFlow GPU...")
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print(f"   GPUs detectadas: {len(gpus)}")
    for i, gpu in enumerate(gpus):
        print(f"   GPU {i}: {gpu}")
    
    # 4. Verificar variables de entorno
    print("\n4. Variables de entorno CUDA:")
    cuda_vars = ['CUDA_VISIBLE_DEVICES', 'CUDA_DEVICE_ORDER', 'CUDA_CACHE_DISABLE']
    for var in cuda_vars:
        value = os.environ.get(var, 'No definida')
        print(f"   {var}: {value}")
    
    # 5. Test de rendimiento simple
    print("\n5. Test de rendimiento CUDA vs CPU...")
    try:
        # Crear datos de prueba
        test_data = np.random.randn(1, 3, 128, 128).astype(np.float32)
        
        # Test con CPU
        import time
        start_time = time.time()
        # Simular procesamiento CPU
        for _ in range(10):
            _ = np.sum(test_data)
        cpu_time = time.time() - start_time
        
        print(f"   Tiempo CPU (simulado): {cpu_time:.3f}s")
        print("   ⚠️  No se puede hacer test real de CUDA sin modelo")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

if __name__ == "__main__":
    debug_cuda_usage() 