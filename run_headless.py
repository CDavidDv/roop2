#!/usr/bin/env python3
"""
Versión headless de run.py específica para Google Colab
Sin dependencias GUI (customtkinter, tkinter)
"""

import os
import sys
# single thread doubles cuda performance - needs to be set before torch import
if any(arg.startswith('--execution-provider') for arg in sys.argv):
    os.environ['OMP_NUM_THREADS'] = '1'
# reduce tensorflow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# Optimizaciones de memoria para numpy y torch
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
import warnings
from typing import List
import platform
import signal
import shutil
import argparse
import onnxruntime
import tensorflow
import roop.globals
import roop.metadata
# NO importar roop.ui - causa problemas en Colab
from roop.predictor import predict_image, predict_video
from roop.processors.frame.core import get_frame_processors_modules
from roop.utilities import has_image_extension, is_image, is_video, detect_fps, create_video, extract_frames, get_temp_frame_paths, restore_audio, create_temp, move_temp, clean_temp, normalize_output_path

warnings.filterwarnings('ignore', category=FutureWarning, module='insightface')
warnings.filterwarnings('ignore', category=UserWarning, module='torchvision')

def parse_args() -> None:
    signal.signal(signal.SIGINT, lambda signal_number, frame: destroy())
    program = argparse.ArgumentParser(formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=100))
    program.add_argument('-s', '--source', help='select an source image', dest='source_path')
    program.add_argument('-t', '--target', help='select an target image or video', dest='target_path')
    program.add_argument('-o', '--output', help='select output file or directory', dest='output_path')
    program.add_argument('--frame-processor', help='frame processors (choices: face_swapper, face_enhancer, ...)', dest='frame_processor', default=['face_swapper', 'face_enhancer'], nargs='+')
    program.add_argument('--keep-fps', help='keep target fps', dest='keep_fps', action='store_true')
    program.add_argument('--keep-frames', help='keep temporary frames', dest='keep_frames', action='store_true')
    program.add_argument('--skip-audio', help='skip target audio', dest='skip_audio', action='store_true')
    program.add_argument('--many-faces', help='process every face', dest='many_faces', action='store_true')
    program.add_argument('--reference-face-position', help='position of the reference face', dest='reference_face_position', type=int, default=0)
    program.add_argument('--reference-frame-number', help='number of the reference frame', dest='reference_frame_number', type=int, default=0)
    program.add_argument('--similar-face-distance', help='face distance used for recognition', dest='similar_face_distance', type=float, default=0.85)
    program.add_argument('--temp-frame-format', help='image format used for frame extraction', dest='temp_frame_format', default='png', choices=['jpg', 'png'])
    program.add_argument('--temp-frame-quality', help='image quality used for frame extraction', dest='temp_frame_quality', type=int, default=0, choices=range(101), metavar='[0-100]')
    program.add_argument('--output-video-encoder', help='encoder used for the output video', dest='output_video_encoder', default='libx264', choices=['libx264', 'libx265', 'libvpx-vp9', 'h264_nvenc', 'hevc_nvenc'])
    program.add_argument('--output-video-quality', help='quality used for the output video', dest='output_video_quality', type=int, default=35, choices=range(101), metavar='[0-100]')
    program.add_argument('--max-memory', help='maximum amount of RAM in GB', dest='max_memory', type=int, default=0)
    program.add_argument('--execution-provider', help='available execution provider (choices: cpu, ...)', dest='execution_provider', default=['cpu'], choices=suggest_execution_providers(), nargs='+')
    program.add_argument('--execution-threads', help='number of execution threads', dest='execution_threads', type=int, default=suggest_execution_threads())
    
    # Argumentos de optimización de memoria
    program.add_argument('--memory-optimization', help='enable memory optimization', dest='memory_optimization', action='store_true')
    program.add_argument('--batch-size', help='batch size for processing', dest='batch_size', type=int, default=1)
    
    program.add_argument('-v', '--version', action='version', version=f'{roop.metadata.name} {roop.metadata.version}')
    args = program.parse_args()

    roop.globals.source_path = args.source_path
    roop.globals.target_path = args.target_path
    roop.globals.output_path = args.output_path
    roop.globals.frame_processors = args.frame_processor
    roop.globals.headless = True  # Siempre headless en esta versión
    roop.globals.keep_fps = args.keep_fps
    roop.globals.keep_frames = args.keep_frames
    roop.globals.skip_audio = args.skip_audio
    roop.globals.many_faces = args.many_faces
    roop.globals.reference_face_position = args.reference_face_position
    roop.globals.reference_frame_number = args.reference_frame_number
    roop.globals.similar_face_distance = args.similar_face_distance
    roop.globals.temp_frame_format = args.temp_frame_format
    roop.globals.temp_frame_quality = args.temp_frame_quality
    roop.globals.output_video_encoder = args.output_video_encoder
    roop.globals.output_video_quality = args.output_video_quality
    roop.globals.max_memory = args.max_memory
    roop.globals.execution_providers = decode_execution_providers(args.execution_provider)
    roop.globals.execution_threads = args.execution_threads
    
    # Configurar optimizaciones de memoria
    if args.memory_optimization:
        roop.globals.memory_optimization = True
        roop.globals.batch_size = args.batch_size

def encode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [execution_provider.replace('ExecutionProvider', '').lower() for execution_provider in execution_providers]

def decode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [provider for provider, encoded_provider in zip(onnxruntime.get_available_providers(), encode_execution_providers(onnxruntime.get_available_providers()))
            if any(execution_provider in encoded_provider for execution_provider in execution_providers)]

def suggest_execution_providers() -> List[str]:
    return encode_execution_providers(onnxruntime.get_available_providers())

def suggest_execution_threads() -> int:
    if 'DmlExecutionProvider' in onnxruntime.get_available_providers():
        return 1
    if 'ROCMExecutionProvider' in onnxruntime.get_available_providers():
        return 1
    return 8

def limit_resources() -> None:
    # En Colab, limitar uso de memoria automáticamente
    if roop.globals.max_memory:
        memory = roop.globals.max_memory
    elif hasattr(roop.globals, 'memory_optimization') and roop.globals.memory_optimization:
        memory = 8  # 8GB por defecto para Colab
    else:
        memory = None
    
    if memory:
        print(f"💾 Limitando memoria a {memory}GB")

def pre_check() -> bool:
    if sys.version_info < (3, 9):
        print('Python 3.9 or higher is required')
        return False
    if not shutil.which('ffmpeg'):
        print('ffmpeg is not installed')
        return False
    return True

def conditional_download(download_directory_path: str, urls: List[str]) -> None:
    if not os.path.exists(download_directory_path):
        os.makedirs(download_directory_path)
    for url in urls:
        download_file_path = os.path.join(download_directory_path, os.path.basename(url))
        if not os.path.exists(download_file_path):
            request = urllib.request.urlopen(url)  # type: ignore[attr-defined]
            total = int(request.headers.get('Content-Length', 0))
            with tqdm(total=total, desc=f'Downloading {url}', unit='B', unit_scale=True, unit_divisor=1024) as progress:
                urllib.request.urlretrieve(url, download_file_path, reporthook=lambda count, block_size, total_size: progress.update(block_size))  # type: ignore[attr-defined]

def run() -> None:
    parse_args()
    if not pre_check():
        return
    
    print(f"🚀 ROOP Headless para Colab")
    print(f"🎯 GPU: {onnxruntime.get_available_providers()}")
    
    limit_resources()
    
    # No mostrar preview ni UI - procesamiento directo
    if roop.globals.source_path and roop.globals.target_path and roop.globals.output_path:
        print("🎬 Iniciando procesamiento...")
        
        # Importar el procesamiento de memoria si está habilitado
        if hasattr(roop.globals, 'memory_optimization') and roop.globals.memory_optimization:
            try:
                from roop.memory_optimizer import process_with_memory_optimization
                process_with_memory_optimization()
            except ImportError:
                # Fallback al procesamiento normal
                print("⚠️ Memory optimizer no disponible, usando procesamiento normal")
                start_processing()
        else:
            start_processing()
    else:
        print("❌ Necesitas especificar source, target y output")
        print("Uso: python run_headless.py -s source.jpg -t target.mp4 -o output.mp4")

def start_processing() -> None:
    """Inicia el procesamiento de video/imagen"""
    if is_image(roop.globals.target_path):
        start_image_processing()
    if is_video(roop.globals.target_path):
        start_video_processing()

def start_image_processing() -> None:
    """Procesa una imagen"""
    print("📸 Procesando imagen...")
    if predict_image(roop.globals.target_path):
        destroy()
    shutil.copy2(roop.globals.target_path, roop.globals.output_path)
    process_image(roop.globals.source_path, roop.globals.output_path, roop.globals.output_path)
    
def start_video_processing() -> None:
    """Procesa un video"""
    print("🎬 Procesando video...")
    if predict_video(roop.globals.target_path, roop.globals.output_path):
        destroy()
    extract_frames(roop.globals.target_path)
    process_video(roop.globals.source_path, get_temp_frame_paths(roop.globals.target_path))
    create_video(roop.globals.target_path, roop.globals.output_path)
    restore_audio(roop.globals.target_path, roop.globals.output_path)
    clean_temp(roop.globals.target_path)

def process_image(source_path: str, target_path: str, output_path: str) -> None:
    """Procesa una imagen individual"""
    for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
        print(f"🔄 Aplicando {frame_processor.__name__}")
        frame_processor.process_image(source_path, target_path, output_path)

def process_video(source_path: str, temp_frame_paths: List[str]) -> None:
    """Procesa frames de video"""
    from tqdm import tqdm
    
    for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
        print(f"🔄 Aplicando {frame_processor.__name__}")
        
        progress_bar = tqdm(temp_frame_paths, desc=f"Processing {frame_processor.__name__}")
        for temp_frame_path in progress_bar:
            frame_processor.process_frame(source_path, temp_frame_path, temp_frame_path)

def destroy() -> None:
    if roop.globals.target_path:
        clean_temp(roop.globals.target_path)
    sys.exit()