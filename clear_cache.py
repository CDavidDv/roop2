#!/usr/bin/env python3
"""
Script para limpiar el cache del análisis automático
"""

def clear_analysis_cache():
    """Limpia el cache del análisis automático"""
    try:
        # Importar el módulo de configuración
        import face_config
        
        # Limpiar el cache
        if hasattr(face_config, 'AUTO_ANALYSIS_CACHE'):
            face_config.AUTO_ANALYSIS_CACHE.clear()
            print("✅ Cache del análisis automático limpiado")
        else:
            print("ℹ️  No hay cache para limpiar")
            
        print("💡 Los próximos análisis usarán la nueva configuración")
        print("   • temp_frame_quality: 100 (calidad máxima)")
        print("   • Mejor detección de rostros")
        
    except ImportError:
        print("❌ No se pudo importar face_config.py")
    except Exception as e:
        print(f"❌ Error limpiando cache: {e}")

if __name__ == "__main__":
    print("🧹 LIMPIANDO CACHE DEL ANÁLISIS AUTOMÁTICO")
    print("=" * 50)
    clear_analysis_cache()
    print("\n📊 PRÓXIMOS PASOS:")
    print("  1. Ejecuta: python batch_processor.py")
    print("  2. El sistema usará temp_frame_quality: 100")
    print("  3. Mejor detección de rostros con calidad máxima") 