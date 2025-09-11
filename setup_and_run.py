#!/usr/bin/env python3
"""
Script TODO-EN-UNO para Google Colab
Configura todo y ejecuta procesamiento por lotes

Basado en el roop original que funcionaba
"""

import os
import subprocess
import sys
from pathlib import Path
import time

def create_folders():
    """Crea las carpetas necesarias"""
    print("📁 Creando estructura de carpetas...")
    folders = ["source", "videos_input", "videos_output"]
    for folder in folders:
        Path(folder).mkdir(exist_ok=True)
        print(f"✅ {folder}/")
    return folders

def simple_install():
    """Instalación mínima - solo lo esencial"""
    print("📦 Instalación mínima de dependencias...")
    
    # Solo instalar lo que realmente falta, sin tocar lo que ya funciona
    essential = [
        "onnxruntime-gpu",
        "insightface", 
        "gfpgan"
    ]
    
    for package in essential:
        print(f"📦 {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True, timeout=120)
            print("✅ OK")
        except:
            print("⚠️ Ya instalado o error - continuando...")

def find_files():
    """Encuentra archivos fuente y videos"""
    source_files = list(Path("source").glob("*.*"))
    video_files = list(Path("videos_input").glob("*.*"))
    
    # Filtrar solo formatos válidos
    valid_image_ext = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    valid_video_ext = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    
    source_files = [f for f in source_files if f.suffix.lower() in valid_image_ext]
    video_files = [f for f in video_files if f.suffix.lower() in valid_video_ext]
    
    return source_files, video_files

def process_with_original_command(source_img, target_video, output_path):
    """Usa el comando original de roop sin modificaciones complejas"""
    
    print(f"🎬 Procesando: {target_video.name}")
    print(f"📸 Fuente: {source_img.name}")
    print(f"💾 Salida: {output_path}")
    
    # Comando básico como el original
    cmd = [
        sys.executable, "run.py",  # Usar el run.py original
        "-s", str(source_img),
        "-t", str(target_video),
        "-o", str(output_path),
        "--execution-provider", "cuda",  # Usar GPU
        "--execution-threads", "8",
        "--keep-fps"
    ]
    
    print(f"🔧 Comando: {' '.join(cmd)}")
    
    try:
        # Ejecutar sin capturar salida para ver errores en tiempo real
        result = subprocess.run(cmd, timeout=3600)  # 1 hora timeout
        
        if result.returncode == 0:
            print("✅ ¡Procesamiento exitoso!")
            return True
        else:
            print(f"❌ Error - código de salida: {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout - video muy largo")
        return False
    except KeyboardInterrupt:
        print("❌ Cancelado por usuario")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando: {e}")
        return False

def batch_process():
    """Procesamiento por lotes simple"""
    print("🚀" * 60)
    print("🎬 ROOP BATCH PROCESSOR - Versión Original Mejorada")
    print("🚀" * 60)
    
    # 1. Crear carpetas
    create_folders()
    
    # 2. Instalar dependencias mínimas
    simple_install()
    
    # 3. Buscar archivos
    source_files, video_files = find_files()
    
    if not source_files:
        print("\n❌ PROBLEMA: No hay imágenes fuente")
        print("📤 SOLUCIÓN: Sube una imagen a la carpeta 'source/'")
        print("   Formatos válidos: .jpg, .png, .jpeg, .bmp, .tiff")
        return
    
    if not video_files:
        print("\n❌ PROBLEMA: No hay videos para procesar")
        print("📤 SOLUCIÓN: Sube videos a la carpeta 'videos_input/'")
        print("   Formatos válidos: .mp4, .avi, .mov, .mkv, .wmv")
        return
    
    # 4. Seleccionar imagen fuente (primera disponible)
    source_image = source_files[0]
    print(f"\n📸 Imagen fuente: {source_image.name}")
    
    # 5. Mostrar videos encontrados
    print(f"\n🎬 Videos a procesar ({len(video_files)}):")
    for i, video in enumerate(video_files, 1):
        print(f"   {i}. {video.name}")
    
    # 6. Procesar cada video
    print(f"\n🚀 Iniciando procesamiento por lotes...")
    success_count = 0
    
    for i, video in enumerate(video_files, 1):
        print(f"\n{'='*60}")
        print(f"📊 PROGRESO: {i}/{len(video_files)}")
        print(f"{'='*60}")
        
        # Nombre de salida simple
        output_name = f"processed_{video.name}"
        output_path = Path("videos_output") / output_name
        
        start_time = time.time()
        
        if process_with_original_command(source_image, video, output_path):
            success_count += 1
            elapsed = time.time() - start_time
            print(f"⏱️ Tiempo: {elapsed:.1f} segundos")
        else:
            print("💡 TIP: Si hay errores, verifica que las dependencias estén bien instaladas")
    
    # 7. Resumen final
    print(f"\n{'🚀'*60}")
    print("🎉 PROCESAMIENTO COMPLETADO")
    print(f"{'🚀'*60}")
    print(f"✅ Videos exitosos: {success_count}/{len(video_files)}")
    print(f"📁 Resultados en: videos_output/")
    
    if success_count < len(video_files):
        failed = len(video_files) - success_count
        print(f"⚠️ {failed} videos fallaron")
        print("💡 TIPS para solucionar:")
        print("   • Verifica que los videos no estén corruptos")
        print("   • Asegúrate de que la imagen fuente sea clara")
        print("   • Prueba con un video más pequeño primero")
    
    # 8. Mostrar archivos generados
    output_files = list(Path("videos_output").glob("*.*"))
    if output_files:
        print(f"\n📋 Archivos generados:")
        for file in output_files:
            print(f"   • {file.name}")

def main():
    """Función principal - TODO EN UNO"""
    try:
        batch_process()
    except KeyboardInterrupt:
        print("\n❌ Proceso cancelado por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("💡 Intenta ejecutar el script nuevamente")

if __name__ == "__main__":
    main()