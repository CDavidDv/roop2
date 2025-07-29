#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Configuración optimizada para Tesla T4 con 15GB VRAM
def add_tesla_t4_args():
    """Agrega argumentos optimizados para Tesla T4"""
    if len(sys.argv) == 1:
        # No se proporcionaron argumentos, usar configuración Tesla T4
        print("🚀 Ejecutando con configuración optimizada para Tesla T4 (15GB VRAM)...")
        print("📋 Configuración Tesla T4:")
        print("   - Execution Provider: CUDA")
        print("   - Max Memory: 12GB (de 15GB disponibles)")
        print("   - Execution Threads: 8 (optimizado para T4)")
        print("   - Temp Frame Quality: 100")
        print("   - Keep FPS: Sí")
        print("   - Frame Processors: face_swapper + face_enhancer")
        print("   - NSFW Check: DESACTIVADO")
        print("   - GPU Memory: 12GB/15GB (80% utilización)")
        print("=" * 60)
        
        # Argumentos optimizados para Tesla T4
        tesla_t4_args = [
            "--execution-provider", "cuda",
            "--max-memory", "12",
            "--execution-threads", "8",
            "--temp-frame-quality", "100",
            "--keep-fps",
            "--frame-processor", "face_swapper", "face_enhancer"
        ]
        
        # Insertar después del nombre del script
        sys.argv[1:1] = tesla_t4_args

if __name__ == '__main__':
    add_tesla_t4_args()
    
    # Importar y ejecutar core
    from roop import core
    core.run() 