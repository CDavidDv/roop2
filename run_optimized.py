#!/usr/bin/env python3

import os
import sys
import subprocess

def run_optimized_roop(source_path, target_path, output_path):
    """
    Ejecuta Roop con configuraciones optimizadas para Tesla T4
    """
    
    # Configuraciones optimizadas para Tesla T4
    cmd = [
        sys.executable, "run.py",
        "-s", source_path,
        "-t", target_path,
        "-o", output_path,
        "--execution-provider", "cuda",
        "--execution-threads", "6",
        "--output-video-encoder", "h264_nvenc",
        "--output-video-quality", "35",
        "--temp-frame-format", "jpg",
        "--temp-frame-quality", "85",
        "--keep-fps"
    ]
    
    print("🚀 Ejecutando Roop optimizado para Tesla T4...")
    print(f"Comando: {' '.join(cmd)}")
    print("=" * 60)
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Procesamiento completado exitosamente!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error durante el procesamiento: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Uso: python run_optimized.py <source_image> <target_video> <output_video>")
        print("Ejemplo: python run_optimized.py source.jpg target.mp4 output.mp4")
        sys.exit(1)
    
    source_path = sys.argv[1]
    target_path = sys.argv[2]
    output_path = sys.argv[3]
    
    # Verificar que los archivos existen
    if not os.path.exists(source_path):
        print(f"❌ Error: No se encuentra el archivo fuente: {source_path}")
        sys.exit(1)
    
    if not os.path.exists(target_path):
        print(f"❌ Error: No se encuentra el archivo objetivo: {target_path}")
        sys.exit(1)
    
    print("🎯 Configuración optimizada para Tesla T4:")
    print("   - CUDA habilitado")
    print("   - 6 threads de ejecución")
    print("   - Codificador NVIDIA (h264_nvenc)")
    print("   - Memoria GPU: 6GB")
    print("   - Verificación NSFW: DESACTIVADA")
    print("=" * 60)
    
    success = run_optimized_roop(source_path, target_path, output_path)
    sys.exit(0 if success else 1) 