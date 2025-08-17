"""
Optimizador de memoria para ROOP
Maneja la memoria del sistema y GPU de manera eficiente
"""

import gc
import psutil
import os
import torch
import numpy as np
from typing import Optional, Tuple
import roop.globals


class MemoryOptimizer:
    def __init__(self):
        self.memory_threshold = 0.85  # 85% de uso de memoria
        self.gpu_memory_threshold = 0.90  # 90% de uso de GPU
        self.cleanup_interval = 10  # Limpiar cada 10 operaciones
        
    def get_memory_usage(self) -> Tuple[float, float]:
        """Obtiene el uso de memoria del sistema y GPU"""
        # Memoria del sistema
        system_memory = psutil.virtual_memory()
        system_usage = system_memory.percent / 100.0
        
        # Memoria GPU (si está disponible)
        gpu_usage = 0.0
        if torch.cuda.is_available() and 'CUDAExecutionProvider' in roop.globals.execution_providers:
            try:
                gpu_memory = torch.cuda.memory_stats()
                allocated = gpu_memory.get('allocated_bytes.all.current', 0)
                reserved = gpu_memory.get('reserved_bytes.all.current', 0)
                total = torch.cuda.get_device_properties(0).total_memory
                gpu_usage = allocated / total if total > 0 else 0.0
            except:
                gpu_usage = 0.0
        
        return system_usage, gpu_usage
    
    def should_cleanup(self) -> bool:
        """Determina si se debe limpiar la memoria"""
        system_usage, gpu_usage = self.get_memory_usage()
        return system_usage > self.memory_threshold or gpu_usage > self.gpu_memory_threshold
    
    def cleanup_memory(self, aggressive: bool = False) -> None:
        """Limpia la memoria del sistema"""
        # Limpieza básica
        gc.collect()
        
        # Limpieza de GPU si está disponible
        if torch.cuda.is_available() and 'CUDAExecutionProvider' in roop.globals.execution_providers:
            try:
                torch.cuda.empty_cache()
                if aggressive:
                    torch.cuda.synchronize()
            except:
                pass
        
        # Limpieza agresiva del sistema si es necesario
        if aggressive:
            # Forzar limpieza de memoria del sistema
            if hasattr(psutil, 'Process'):
                process = psutil.Process(os.getpid())
                try:
                    # En Windows, intentar liberar memoria
                    if os.name == 'nt':
                        import ctypes
                        kernel32 = ctypes.windll.kernel32
                        kernel32.SetProcessWorkingSetSize(-1, -1, -1)
                except:
                    pass
    
    def optimize_batch_size(self, current_batch_size: int, memory_usage: float) -> int:
        """Optimiza el tamaño del batch basado en el uso de memoria"""
        if memory_usage > 0.8:
            return max(1, current_batch_size // 2)
        elif memory_usage < 0.5:
            return min(current_batch_size * 2, roop.globals.execution_threads)
        return current_batch_size
    
    def monitor_memory(self, operation_name: str = "Unknown") -> None:
        """Monitorea el uso de memoria y limpia si es necesario"""
        system_usage, gpu_usage = self.get_memory_usage()
        
        if self.should_cleanup():
            print(f"[MEMORY] High memory usage detected - System: {system_usage:.1%}, GPU: {gpu_usage:.1%}")
            self.cleanup_memory(aggressive=system_usage > 0.95)
        
        # Log de uso de memoria
        if system_usage > 0.7 or gpu_usage > 0.7:
            print(f"[MEMORY] {operation_name} - System: {system_usage:.1%}, GPU: {gpu_usage:.1%}")


# Instancia global del optimizador
memory_optimizer = MemoryOptimizer()


def get_memory_optimizer() -> MemoryOptimizer:
    """Obtiene la instancia global del optimizador de memoria"""
    return memory_optimizer


def optimize_array_memory(array: np.ndarray, target_dtype: Optional[np.dtype] = None) -> np.ndarray:
    """Optimiza la memoria de un array numpy"""
    if target_dtype is None:
        # Usar float32 en lugar de float64 para ahorrar memoria
        if array.dtype == np.float64:
            target_dtype = np.float32
        else:
            return array
    
    if array.dtype != target_dtype:
        return array.astype(target_dtype)
    
    return array


def safe_array_operation(func):
    """Decorador para operaciones seguras de arrays con manejo de memoria"""
    def wrapper(*args, **kwargs):
        try:
            # Verificar memoria antes de la operación
            memory_optimizer.monitor_memory(func.__name__)
            
            # Ejecutar la función
            result = func(*args, **kwargs)
            
            # Limpiar memoria después si es necesario
            if memory_optimizer.should_cleanup():
                memory_optimizer.cleanup_memory()
            
            return result
            
        except MemoryError:
            # Si hay error de memoria, limpiar agresivamente
            memory_optimizer.cleanup_memory(aggressive=True)
            raise
        except Exception as e:
            print(f"Error in {func.__name__}: {e}")
            raise
    
    return wrapper
