#!/usr/bin/env python3

import os
from pathlib import Path

def setup_folders():
    """Configura las carpetas necesarias para el procesamiento por lotes"""
    print("📁 Configurando carpetas para procesamiento por lotes...")
    print("=" * 50)
    
    folders = {
        "source": "Carpeta para la imagen fuente (rostro a intercambiar)",
        "videos_input": "Carpeta para videos de entrada a procesar",
        "videos_output": "Carpeta para videos procesados"
    }
    
    for folder_name, description in folders.items():
        folder_path = Path(folder_name)
        
        if folder_path.exists():
            print(f"✅ {folder_name}/ - Ya existe")
        else:
            folder_path.mkdir(exist_ok=True)
            print(f"📁 {folder_name}/ - Creada")
        
        print(f"   📝 {description}")
    
    print("\n" + "=" * 50)
    print("📋 INSTRUCCIONES DE USO:")
    print("=" * 50)
    print("1. Coloca tu imagen fuente en la carpeta 'source/'")
    print("2. Coloca los videos a procesar en 'videos_input/'")
    print("3. Ejecuta uno de estos comandos:")
    print("")
    print("   🚀 Procesamiento por lotes:")
    print("   python batch_processor.py")
    print("")
    print("   🎯 Procesamiento individual:")
    print("   python run_simple.py -s source.jpg -t video.mp4 -o output.mp4")
    print("")
    print("   ⚡ Comando simple (con configuraciones por defecto):")
    print("   python run_simple.py -s source.jpg -t video.mp4 -o output.mp4")
    print("")
    print("📁 Los videos procesados aparecerán en 'videos_output/'")
    print("=" * 50)

if __name__ == "__main__":
    setup_folders() 