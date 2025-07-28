#!/usr/bin/env python3

import sys
import os
from pathlib import Path

# Agregar argumentos por defecto si no se proporcionan
def add_default_args():
    """Agrega argumentos por defecto si no se proporcionan"""
    if len(sys.argv) == 1:
        # No se proporcionaron argumentos, usar configuración por defecto
        print("🚀 Ejecutando con configuración optimizada por defecto...")
        print("📋 Configuración:")
        print("   - Execution Provider: CUDA")
        print("   - Max Memory: 12GB")
        print("   - Execution Threads: 8")
        print("   - Temp Frame Quality: 100")
        print("   - Keep FPS: Sí")
        print("   - NSFW Check: DESACTIVADO")
        print("=" * 50)
        
        # Agregar argumentos por defecto
        default_args = [
            "--execution-provider", "cuda",
            "--max-memory", "12",
            "--execution-threads", "8",
            "--temp-frame-quality", "100",
            "--keep-fps"
        ]
        
        # Insertar después del nombre del script
        sys.argv[1:1] = default_args

if __name__ == '__main__':
    add_default_args()
    
    # Importar y ejecutar core
    from roop import core
    core.run() 