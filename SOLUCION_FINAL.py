#!/usr/bin/env python3
"""
🚨 SOLUCIÓN FINAL - NUCLEAR
Fuerza NumPy 1.26.4 y evita todos los problemas

IMPORTANTE: Ejecutar DESPUÉS de reiniciar runtime
"""

import subprocess
import sys
import os
from pathlib import Path

def nuclear_numpy_fix():
    """Solución nuclear para NumPy"""
    print("💥 SOLUCIÓN NUCLEAR - FORZANDO NUMPY 1.26.4")
    print("=" * 60)
    
    commands = [
        # 1. Desinstalar TODAS las versiones de NumPy
        "pip uninstall numpy -y",
        
        # 2. Limpiar cache completamente
        "pip cache purge",
        
        # 3. Instalar NumPy 1.26.4 CON --force-reinstall
        "pip install numpy==1.26.4 --force-reinstall --no-cache-dir",
        
        # 4. Desinstalar y reinstalar OpenCV con la versión correcta
        "pip uninstall opencv-python opencv-contrib-python -y",
        "pip install opencv-python==4.8.0.74 --no-cache-dir",
        
        # 5. Verificar versiones
        "python -c 'import numpy; print(f\"NumPy: {numpy.__version__}\")'",
    ]
    
    for cmd in commands:
        print(f"🔧 {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=180)
            if "import numpy" in cmd:
                print(f"✅ {result.stdout.strip()}")
            elif result.returncode == 0:
                print("✅ OK")
            else:
                print(f"⚠️ {result.stderr[:100] if result.stderr else 'Warning'}")
        except Exception as e:
            print(f"❌ {e}")

def simple_direct_processing():
    """Procesamiento directo sin imports complejos"""
    print("\n🎯 PROCESAMIENTO DIRECTO")
    print("=" * 40)
    
    # Crear carpetas
    for folder in ["source", "videos_input", "videos_output"]:
        Path(folder).mkdir(exist_ok=True)
        print(f"📁 {folder}/")
    
    # Buscar archivos
    source_files = list(Path("source").glob("*.*"))
    video_files = list(Path("videos_input").glob("*.*"))
    
    if not source_files or not video_files:
        print("❌ Faltan archivos - sube imagen a source/ y videos a videos_input/")
        return
    
    source_img = source_files[0]
    
    print(f"📸 Fuente: {source_img.name}")
    print(f"🎬 Videos: {len(video_files)}")
    
    # Procesar cada video con comando básico
    for i, video in enumerate(video_files, 1):
        print(f"\n📊 {i}/{len(video_files)}: {video.name}")
        
        output_name = f"final_{video.name}"
        output_path = Path("videos_output") / output_name
        
        # Comando BÁSICO sin parámetros complejos
        cmd = [
            sys.executable, "run.py",
            "-s", str(source_img),
            "-t", str(video),
            "-o", str(output_path)
        ]
        
        print(f"🔧 Ejecutando procesamiento básico...")
        
        try:
            # Ejecutar sin timeout y mostrar salida en tiempo real
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, bufsize=1, universal_newlines=True)
            
            # Mostrar salida en tiempo real
            for line in process.stdout:
                if "Processing" in line or "%" in line or "frame" in line:
                    print(f"   {line.strip()}")
            
            process.wait()
            
            if process.returncode == 0:
                print(f"✅ {video.name} procesado exitosamente")
            else:
                print(f"❌ {video.name} falló")
                
        except Exception as e:
            print(f"❌ Error: {e}")

def main():
    """Función principal"""
    print("🚨" * 70)
    print("🚨 SOLUCIÓN FINAL - ROOP PARA COLAB")
    print("🚨" * 70)
    print("⚠️ IMPORTANTE: Ejecuta esto DESPUÉS de reiniciar runtime")
    print("🚨" * 70)
    
    # Paso 1: Fix nuclear de NumPy
    nuclear_numpy_fix()
    
    # Paso 2: Instalar mínimo necesario
    print("\n📦 INSTALANDO DEPENDENCIAS MÍNIMAS")
    essential = ["onnxruntime-gpu", "insightface"]
    for pkg in essential:
        print(f"📦 {pkg}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg, "--no-cache-dir"], 
                         check=True, capture_output=True, timeout=180)
            print("✅ OK")
        except:
            print("⚠️ Warning")
    
    # Paso 3: Procesamiento directo
    simple_direct_processing()
    
    print("\n🚨" * 70)
    print("🎉 PROCESAMIENTO COMPLETADO")
    print("🚨" * 70)
    print("📁 Revisa videos_output/ para los resultados")

if __name__ == "__main__":
    main()