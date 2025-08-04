#!/usr/bin/env python3
"""
Configuración para detección y procesamiento de rostros en batch_processor.py
"""

from pathlib import Path
import os

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

# Cache para análisis automático
AUTO_ANALYSIS_CACHE = {}

def get_face_args_for_video(video_path):
    """
    Obtiene argumentos específicos para un video basado en su nombre
    y análisis automático si está disponible
    """
    video_name = Path(video_path).name.lower()
    
    # Intentar análisis automático primero
    auto_config = get_auto_analysis_config(video_path)
    if auto_config:
        print(f"🤖 Usando configuración automática para {Path(video_path).name}")
        return auto_config
    
    # Fallback a configuración basada en nombre
    print(f"📝 Usando configuración basada en nombre para {Path(video_path).name}")
    return get_name_based_config(video_path)

def get_auto_analysis_config(video_path):
    """
    Obtiene configuración basada en análisis automático del video
    """
    try:
        # Verificar si existe el analizador
        from video_analyzer import analyze_video_auto
        
        # Verificar cache
        if video_path in AUTO_ANALYSIS_CACHE:
            config = AUTO_ANALYSIS_CACHE[video_path]
        else:
            # Realizar análisis automático
            config = analyze_video_auto(video_path)
            AUTO_ANALYSIS_CACHE[video_path] = config
        
        # Convertir configuración a argumentos
        args = []
        
        if config.get("many_faces", False):
            args.append("--many-faces")
        
        args.extend([
            "--similar-face-distance", config.get("similar_face_distance", "0.85"),
            "--reference-face-position", config.get("reference_face_position", "0"),
            "--temp-frame-format", "jpg",
            "--temp-frame-quality", config.get("temp_frame_quality", "100")
        ])
        
        return args
        
    except ImportError:
        print("⚠️  Analizador automático no disponible, usando configuración manual")
        return None
    except Exception as e:
        print(f"⚠️  Error en análisis automático: {e}")
        return None

def get_name_based_config(video_path):
    """
    Obtiene configuración basada en el nombre del video
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

def analyze_all_videos_in_folder(folder_path="videos_input"):
    """
    Analiza automáticamente todos los videos en una carpeta
    """
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ La carpeta {folder_path} no existe")
        return
    
    video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv']
    video_files = []
    
    for ext in video_extensions:
        video_files.extend(folder.glob(ext))
    
    if not video_files:
        print(f"⚠️  No se encontraron videos en {folder_path}")
        return
    
    print(f"🔍 Analizando {len(video_files)} videos automáticamente...")
    print("=" * 60)
    
    try:
        from video_analyzer import VideoAnalyzer
        analyzer = VideoAnalyzer()
        
        for video_file in video_files:
            try:
                analyzer.analyze_video(str(video_file))
                analyzer.print_analysis_report(str(video_file))
            except Exception as e:
                print(f"❌ Error analizando {video_file.name}: {e}")
        
        print("\n✅ Análisis automático completado")
        print("💡 Los resultados se usarán automáticamente en el procesamiento")
        
    except ImportError:
        print("❌ El analizador automático no está disponible")
        print("💡 Instala opencv-python: pip install opencv-python")

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
    
    print("\n🤖 ANÁLISIS AUTOMÁTICO:")
    print("  • Detecta automáticamente características del video")
    print("  • Configura parámetros óptimos sin intervención manual")
    print("  • Analiza resolución, calidad, rostros, etc.")
    
    print("\nTipos de video detectados automáticamente:")
    for video_type, config in FACE_DETECTION_CONFIG["video_types"].items():
        print(f"  • {video_type}: {config['description']}")
    
    print("\n💡 Consejos para mejorar la detección:")
    print("  • Si no detecta bien los rostros, reduce 'similar_face_distance'")
    print("  • Para videos con múltiples personas, usa 'many_faces'")
    print("  • Para rostros pequeños, aumenta 'temp_frame_quality'")
    print("  • Nombra tus videos incluyendo palabras clave como 'group', 'closeup', etc.")
    print("  • O usa el análisis automático que detecta todo automáticamente")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "analyze":
        # Analizar todos los videos en la carpeta
        analyze_all_videos_in_folder()
    else:
        # Mostrar ayuda
        print_config_help()
        print("\n📊 COMANDOS DISPONIBLES:")
        print("  python face_config.py          - Mostrar esta ayuda")
        print("  python face_config.py analyze  - Analizar todos los videos automáticamente")
        print("  python video_analyzer.py <video> - Analizar un video específico") 