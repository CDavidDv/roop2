#!/usr/bin/env python3

import os
import sys
import importlib

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todos los módulos se pueden importar correctamente"""
    print("🔍 Probando imports...")
    
    modules_to_test = [
        'roop.processors.frame.pre_face_enhancer',
        'roop.processors.frame.post_face_enhancer',
        'roop.processors.frame.face_swapper',
        'roop.processors.frame.face_enhancer'
    ]
    
    for module_name in modules_to_test:
        try:
            module = importlib.import_module(module_name)
            print(f"✅ {module_name} - OK")
            
            # Verificar que tiene los métodos requeridos
            required_methods = [
                'pre_check', 'pre_start', 'post_process',
                'process_frame', 'process_frames', 'process_image', 'process_video'
            ]
            
            for method in required_methods:
                if hasattr(module, method):
                    print(f"   ✅ {method} - OK")
                else:
                    print(f"   ❌ {method} - FALTANTE")
                    
        except ImportError as e:
            print(f"❌ {module_name} - ERROR: {e}")
        except Exception as e:
            print(f"❌ {module_name} - ERROR: {e}")

def test_pipeline_configuration():
    """Prueba la configuración del pipeline"""
    print("\n🔧 Probando configuración del pipeline...")
    
    try:
        import roop.globals
        import roop.processors.frame.core
        
        # Configurar un pipeline de prueba
        test_processors = ['pre_face_enhancer', 'face_swapper', 'post_face_enhancer']
        
        # Probar que se pueden cargar los módulos
        modules = roop.processors.frame.core.get_frame_processors_modules(test_processors)
        
        if len(modules) == 3:
            print("✅ Pipeline completo cargado correctamente")
            for i, module in enumerate(modules):
                print(f"   {i+1}. {module.__name__}")
        else:
            print(f"❌ Error: Se esperaban 3 módulos, se cargaron {len(modules)}")
            
    except Exception as e:
        print(f"❌ Error en configuración del pipeline: {e}")

def test_cuda_detection():
    """Prueba la detección de CUDA"""
    print("\n⚡ Probando detección de CUDA...")
    
    try:
        import onnxruntime
        
        available_providers = onnxruntime.get_available_providers()
        print(f"Providers disponibles: {available_providers}")
        
        if 'CUDAExecutionProvider' in available_providers:
            print("✅ CUDA detectado - Rendimiento optimizado")
        else:
            print("⚠️ CUDA no detectado - Usando CPU")
            
    except Exception as e:
        print(f"❌ Error detectando CUDA: {e}")

def show_usage_examples():
    """Muestra ejemplos de uso"""
    print("\n📖 Ejemplos de uso:")
    print("=" * 50)
    
    print("1. Pipeline completo (recomendado):")
    print("   python run_enhanced_pipeline.py -s imagen.jpg -t video.mp4 -o resultado.mp4 --keep-fps")
    print()
    
    print("2. Pipeline personalizado:")
    print("   python run_custom_pipeline.py -s imagen.jpg -t video.mp4 --processors pre_face_enhancer face_swapper post_face_enhancer")
    print()
    
    print("3. Solo mejora antes del swap:")
    print("   python run_custom_pipeline.py -s imagen.jpg -t video.mp4 --processors pre_face_enhancer face_swapper")
    print()
    
    print("4. Solo mejora después del swap:")
    print("   python run_custom_pipeline.py -s imagen.jpg -t video.mp4 --processors face_swapper post_face_enhancer")
    print()
    
    print("5. Ver todos los presets disponibles:")
    print("   python run_custom_pipeline.py --list-presets")

def main():
    print("🚀 Test del Pipeline Mejorado de Roop")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    test_imports()
    test_pipeline_configuration()
    test_cuda_detection()
    show_usage_examples()
    
    print("\n" + "=" * 50)
    print("✅ Test completado. Si no hay errores, el pipeline está listo para usar.")
    print("🎬 ¡Disfruta de tus videos con calidad mejorada!")

if __name__ == "__main__":
    main() 