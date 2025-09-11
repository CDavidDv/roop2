#!/usr/bin/env python3
"""
Batch Processor para ROOP con optimizaciones de memoria
Perfecto para usar con !python en Google Colab o Jupyter Notebook
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
import time

def print_banner():
    """Muestra un banner informativo"""
    print("🚀" * 50)
    print("🎬 ROOP BATCH PROCESSOR - Optimizado para Memoria 🎬")
    print("🚀" * 50)
    print("✨ Características:")
    print("   • Optimización automática de memoria")
    print("   • Procesamiento en lotes inteligentes")
    print("   • Monitoreo de memoria en tiempo real")
    print("   • Configuración automática según el sistema")
    print("🚀" * 50)

def get_system_info():
    """Obtiene información del sistema para optimización automática"""
    try:
        import psutil
        memory_gb = psutil.virtual_memory().total / (1024**3)
        
        if memory_gb < 8:
            return "low_memory"
        elif memory_gb < 16:
            return "medium_memory"
        else:
            return "high_memory"
    except:
        return "medium_memory"  # Default seguro

def get_optimal_settings(memory_profile):
    """Obtiene configuraciones óptimas según el perfil de memoria"""
    settings = {
        "low_memory": {
            "batch_size": 1,
            "max_memory": 4,
            "execution_threads": 6,
            "temp_frame_format": "jpg",
            "temp_frame_quality": 85
        },
        "medium_memory": {
            "batch_size": 2,
            "max_memory": 8,
            "execution_threads": 12,
            "temp_frame_format": "png",
            "temp_frame_quality": 95
        },
        "high_memory": {
            "batch_size": 3,
            "max_memory": 16,
            "execution_threads": 20,
            "temp_frame_format": "png",
            "temp_frame_quality": 100
        }
    }
    return settings.get(memory_profile, settings["medium_memory"])

def find_video_files(directory="videos_input"):
    """Encuentra archivos de video en la carpeta videos_input"""
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm']
    video_files = []
    
    # Verificar si la carpeta existe
    if not Path(directory).exists():
        print(f"⚠️  Carpeta '{directory}' no encontrada, creando...")
        Path(directory).mkdir(exist_ok=True)
        return video_files
    
    for ext in video_extensions:
        video_files.extend(Path(directory).glob(f"*{ext}"))
        video_files.extend(Path(directory).glob(f"*{ext.upper()}"))
    
    return sorted(video_files)

def find_image_files(directory="source"):
    """Encuentra archivos de imagen en la carpeta source"""
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    image_files = []
    
    # Verificar si la carpeta existe
    if not Path(directory).exists():
        print(f"⚠️  Carpeta '{directory}' no encontrada, creando...")
        Path(directory).mkdir(exist_ok=True)
        return image_files
    
    for ext in image_extensions:
        image_files.extend(Path(directory).glob(f"*{ext}"))
        image_files.extend(Path(directory).glob(f"*{ext.upper()}"))
    
    return sorted(image_files)

def process_single_video(source_image, target_video, output_dir, settings):
    """Procesa un solo video con las configuraciones optimizadas"""
    output_path = Path(output_dir) / f"processed_{target_video.name}"
    
    cmd = [
        "python", "run_headless.py",
        "-s", str(source_image),
        "-t", str(target_video),
        "-o", str(output_path),
        "--max-memory", str(settings["max_memory"]),
        "--execution-threads", str(settings["execution_threads"]),
        "--temp-frame-format", settings["temp_frame_format"],
        "--temp-frame-quality", str(settings["temp_frame_quality"]),
        "--keep-fps"
    ]
    
    print(f"\n🎬 Procesando: {target_video.name}")
    print(f"📸 Fuente: {source_image.name}")
    print(f"💾 Salida: {output_path}")
    print(f"⚙️  Configuración: batch={settings['batch_size']}, mem={settings['max_memory']}GB, threads={settings['execution_threads']}")
    
    try:
        start_time = time.time()
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✅ Completado en {duration:.1f} segundos")
        
        return True, duration
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error procesando {target_video.name}: {e}")
        if e.stderr:
            print(f"Detalles del error: {e.stderr}")
        return False, 0

def main():
    """Función principal del procesador por lotes"""
    parser = argparse.ArgumentParser(description="ROOP Batch Processor con optimización de memoria")
    parser.add_argument("--source", "-s", help="Imagen fuente (opcional, se detecta automáticamente)")
    parser.add_argument("--output-dir", "-o", default="videos_output", help="Directorio de salida (default: videos_output)")
    parser.add_argument("--input-dir", "-i", default="videos_input", help="Directorio de entrada (default: videos_input)")
    parser.add_argument("--source-dir", default="source", help="Directorio de imágenes fuente (default: source)")
    parser.add_argument("--force", "-f", action="store_true", help="Forzar reprocesamiento")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar qué se procesaría")
    parser.add_argument("--auto", "-a", action="store_true", help="Procesar automáticamente sin confirmación")
    
    args = parser.parse_args()
    
    print_banner()
    
    # Detectar configuración del sistema
    memory_profile = get_system_info()
    settings = get_optimal_settings(memory_profile)
    
    print(f"\n💻 Perfil de sistema detectado: {memory_profile}")
    print(f"⚙️  Configuración automática:")
    print(f"   • Batch size: {settings['batch_size']}")
    print(f"   • Memoria máxima: {settings['max_memory']}GB")
    print(f"   • Threads: {settings['execution_threads']}")
    print(f"   • Formato temporal: {settings['temp_frame_format']}")
    
    # Crear directorio de salida
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    print(f"\n📁 Directorio de salida: {output_dir.absolute()}")
    
    # Encontrar archivos en las carpetas específicas
    source_images = find_image_files(args.source_dir)
    video_files = find_video_files(args.input_dir)
    
    if not source_images:
        print(f"\n❌ No se encontraron archivos de imagen fuente en '{args.source_dir}'")
        print(f"   Coloca una imagen .jpg, .png, etc. en la carpeta '{args.source_dir}'")
        print(f"   O usa --source-dir para especificar otra carpeta")
        return
    
    if not video_files:
        print(f"\n❌ No se encontraron archivos de video en '{args.input_dir}'")
        print(f"   Coloca videos .mp4, .avi, etc. en la carpeta '{args.input_dir}'")
        print(f"   O usa --input-dir para especificar otra carpeta")
        return
    
    # Seleccionar imagen fuente
    if args.source:
        source_image = Path(args.source)
        if not source_image.exists():
            print(f"❌ La imagen fuente especificada no existe: {args.source}")
            return
    else:
        if len(source_images) == 1:
            source_image = source_images[0]
        else:
            print(f"\n📸 Imágenes fuente encontradas en '{args.source_dir}':")
            for i, img in enumerate(source_images):
                print(f"   {i+1}. {img.name}")
            
            try:
                choice = int(input("\nSelecciona una imagen (número): ")) - 1
                if 0 <= choice < len(source_images):
                    source_image = source_images[choice]
                else:
                    print("❌ Selección inválida")
                    return
            except (ValueError, KeyboardInterrupt):
                print("\n❌ Selección inválida")
                return
    
    print(f"\n🎯 Imagen fuente seleccionada: {source_image.name}")
    
    # Filtrar videos que ya fueron procesados
    if not args.force:
        unprocessed_videos = []
        for video in video_files:
            output_path = output_dir / f"processed_{video.name}"
            if not output_path.exists():
                unprocessed_videos.append(video)
        
        if not unprocessed_videos:
            print("✅ Todos los videos ya han sido procesados")
            print("   Usa --force para reprocesar")
            return
        
        video_files = unprocessed_videos
    
    print(f"\n🎬 Videos a procesar desde '{args.input_dir}' ({len(video_files)}):")
    for video in video_files:
        print(f"   • {video.name}")
    
    if args.dry_run:
        print("\n🔍 Modo dry-run - No se procesará nada")
        return
    
    print(f"\n🚀 Procesando automáticamente {len(video_files)} videos...")
    
    # Procesar videos
    print(f"\n🚀 Iniciando procesamiento por lotes...")
    successful = 0
    total_duration = 0
    
    for i, video in enumerate(video_files, 1):
        print(f"\n📊 Progreso: {i}/{len(video_files)} ({(i/len(video_files)*100):.1f}%)")
        
        success, duration = process_single_video(source_image, video, output_dir, settings)
        
        if success:
            successful += 1
            total_duration += duration
        
        # Pausa entre videos para permitir limpieza de memoria
        if i < len(video_files):
            print("⏳ Pausa de 5 segundos para limpieza de memoria...")
            time.sleep(5)
    
    # Resumen final
    print("\n" + "="*60)
    print("🎉 PROCESAMIENTO COMPLETADO")
    print("="*60)
    print(f"✅ Videos procesados exitosamente: {successful}/{len(video_files)}")
    print(f"⏱️  Tiempo total: {total_duration:.1f} segundos")
    print(f"📁 Archivos de salida en: {output_dir.absolute()}")
    
    if successful < len(video_files):
        print(f"⚠️  {len(video_files) - successful} videos fallaron")
        print("   Revisa los logs de error arriba")
    
    print("\n💡 Consejos:")
    print("   • Si tuviste errores de memoria, reduce --batch-size")
    print("   • Para mejor calidad, usa --temp-frame-format png")
    print("   • Cierra otras aplicaciones durante el procesamiento")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Procesamiento interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("Por favor, reporta este error con los detalles completos") 