#!/usr/bin/env python3
"""
ROOP Simple para Google Colab - Sin dependencias GUI
Soluciona todos los problemas de compatibilidad
"""

import subprocess
import sys
import os
from pathlib import Path

def fix_environment():
    """Arregla el entorno de Colab"""
    print("🔧 Preparando entorno para Colab...")
    
    # Fix NumPy compatibility - usar la versión que funciona en tu entorno
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.26.4"], 
                      check=True, capture_output=True)
        print("✅ NumPy 1.26.4 instalado")
    except:
        print("⚠️ Warning: No se pudo instalar NumPy 1.26.4")
    
    # Install essentials
    packages = ["onnxruntime-gpu", "insightface", "opennsfw2", "gfpgan"]
    for pkg in packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", pkg], 
                          check=True, capture_output=True)
            print(f"✅ {pkg} instalado")
        except:
            print(f"⚠️ Warning: {pkg} falló")

def process_single_video(source_img, target_video, output_path):
    """Procesa un video usando comandos directos - evita imports problemáticos"""
    
    print(f"🎬 Procesando: {target_video}")
    print(f"📸 Fuente: {source_img}")
    print(f"💾 Salida: {output_path}")
    
    # Comando directo sin imports complejos
    cmd = [
        sys.executable, "run_headless.py",
        "-s", str(source_img),
        "-t", str(target_video), 
        "-o", str(output_path),
        "--memory-optimization",
        "--batch-size", "1",
        "--max-memory", "8",
        "--execution-threads", "8",
        "--temp-frame-format", "jpg",
        "--temp-frame-quality", "85",
        "--keep-fps"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode == 0:
            print("✅ Video procesado exitosamente")
            return True
        else:
            print(f"❌ Error procesando video:")
            print(f"STDOUT: {result.stdout[-500:]}")  # Últimas 500 chars
            print(f"STDERR: {result.stderr[-500:]}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Timeout - video muy largo o sistema lento")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando comando: {e}")
        return False

def main():
    print("🚀" * 50)
    print("🎬 ROOP SIMPLE - Google Colab Edition")
    print("🚀" * 50)
    
    # Verificar estructura de carpetas
    for folder in ["source", "videos_input", "videos_output"]:
        Path(folder).mkdir(exist_ok=True)
        print(f"📁 Carpeta {folder}/ verificada")
    
    # Buscar archivos
    source_files = list(Path("source").glob("*.*"))
    video_files = list(Path("videos_input").glob("*.*"))
    
    if not source_files:
        print("❌ No hay imágenes fuente en source/")
        print("💡 Sube una imagen a la carpeta source/")
        return
    
    if not video_files:
        print("❌ No hay videos en videos_input/")
        print("💡 Sube videos a la carpeta videos_input/")
        return
    
    source_image = source_files[0]
    print(f"📸 Usando imagen fuente: {source_image.name}")
    
    print(f"🎬 Videos encontrados: {len(video_files)}")
    for video in video_files:
        print(f"   • {video.name}")
    
    # Arreglar entorno antes de procesar
    fix_environment()
    
    # Procesar cada video
    success_count = 0
    for i, video in enumerate(video_files, 1):
        print(f"\n📊 Progreso: {i}/{len(video_files)}")
        
        output_name = f"processed_{video.name}"
        output_path = Path("videos_output") / output_name
        
        if process_single_video(source_image, video, output_path):
            success_count += 1
        
        print("-" * 50)
    
    print("\n" + "🚀" * 50)
    print("🎉 PROCESAMIENTO COMPLETADO")
    print("🚀" * 50)
    print(f"✅ Videos exitosos: {success_count}/{len(video_files)}")
    print(f"📁 Resultados en: videos_output/")
    
    if success_count < len(video_files):
        print(f"⚠️ {len(video_files) - success_count} videos fallaron")
        print("💡 Revisa los logs de error arriba")

if __name__ == "__main__":
    main()