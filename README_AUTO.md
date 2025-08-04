# 🤖 Sistema de Análisis Automático de Videos

## 🎯 **¿Qué hace?**

Este sistema **analiza automáticamente** tus videos y configura los parámetros óptimos para la detección de rostros **sin que tengas que hacer nada manualmente**.

## 🚀 **Instalación Rápida**

```bash
# 1. Instalar dependencias para análisis automático
python install_analyzer.py

# 2. ¡Listo! Ya puedes usar el sistema
```

## 📊 **Cómo Funciona**

### **Análisis Automático**
El sistema analiza cada video y detecta:
- ✅ **Número de rostros** en el video
- ✅ **Tamaño de los rostros** (pequeños, medianos, grandes)
- ✅ **Calidad del video** (resolución, bitrate)
- ✅ **Duración del video**
- ✅ **Posición de los rostros**

### **Configuración Automática**
Basado en el análisis, configura automáticamente:
- 🎯 **Distancia de reconocimiento** óptima
- 👥 **Procesamiento de múltiples rostros** si es necesario
- 📐 **Calidad de frames** según la calidad del video
- ⚙️ **Parámetros específicos** para cada tipo de video

## 🎮 **Uso Simple**

### **Procesar todos los videos automáticamente:**
```bash
python batch_processor.py
```

### **Analizar videos antes de procesar:**
```bash
# Analizar todos los videos en videos_input
python face_config.py analyze

# Analizar un video específico
python video_analyzer.py videos_input/mi_video.mp4
```

### **Ver configuración actual:**
```bash
python show_config.py
```

## 🔧 **Configuraciones Automáticas**

### **Videos con Múltiples Personas**
- ✅ Detecta automáticamente múltiples rostros
- ⚙️ Configura `--many-faces`
- 🎯 Ajusta distancia a `0.80`

### **Videos con Rostros Pequeños**
- 🔍 Detecta rostros pequeños automáticamente
- ⚙️ Reduce distancia a `0.75`
- 📐 Mantiene calidad máxima

### **Videos de Baja Calidad**
- 📊 Analiza resolución y bitrate
- ⚙️ Ajusta parámetros para mejor detección
- 📐 Reduce calidad de frames si es necesario

### **Videos Largos**
- ⏱️ Detecta duración automáticamente
- ⚙️ Optimiza para procesamiento eficiente
- 📐 Ajusta calidad según duración

## 📁 **Estructura de Archivos**

```
roop2/
├── batch_processor.py      # Procesador principal (actualizado)
├── video_analyzer.py       # Analizador automático de videos
├── face_config.py          # Configuración inteligente
├── install_analyzer.py     # Instalador de dependencias
├── show_config.py          # Visualizador de configuración
├── source/                 # Imagen fuente
├── videos_input/           # Videos a procesar
└── videos_output/          # Videos procesados
```

## 🎯 **Ventajas del Sistema Automático**

### **✅ Sin Configuración Manual**
- No necesitas saber el formato del video
- No necesitas ajustar parámetros manualmente
- El sistema detecta todo automáticamente

### **✅ Optimización Inteligente**
- Configuración específica para cada video
- Ajustes basados en características reales
- Mejor detección de rostros

### **✅ Compatibilidad Total**
- Funciona con cualquier formato de video
- Detecta automáticamente la calidad
- Se adapta a diferentes tipos de contenido

### **✅ Fallback Inteligente**
- Si el análisis automático falla, usa configuración manual
- Sistema robusto que siempre funciona
- Mensajes informativos sobre qué está haciendo

## 🔍 **Ejemplo de Análisis Automático**

```
🔍 Analizando video: mi_video.mp4
   📊 Analizando 50 frames de 3000 totales...

📊 REPORTE DE ANÁLISIS: mi_video.mp4
============================================================
📹 INFORMACIÓN DEL VIDEO:
   • Resolución: 1920x1080
   • Duración: 120.5 segundos
   • FPS: 30.0
   • Tamaño: 45.2 MB
   • Calidad: high

👥 ANÁLISIS DE ROSTROS:
   • Rostros promedio por frame: 1.85
   • Máximo rostros en un frame: 3
   • Tamaño promedio de rostros: 0.0234
   • Frames con rostros: 48/50

⚙️  CONFIGURACIÓN RECOMENDADA:
   • similar_face_distance: 0.80
   • reference_face_position: 0
   • temp_frame_quality: 100
   • many_faces: True

💡 RAZONES:
   • Múltiples rostros detectados
   • Video de alta calidad
============================================================
```

## 🚀 **Comandos Disponibles**

| Comando | Descripción |
|---------|-------------|
| `python batch_processor.py` | Procesar todos los videos con análisis automático |
| `python face_config.py analyze` | Analizar todos los videos antes de procesar |
| `python video_analyzer.py <video>` | Analizar un video específico |
| `python show_config.py` | Ver configuración y parámetros disponibles |
| `python install_analyzer.py` | Instalar dependencias para análisis automático |

## 💡 **Consejos**

### **Para Mejor Resultado:**
1. **Instala las dependencias** primero con `python install_analyzer.py`
2. **Coloca tus videos** en la carpeta `videos_input/`
3. **Coloca tu imagen fuente** en la carpeta `source/`
4. **Ejecuta** `python batch_processor.py`

### **Si Tienes Problemas:**
- El sistema tiene **fallback automático** a configuración manual
- Siempre muestra **información detallada** de lo que está haciendo
- Puedes **ver el análisis** antes de procesar

### **Personalización:**
- Puedes **editar** `face_config.py` para ajustar parámetros
- El sistema **combina** análisis automático + configuración manual
- **Nombra tus videos** con palabras clave para configuración específica

## 🎉 **¡Listo!**

Ahora tu sistema **detecta automáticamente** las características de cada video y configura los parámetros óptimos **sin intervención manual**. ¡Solo ejecuta `python batch_processor.py` y disfruta de los resultados! 