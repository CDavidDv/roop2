#!/usr/bin/env python3
"""
Configuración para detección y procesamiento de rostros en batch_processor.py
"""

# Configuración general para mejor detección de rostros
FACE_DETECTION_CONFIG = {
    # Distancia para reconocimiento de rostros (0.0 - 1.0)
    # Valores más bajos = más estricto, valores más altos = más permisivo
    "similar_face_distance": "0.85",
    
    # Posición del rostro de referencia (0 = primer rostro detectado)
    "reference_face_position": "0",
    
    # Formato de frames temporales
    "temp_frame_format": "jpg",
    
    # Calidad de frames temporales (0-100)
    "temp_frame_quality": "100",
    
    # Procesar múltiples rostros
    "many_faces": True,
    
    # Configuraciones específicas por tipo de video
    "video_types": {
        "group": {
            "description": "Videos con múltiples personas",
            "similar_face_distance": "0.80",
            "many_faces": True
        },
        "closeup": {
            "description": "Videos con rostros cercanos",
            "similar_face_distance": "0.90",
            "reference_face_position": "0"
        },
        "portrait": {
            "description": "Videos tipo retrato",
            "similar_face_distance": "0.90",
            "reference_face_position": "0"
        },
        "low_quality": {
            "description": "Videos de baja calidad",
            "similar_face_distance": "0.75",
            "temp_frame_quality": "90"
        }
    }
}

# Parámetros de ejecución optimizados
EXECUTION_CONFIG = {
    "execution_provider": "cuda",
    "max_memory": "12",
    "execution_threads": "30",
    "keep_fps": True,
    "keep_frames": True
}

def get_face_args_for_video(video_path):
    """
    Obtiene argumentos específicos para un video basado en su nombre
    """
    video_name = Path(video_path).name.lower()
    
    # Argumentos base
    args = [
        "--many-faces" if FACE_DETECTION_CONFIG["many_faces"] else None,
        "--similar-face-distance", FACE_DETECTION_CONFIG["similar_face_distance"],
        "--reference-face-position", FACE_DETECTION_CONFIG["reference_face_position"],
        "--temp-frame-format", FACE_DETECTION_CONFIG["temp_frame_format"],
        "--temp-frame-quality", FACE_DETECTION_CONFIG["temp_frame_quality"]
    ]
    
    # Filtrar valores None
    args = [arg for arg in args if arg is not None]
    
    # Aplicar configuraciones específicas según el tipo de video
    for video_type, config in FACE_DETECTION_CONFIG["video_types"].items():
        if video_type in video_name:
            print(f"🔧 Aplicando configuración para tipo '{video_type}': {config['description']}")
            
            if "similar_face_distance" in config:
                # Reemplazar el valor existente
                for i, arg in enumerate(args):
                    if arg == "--similar-face-distance":
                        args[i + 1] = config["similar_face_distance"]
                        break
            
            if "reference_face_position" in config:
                # Reemplazar el valor existente
                for i, arg in enumerate(args):
                    if arg == "--reference-face-position":
                        args[i + 1] = config["reference_face_position"]
                        break
            
            if "temp_frame_quality" in config:
                # Reemplazar el valor existente
                for i, arg in enumerate(args):
                    if arg == "--temp-frame-quality":
                        args[i + 1] = config["temp_frame_quality"]
                        break
            
            break
    
    return args

def print_config_help():
    """
    Imprime información de ayuda sobre la configuración
    """
    print("\n🔧 CONFIGURACIÓN DE DETECCIÓN DE ROSTROS")
    print("=" * 50)
    print("Parámetros principales:")
    print(f"  • Distancia de rostros: {FACE_DETECTION_CONFIG['similar_face_distance']}")
    print(f"  • Posición de referencia: {FACE_DETECTION_CONFIG['reference_face_position']}")
    print(f"  • Formato de frames: {FACE_DETECTION_CONFIG['temp_frame_format']}")
    print(f"  • Calidad de frames: {FACE_DETECTION_CONFIG['temp_frame_quality']}")
    print(f"  • Múltiples rostros: {FACE_DETECTION_CONFIG['many_faces']}")
    
    print("\nTipos de video detectados automáticamente:")
    for video_type, config in FACE_DETECTION_CONFIG["video_types"].items():
        print(f"  • {video_type}: {config['description']}")
    
    print("\n💡 Consejos para mejorar la detección:")
    print("  • Si no detecta bien los rostros, reduce 'similar_face_distance'")
    print("  • Para videos con múltiples personas, usa 'many_faces'")
    print("  • Para rostros pequeños, aumenta 'temp_frame_quality'")
    print("  • Nombra tus videos incluyendo palabras clave como 'group', 'closeup', etc.")

if __name__ == "__main__":
    from pathlib import Path
    print_config_help() 