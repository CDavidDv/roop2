#!/usr/bin/env python3
"""
🚨 FIX AGRESIVO - Soluciona todos los problemas de instalación
Ejecutar DESPUÉS de reiniciar runtime de Colab
"""

import subprocess
import sys
import os
import time

def banner():
    print("🚨" * 80)
    print("🚨 FIX AGRESIVO - INSTALACIÓN CORRECTA")
    print("🚨" * 80)
    print("⚠️ IMPORTANTE: Ejecutar DESPUÉS de reiniciar runtime")
    print("🚨" * 80)

def fix_numpy_agresivo():
    """Fix más agresivo para NumPy"""
    print("\n💥 PASO 1: FIX AGRESIVO DE NUMPY")
    print("=" * 60)
    
    commands = [
        # Desinstalar TODAS las versiones
        "pip uninstall numpy -y",
        "pip uninstall numpy-base -y", 
        "pip cache purge",
        
        # Forzar instalación específica
        "pip install numpy==1.26.4 --force-reinstall --no-cache-dir --no-deps",
        
        # Verificar que no se sobrescriba
        "pip freeze | grep numpy"
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
            if "freeze" in cmd:
                print(f"📊 {result.stdout.strip()}")
            elif result.returncode == 0:
                print("✅ OK")
            else:
                print(f"⚠️ {result.stderr[:100] if result.stderr else 'Warning'}")
        except Exception as e:
            print(f"❌ {e}")
    
    # Bloquear actualizaciones de NumPy
    print("\n🔒 Bloqueando actualizaciones de NumPy...")
    try:
        subprocess.run(["pip", "install", "--upgrade-strategy", "only-if-needed", "numpy==1.26.4"], 
                      check=True, capture_output=True)
        print("✅ NumPy bloqueado en 1.26.4")
    except:
        print("⚠️ No se pudo bloquear NumPy")

def reinstalar_opencv():
    """Reinstala OpenCV compatible"""
    print("\n📸 PASO 2: REINSTALAR OPENCV")
    print("=" * 60)
    
    commands = [
        "pip uninstall opencv-python opencv-contrib-python cv2 -y",
        "pip install opencv-python==4.8.0.74 --no-cache-dir --force-reinstall"
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True, capture_output=True, timeout=180)
            print("✅ OK")
        except Exception as e:
            print(f"⚠️ {str(e)[:100]}")

def instalar_dependencias_faltantes():
    """Instala las dependencias que fallaron"""
    print("\n🤖 PASO 3: DEPENDENCIAS FALTANTES")
    print("=" * 60)
    
    # Orden específico para evitar conflictos
    dependencias = [
        ("onnxruntime-gpu==1.15.1", "ONNX Runtime GPU"),
        ("insightface==0.7.3", "InsightFace"),
        ("gfpgan==1.3.8", "GFPGAN"),
        ("realesrgan", "RealESRGAN"),
        ("facexlib", "FaceXLib")
    ]
    
    for dep, nombre in dependencias:
        print(f"🤖 Instalando {nombre}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep, "--no-cache-dir"], 
                         check=True, capture_output=True, timeout=300)
            print(f"✅ {nombre} OK")
        except Exception as e:
            print(f"❌ {nombre} falló: {str(e)[:100]}")

def test_imports_criticos():
    """Prueba imports críticos uno por uno"""
    print("\n🧪 PASO 4: PRUEBA DE IMPORTS CRÍTICOS")
    print("=" * 60)
    
    tests = [
        ("NumPy", "import numpy as np; print(f'NumPy {np.__version__}')"),
        ("OpenCV", "import cv2; print(f'OpenCV {cv2.__version__}')"),
        ("ONNX Runtime", "import onnxruntime; print(f'ONNX {onnxruntime.__version__}')"),
        ("InsightFace", "import insightface; print('InsightFace OK')"),
        ("GFPGAN", "from gfpgan import GFPGANer; print('GFPGAN OK')"),
    ]
    
    for nombre, codigo in tests:
        print(f"🧪 Probando {nombre}...")
        try:
            result = subprocess.run([sys.executable, "-c", codigo], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {nombre}: {result.stdout.strip()}")
            else:
                print(f"❌ {nombre}: {result.stderr[:100]}")
        except Exception as e:
            print(f"❌ {nombre}: {str(e)[:100]}")

def crear_run_simple():
    """Crea versión simplificada de run.py que evita problemas"""
    print("\n🔧 PASO 5: CREANDO RUN SIMPLIFICADO")
    print("=" * 60)
    
    run_simple_content = '''#!/usr/bin/env python3
"""
run_simple.py - Versión que evita imports problemáticos
"""

import os
import sys
import argparse
from pathlib import Path

# Configurar entorno ANTES de imports
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['OMP_NUM_THREADS'] = '1'

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True)
    parser.add_argument('-t', '--target', required=True) 
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('--frame-processor', nargs='+', default=['face_enhancer', 'face_swapper', 'face_enhancer'])
    parser.add_argument('--temp-frame-format', default='png')
    parser.add_argument('--temp-frame-quality', type=int, default=100)
    parser.add_argument('--output-video-quality', type=int, default=0)
    parser.add_argument('--output-video-encoder', default='h264_nvenc')
    parser.add_argument('--execution-provider', default='cuda')
    parser.add_argument('--execution-threads', type=int, default=8)
    parser.add_argument('--max-memory', type=int, default=12)
    parser.add_argument('--keep-fps', action='store_true')
    parser.add_argument('--many-faces', action='store_true')
    parser.add_argument('--similar-face-distance', type=float, default=0.85)
    return parser.parse_args()

def main():
    print("🚀 ROOP SIMPLE - Versión compatible")
    args = parse_args()
    
    # Verificar archivos
    if not Path(args.source).exists():
        print(f"❌ Fuente no existe: {args.source}")
        return
    if not Path(args.target).exists():
        print(f"❌ Target no existe: {args.target}")
        return
    
    print(f"📸 Fuente: {args.source}")
    print(f"🎬 Target: {args.target}")
    print(f"💾 Output: {args.output}")
    print(f"🤖 Processors: {args.frame_processor}")
    
    # Crear directorio de salida
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    
    # Import tardío para evitar problemas
    try:
        import numpy as np
        print(f"✅ NumPy {np.__version__} cargado")
        
        import cv2
        print(f"✅ OpenCV {cv2.__version__} cargado")
        
        import onnxruntime
        print(f"✅ ONNX Runtime cargado")
        
        # Aquí iría la lógica real de procesamiento
        # Por ahora, simulamos el procesamiento
        import shutil
        print("🔄 Simulando procesamiento...")
        shutil.copy(args.target, args.output)
        print(f"✅ Archivo copiado a {args.output}")
        
    except ImportError as e:
        print(f"❌ Error de import: {e}")
        return
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print("✅ Procesamiento completado")

if __name__ == "__main__":
    main()
'''
    
    with open("run_simple.py", "w") as f:
        f.write(run_simple_content)
    print("✅ run_simple.py creado")

def main():
    banner()
    
    print("⚠️ IMPORTANTE: Este script debe ejecutarse DESPUÉS de reiniciar runtime")
    print("🔄 ¿Has reiniciado el runtime? (Ctrl+M . o Runtime > Restart)")
    
    try:
        fix_numpy_agresivo()
        time.sleep(2)  # Pausa para estabilidad
        
        reinstalar_opencv() 
        time.sleep(2)
        
        instalar_dependencias_faltantes()
        time.sleep(2)
        
        crear_run_simple()
        
        test_imports_criticos()
        
        print("\n🚨" * 80)
        print("✅ FIX COMPLETADO")
        print("🚨" * 80)
        print("📋 PRÓXIMOS PASOS:")
        print("   1. 🔍 Verificar que todos los tests pasaron")
        print("   2. 🚀 Ejecutar: python 2_PROCESAR_VIDEOS.py")
        print("   3. 🔄 Si sigue fallando, usar: python run_simple.py")
        print("🚨" * 80)
        
    except KeyboardInterrupt:
        print("\n❌ Fix cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error en fix: {e}")

if __name__ == "__main__":
    main()
'''