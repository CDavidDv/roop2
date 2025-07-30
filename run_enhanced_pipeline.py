#!/usr/bin/env python3

import os
import sys
import argparse

# Agregar el directorio actual al path para importar roop
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import roop.globals
import roop.core
from roop.utilities import normalize_output_path


def main():
    parser = argparse.ArgumentParser(description='Roop Enhanced Pipeline con 2 Face Enhancers')
    parser.add_argument('-s', '--source', required=True, help='Imagen fuente para el face swap')
    parser.add_argument('-t', '--target', required=True, help='Video o imagen objetivo')
    parser.add_argument('-o', '--output', help='Archivo de salida (opcional)')
    parser.add_argument('--keep-fps', action='store_true', help='Mantener FPS original')
    parser.add_argument('--skip-audio', action='store_true', help='Saltar audio')
    parser.add_argument('--many-faces', action='store_true', help='Procesar todas las caras')
    
    args = parser.parse_args()
    
    # Configurar el pipeline completo: pre_enhancer -> face_swapper -> post_enhancer
    roop.globals.source_path = args.source
    roop.globals.target_path = args.target
    roop.globals.output_path = normalize_output_path(args.source, args.target, args.output)
    roop.globals.headless = True
    
    # Pipeline completo con 3 processors en orden
    roop.globals.frame_processors = [
        'pre_face_enhancer',    # 1. Mejora la calidad del video original
        'face_swapper',         # 2. Hace el face swap
        'post_face_enhancer'    # 3. Mejora la calidad después del face swap
    ]
    
    roop.globals.keep_fps = args.keep_fps
    roop.globals.skip_audio = args.skip_audio
    roop.globals.many_faces = args.many_faces
    
    # Configurar CUDA si está disponible
    import onnxruntime
    if 'CUDAExecutionProvider' in onnxruntime.get_available_providers():
        roop.globals.execution_providers = ['CUDAExecutionProvider']
        roop.globals.execution_threads = 8  # Optimizado para Tesla T4
    else:
        roop.globals.execution_providers = ['CPUExecutionProvider']
        roop.globals.execution_threads = 1
    
    print("🚀 Iniciando Pipeline Mejorado de Roop")
    print(f"📁 Imagen fuente: {args.source}")
    print(f"🎬 Video objetivo: {args.target}")
    print(f"💾 Archivo de salida: {roop.globals.output_path}")
    print(f"🔧 Processors: {' -> '.join(roop.globals.frame_processors)}")
    print(f"⚡ Execution providers: {roop.globals.execution_providers}")
    print(f"🧵 Threads: {roop.globals.execution_threads}")
    print("=" * 60)
    
    # Ejecutar el pipeline
    roop.core.run()


if __name__ == "__main__":
    main() 