#!/usr/bin/env python3

import os
import sys
import subprocess
import glob
from pathlib import Path
import time
from filename_generator import generate_output_filename

class EnhancedBatchProcessor:
    def __init__(self, pipeline_type="full"):
        self.source_dir = "source"
        self.input_dir = "videos_input"
        self.output_dir = "videos_output"
        
        # Configurar diferentes pipelines según el tipo
        if pipeline_type == "full":
            # Pipeline completo: pre_enhancer -> face_swapper -> post_enhancer
            self.frame_processors = ["pre_face_enhancer", "face_swapper", "post_face_enhancer"]
            self.pipeline_name = "Pipeline Completo"
        elif pipeline_type == "basic":
            # Pipeline básico: face_swapper -> face_enhancer (original)
            self.frame_processors = ["face_swapper", "face_enhancer"]
            self.pipeline_name = "Pipeline Básico"
        elif pipeline_type == "pre_only":
            # Solo mejora antes del swap
            self.frame_processors = ["pre_face_enhancer", "face_swapper"]
            self.pipeline_name = "Mejora Antes del Swap"
        elif pipeline_type == "post_only":
            # Solo mejora después del swap
            self.frame_processors = ["face_swapper", "post_face_enhancer"]
            self.pipeline_name = "Mejora Después del Swap"
        else:
            # Pipeline personalizado
            self.frame_processors = pipeline_type.split(",")
            self.pipeline_name = f"Pipeline Personalizado: {', '.join(self.frame_processors)}"
        
        self.default_args = [
            "--execution-provider", "cuda",
            "--max-memory", "12",
            "--execution-threads", "8",  # Optimizado para Tesla T4
            "--temp-frame-quality", "100",
            "--keep-fps",
            "--frame-processor"
        ] + self.frame_processors
    
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
    
    def process_video(self, source_image, input_video):
        """Procesa un video individual"""
        # Crear nombre de archivo de salida combinando imagen y video
        output_path = generate_output_filename(source_image, input_video, self.output_dir)
        
        # Construir comando usando el script mejorado
        cmd = [
            sys.executable, "run_enhanced_pipeline.py",
            "-s", source_image,
            "-t", input_video,
            "-o", str(output_path)
        ] + self.default_args
        
        input_path = Path(input_video)
        print(f"\n🎬 Procesando: {input_path.name}")
        print(f"   Entrada: {input_video}")
        print(f"   Salida: {output_path}")
        print(f"   Pipeline: {self.pipeline_name}")
        print(f"   Processors: {' -> '.join(self.frame_processors)}")
        print("-" * 60)
        
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            end_time = time.time()
            processing_time = end_time - start_time
            
            print(f"✅ Completado en {processing_time:.1f} segundos")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error procesando {input_path.name}:")
            print(f"   Código de error: {e.returncode}")
            if e.stdout:
                print(f"   Salida: {e.stdout}")
            if e.stderr:
                print(f"   Error: {e.stderr}")
            return False
    
    def run_batch_processing(self):
        """Ejecuta el procesamiento por lotes"""
        print("🚀 Iniciando procesamiento por lotes MEJORADO...")
        print("=" * 60)
        print(f"🔧 Pipeline: {self.pipeline_name}")
        print(f"⚙️  Processors: {' -> '.join(self.frame_processors)}")
        print("=" * 60)
        
        # Verificar imagen fuente
        source_image = self.find_source_image()
        if not source_image:
            return False
        
        # Verificar videos de entrada
        input_videos = self.find_input_videos()
        if not input_videos:
            return False
        
        # Asegurar carpeta de salida
        self.ensure_output_dir()
        
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
        print(f"🔧 Pipeline usado: {self.pipeline_name}")
        print(f"✅ Videos procesados exitosamente: {successful}")
        print(f"❌ Videos con errores: {failed}")
        print(f"📁 Videos guardados en: {self.output_dir}")
        
        if successful > 0:
            print(f"\n🎉 ¡Procesamiento completado! {successful} videos procesados.")
        else:
            print(f"\n⚠️  No se pudo procesar ningún video.")
        
        return successful > 0

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch Processor Mejorado para Roop')
    parser.add_argument('--pipeline', choices=['full', 'basic', 'pre_only', 'post_only', 'custom'],
                       default='full', help='Tipo de pipeline a usar')
    parser.add_argument('--custom-processors', help='Processors personalizados separados por coma (ej: pre_face_enhancer,face_swapper,post_face_enhancer)')
    
    args = parser.parse_args()
    
    if args.pipeline == 'custom':
        if not args.custom_processors:
            print("❌ Error: --custom-processors es requerido cuando --pipeline=custom")
            return False
        pipeline_type = args.custom_processors
    else:
        pipeline_type = args.pipeline
    
    processor = EnhancedBatchProcessor(pipeline_type)
    success = processor.run_batch_processing()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 