#!/usr/bin/env python3
"""
🚀 COMANDO ÚNICO PARA TODO
Ejecuta esto y ya tienes procesamiento por lotes funcionando

Para Google Colab - Basado en roop original
"""

import os
import subprocess
import sys
from pathlib import Path

def ejecutar_todo():
    """Un solo comando que hace todo"""
    
    print("🚀" * 70)
    print("🎬 ROOP - CONFIGURACIÓN Y EJECUCIÓN AUTOMÁTICA")
    print("🚀" * 70)
    print("✨ Basado en el roop original que funcionaba")
    print("🚀" * 70)
    
    # PASO 1: Configurar NumPy que funciona
    print("🔧 PASO 1: Configurando NumPy 1.26.4 (versión que funciona)")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "numpy==1.26.4"], 
                      check=True, capture_output=True)
        print("✅ NumPy 1.26.4 configurado")
    except:
        print("⚠️ NumPy ya configurado")
    
    # PASO 2: Instalar solo lo esencial
    print("\n📦 PASO 2: Instalando dependencias esenciales")
    esenciales = ["onnxruntime-gpu", "insightface", "gfpgan"]
    for dep in esenciales:
        print(f"   📦 {dep}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", dep], 
                         check=True, capture_output=True, timeout=120)
            print(f"   ✅ {dep} OK")
        except:
            print(f"   ⚠️ {dep} ya existe o error")
    
    # PASO 3: Crear carpetas
    print("\n📁 PASO 3: Creando estructura de carpetas")
    carpetas = ["source", "videos_input", "videos_output"]
    for carpeta in carpetas:
        Path(carpeta).mkdir(exist_ok=True)
        print(f"   ✅ {carpeta}/")
    
    # PASO 4: Verificar archivos
    print("\n📋 PASO 4: Verificando archivos")
    source_files = list(Path("source").glob("*.*"))
    video_files = list(Path("videos_input").glob("*.*"))
    
    print(f"   📸 Imágenes fuente: {len(source_files)}")
    print(f"   🎬 Videos: {len(video_files)}")
    
    if not source_files:
        print("\n⚠️ ACCIÓN REQUERIDA:")
        print("   📤 Sube UNA imagen a la carpeta 'source/'")
        print("   💡 Formatos: .jpg, .png, .jpeg")
        return False
    
    if not video_files:
        print("\n⚠️ ACCIÓN REQUERIDA:")
        print("   📤 Sube videos a la carpeta 'videos_input/'")
        print("   💡 Formatos: .mp4, .avi, .mov")
        return False
    
    # PASO 5: Ejecutar procesamiento
    print(f"\n🚀 PASO 5: Ejecutando procesamiento por lotes")
    print(f"   📸 Usando: {source_files[0].name}")
    print(f"   🎬 Procesando: {len(video_files)} videos")
    
    # Ejecutar el procesador por lotes
    try:
        subprocess.run([sys.executable, "setup_and_run.py"], check=True)
        return True
    except subprocess.CalledProcessError:
        print("❌ Error en procesamiento - revisa logs arriba")
        return False
    except KeyboardInterrupt:
        print("❌ Cancelado por usuario")
        return False

def instrucciones_uso():
    """Muestra instrucciones claras"""
    print("\n" + "📖" * 70)
    print("📖 INSTRUCCIONES DE USO")
    print("📖" * 70)
    print("1. 📤 SUBIR ARCHIVOS:")
    print("   • Sube 1 imagen a source/ (el rostro que quieres usar)")
    print("   • Sube videos a videos_input/ (los videos a procesar)")
    print()
    print("2. 🚀 EJECUTAR:")
    print("   !python EJECUTAR_TODO.py")
    print()
    print("3. 📥 DESCARGAR:")
    print("   • Los videos procesados estarán en videos_output/")
    print()
    print("📖" * 70)
    print("💡 ESTE SCRIPT HACE TODO AUTOMÁTICAMENTE:")
    print("   ✅ Instala dependencias")
    print("   ✅ Crea carpetas")
    print("   ✅ Procesa todos los videos")
    print("   ✅ Usa el roop original (sin modificaciones complejas)")
    print("📖" * 70)

def main():
    """Función principal"""
    # Mostrar instrucciones primero
    instrucciones_uso()
    
    # Ejecutar todo
    if ejecutar_todo():
        print("\n🎉" * 70)
        print("🎉 ¡PROCESAMIENTO COMPLETADO EXITOSAMENTE!")
        print("🎉" * 70)
        print("📁 Revisa la carpeta 'videos_output/' para tus resultados")
    else:
        print("\n❌" * 70)
        print("❌ PROCESAMIENTO INCOMPLETO")
        print("❌" * 70)
        print("💡 Sigue las instrucciones arriba y ejecuta nuevamente")

if __name__ == "__main__":
    main()