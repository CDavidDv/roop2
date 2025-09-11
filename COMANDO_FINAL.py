#!/usr/bin/env python3
"""
🎯 COMANDO FINAL - LA SOLUCIÓN DEFINITIVA
Esto DEBE funcionar en Colab
"""

import subprocess
import sys
import os
from pathlib import Path

def solucion_definitiva():
    """La solución que SÍ va a funcionar"""
    
    print("🎯" * 80)
    print("🎯 SOLUCIÓN DEFINITIVA - COLAB ROOP")
    print("🎯" * 80)
    print("💡 Estrategia: Evitar completamente los imports problemáticos")
    print("🎯" * 80)
    
    # PASO 1: Reinstalar NumPy AGRESIVAMENTE
    print("\n💥 PASO 1: REINSTALACIÓN AGRESIVA DE NUMPY")
    try:
        # Forzar reinstalación
        subprocess.run([sys.executable, "-m", "pip", "uninstall", "numpy", "-y"], 
                      capture_output=True)
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.26.4", 
                       "--force-reinstall", "--no-cache-dir"], 
                      check=True, capture_output=True)
        print("✅ NumPy 1.26.4 forzado")
    except:
        print("⚠️ NumPy warning - continuando...")
    
    # PASO 2: Crear carpetas
    print("\n📁 PASO 2: ESTRUCTURA")
    for folder in ["source", "videos_input", "videos_output"]:
        Path(folder).mkdir(exist_ok=True)
        print(f"✅ {folder}/")
    
    # PASO 3: Buscar archivos
    print("\n📋 PASO 3: ARCHIVOS")
    source_files = list(Path("source").glob("*.*"))
    video_files = list(Path("videos_input").glob("*.*"))
    
    if not source_files:
        print("❌ Sube imagen a source/")
        return
    if not video_files:
        print("❌ Sube videos a videos_input/")
        return
    
    source_img = source_files[0]
    print(f"📸 Fuente: {source_img.name}")
    print(f"🎬 Videos: {len(video_files)}")
    
    # PASO 4: PROCESAMIENTO DIRECTO - EVITAR TODOS LOS IMPORTS
    print(f"\n🚀 PASO 4: PROCESAMIENTO DIRECTO")
    
    for i, video in enumerate(video_files, 1):
        print(f"\n{'='*60}")
        print(f"📊 PROGRESO: {i}/{len(video_files)} - {video.name}")
        print(f"{'='*60}")
        
        output_name = f"result_{video.name}"
        output_path = Path("videos_output") / output_name
        
        # USAR EL SCRIPT COLAB ESPECÍFICO (sin imports problemáticos)
        cmd = [
            sys.executable, "run_colab.py",
            "-s", str(source_img),
            "-t", str(video),
            "-o", str(output_path),
            "--keep-fps"
        ]
        
        print(f"🔧 Comando: python run_colab.py...")
        
        try:
            result = subprocess.run(cmd, timeout=1800, text=True)  # 30 min timeout
            
            if result.returncode == 0:
                print(f"✅ {video.name} → {output_name}")
            else:
                print(f"❌ {video.name} falló")
                
        except subprocess.TimeoutExpired:
            print(f"⏰ {video.name} timeout")
        except KeyboardInterrupt:
            print("❌ Cancelado")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # PASO 5: RESULTADOS
    print(f"\n🎯" * 80)
    print("🎉 PROCESAMIENTO COMPLETADO")
    print(f"🎯" * 80)
    
    output_files = list(Path("videos_output").glob("*.*"))
    print(f"📁 Archivos generados: {len(output_files)}")
    for file in output_files:
        print(f"   ✅ {file.name}")
    
    if output_files:
        print("\n💡 PARA DESCARGAR EN COLAB:")
        print("from google.colab import files")
        print("import zipfile")
        print("!zip -r resultados.zip videos_output/")
        print("files.download('resultados.zip')")

def verificar_entorno():
    """Verificación rápida del entorno"""
    print("🔍 VERIFICANDO ENTORNO...")
    
    # Verificar Python
    print(f"🐍 Python: {sys.version}")
    
    # Verificar NumPy
    try:
        result = subprocess.run([sys.executable, "-c", "import numpy; print(f'NumPy: {numpy.__version__}')"], 
                              capture_output=True, text=True)
        print(f"✅ {result.stdout.strip()}")
    except:
        print("❌ NumPy problema")
    
    # Verificar CUDA
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ GPU disponible")
        else:
            print("⚠️ GPU no detectada")
    except:
        print("⚠️ nvidia-smi no disponible")

def main():
    """Comando principal"""
    print("🚀 INICIANDO SOLUCIÓN DEFINITIVA...")
    
    verificar_entorno()
    solucion_definitiva()
    
    print("\n🎯" * 80)
    print("✅ SCRIPT COMPLETADO")
    print("🎯" * 80)

if __name__ == "__main__":
    main()