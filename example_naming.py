#!/usr/bin/env python3

from filename_generator import generate_output_filename

def show_naming_examples():
    """Muestra ejemplos de cómo se generan los nombres de archivo"""
    print("📝 EJEMPLOS DE NOMBRES DE ARCHIVO")
    print("=" * 50)
    
    examples = [
        {
            "source": "source/rostro.jpg",
            "target": "videos_input/pelicula.mp4",
            "description": "Rostro en película"
        },
        {
            "source": "source/persona.png", 
            "target": "videos_input/video_clip.avi",
            "description": "Persona en video clip"
        },
        {
            "source": "source/face.jpeg",
            "target": "videos_input/entrevista.mov", 
            "description": "Face en entrevista"
        },
        {
            "source": "source/actor.jpg",
            "target": "videos_input/escena_1.mp4",
            "description": "Actor en escena"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        output = generate_output_filename(example["source"], example["target"])
        
        print(f"\n📋 Ejemplo {i}: {example['description']}")
        print(f"   📁 Imagen fuente: {example['source']}")
        print(f"   🎬 Video objetivo: {example['target']}")
        print(f"   📤 Archivo salida: {output}")
    
    print("\n" + "=" * 50)
    print("🎯 VENTAJAS DEL SISTEMA DE NOMBRES:")
    print("=" * 50)
    print("✅ Identifica fácilmente qué rostro se usó")
    print("✅ Identifica fácilmente qué video se procesó")
    print("✅ Evita conflictos de nombres")
    print("✅ Organización automática")
    print("✅ Fácil de buscar y filtrar")
    
    print("\n📁 Estructura de carpetas resultante:")
    print("videos_output/")
    print("├── rostro_pelicula.mp4")
    print("├── persona_video_clip.mp4") 
    print("├── face_entrevista.mp4")
    print("└── actor_escena_1.mp4")

if __name__ == "__main__":
    show_naming_examples() 