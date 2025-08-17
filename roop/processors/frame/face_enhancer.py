from typing import Any, List, Callable
import cv2
import threading
from gfpgan.utils import GFPGANer

import roop.globals
import roop.processors.frame.core
from roop.core import update_status
from roop.face_analyser import get_many_faces
from roop.typing import Frame, Face
from roop.utilities import conditional_download, resolve_relative_path, is_image, is_video
import cv2
import numpy as np
import gc
import threading
from typing import Any, List, Callable

FACE_ENHANCER = None
THREAD_SEMAPHORE = threading.Semaphore()
THREAD_LOCK = threading.Lock()
NAME = 'ROOP.FACE-ENHANCER'

# Configuración de memoria optimizada
MAX_FACE_SIZE = 512  # Tamaño máximo para procesar caras individuales
MEMORY_CLEANUP_THRESHOLD = 0.8  # Limpiar memoria cuando se use más del 80%


def get_face_enhancer() -> Any:
    global FACE_ENHANCER

    with THREAD_LOCK:
        if FACE_ENHANCER is None:
            model_path = resolve_relative_path('../models/GFPGANv1.4.pth')
            # Configuración optimizada para memoria
            FACE_ENHANCER = GFPGANer(
                model_path=model_path, 
                upscale=1, 
                device=get_device(),
                bg_upsampler=None  # Deshabilitar upsampler de fondo para ahorrar memoria
            )
    return FACE_ENHANCER


def get_device() -> str:
    if 'CUDAExecutionProvider' in roop.globals.execution_providers:
        return 'cuda'
    if 'CoreMLExecutionProvider' in roop.globals.execution_providers:
        return 'mps'
    return 'cpu'


def clear_face_enhancer() -> None:
    global FACE_ENHANCER

    FACE_ENHANCER = None


def pre_check() -> bool:
    download_directory_path = resolve_relative_path('../models')
    conditional_download(download_directory_path, ['https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth'])
    return True


def pre_start() -> bool:
    if not is_image(roop.globals.target_path) and not is_video(roop.globals.target_path):
        update_status('Select an image or video for target path.', NAME)
        return False
    return True


def post_process() -> None:
    clear_face_enhancer()
    # Limpiar memoria explícitamente
    gc.collect()


def optimize_face_size(face_img: np.ndarray) -> np.ndarray:
    """Optimiza el tamaño de la cara para procesamiento eficiente"""
    height, width = face_img.shape[:2]
    
    # Si la cara es muy grande, redimensionar para ahorrar memoria
    if max(height, width) > MAX_FACE_SIZE:
        scale = MAX_FACE_SIZE / max(height, width)
        new_width = int(width * scale)
        new_height = int(height * scale)
        face_img = cv2.resize(face_img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
    
    return face_img


def enhance_face(target_face: Face, temp_frame: Frame) -> Frame:
    start_x, start_y, end_x, end_y = map(int, target_face['bbox'])
    padding_x = int((end_x - start_x) * 0.5)
    padding_y = int((end_y - start_y) * 0.5)
    start_x = max(0, start_x - padding_x)
    start_y = max(0, start_y - padding_y)
    end_x = max(0, end_x + padding_x)
    end_y = max(0, end_y + padding_y)
    
    temp_face = temp_frame[start_y:end_y, start_x:end_x]
    
    if temp_face.size:
        try:
            with THREAD_SEMAPHORE:
                # Optimizar tamaño de la cara antes del procesamiento
                optimized_face = optimize_face_size(temp_face.copy())
                
                # Procesar con manejo de memoria
                _, _, enhanced_face = get_face_enhancer().enhance(
                    optimized_face,
                    paste_back=False  # No pegar automáticamente para controlar memoria
                )
                
                # Redimensionar de vuelta al tamaño original si es necesario
                if enhanced_face.shape != temp_face.shape:
                    enhanced_face = cv2.resize(enhanced_face, (temp_face.shape[1], temp_face.shape[0]), interpolation=cv2.INTER_LANCZOS4)
                
                # Aplicar máscara suave para transición natural
                mask = np.ones_like(temp_face) * 0.9
                temp_frame[start_y:end_y, start_x:end_x] = (
                    enhanced_face * mask + temp_face * (1 - mask)
                ).astype(np.uint8)
                
                # Limpiar memoria local
                del optimized_face, enhanced_face, mask
                gc.collect()
                
        except Exception as e:
            # Si falla la mejora, mantener la cara original
            print(f"Face enhancement failed for face at ({start_x}, {start_y}): {e}")
            pass
    
    return temp_frame


def process_frame(source_face: Face, reference_face: Face, temp_frame: Frame) -> Frame:
    many_faces = get_many_faces(temp_frame)
    if many_faces:
        for target_face in many_faces:
            temp_frame = enhance_face(target_face, temp_frame)
            
            # Limpiar memoria periódicamente
            if len(many_faces) > 5:  # Si hay muchas caras, limpiar más frecuentemente
                gc.collect()
    
    return temp_frame


def process_frames(source_path: str, temp_frame_paths: List[str], update: Callable[[], None]) -> None:
    for i, temp_frame_path in enumerate(temp_frame_paths):
        try:
            temp_frame = cv2.imread(temp_frame_path)
            result = process_frame(None, None, temp_frame)
            cv2.imwrite(temp_frame_path, result)
            
            # Limpiar memoria cada 10 frames
            if i % 10 == 0:
                gc.collect()
            
            if update:
                update()
                
        except Exception as e:
            print(f"Error processing frame {temp_frame_path}: {e}")
            # Continuar con el siguiente frame
            if update:
                update()


def process_image(source_path: str, target_path: str, output_path: str) -> None:
    target_frame = cv2.imread(target_path)
    result = process_frame(None, None, target_frame)
    cv2.imwrite(output_path, result)
    # Limpiar memoria después de procesar imagen
    gc.collect()


def process_video(source_path: str, temp_frame_paths: List[str]) -> None:
    roop.processors.frame.core.process_video(None, temp_frame_paths, process_frames)
