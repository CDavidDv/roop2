# 🚀 Procesamiento por Lotes - Roop Optimizado

Sistema automatizado para procesar múltiples videos usando una imagen fuente.

## 📁 Estructura de Carpetas

```
roop2/
├── source/              # Imagen fuente (rostro a intercambiar)
├── videos_input/        # Videos a procesar
├── videos_output/       # Videos procesados
├── batch_processor.py   # Procesador por lotes
├── run_simple.py        # Script optimizado
└── setup_folders.py     # Configurador de carpetas
```

## ⚡ Configuración Rápida

### 1. Configurar carpetas
```bash
python setup_folders.py
```

### 2. Preparar archivos
- Coloca tu imagen fuente en `source/` (jpg, png, etc.)
- Coloca los videos a procesar en `videos_input/` (mp4, avi, mov, etc.)

### 3. Ejecutar procesamiento

#### 🚀 Procesamiento por lotes (recomendado)
```bash
python batch_processor.py
```

#### 🎯 Procesamiento individual
```bash
python run_simple.py -s source.jpg -t video.mp4 -o output.mp4
```

## 🎯 Configuraciones Optimizadas

El sistema usa automáticamente estas configuraciones optimizadas:

- **Execution Provider**: CUDA (GPU)
- **Max Memory**: 12GB
- **Execution Threads**: 8
- **Temp Frame Quality**: 100
- **Keep FPS**: Sí
- **Frame Processors**: face_swapper + face_enhancer
- **NSFW Check**: DESACTIVADO

## 📊 Características

### ✅ Ventajas del sistema por lotes:
- **Automático**: Procesa todos los videos sin intervención
- **Optimizado**: Usa GPU Tesla T4 al máximo
- **Organizado**: Estructura de carpetas clara
- **Robusto**: Manejo de errores y reportes
- **Rápido**: Configuraciones optimizadas por defecto
- **Calidad**: Face swapper + face enhancer para máxima calidad

### 📈 Rendimiento esperado:
- **Tesla T4**: ~2-5 segundos por frame
- **Mejora**: 10-25x más rápido que CPU
- **Memoria**: 12GB GPU + 12GB RAM

## 🔧 Comandos Útiles

### Monitorear GPU
```bash
python monitor_gpu.py
```

### Diagnosticar CUDA
```bash
python debug_cuda.py
```

### Verificar configuración
```bash
python test_cuda.py
```

## 📋 Formatos Soportados

### Imágenes fuente:
- JPG, JPEG, PNG, BMP, TIFF

### Videos de entrada:
- MP4, AVI, MOV, MKV, WMV, FLV

### Videos de salida:
- MP4 (con codificador NVIDIA)

## 🚨 Solución de Problemas

### GPU no se usa:
```bash
python debug_cuda.py
```

### Error de memoria:
- Reduce `--max-memory` a 8 o 6
- Reduce `--execution-threads` a 20

### Videos no se procesan:
- Verifica que las carpetas existan
- Verifica formatos de archivo
- Revisa logs de error

## 📊 Ejemplo de Uso

```bash
# 1. Configurar carpetas
python setup_folders.py

# 2. Colocar archivos
# - source/rostro.jpg
# - videos_input/video1.mp4
# - videos_input/video2.mp4

# 3. Procesar por lotes
python batch_processor.py

# 4. Resultados en videos_output/
# - processed_video1.mp4
# - processed_video2.mp4
```

## 🎉 ¡Listo para usar!

El sistema está optimizado para tu Tesla T4 y procesará automáticamente todos los videos con la máxima velocidad posible. 