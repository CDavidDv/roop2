#!/usr/bin/env python3
"""
Script de prueba rápida para verificar la instalación de ROOP
Prueba todas las funcionalidades principales sin procesar archivos reales
"""

import sys
import traceback
import numpy as np
import time

def test_imports():
    """Prueba las importaciones críticas"""
    print("🧪 PRUEBAS DE IMPORTACIÓN")
    print("="*40)
    
    tests = [
        ("NumPy", lambda: __import__("numpy")),
        ("OpenCV", lambda: __import__("cv2")),
        ("PIL/Pillow", lambda: __import__("PIL")),
        ("PyTorch", lambda: __import__("torch")),
        ("TensorFlow", lambda: __import__("tensorflow")),
        ("ONNX", lambda: __import__("onnx")),
        ("ONNX Runtime", lambda: __import__("onnxruntime")),
        ("InsightFace", lambda: __import__("insightface")),
        ("GFPGAN", lambda: __import__("gfpgan")),
        ("PSUtil", lambda: __import__("psutil")),
        ("TQDM", lambda: __import__("tqdm")),
    ]
    
    passed = 0
    failed = []
    
    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except ImportError as e:
            print(f"❌ {name}: {e}")
            failed.append(name)
        except Exception as e:
            print(f"⚠️ {name}: Error inesperado - {e}")
            failed.append(name)
    
    print(f"\n📊 Resultados: {passed}/{len(tests)} importaciones exitosas")
    
    if failed:
        print(f"❌ Fallaron: {', '.join(failed)}")
        return False
    else:
        print("✅ Todas las importaciones exitosas!")
        return True

def test_cuda():
    """Prueba funcionalidad CUDA"""
    print("\n🚀 PRUEBAS DE CUDA")
    print("="*40)
    
    try:
        import torch
        import onnxruntime as ort
        
        # PyTorch CUDA
        if torch.cuda.is_available():
            device_name = torch.cuda.get_device_name(0)
            memory_gb = torch.cuda.get_device_properties(0).total_memory / 1024**3
            print(f"✅ PyTorch CUDA: {device_name}")
            print(f"💾 Memoria GPU: {memory_gb:.1f}GB")
            
            # Prueba simple con tensor
            x = torch.randn(1000, 1000).cuda()
            y = torch.mm(x, x.t())
            print("✅ Operación CUDA exitosa")
            
            del x, y
            torch.cuda.empty_cache()
        else:
            print("⚠️ PyTorch CUDA no disponible")
        
        # ONNX Runtime CUDA
        providers = ort.get_available_providers()
        if 'CUDAExecutionProvider' in providers:
            print("✅ ONNX Runtime CUDA disponible")
        else:
            print("⚠️ ONNX Runtime CUDA no disponible")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas CUDA: {e}")
        return False

def test_face_processing():
    """Prueba librerías de procesamiento facial"""
    print("\n👤 PRUEBAS DE PROCESAMIENTO FACIAL")
    print("="*40)
    
    try:
        import insightface
        print("✅ InsightFace importado")
        
        # Crear una imagen de prueba
        test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        print("✅ Imagen de prueba creada")
        
        # Esto normalmente requeriría modelos descargados
        print("⚠️ Prueba de detección facial requiere modelos descargados")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas faciales: {e}")
        traceback.print_exc()
        return False

def test_memory_optimization():
    """Prueba optimizaciones de memoria"""
    print("\n💾 PRUEBAS DE MEMORIA")
    print("="*40)
    
    try:
        import psutil
        import gc
        
        # Información del sistema
        memory = psutil.virtual_memory()
        print(f"💻 RAM Total: {memory.total / 1024**3:.1f}GB")
        print(f"💾 RAM Disponible: {memory.available / 1024**3:.1f}GB")
        print(f"📊 Uso RAM: {memory.percent}%")
        
        # Prueba de limpieza
        # Crear arrays grandes
        large_arrays = []
        for i in range(5):
            arr = np.random.randn(1000, 1000).astype(np.float32)
            large_arrays.append(arr)
        
        print("✅ Arrays creados")
        
        # Limpiar
        del large_arrays
        gc.collect()
        print("✅ Memoria limpiada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en pruebas de memoria: {e}")
        return False

def test_roop_modules():
    """Prueba módulos específicos de ROOP"""
    print("\n🎬 PRUEBAS DE MÓDULOS ROOP")
    print("="*40)
    
    try:
        # Importar módulos principales de ROOP
        import roop.globals
        print("✅ roop.globals")
        
        import roop.utilities
        print("✅ roop.utilities")
        
        try:
            import roop.face_analyser
            print("✅ roop.face_analyser")
        except Exception as e:
            print(f"⚠️ roop.face_analyser: {e}")
        
        try:
            import roop.processors.frame.core
            print("✅ roop.processors.frame.core")
        except Exception as e:
            print(f"⚠️ roop.processors.frame.core: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importando módulos ROOP: {e}")
        return False

def main():
    """Función principal de pruebas"""
    print("🧪" * 20)
    print("🎬 ROOP - PRUEBAS DE INSTALACIÓN")
    print("🧪" * 20)
    print(f"🐍 Python {sys.version}")
    print(f"⏰ Fecha: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = []
    
    # Ejecutar todas las pruebas
    results.append(("Importaciones", test_imports()))
    results.append(("CUDA", test_cuda()))
    results.append(("Procesamiento Facial", test_face_processing()))
    results.append(("Memoria", test_memory_optimization()))
    results.append(("Módulos ROOP", test_roop_modules()))
    
    # Resumen final
    print("\n" + "🎯" * 20)
    print("📋 RESUMEN DE PRUEBAS")
    print("🎯" * 20)
    
    passed_tests = 0
    total_tests = len(results)
    
    for test_name, success in results:
        if success:
            print(f"✅ {test_name}")
            passed_tests += 1
        else:
            print(f"❌ {test_name}")
    
    success_rate = (passed_tests / total_tests) * 100
    
    print(f"\n📊 Resultado: {passed_tests}/{total_tests} ({success_rate:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ¡TODAS LAS PRUEBAS EXITOSAS!")
        print("✨ ROOP está listo para usar")
        return True
    elif passed_tests >= total_tests * 0.7:  # 70% o más
        print("\n⚠️ INSTALACIÓN PARCIAL")
        print("🔧 Algunas funcionalidades pueden estar limitadas")
        return True
    else:
        print("\n❌ INSTALACIÓN PROBLEMÁTICA")
        print("🔧 Se requiere revisar y reinstalar dependencias")
        return False

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Pruebas interrumpidas por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado durante las pruebas: {e}")
        traceback.print_exc()
        sys.exit(1)