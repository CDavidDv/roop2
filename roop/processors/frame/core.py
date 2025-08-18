import os
import sys
import importlib
import psutil
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from types import ModuleType
from typing import Any, List, Callable
from tqdm import tqdm

# Importar roop al final para evitar problemas de import circular
# import roop

FRAME_PROCESSORS_MODULES: List[ModuleType] = []
FRAME_PROCESSORS_INTERFACE = [
    'pre_check',
    'pre_start',
    'process_frame',
    'process_frames',
    'process_image',
    'process_video',
    'post_process'
]


def load_frame_processor_module(frame_processor: str) -> Any:
    try:
        frame_processor_module = importlib.import_module(f'roop.processors.frame.{frame_processor}')
        for method_name in FRAME_PROCESSORS_INTERFACE:
            if not hasattr(frame_processor_module, method_name):
                raise NotImplementedError
    except ModuleNotFoundError:
        sys.exit(f'Frame processor {frame_processor} not found.')
    except NotImplementedError:
        sys.exit(f'Frame processor {frame_processor} not implemented correctly.')
    return frame_processor_module


def get_frame_processors_modules(frame_processors: List[str]) -> List[ModuleType]:
    global FRAME_PROCESSORS_MODULES

    if not FRAME_PROCESSORS_MODULES:
        for frame_processor in frame_processors:
            frame_processor_module = load_frame_processor_module(frame_processor)
            FRAME_PROCESSORS_MODULES.append(frame_processor_module)
    return FRAME_PROCESSORS_MODULES


def multi_process_frame(source_path: str, temp_frame_paths: List[str], process_frames: Callable[[str, List[str], Any], None], update: Callable[[], None]) -> None:
    # Importar roop solo cuando sea necesario
    import roop
    
    # Usar batch size optimizado si está habilitado
    batch_size = getattr(roop.globals, 'batch_size', 5)
    max_workers = min(roop.globals.execution_threads, batch_size)
    
    # Verificar si memory_optimization está disponible
    memory_optimization = getattr(roop.globals, 'memory_optimization', False)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        queue = create_queue(temp_frame_paths)
        
        # Procesar en lotes más pequeños para optimizar memoria
        if memory_optimization:
            queue_per_future = max(1, min(len(temp_frame_paths) // max_workers, batch_size))
        else:
            queue_per_future = max(len(temp_frame_paths) // roop.globals.execution_threads, 1)
            
        while not queue.empty():
            future = executor.submit(process_frames, source_path, pick_queue(queue, queue_per_future), update)
            futures.append(future)
            
            # Pausa entre lotes para permitir limpieza de memoria
            if memory_optimization and len(futures) % 3 == 0:
                import gc
                gc.collect()
        
        for future in as_completed(futures):
            future.result()


def create_queue(temp_frame_paths: List[str]) -> Queue[str]:
    queue: Queue[str] = Queue()
    for frame_path in temp_frame_paths:
        queue.put(frame_path)
    return queue


def pick_queue(queue: Queue[str], queue_per_future: int) -> List[str]:
    queues = []
    for _ in range(queue_per_future):
        if not queue.empty():
            queues.append(queue.get())
    return queues


def process_video(source_path: str, frame_paths: list[str], process_frames: Callable[[str, List[str], Any], None]) -> None:
    progress_bar_format = '{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]'
    total = len(frame_paths)
    with tqdm(total=total, desc='Processing', unit='frame', dynamic_ncols=True, bar_format=progress_bar_format) as progress:
        multi_process_frame(source_path, frame_paths, process_frames, lambda: update_progress(progress))


def update_progress(progress: Any = None) -> None:
    # Importar roop solo cuando sea necesario
    import roop
    
    process = psutil.Process(os.getpid())
    memory_usage = process.memory_info().rss / 1024 / 1024 / 1024
    
    # Información adicional de memoria si está habilitada la optimización
    memory_info = f'{memory_usage:.2f}GB'
    
    # Verificar si memory_optimization está disponible
    memory_optimization = getattr(roop.globals, 'memory_optimization', False)
    
    if memory_optimization:
        try:
            import roop.memory_optimizer
            optimizer = roop.memory_optimizer.get_memory_optimizer()
            system_usage, gpu_usage = optimizer.get_memory_usage()
            memory_info += f' (S:{system_usage:.1%}, G:{gpu_usage:.1%})'
        except:
            pass
    
    progress.set_postfix({
        'memory_usage': memory_info,
        'execution_providers': roop.globals.execution_providers,
        'execution_threads': roop.globals.execution_threads,
        'batch_size': getattr(roop.globals, 'batch_size', 'N/A')
    })
    progress.refresh()
    progress.update(1)
