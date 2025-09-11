#!/usr/bin/env python3
"""
Test específico para el frame processor face_swapper
"""

import sys
import os

def test_face_swapper_import():
    """Test directo del módulo face_swapper"""
    print("🧪 PRUEBA ESPECÍFICA DE FACE_SWAPPER")
    print("="*50)
    
    try:
        # Test 1: Importar roop.globals
        print("1. Importando roop.globals...")
        import roop.globals
        print("   ✅ roop.globals importado")
        
        # Test 2: Importar face_swapper directamente
        print("2. Importando face_swapper...")
        from roop.processors.frame import face_swapper
        print("   ✅ face_swapper importado")
        
        # Test 3: Verificar funciones requeridas
        print("3. Verificando interfaz...")
        required_functions = [
            'pre_check',
            'pre_start', 
            'process_frame',
            'process_frames',
            'process_image',
            'process_video',
            'post_process'
        ]
        
        missing_functions = []
        for func_name in required_functions:
            if hasattr(face_swapper, func_name):
                print(f"   ✅ {func_name}")
            else:
                print(f"   ❌ {func_name}")
                missing_functions.append(func_name)
        
        if missing_functions:
            print(f"\n❌ Funciones faltantes: {missing_functions}")
            return False
        
        # Test 4: Importar usando importlib como en core.py
        print("4. Test con importlib...")
        import importlib
        frame_processor_module = importlib.import_module('roop.processors.frame.face_swapper')
        print("   ✅ Importación con importlib exitosa")
        
        # Test 5: Verificar NAME
        if hasattr(frame_processor_module, 'NAME'):
            print(f"   ✅ NAME: {frame_processor_module.NAME}")
        else:
            print("   ❌ NAME no encontrado")
        
        print("\n🎉 FACE_SWAPPER FUNCIONA CORRECTAMENTE!")
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_frame_processors_core():
    """Test de la función get_frame_processors_modules"""
    print("\n🧪 PRUEBA DE FRAME PROCESSORS CORE")
    print("="*50)
    
    try:
        # Importar core
        from roop.processors.frame.core import get_frame_processors_modules
        print("✅ core importado")
        
        # Test con face_swapper
        print("Probando get_frame_processors_modules(['face_swapper'])...")
        modules = get_frame_processors_modules(['face_swapper'])
        
        if modules:
            print(f"✅ Módulos obtenidos: {len(modules)}")
            for module in modules:
                print(f"   - {module.__name__}")
                if hasattr(module, 'NAME'):
                    print(f"     NAME: {module.NAME}")
        else:
            print("❌ No se obtuvieron módulos")
            return False
        
        print("\n🎉 FRAME PROCESSORS CORE FUNCIONA!")
        return True
        
    except SystemExit as e:
        print(f"❌ SystemExit capturado: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 DIAGNÓSTICO DE FACE_SWAPPER")
    print("="*60)
    
    # Información del sistema
    print(f"Python: {sys.version}")
    print(f"Directorio actual: {os.getcwd()}")
    print(f"Path de Python: {sys.path[:3]}...")  # Mostrar solo los primeros 3
    
    # Ejecutar tests
    test1_ok = test_face_swapper_import()
    test2_ok = test_frame_processors_core()
    
    print("\n" + "="*60)
    print("📋 RESUMEN")
    print("="*60)
    
    if test1_ok and test2_ok:
        print("🎉 TODOS LOS TESTS PASARON")
        print("✨ face_swapper debería funcionar correctamente")
        sys.exit(0)
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("🔧 Revisar los errores arriba")
        sys.exit(1)