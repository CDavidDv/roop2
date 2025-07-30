#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path

def show_usage_examples():
    """Muestra ejemplos de uso del batch processor mejorado"""
    print("🚀 Batch Processor Mejorado - Ejemplos de Uso")
    print("=" * 60)
    
    print("\n📁 Estructura de carpetas requerida:")
    print("   source/           - Imagen fuente para el face swap")
    print("   videos_input/     - Videos a procesar")
    print("   videos_output/    - Videos procesados (se crea automáticamente)")
    
    print("\n🎯 Pipelines disponibles:")
    print("1. Pipeline Completo (recomendado):")
    print("   python batch_processor_enhanced.py --pipeline full")
    print("   → pre_face_enhancer -> face_swapper -> post_face_enhancer")
    
    print("\n2. Pipeline Básico (original):")
    print("   python batch_processor_enhanced.py --pipeline basic")
    print("   → face_swapper -> face_enhancer")
    
    print("\n3. Solo mejora antes del swap:")
    print("   python batch_processor_enhanced.py --pipeline pre_only")
    print("   → pre_face_enhancer -> face_swapper")
    
    print("\n4. Solo mejora después del swap:")
    print("   python batch_processor_enhanced.py --pipeline post_only")
    print("   → face_swapper -> post_face_enhancer")
    
    print("\n5. Pipeline personalizado:")
    print("   python batch_processor_enhanced.py --pipeline custom --custom-processors pre_face_enhancer,face_swapper")
    print("   → Define tus propios processors en orden")
    
    print("\n⚡ Configuración optimizada:")
    print("   - CUDA habilitado automáticamente")
    print("   - 8 threads optimizados para Tesla T4")
    print("   - Calidad máxima de frames temporales")
    print("   - FPS original mantenido")
    
    print("\n📊 Comparación de calidad:")
    print("   Pipeline Completo: ⭐⭐⭐⭐⭐ (máxima calidad)")
    print("   Pipeline Básico:   ⭐⭐⭐ (calidad original)")
    print("   Pre Only:          ⭐⭐⭐⭐ (mejor entrada)")
    print("   Post Only:         ⭐⭐⭐⭐ (mejor salida)")

def check_requirements():
    """Verifica que existan los archivos y carpetas necesarios"""
    print("🔍 Verificando requisitos...")
    
    # Verificar carpetas
    required_dirs = ["source", "videos_input"]
    missing_dirs = []
    
    for dir_name in required_dirs:
        if not Path(dir_name).exists():
            missing_dirs.append(dir_name)
    
    if missing_dirs:
        print(f"❌ Carpetas faltantes: {', '.join(missing_dirs)}")
        print("   Crea las carpetas antes de ejecutar el batch processor")
        return False
    
    # Verificar archivos de script
    required_files = [
        "batch_processor_enhanced.py",
        "run_enhanced_pipeline.py",
        "filename_generator.py"
    ]
    missing_files = []
    
    for file_name in required_files:
        if not Path(file_name).exists():
            missing_files.append(file_name)
    
    if missing_files:
        print(f"❌ Archivos faltantes: {', '.join(missing_files)}")
        return False
    
    # Verificar contenido de carpetas
    source_files = list(Path("source").glob("*"))
    if not source_files:
        print("❌ No hay imágenes en la carpeta 'source'")
        return False
    
    input_files = list(Path("videos_input").glob("*"))
    if not input_files:
        print("❌ No hay videos en la carpeta 'videos_input'")
        return False
    
    print("✅ Todos los requisitos cumplidos")
    return True

def run_batch_example():
    """Ejecuta un ejemplo de batch processing"""
    print("\n🎬 Ejecutando ejemplo de batch processing...")
    
    # Verificar requisitos
    if not check_requirements():
        print("❌ No se pueden ejecutar los ejemplos")
        return
    
    # Ejecutar pipeline completo
    print("\n🚀 Ejecutando Pipeline Completo...")
    cmd = [sys.executable, "batch_processor_enhanced.py", "--pipeline", "full"]
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Pipeline completo ejecutado exitosamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando pipeline: {e}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Ejemplos de Batch Processor Mejorado')
    parser.add_argument('--show-examples', action='store_true', help='Mostrar ejemplos de uso')
    parser.add_argument('--check-requirements', action='store_true', help='Verificar requisitos')
    parser.add_argument('--run-example', action='store_true', help='Ejecutar ejemplo')
    
    args = parser.parse_args()
    
    if args.show_examples:
        show_usage_examples()
    elif args.check_requirements:
        check_requirements()
    elif args.run_example:
        run_batch_example()
    else:
        # Mostrar ayuda por defecto
        show_usage_examples()
        print("\n" + "=" * 60)
        print("💡 Usa --show-examples, --check-requirements o --run-example para más opciones")

if __name__ == "__main__":
    main() 