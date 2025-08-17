#!/usr/bin/env python3
"""
ROOP Batch Processor para Google Colab
Versión simplificada con optimizaciones de memoria automáticas
"""

import os
import subprocess
from pathlib import Path
import time

def print_colab_banner():
    """Banner específico para Colab"""
    print("🚀" * 50)
    print("🎬 ROOP BATCH PROCESSOR - Google Colab Edition 🎬")
    print("🚀" * 50)
    print("✨ Optimizado para memoria automáticamente")
    print("🚀" * 50)

def get_colab_settings():
    """Configuraciones optimizadas para Colab"""
    return {
        "batch_size": 1,           # Muy conservador para Colab
        "max_memory": 6,           # Límite de memoria para Colab
        "execution_threads": 8,    # Threads reducidos
        "temp_frame_format": "jpg", # JPG para ahorrar memoria
        "temp_frame_quality": 90   # Calidad alta pero no máxima
    }

def find_files():
    """Encuentra archivos en el directorio actual"""
    # Buscar imágenes
    image_files = list(Path(".").glob("*.jpg")) + list(Path(".").glob("*.png"))
    
    # Buscar videos
    video_files = list(Path(".").glob("*.mp4")) + list(Path(".").glob("*.avi"))
    
    return image_files, video_files

def process_video_colab(source_image, target_video, settings):
    """Procesa un video en Colab con configuraciones optimizadas"""
    output_name = f"processed_{target_video.name}"
    
    cmd = [
        "python", "run.py",
        "-s", str(source_image),
        "-t", str(target_video),
        "-o", output_name,
        "--memory-optimization",
        "--batch-size", str(settings["batch_size"]),
        "--max-memory", str(settings["max_memory"]),
        "--execution-threads", str(settings["execution_threads"]),
        "--temp-frame-format", settings["temp_frame_format"],
        "--temp-frame-quality", str(settings["temp_frame_quality"]),
        "--keep-fps"
    ]
    
    print(f"\n🎬 Procesando: {target_video.name}")
    print(f"📸 Fuente: {source_image.name}")
    print(f"💾 Salida: {output_name}")
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✅ Completado en {duration:.1f} segundos")
        
        return True, duration
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        if e.stderr:
            print(f"Detalles: {e.stderr[:200]}...")
        return False, 0

def main_colab():
    """Función principal para Colab"""
    print_colab_banner()
    
    # Obtener configuraciones para Colab
    settings = get_colab_settings()
    
    print(f"\n⚙️  Configuración para Colab:")
    print(f"   • Batch size: {settings['batch_size']}")
    print(f"   • Memoria máxima: {settings['max_memory']}GB")
    print(f"   • Threads: {settings['execution_threads']}")
    print(f"   • Formato: {settings['temp_frame_format']}")
    
    # Encontrar archivos
    image_files, video_files = find_files()
    
    if not image_files:
        print("\n❌ No se encontraron imágenes fuente (.jpg, .png)")
        print("   Sube una imagen al directorio actual")
        return
    
    if not video_files:
        print("\n❌ No se encontraron videos (.mp4, .avi)")
        print("   Sube un video al directorio actual")
        return
    
    # Seleccionar imagen fuente
    if len(image_files) == 1:
        source_image = image_files[0]
        print(f"\n📸 Imagen fuente automática: {source_image.name}")
    else:
        print("\n📸 Imágenes encontradas:")
        for i, img in enumerate(image_files):
            print(f"   {i+1}. {img.name}")
        
        try:
            choice = int(input("\nSelecciona imagen (número): ")) - 1
            if 0 <= choice < len(image_files):
                source_image = image_files[choice]
            else:
                print("❌ Selección inválida")
                return
        except:
            print("❌ Selección inválida")
            return
    
    # Mostrar videos a procesar
    print(f"\n🎬 Videos encontrados ({len(video_files)}):")
    for video in video_files:
        print(f"   • {video.name}")
    
    # Confirmar
    print(f"\n⚠️  ¿Procesar {len(video_files)} videos? (s/N): ", end="")
    try:
        confirm = input().lower().strip()
        if confirm not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Cancelado")
            return
    except:
        print("❌ Cancelado")
        return
    
    # Procesar videos
    print(f"\n🚀 Iniciando procesamiento...")
    successful = 0
    total_time = 0
    
    for i, video in enumerate(video_files, 1):
        print(f"\n📊 Progreso: {i}/{len(video_files)} ({(i/len(video_files)*100):.1f}%)")
        
        success, duration = process_video_colab(source_image, video, settings)
        
        if success:
            successful += 1
            total_time += duration
        
        # Pausa entre videos para Colab
        if i < len(video_files):
            print("⏳ Pausa de 10 segundos para Colab...")
            time.sleep(10)
    
    # Resumen
    print("\n" + "="*50)
    print("🎉 COMPLETADO")
    print("="*50)
    print(f"✅ Exitosos: {successful}/{len(video_files)}")
    print(f"⏱️  Tiempo total: {total_time:.1f}s")
    
    if successful < len(video_files):
        print(f"⚠️  {len(video_files) - successful} fallaron")
        print("   Revisa los errores arriba")

if __name__ == "__main__":
    try:
        main_colab()
    except KeyboardInterrupt:
        print("\n❌ Interrumpido")
    except Exception as e:
        print(f"\n❌ Error: {e}")
