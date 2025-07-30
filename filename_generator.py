#!/usr/bin/env python3

from pathlib import Path

def generate_output_filename(source_path: str, target_path: str, output_dir: str = "videos_output") -> str:
    """
    Genera un nombre de archivo de salida combinando imagen fuente y video
    
    Args:
        source_path: Ruta de la imagen fuente
        target_path: Ruta del video objetivo
        output_dir: Directorio de salida
    
    Returns:
        Ruta completa del archivo de salida
    """
    source_path_obj = Path(source_path)
    target_path_obj = Path(target_path)
    output_dir_obj = Path(output_dir)
    
    # Obtener nombres sin extensión
    source_name = source_path_obj.stem
    target_name = target_path_obj.stem
    
    # Crear nombre combinado: imagen_video.mp4
    output_filename = f"{source_name}_{target_name}.mp4"
    output_path = output_dir_obj / output_filename
    
    return str(output_path)

def generate_batch_output_filename(source_path: str, target_path: str, output_dir: str = "videos_output") -> str:
    """
    Genera nombre para procesamiento por lotes
    """
    return generate_output_filename(source_path, target_path, output_dir)

# Ejemplos de uso
if __name__ == "__main__":
    print("📝 GENERADOR DE NOMBRES DE ARCHIVO")
    print("=" * 50)
    
    examples = [
        ("source/rostro.jpg", "videos_input/video1.mp4"),
        ("source/persona.png", "videos_input/pelicula.avi"),
        ("source/face.jpeg", "videos_input/clip.mov")
    ]
    
    for source, target in examples:
        output = generate_output_filename(source, target)
        print(f"📁 Entrada: {source}")
        print(f"🎬 Video: {target}")
        print(f"📤 Salida: {output}")
        print("-" * 30) 