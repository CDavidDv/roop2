#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
from pathlib import Path
import time
from filename_generator import generate_output_filename

class BatchProcessor:
    def __init__(self):
        self.source_dir = "source"
        self.input_dir = "videos_input"
        self.output_dir = "videos_output"
        self.temp_dir = "temp_processing"
        self.default_args = [
            "--execution-provider", "cuda",
            "--max-memory", "12",
            "--execution-threads", "30",
            "--temp-frame-quality", "100",
            "--keep-fps"
        ]
    
    def find_source_image(self):
        """Busca la imagen fuente en la carpeta source"""
        source_path = Path(self.source_dir)
        if not source_path.exists():
            print(f"❌ Error: Carpeta '{self.source_dir}' no existe")
            return None
        
        # Buscar archivos de imagen comunes
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff']
        source_files = []
        
        for ext in image_extensions:
            source_files.extend(source_path.glob(ext))
        
        if not source_files:
            print(f"❌ Error: No se encontraron imágenes en '{self.source_dir}'")
            return None
        
        # Usar la primera imagen encontrada
        source_image = str(source_files[0])
        print(f"✅ Imagen fuente encontrada: {source_image}")
        return source_image
    
    def find_input_videos(self):
        """Busca todos los videos en videos_input"""
        input_path = Path(self.input_dir)
        if not input_path.exists():
            print(f"❌ Error: Carpeta '{self.input_dir}' no existe")
            return []
        
        # Buscar archivos de video comunes
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(input_path.glob(ext))
        
        if not video_files:
            print(f"⚠️  No se encontraron videos en '{self.input_dir}'")
            return []
        
        print(f"✅ Encontrados {len(video_files)} videos para procesar:")
        for video in video_files:
            print(f"   - {video.name}")
        
        return [str(video) for video in video_files]
    
    def ensure_output_dir(self):
        """Asegura que existe la carpeta de salida"""
        output_path = Path(self.output_dir)
        output_path.mkdir(exist_ok=True)
        print(f"✅ Carpeta de salida: {self.output_dir}")
    
    def ensure_temp_dir(self):
        """Asegura que existe la carpeta temporal"""
        temp_path = Path(self.temp_dir)
        temp_path.mkdir(exist_ok=True)
        print(f"✅ Carpeta temporal: {self.temp_dir}")
    
    def process_video(self, source_image, input_video):
        """Procesa un video individual con doble face enhancer"""
        # Crear nombre de archivo de salida combinando imagen y video
        output_path = generate_output_filename(source_image, input_video, self.output_dir)
        temp_output = Path(self.temp_dir) / f"temp_{Path(input_video).stem}.mp4"
        temp_output_swap = Path(self.temp_dir) / f"swap_{Path(input_video).stem}.mp4"
        
        # Argumentos básicos para detección de rostros
        face_args = [
            "--many-faces",
            "--similar-face-distance", "0.85",
            "--reference-face-position", "0"
        ]
        
        # Paso 1: Primer face enhancer
        print(f"\n🎬 Procesando: {Path(input_video).name}")
        print(f"   Entrada: {input_video}")
        print(f"   Paso 1: Primer face enhancer")
        print("-" * 60)
        
        cmd_step1 = [
            sys.executable, "run.py",
            "-s", source_image,
            "-t", input_video,
            "-o", str(temp_output)
        ] + self.default_args + face_args + ["--frame-processor", "face_enhancer"]
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd_step1, check=True, capture_output=True, text=True)
            print(f"✅ Primer face enhancer completado")
            
            # Verificar que el archivo temporal se creó correctamente
            if not temp_output.exists():
                print(f"❌ Error: No se creó el archivo temporal {temp_output}")
                return False
            
            # Paso 2: Face swap
            print(f"\n🔄 Paso 2: Face swap")
            print("-" * 60)
            
            temp_input = temp_output
            
            cmd_step2 = [
                sys.executable, "run.py",
                "-s", source_image,
                "-t", str(temp_input),
                "-o", str(temp_output_swap)
            ] + self.default_args + face_args + ["--frame-processor", "face_swapper"]
            
            result = subprocess.run(cmd_step2, check=True, capture_output=True, text=True)
            print(f"✅ Face swap completado")
            
            # Verificar que el archivo de face swap se creó correctamente
            if not temp_output_swap.exists():
                print(f"❌ Error: No se creó el archivo de face swap {temp_output_swap}")
                # Limpiar archivo temporal del paso 1
                if temp_output.exists():
                    temp_output.unlink()
                return False
            
            # Paso 3: Segundo face enhancer
            print(f"\n✨ Paso 3: Segundo face enhancer")
            print("-" * 60)
            
            cmd_step3 = [
                sys.executable, "run.py",
                "-s", source_image,
                "-t", str(temp_output_swap),
                "-o", str(output_path)
            ] + self.default_args + face_args + ["--frame-processor", "face_enhancer"]
            
            result = subprocess.run(cmd_step3, check=True, capture_output=True, text=True)
            
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"✅ Segundo face enhancer completado")
            print(f"✅ Procesamiento completo en {processing_time:.1f} segundos")
            print(f"📁 Archivo final: {output_path}")
            
            # Verificar que el archivo final se creó correctamente
            if not Path(output_path).exists():
                print(f"❌ Error: No se creó el archivo final {output_path}")
                # Limpiar archivos temporales
                if temp_output.exists():
                    temp_output.unlink()
                if temp_output_swap.exists():
                    temp_output_swap.unlink()
                return False
            
            # Limpiar archivos temporales
            if temp_output.exists():
                temp_output.unlink()
            if temp_output_swap.exists():
                temp_output_swap.unlink()
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error procesando {Path(input_video).name}:")
            print(f"   Código de error: {e.returncode}")
            if e.stdout:
                print(f"   Salida: {e.stdout}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            
            # Limpiar archivos temporales en caso de error
            if temp_output.exists():
                temp_output.unlink()
            if temp_output_swap.exists():
                temp_output_swap.unlink()
            
            return False
    
    def run_batch_processing(self):
        """Ejecuta el procesamiento por lotes"""
        print("🚀 Iniciando procesamiento por lotes con doble face enhancer...")
        print("=" * 60)
        
        # Verificar imagen fuente
        source_image = self.find_source_image()
        if not source_image:
            return False
        
        # Verificar videos de entrada
        input_videos = self.find_input_videos()
        if not input_videos:
            return False
        
        # Asegurar carpetas de salida y temporal
        self.ensure_output_dir()
        self.ensure_temp_dir()
        
        # Procesar cada video
        total_videos = len(input_videos)
        successful = 0
        failed = 0
        
        print(f"\n📊 Iniciando procesamiento de {total_videos} videos...")
        print("=" * 60)
        
        for i, video in enumerate(input_videos, 1):
            print(f"\n[{i}/{total_videos}] Procesando video...")
            
            if self.process_video(source_image, video):
                successful += 1
            else:
                failed += 1
        
        # Resumen final
        print("\n" + "=" * 60)
        print("📊 RESUMEN FINAL")
        print("=" * 60)
        print(f"✅ Videos procesados exitosamente: {successful}")
        print(f"❌ Videos con errores: {failed}")
        print(f"📁 Videos guardados en: {self.output_dir}")
        
        if successful > 0:
            print(f"\n🎉 ¡Procesamiento completado! {successful} videos procesados.")
        else:
            print(f"\n⚠️  No se pudo procesar ningún video.")
        
        return successful > 0

def main():
    processor = BatchProcessor()
    success = processor.run_batch_processing()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 