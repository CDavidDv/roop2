#!/usr/bin/env python3
"""
🎬 SCRIPT 2: PROCESAMIENTO DE VIDEOS CON MÁXIMA CALIDAD
Pipeline: face_enhancer → face_swapper → face_enhancer
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from datetime import datetime

def banner():
    """Banner del procesador"""
    print("🎬" * 80)
    print("🎬 SCRIPT 2: PROCESAMIENTO CON MÁXIMA CALIDAD")
    print("🎬" * 80)
    print("🎯 Pipeline: face_enhancer → face_swapper → face_enhancer")
    print("🎯 Calidad: MÁXIMA (PNG 100%, Video sin compresión)")
    print("🎯 GPU: Tesla T4 optimizado")
    print("🎬" * 80)

def verificar_entorno():
    """Verifica que todo esté instalado"""
    print("\n🔍 VERIFICANDO ENTORNO...")
    print("=" * 50)
    
    # Verificar NumPy
    try:
        result = subprocess.run([sys.executable, "-c", "import numpy; print(f'NumPy: {numpy.__version__}')"], 
                              capture_output=True, text=True)
        print(f"✅ {result.stdout.strip()}")
        
        # Verificar que es la versión correcta
        if "1.26.4" not in result.stdout:
            print("⚠️ NumPy puede no ser compatible - se recomienda 1.26.4")
    except:
        print("❌ NumPy no disponible - ejecuta 1_INSTALAR_TODO.py primero")
        return False
    
    # Verificar GPU
    try:
        result = subprocess.run([sys.executable, "-c", """
import onnxruntime as ort
providers = ort.get_available_providers()
if 'CUDAExecutionProvider' in providers:
    print('✅ GPU CUDA disponible')
else:
    print('⚠️ Solo CPU disponible')
"""], capture_output=True, text=True)
        print(result.stdout.strip())
    except:
        print("❌ ONNX Runtime no disponible")
        return False
    
    return True

def verificar_archivos():
    """Verifica que los archivos necesarios estén presentes"""
    print("\n📁 VERIFICANDO ARCHIVOS...")
    print("=" * 50)
    
    # Verificar imagen fuente
    source_files = list(Path("source").glob("*.*"))
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    source_images = [f for f in source_files if f.suffix.lower() in image_extensions]
    
    if not source_images:
        print("❌ No hay imágenes fuente en source/")
        print("💡 Sube una imagen (.jpg, .png, etc.) a la carpeta source/")
        return None, []
    
    # Verificar videos
    video_files = list(Path("videos_input").glob("*.*"))
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv'}
    videos = [f for f in video_files if f.suffix.lower() in video_extensions]
    
    if not videos:
        print("❌ No hay videos en videos_input/")
        print("💡 Sube videos a la carpeta videos_input/")
        return None, []
    
    source_image = source_images[0]
    print(f"📸 Imagen fuente: {source_image.name}")
    print(f"🎬 Videos encontrados: {len(videos)}")
    for i, video in enumerate(videos, 1):
        print(f"   {i}. {video.name}")
    
    return source_image, videos

def crear_comando_maxima_calidad(source_path, target_path, output_path):
    """Crea comando optimizado para máxima calidad"""
    
    # Configuración de MÁXIMA CALIDAD
    cmd = [
        sys.executable, "run_simple.py",
        "-s", str(source_path),
        "-t", str(target_path),
        "-o", str(output_path),
        
        # Pipeline de calidad: enhancer → swapper → enhancer
        "--frame-processor", "face_enhancer", "face_swapper", "face_enhancer",
        
        # CALIDAD MÁXIMA - FRAMES
        "--temp-frame-format", "png",           # PNG sin compresión
        "--temp-frame-quality", "100",          # Calidad máxima
        
        # CALIDAD MÁXIMA - VIDEO
        "--output-video-quality", "0",          # Sin compresión de video
        "--output-video-encoder", "h264_nvenc", # Hardware encoding
        "--keep-fps",                           # Mantener FPS original
        
        # GPU Y MEMORIA
        "--execution-provider", "cuda",         # Usar GPU
        "--execution-threads", "8",             # Threads optimizados
        "--max-memory", "12",                   # Máxima memoria Tesla T4
        
        # CONFIGURACIÓN DE ROSTROS
        "--similar-face-distance", "0.85",     # Precisión alta
        "--reference-face-position", "0",      # Primera cara detectada
        "--many-faces",                         # Procesar todas las caras
        
        # AUDIO Y LIMPIEZA
        # NO skip audio - mantener audio original
        # NO keep frames - limpiar al final
    ]
    
    return cmd

def procesar_video_calidad_maxima(source_image, video_file, progress_info):
    """Procesa un video con configuración de máxima calidad"""
    
    print(f"\n{'='*80}")
    print(f"📊 {progress_info}")
    print(f"{'='*80}")
    print(f"🎬 Video: {video_file.name}")
    print(f"📸 Fuente: {source_image.name}")
    
    # Nombre de salida con timestamp para evitar sobrescribir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"MAXCAL_{timestamp}_{video_file.stem}.mp4"
    output_path = Path("videos_output") / output_name
    
    print(f"💾 Salida: {output_name}")
    
    # Crear comando de máxima calidad
    cmd = crear_comando_maxima_calidad(source_image, video_file, output_path)
    
    print(f"\n🔧 CONFIGURACIÓN APLICADA:")
    print(f"   📸 Frames: PNG 100% (sin compresión)")
    print(f"   🎬 Video: Calidad 0 (sin compresión)")
    print(f"   🤖 Pipeline: enhancer → swapper → enhancer")
    print(f"   🚀 GPU: CUDA con {cmd[cmd.index('--execution-threads') + 1]} threads")
    print(f"   💾 Memoria: {cmd[cmd.index('--max-memory') + 1]}GB")
    
    print(f"\n🚀 Iniciando procesamiento...")
    start_time = time.time()
    
    try:
        # Ejecutar con salida en tiempo real
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            text=True, 
            bufsize=1, 
            universal_newlines=True
        )
        
        # Mostrar progreso en tiempo real
        last_progress = ""
        for line in process.stdout:
            line = line.strip()
            
            # Mostrar líneas de progreso
            if any(keyword in line.lower() for keyword in ['processing', '%', 'frame', 'fps']):
                if line != last_progress:  # Evitar spam
                    print(f"   📊 {line}")
                    last_progress = line
            
            # Mostrar errores importantes
            elif any(keyword in line.lower() for keyword in ['error', 'fail', 'exception']):
                print(f"   ⚠️ {line}")
        
        process.wait()
        elapsed_time = time.time() - start_time
        
        if process.returncode == 0:
            # Verificar que el archivo se creó y obtener su tamaño
            if output_path.exists():
                size_mb = output_path.stat().st_size / (1024 * 1024)
                print(f"\n✅ PROCESAMIENTO EXITOSO")
                print(f"   ⏱️ Tiempo: {elapsed_time:.1f} segundos")
                print(f"   📁 Archivo: {output_name}")
                print(f"   📊 Tamaño: {size_mb:.1f} MB")
                return True, elapsed_time, output_name
            else:
                print(f"\n❌ Archivo de salida no se creó")
                return False, elapsed_time, None
        else:
            print(f"\n❌ PROCESAMIENTO FALLÓ")
            print(f"   Código de error: {process.returncode}")
            return False, elapsed_time, None
            
    except subprocess.TimeoutExpired:
        print(f"\n❌ TIMEOUT - Video muy largo")
        process.kill()
        return False, time.time() - start_time, None
        
    except KeyboardInterrupt:
        print(f"\n❌ CANCELADO POR USUARIO")
        process.kill()
        return False, time.time() - start_time, None
        
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        return False, time.time() - start_time, None

def procesar_todos_los_videos():
    """Procesa todos los videos con máxima calidad"""
    
    # Verificar entorno
    if not verificar_entorno():
        return
    
    # Verificar archivos
    source_image, videos = verificar_archivos()
    if not source_image or not videos:
        return
    
    print(f"\n🚀 INICIANDO PROCESAMIENTO POR LOTES")
    print(f"📊 Total de videos: {len(videos)}")
    print(f"🎯 Configuración: MÁXIMA CALIDAD")
    
    # Estadísticas de procesamiento
    resultados = []
    tiempo_total_inicio = time.time()
    
    # Procesar cada video
    for i, video in enumerate(videos, 1):
        progress_info = f"PROGRESO: {i}/{len(videos)}"
        
        success, elapsed, output_name = procesar_video_calidad_maxima(
            source_image, video, progress_info
        )
        
        resultados.append({
            'video': video.name,
            'success': success,
            'time': elapsed,
            'output': output_name
        })
        
        # Pequeña pausa entre videos para estabilidad
        if i < len(videos):
            print(f"\n⏸️ Pausa de 2 segundos antes del siguiente video...")
            time.sleep(2)
    
    # Resumen final
    tiempo_total = time.time() - tiempo_total_inicio
    exitosos = sum(1 for r in resultados if r['success'])
    
    print(f"\n🎬" * 80)
    print("🎉 PROCESAMIENTO COMPLETADO")
    print("🎬" * 80)
    
    print(f"📊 ESTADÍSTICAS:")
    print(f"   ✅ Videos exitosos: {exitosos}/{len(videos)}")
    print(f"   ⏱️ Tiempo total: {tiempo_total:.1f} segundos ({tiempo_total/60:.1f} minutos)")
    print(f"   📁 Archivos generados:")
    
    archivos_salida = list(Path("videos_output").glob("MAXCAL_*.mp4"))
    for archivo in archivos_salida:
        size_mb = archivo.stat().st_size / (1024 * 1024)
        print(f"      • {archivo.name} ({size_mb:.1f} MB)")
    
    # Información de descarga para Colab
    if archivos_salida:
        print(f"\n📥 PARA DESCARGAR EN COLAB:")
        print(f"```python")
        print(f"from google.colab import files")
        print(f"import zipfile")
        print(f"!zip -r videos_maxima_calidad.zip videos_output/MAXCAL_*.mp4")
        print(f"files.download('videos_maxima_calidad.zip')")
        print(f"```")
    
    print("🎬" * 80)

def main():
    """Función principal"""
    banner()
    
    try:
        procesar_todos_los_videos()
    except KeyboardInterrupt:
        print("\n❌ Procesamiento cancelado por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()