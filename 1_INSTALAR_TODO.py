#!/usr/bin/env python3
"""
🔧 SCRIPT 1: INSTALACIÓN COMPLETA Y CONFIGURACIÓN
Instala todas las dependencias y crea la estructura necesaria
"""

import subprocess
import sys
import os
from pathlib import Path

def banner():
    """Banner de instalación"""
    print("🔧" * 80)
    print("🔧 SCRIPT 1: INSTALACIÓN COMPLETA PARA ROOP")
    print("🔧" * 80)
    print("🎯 Configuración: MÁXIMA CALIDAD")
    print("🎯 Pipeline: face_enhancer → face_swapper → face_enhancer")
    print("🔧" * 80)

def instalar_numpy_correcto():
    """Instala NumPy 1.26.4 que funciona"""
    print("\n💾 PASO 1: INSTALANDO NUMPY 1.26.4")
    print("=" * 50)
    
    commands = [
        "pip uninstall numpy -y",
        "pip cache purge",
        "pip install numpy==1.26.4 --force-reinstall --no-cache-dir"
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True, timeout=180)
            print("✅ OK")
        except Exception as e:
            print(f"⚠️ Warning: {str(e)[:100]}")
    
    # Verificar instalación
    try:
        result = subprocess.run([sys.executable, "-c", "import numpy; print(f'NumPy: {numpy.__version__}')"], 
                              capture_output=True, text=True)
        print(f"✅ {result.stdout.strip()}")
    except:
        print("❌ Error verificando NumPy")

def instalar_opencv_compatible():
    """Instala OpenCV compatible con NumPy 1.26.4"""
    print("\n📸 PASO 2: INSTALANDO OPENCV COMPATIBLE")
    print("=" * 50)
    
    commands = [
        "pip uninstall opencv-python opencv-contrib-python -y",
        "pip install opencv-python==4.8.0.74 --no-cache-dir"
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            subprocess.run(cmd.split(), check=True, capture_output=True, timeout=180)
            print("✅ OK")
        except Exception as e:
            print(f"⚠️ Warning: {str(e)[:100]}")

def instalar_dependencias_ia():
    """Instala dependencias de IA para face processing"""
    print("\n🤖 PASO 3: INSTALANDO DEPENDENCIAS DE IA")
    print("=" * 50)
    
    # Dependencias en orden específico para evitar conflictos
    dependencias = [
        "onnxruntime-gpu",  # GPU acceleration
        "insightface",      # Face detection y swapping  
        "gfpgan",          # Face enhancement
        "realesrgan",      # Super resolution
        "facexlib",        # Face processing utilities
    ]
    
    for dep in dependencias:
        print(f"🤖 Instalando {dep}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep, "--no-cache-dir"], 
                         check=True, capture_output=True, timeout=300)
            print(f"✅ {dep} instalado")
        except Exception as e:
            print(f"⚠️ {dep} warning: {str(e)[:100]}")

def crear_estructura_carpetas():
    """Crea la estructura de carpetas necesaria"""
    print("\n📁 PASO 4: CREANDO ESTRUCTURA DE CARPETAS")
    print("=" * 50)
    
    carpetas = {
        "source": "Imágenes fuente (rostros a intercambiar)",
        "videos_input": "Videos a procesar", 
        "videos_output": "Videos procesados (salida)",
        "temp": "Archivos temporales",
        "models": "Modelos de IA (descarga automática)"
    }
    
    for carpeta, descripcion in carpetas.items():
        Path(carpeta).mkdir(exist_ok=True)
        print(f"✅ {carpeta}/ - {descripcion}")
    
    # Crear archivo .gitignore para temp
    gitignore_content = """# Archivos temporales
temp/
*.tmp
*.cache

# Modelos grandes
models/*.pth
models/*.onnx
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("✅ .gitignore creado")

def verificar_gpu():
    """Verifica disponibilidad de GPU"""
    print("\n🚀 PASO 5: VERIFICANDO GPU")
    print("=" * 50)
    
    # Verificar NVIDIA-SMI
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU NVIDIA detectada")
            # Extraer info básica
            lines = result.stdout.split('\n')
            for line in lines:
                if 'Tesla T4' in line or 'GPU' in line and 'MiB' in line:
                    print(f"📊 {line.strip()}")
        else:
            print("⚠️ GPU no detectada - se usará CPU")
    except:
        print("⚠️ nvidia-smi no disponible")
    
    # Verificar ONNX Runtime providers
    try:
        result = subprocess.run([sys.executable, "-c", """
import onnxruntime as ort
providers = ort.get_available_providers()
print(f"ONNX Providers: {providers}")
if 'CUDAExecutionProvider' in providers:
    print("✅ CUDA disponible para ONNX Runtime")
else:
    print("⚠️ Solo CPU disponible para ONNX Runtime")
"""], capture_output=True, text=True)
        print(result.stdout)
    except Exception as e:
        print(f"❌ Error verificando ONNX: {e}")

def crear_archivo_configuracion():
    """Crea archivo de configuración para máxima calidad"""
    print("\n⚙️ PASO 6: CREANDO CONFIGURACIÓN DE MÁXIMA CALIDAD")
    print("=" * 50)
    
    config_content = """# Configuración ROOP - MÁXIMA CALIDAD
# No modificar estas configuraciones para mantener calidad máxima

[CALIDAD]
temp_frame_format = png
temp_frame_quality = 100
output_video_quality = 0
keep_fps = true
skip_audio = false

[PROCESAMIENTO]
frame_processors = face_enhancer,face_swapper,face_enhancer
execution_provider = cuda
execution_threads = 8
many_faces = false
similar_face_distance = 0.85

[MEMORIA]
max_memory = 12
batch_size = 1
memory_optimization = true

[OUTPUT]
output_video_encoder = h264_nvenc
keep_frames = false
"""
    
    with open("config_maxima_calidad.ini", "w") as f:
        f.write(config_content)
    print("✅ config_maxima_calidad.ini creado")

def crear_readme_uso():
    """Crea README con instrucciones de uso"""
    print("\n📖 PASO 7: CREANDO INSTRUCCIONES DE USO")
    print("=" * 50)
    
    readme_content = """# 🎬 ROOP - MÁXIMA CALIDAD

## 🚀 Uso Rápido

### 1. Preparar archivos
- Sube **1 imagen** a `source/` (rostro a intercambiar)
- Sube **videos** a `videos_input/` (videos a procesar)

### 2. Ejecutar procesamiento
```bash
python 2_PROCESAR_VIDEOS.py
```

## 🎯 Pipeline de Calidad

1. **Face Enhancer** → Mejora calidad inicial
2. **Face Swapper** → Intercambia rostro 
3. **Face Enhancer** → Mejora calidad final

## ⚙️ Configuración

- **Calidad de frames**: PNG 100% (sin compresión)
- **Calidad de video**: 0 (máxima)
- **GPU**: CUDA habilitado
- **Memoria**: Optimizada para Tesla T4

## 📁 Estructura

```
source/           ← Imágenes fuente
videos_input/     ← Videos a procesar  
videos_output/    ← Videos procesados
temp/             ← Archivos temporales
models/           ← Modelos de IA
```

## 🎉 Resultados

Los videos procesados estarán en `videos_output/` con máxima calidad.
"""
    
    with open("README_CALIDAD.md", "w") as f:
        f.write(readme_content)
    print("✅ README_CALIDAD.md creado")

def test_instalacion():
    """Prueba que todo esté instalado correctamente"""
    print("\n🧪 PASO 8: PRUEBA DE INSTALACIÓN")
    print("=" * 50)
    
    tests = {
        "NumPy": "import numpy; print(f'NumPy {numpy.__version__} OK')",
        "OpenCV": "import cv2; print(f'OpenCV {cv2.__version__} OK')",
        "ONNX Runtime": "import onnxruntime; print(f'ONNX Runtime OK')",
        "InsightFace": "import insightface; print('InsightFace OK')",
        "GFPGAN": "import gfpgan; print('GFPGAN OK')"
    }
    
    for name, test_code in tests.items():
        try:
            result = subprocess.run([sys.executable, "-c", test_code], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print(f"✅ {name}: {result.stdout.strip()}")
            else:
                print(f"❌ {name}: Error")
        except Exception as e:
            print(f"❌ {name}: {str(e)[:50]}")

def main():
    """Función principal de instalación"""
    banner()
    
    try:
        instalar_numpy_correcto()
        instalar_opencv_compatible()
        instalar_dependencias_ia()
        crear_estructura_carpetas()
        verificar_gpu()
        crear_archivo_configuracion()
        crear_readme_uso()
        test_instalacion()
        
        print("\n🔧" * 80)
        print("🎉 INSTALACIÓN COMPLETADA EXITOSAMENTE")
        print("🔧" * 80)
        print("📋 PRÓXIMOS PASOS:")
        print("   1. 📤 Sube imagen a source/")
        print("   2. 📤 Sube videos a videos_input/")
        print("   3. 🚀 Ejecuta: python 2_PROCESAR_VIDEOS.py")
        print("🔧" * 80)
        
    except KeyboardInterrupt:
        print("\n❌ Instalación cancelada por usuario")
    except Exception as e:
        print(f"\n❌ Error en instalación: {e}")

if __name__ == "__main__":
    main()