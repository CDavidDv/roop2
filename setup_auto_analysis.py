#!/usr/bin/env python3
"""
Script para configurar el análisis automático de videos
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Instala las dependencias necesarias para el análisis automático"""
    print("🔧 INSTALANDO DEPENDENCIAS PARA ANÁLISIS AUTOMÁTICO")
    print("=" * 60)
    
    try:
        # Instalar opencv-python
        print("📦 Instalando OpenCV...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
        print("✅ OpenCV instalado correctamente")
        
        # Instalar numpy si no está disponible
        try:
            import numpy
            print("✅ NumPy ya está disponible")
        except ImportError:
            print("📦 Instalando NumPy...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
            print("✅ NumPy instalado correctamente")
        
        print("\n🎉 Todas las dependencias instaladas correctamente!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_installation():
    """Prueba si la instalación fue exitosa"""
    print("\n🧪 PROBANDO INSTALACIÓN")
    print("=" * 40)
    
    try:
        import cv2
        print(f"✅ OpenCV {cv2.__version__} importado correctamente")
        
        import numpy as np
        print(f"✅ NumPy {np.__version__} importado correctamente")
        
        # Probar detección de rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        if face_cascade.empty():
            print("⚠️  Cascada de rostros no disponible")
        else:
            print("✅ Cascada de rostros cargada correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando módulos: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def create_sample_config():
    """Crea un archivo de configuración de ejemplo"""
    print("\n📝 CREANDO CONFIGURACIÓN DE EJEMPLO")
    print("=" * 40)
    
    config_content = """# Configuración automática de detección de rostros
# Este archivo se genera automáticamente

# Configuración para videos con múltiples personas
group_videos = [
    "family_video.mp4",
    "team_meeting.avi",
    "group_photo.mov"
]

# Configuración para videos de retrato
portrait_videos = [
    "selfie_video.mp4",
    "interview.avi",
    "presentation.mov"
]

# Configuración para videos de baja calidad
low_quality_videos = [
    "old_recording.mp4",
    "compressed_video.avi"
]

# Los videos se analizan automáticamente, pero puedes
# forzar configuraciones específicas aquí
"""
    
    try:
        with open("auto_config_example.txt", "w", encoding="utf-8") as f:
            f.write(config_content)
        print("✅ Archivo de configuración de ejemplo creado: auto_config_example.txt")
    except Exception as e:
        print(f"❌ Error creando archivo de configuración: {e}")

def show_usage():
    """Muestra cómo usar el sistema automático"""
    print("\n📖 CÓMO USAR EL ANÁLISIS AUTOMÁTICO")
    print("=" * 50)
    
    print("1️⃣  ANÁLISIS AUTOMÁTICO DE TODOS LOS VIDEOS:")
    print("   python face_config.py analyze")
    print("   python video_analyzer.py analyze")
    
    print("\n2️⃣  ANÁLISIS DE UN VIDEO ESPECÍFICO:")
    print("   python video_analyzer.py video.mp4")
    
    print("\n3️⃣  PROCESAMIENTO AUTOMÁTICO:")
    print("   python batch_processor.py")
    print("   (El sistema detectará automáticamente la configuración óptima)")
    
    print("\n4️⃣  VER CONFIGURACIÓN ACTUAL:")
    print("   python face_config.py")
    print("   python show_config.py")
    
    print("\n🤖 EL SISTEMA AUTOMÁTICO:")
    print("   • Analiza cada video antes de procesarlo")
    print("   • Detecta resolución, calidad, número de rostros")
    print("   • Configura parámetros óptimos automáticamente")
    print("   • Guarda resultados en cache para reutilizar")
    print("   • No requiere configuración manual")

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR DE ANÁLISIS AUTOMÁTICO")
    print("=" * 60)
    
    # Verificar si ya están instaladas las dependencias
    try:
        import cv2
        import numpy
        print("✅ Dependencias ya están instaladas")
        test_installation()
    except ImportError:
        print("📦 Dependencias no encontradas, instalando...")
        if not install_requirements():
            print("\n❌ No se pudieron instalar las dependencias")
            print("💡 Intenta instalarlas manualmente:")
            print("   pip install opencv-python numpy")
            return
        
        test_installation()
    
    # Crear configuración de ejemplo
    create_sample_config()
    
    # Mostrar uso
    show_usage()
    
    print("\n🎯 PRÓXIMOS PASOS:")
    print("1. Coloca tus videos en la carpeta 'videos_input'")
    print("2. Ejecuta: python face_config.py analyze")
    print("3. Ejecuta: python batch_processor.py")
    print("\n✨ ¡El sistema configurará todo automáticamente!")

if __name__ == "__main__":
    main()
