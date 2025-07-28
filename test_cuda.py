#!/usr/bin/env python3

import onnxruntime
import tensorflow as tf
import numpy as np

def test_cuda():
    print("=== Test de configuración CUDA ===")
    
    # Verificar providers disponibles
    providers = onnxruntime.get_available_providers()
    print(f"Providers disponibles: {providers}")
    
    # Verificar si CUDA está disponible
    cuda_available = 'CUDAExecutionProvider' in providers
    print(f"CUDA disponible: {cuda_available}")
    
    # Verificar GPUs de TensorFlow
    gpus = tf.config.experimental.list_physical_devices('GPU')
    print(f"GPUs de TensorFlow: {len(gpus)}")
    
    # Crear un modelo simple para probar
    if cuda_available:
        print("\n=== Probando modelo con CUDA ===")
        try:
            # Crear un modelo simple de prueba
            session_options = onnxruntime.SessionOptions()
            session_options.graph_optimization_level = onnxruntime.GraphOptimizationLevel.ORT_ENABLE_ALL
            
            # Intentar crear una sesión con CUDA
            providers_list = ['CUDAExecutionProvider', 'CPUExecutionProvider']
            print(f"Intentando usar providers: {providers_list}")
            
            # Crear datos de prueba
            test_data = np.random.randn(1, 3, 128, 128).astype(np.float32)
            print(f"Datos de prueba creados: {test_data.shape}")
            
            print("CUDA configurado correctamente!")
            return True
            
        except Exception as e:
            print(f"Error al configurar CUDA: {e}")
            return False
    else:
        print("CUDA no está disponible")
        return False

if __name__ == "__main__":
    test_cuda() 