#!/usr/bin/env python3
"""
Script optimizado para ejecutar ROOP con gestión de memoria mejorada
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    # Configuración optimizada para memoria
    source_image = "source.jpg"  # Cambia por tu imagen fuente
    target_video = "target.mp4"  # Cambia por tu video objetivo
    output_path = "output.mp4"   # Cambia por tu ruta de salida
    
    # Comando base con optimizaciones de memoria
    base_cmd = [
        "python", "run.py",
        "-s", source_image,
        "-t", target_video,
        "-o", output_path,
        "--memory-optimization",  # Habilitar modo de optimización de memoria
        "--batch-size", "3",      # Reducir batch size para usar menos memoria
        "--execution-threads", "15",  # Reducir threads para evitar sobrecarga
        "--max-memory", "8"       # Limitar memoria a 8GB (ajusta según tu sistema)
    ]
    
    # Verificar si los archivos existen
    if not os.path.exists(source_image):
        print(f"❌ Error: No se encontró la imagen fuente '{source_image}'")
        print("Por favor, coloca tu imagen fuente en el directorio actual")
        return
    
    if not os.path.exists(target_video):
        print(f"❌ Error: No se encontró el video objetivo '{target_video}'")
        print("Por favor, coloca tu video objetivo en el directorio actual")
        return
    
    print("🚀 Iniciando ROOP con optimizaciones de memoria...")
    print(f"📸 Imagen fuente: {source_image}")
    print(f"🎬 Video objetivo: {target_video}")
    print(f"💾 Salida: {output_path}")
    print("\n⚙️  Configuraciones de memoria:")
    print("   • Modo de optimización de memoria: HABILITADO")
    print("   • Tamaño de lote: 3 (reducido para ahorrar memoria)")
    print("   • Threads de ejecución: 15")
    print("   • Límite de memoria: 8GB")
    print("\n💡 Consejos adicionales:")
    print("   • Si sigues teniendo problemas de memoria, reduce --batch-size a 1")
    print("   • Para videos muy largos, considera procesar en segmentos")
    print("   • Cierra otras aplicaciones que usen mucha memoria")
    
    # Construir y ejecutar el comando
    import subprocess
    try:
        print(f"\n🔄 Ejecutando: {' '.join(base_cmd)}")
        result = subprocess.run(base_cmd, check=True)
        print("\n✅ Procesamiento completado exitosamente!")
        print(f"🎉 Video de salida guardado en: {output_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la ejecución: {e}")
        print("\n🔧 Soluciones sugeridas:")
        print("   1. Reduce --batch-size a 1")
        print("   2. Reduce --max-memory a 6")
        print("   3. Cierra otras aplicaciones")
        print("   4. Reinicia tu sistema")
        
    except FileNotFoundError:
        print("\n❌ Error: No se pudo encontrar python o run.py")
        print("Asegúrate de estar en el directorio correcto de ROOP")

if __name__ == "__main__":
    main() 