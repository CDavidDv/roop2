# 🚀 Roop Enhanced Pipeline - 2 Face Enhancers

Este proyecto ha sido mejorado para incluir **dos face enhancers** que se ejecutan en diferentes momentos del pipeline, proporcionando resultados de mayor calidad.

## 🎯 Pipeline Mejorado

El nuevo pipeline incluye **3 processors en secuencia**:

1. **Pre Face Enhancer** (`pre_face_enhancer`) - Mejora la calidad del video original
2. **Face Swapper** (`face_swapper`) - Realiza el face swap
3. **Post Face Enhancer** (`post_face_enhancer`) - Mejora la calidad después del face swap

## 📁 Nuevos Archivos

### Processors
- `roop/processors/frame/pre_face_enhancer.py` - Face enhancer que se ejecuta ANTES del face swap
- `roop/processors/frame/post_face_enhancer.py` - Face enhancer que se ejecuta DESPUÉS del face swap

### Scripts de Ejecución
- `run_enhanced_pipeline.py` - Pipeline completo con los 3 processors
- `run_custom_pipeline.py` - Pipeline personalizable con diferentes combinaciones
- `batch_processor_enhanced.py` - Procesamiento por lotes con pipelines mejorados
- `run_batch_enhanced.py` - Ejemplos y utilidades para batch processing

## 🚀 Uso Rápido

### Pipeline Completo (Recomendado)
```bash
python run_enhanced_pipeline.py -s imagen_fuente.jpg -t video_objetivo.mp4 -o resultado.mp4 --keep-fps
```

### Pipeline Personalizado
```bash
# Ver presets disponibles
python run_custom_pipeline.py --list-presets

# Pipeline básico (solo face swap + enhancer original)
python run_custom_pipeline.py -s imagen_fuente.jpg -t video_objetivo.mp4 --processors face_swapper face_enhancer

# Solo mejora antes del swap
python run_custom_pipeline.py -s imagen_fuente.jpg -t video_objetivo.mp4 --processors pre_face_enhancer face_swapper

# Solo mejora después del swap
python run_custom_pipeline.py -s imagen_fuente.jpg -t video_objetivo.mp4 --processors face_swapper post_face_enhancer
```

## 📦 Procesamiento por Lotes

### Batch Processor Mejorado
```bash
# Pipeline completo para todos los videos
python batch_processor_enhanced.py --pipeline full

# Pipeline básico (original)
python batch_processor_enhanced.py --pipeline basic

# Solo mejora antes del swap
python batch_processor_enhanced.py --pipeline pre_only

# Solo mejora después del swap
python batch_processor_enhanced.py --pipeline post_only

# Pipeline personalizado
python batch_processor_enhanced.py --pipeline custom --custom-processors pre_face_enhancer,face_swapper
```

### Estructura de Carpetas para Batch Processing
```
tu_proyecto/
├── source/              # Imagen fuente para el face swap
│   └── cara_fuente.jpg
├── videos_input/        # Videos a procesar
│   ├── video1.mp4
│   ├── video2.mp4
│   └── video3.mp4
└── videos_output/       # Videos procesados (se crea automáticamente)
    ├── cara_fuente_video1.mp4
    ├── cara_fuente_video2.mp4
    └── cara_fuente_video3.mp4
```

## ⚙️ Configuraciones Disponibles

### Pipeline Completo
```bash
python run_enhanced_pipeline.py \
  -s imagen_fuente.jpg \
  -t video_objetivo.mp4 \
  -o resultado_mejorado.mp4 \
  --keep-fps \
  --many-faces
```

### Pipeline Personalizado
```bash
python run_custom_pipeline.py \
  -s imagen_fuente.jpg \
  -t video_objetivo.mp4 \
  -o resultado_personalizado.mp4 \
  --processors pre_face_enhancer face_swapper post_face_enhancer \
  --keep-fps \
  --skip-audio
```

## 🎯 Diferencias entre Enhancers

### Pre Face Enhancer
- **Cuándo se ejecuta**: Antes del face swap
- **Propósito**: Mejora la calidad del video original
- **Beneficio**: Proporciona una base de mejor calidad para el face swap

### Post Face Enhancer
- **Cuándo se ejecuta**: Después del face swap
- **Propósito**: Mejora la calidad del resultado final
- **Beneficio**: Refina el resultado del face swap y mejora la integración

### Face Enhancer Original
- **Cuándo se ejecuta**: Después del face swap (como antes)
- **Propósito**: Mejora general de la calidad
- **Compatibilidad**: Mantiene compatibilidad con el pipeline original

## 🔧 Opciones Avanzadas

### Configuración de CUDA
El sistema detecta automáticamente CUDA y optimiza para Tesla T4:
- **Con CUDA**: 8 threads para máximo rendimiento
- **Sin CUDA**: 1 thread para CPU

### Opciones de Procesamiento
- `--keep-fps`: Mantiene el FPS original del video
- `--skip-audio`: Salta el procesamiento de audio
- `--many-faces`: Procesa todas las caras en el video
- `--output-video-quality`: Controla la calidad del video de salida (0-100)

## 📊 Comparación de Calidad

| Pipeline | Calidad Original | Calidad Face Swap | Calidad Final |
|----------|------------------|-------------------|---------------|
| Solo Face Swap | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Face Swap + Enhancer | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Pipeline Completo** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🛠️ Requisitos

Los mismos que Roop original:
- Python 3.8+
- CUDA (opcional, pero recomendado)
- Modelos GFPGAN (se descargan automáticamente)

## 🔍 Troubleshooting

### Error de Memoria
Si tienes problemas de memoria con el pipeline completo:
```bash
# Usar solo post enhancer
python run_custom_pipeline.py -s imagen.jpg -t video.mp4 --processors face_swapper post_face_enhancer

# O usar solo pre enhancer
python run_custom_pipeline.py -s imagen.jpg -t video.mp4 --processors pre_face_enhancer face_swapper
```

### Rendimiento Lento
- Asegúrate de tener CUDA habilitado
- Reduce la resolución del video si es necesario
- Usa `--skip-audio` para procesamiento más rápido

## 🎉 Resultados Esperados

Con el pipeline completo deberías ver:
1. **Mejor calidad inicial** del video procesado
2. **Face swap más natural** y bien integrado
3. **Resultado final más refinado** con mejor textura y detalles

## 📦 Ventajas del Batch Processing

### 🚀 Procesamiento Eficiente
- **Procesamiento automático** de múltiples videos
- **Configuración única** para todos los videos
- **Gestión de errores** mejorada
- **Progreso detallado** con tiempo estimado

### 🎯 Pipelines Optimizados
- **Pipeline Completo**: Máxima calidad (3 processors)
- **Pipeline Básico**: Compatibilidad con original
- **Pipelines Específicos**: Optimizados para diferentes necesidades
- **Pipeline Personalizado**: Total control sobre el proceso

### ⚡ Configuración Automática
- **Detección automática de CUDA** para máximo rendimiento
- **Optimización para Tesla T4** con 8 threads
- **Gestión de memoria** inteligente
- **Calidad máxima** por defecto

### 📊 Monitoreo y Control
- **Progreso en tiempo real** para cada video
- **Resumen final** con estadísticas
- **Gestión de errores** por video individual
- **Logs detallados** para debugging

¡Disfruta de tus videos con calidad profesional! 🎬✨ 