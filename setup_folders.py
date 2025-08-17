#!/usr/bin/env python3
"""
Script de configuración rápida para ROOP
Crea las carpetas necesarias y muestra la estructura
"""

from pathlib import Path
import os

def setup_folders():
    """Configura las carpetas necesarias para ROOP"""
    print("🚀 Configurando carpetas para ROOP...")
    print("=" * 50)
    
    # Carpetas necesarias
    folders = {
        "source": "Imágenes fuente (cara que quieres usar)",
        "videos_input": "Videos que quieres procesar",
        "videos_output": "Videos procesados (salida)",
        "temp_processing": "Archivos temporales durante el procesamiento"
    }
    
    created_folders = []
    existing_folders = []
    
    for folder_name, description in folders.items():
        folder_path = Path(folder_name)
        
        if folder_path.exists():
            existing_folders.append((folder_name, description))
            print(f"✅ {folder_name}/ - Ya existe")
        else:
            folder_path.mkdir(exist_ok=True)
            created_folders.append((folder_name, description))
            print(f"📁 {folder_name}/ - Creada")
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE CARPETAS")
    print("=" * 50)
    
    if created_folders:
        print("🆕 Carpetas creadas:")
        for folder, desc in created_folders:
            print(f"   • {folder}/ - {desc}")
    
    if existing_folders:
        print("\n✅ Carpetas existentes:")
        for folder, desc in existing_folders:
            print(f"   • {folder}/ - {desc}")
    
    print("\n📁 Estructura actual:")
    for folder, desc in folders.items():
        status = "✅" if Path(folder).exists() else "❌"
        print(f"   {status} {folder}/ - {desc}")
    
    print("\n💡 Próximos pasos:")
    print("   1. Coloca tu imagen fuente en la carpeta 'source/'")
    print("   2. Coloca tus videos en la carpeta 'videos_input/'")
    print("   3. Ejecuta: python batch_processor.py")
    print("   4. Los videos procesados aparecerán en 'videos_output/'")
    
    # Verificar archivos existentes
    print("\n🔍 Verificando archivos existentes...")
    
    source_files = list(Path("source").glob("*"))
    input_files = list(Path("videos_input").glob("*"))
    output_files = list(Path("videos_output").glob("*"))
    
    if source_files:
        print(f"\n📸 Imágenes en 'source/' ({len(source_files)}):")
        for file in source_files:
            print(f"   • {file.name}")
    else:
        print("\n⚠️  Carpeta 'source/' está vacía")
        print("   Coloca aquí tu imagen fuente (.jpg, .png)")
    
    if input_files:
        print(f"\n🎬 Videos en 'videos_input/' ({len(input_files)}):")
        for file in input_files:
            print(f"   • {file.name}")
    else:
        print("\n⚠️  Carpeta 'videos_input/' está vacía")
        print("   Coloca aquí tus videos (.mp4, .avi)")
    
    if output_files:
        print(f"\n💾 Archivos en 'videos_output/' ({len(output_files)}):")
        for file in output_files:
            print(f"   • {file.name}")
    else:
        print("\n📁 Carpeta 'videos_output/' está vacía (normal)")
        print("   Aquí aparecerán tus videos procesados")

if __name__ == "__main__":
    try:
        setup_folders()
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        print("Por favor, verifica los permisos del directorio") 