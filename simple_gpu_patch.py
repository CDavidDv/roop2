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