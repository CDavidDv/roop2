#!/usr/bin/env python3

def show_processors_info():
    """Muestra información sobre los procesadores de frames disponibles"""
    print("🎭 PROCESADORES DE FRAMES DISPONIBLES")
    print("=" * 50)
    
    processors = {
        "face_swapper": {
            "descripción": "Intercambia rostros en el video",
            "función": "Reemplaza el rostro del video con el rostro de la imagen fuente",
            "calidad": "Alta - Mantiene expresiones y movimientos",
            "tiempo": "Rápido - Procesamiento principal"
        },
        "face_enhancer": {
            "descripción": "Mejora la calidad de los rostros",
            "función": "Aplica mejoras de calidad usando GFPGAN",
            "calidad": "Muy alta - Rostros más nítidos y realistas",
            "tiempo": "Medio - Procesamiento adicional"
        }
    }
    
    for name, info in processors.items():
        print(f"\n🔧 {name.upper()}")
        print(f"   📝 {info['descripción']}")
        print(f"   ⚙️  {info['función']}")
        print(f"   🎯 {info['calidad']}")
        print(f"   ⏱️  {info['tiempo']}")
    
    print("\n" + "=" * 50)
    print("📋 CONFIGURACIÓN ACTUAL")
    print("=" * 50)
    print("✅ Ambos procesadores activados por defecto:")
    print("   1. face_swapper - Intercambia el rostro")
    print("   2. face_enhancer - Mejora la calidad")
    print("\n🎯 Resultado: Rostros intercambiados + mejorados")
    print("\n⚡ Para usar solo face_swapper (más rápido):")
    print("   --frame-processor face_swapper")
    print("\n🎨 Para usar solo face_enhancer (solo mejora):")
    print("   --frame-processor face_enhancer")
    print("\n🚀 Para usar ambos (máxima calidad):")
    print("   --frame-processor face_swapper face_enhancer")

if __name__ == "__main__":
    show_processors_info() 