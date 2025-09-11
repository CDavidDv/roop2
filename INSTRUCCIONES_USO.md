# 🎬 ROOP - MÁXIMA CALIDAD

## 🚀 Uso en Google Colab

### **PASO 1: Instalación (una sola vez)**
```python
!python 1_INSTALAR_TODO.py
```

### **PASO 2: Subir archivos**
- 📤 Sube **1 imagen** a `source/` (rostro a intercambiar)
- 📤 Sube **videos** a `videos_input/` (videos a procesar)

### **PASO 3: Procesar videos**
```python
!python 2_PROCESAR_VIDEOS.py
```

### **PASO 4: Descargar resultados**
```python
from google.colab import files
!zip -r videos_maxima_calidad.zip videos_output/MAXCAL_*.mp4
files.download('videos_maxima_calidad.zip')
```

## 🎯 Configuración de MÁXIMA CALIDAD

### **Pipeline de Procesamiento:**
1. **Face Enhancer** → Mejora calidad inicial del rostro
2. **Face Swapper** → Intercambia el rostro
3. **Face Enhancer** → Mejora calidad final del resultado

### **Configuración Técnica:**
- **Frames**: PNG 100% (sin compresión)
- **Video**: Calidad 0 (sin compresión)
- **Encoder**: H264_NVENC (hardware GPU)
- **Audio**: Preservado sin modificación
- **FPS**: Mantenido original
- **GPU**: CUDA con 8 threads optimizados
- **Memoria**: 12GB (Tesla T4 completa)

### **Características Especiales:**
- ✅ **NUNCA** reduce calidad de imagen
- ✅ **NUNCA** reduce calidad de video
- ✅ Procesa **TODAS** las caras detectadas
- ✅ Mantiene audio original
- ✅ Optimizado para Tesla T4

## 📁 Estructura de Archivos

```
roop2/
├── source/              ← TU IMAGEN FUENTE AQUÍ
│   └── rostro.jpg
├── videos_input/        ← TUS VIDEOS AQUÍ
│   ├── video1.mp4
│   └── video2.mp4
├── videos_output/       ← RESULTADOS (automático)
│   ├── MAXCAL_20250911_123456_video1.mp4
│   └── MAXCAL_20250911_123457_video2.mp4
├── temp/               ← Archivos temporales
└── models/             ← Modelos IA (descarga automática)
```

## ⚙️ Configuraciones Avanzadas

### **Si necesitas cambiar configuración:**
Edita `config_maxima_calidad.ini`:

```ini
[CALIDAD]
temp_frame_format = png        # PNG para máxima calidad
temp_frame_quality = 100       # 100% sin compresión
output_video_quality = 0       # 0 = sin compresión
keep_fps = true               # Mantener FPS original

[PROCESAMIENTO]
frame_processors = face_enhancer,face_swapper,face_enhancer
execution_provider = cuda      # Usar GPU
execution_threads = 8         # Threads optimizados
many_faces = true            # Procesar todas las caras
similar_face_distance = 0.85 # Precisión alta (0.75-0.95)

[MEMORIA]
max_memory = 12              # Tesla T4 completa
batch_size = 1              # Procesar frame por frame
memory_optimization = true   # Optimizaciones activas
```

## 🚨 Solución de Problemas

### **Error de NumPy:**
```python
!pip install numpy==1.26.4 --force-reinstall
# Luego reinicia runtime y ejecuta 1_INSTALAR_TODO.py
```

### **Error de GPU:**
```python
# Verificar GPU
!nvidia-smi
# Debe mostrar Tesla T4
```

### **Error de memoria:**
- Procesa videos más cortos
- Los scripts ya están optimizados para Tesla T4

### **Video no procesa:**
- Verifica formato (MP4, AVI, MOV soportados)
- Verifica que la imagen fuente sea clara
- Revisa logs para errores específicos

## 📊 Tiempos Esperados (Tesla T4)

- **Video corto** (30 seg): ~2-5 minutos
- **Video medio** (2 min): ~8-15 minutos  
- **Video largo** (5 min): ~20-40 minutos

*Tiempos con máxima calidad - NO se puede acelerar sin perder calidad*

## 💡 Tips para Mejores Resultados

1. **Imagen fuente**:
   - Usar rostro frontal y claro
   - Buena iluminación
   - Resolución alta
   - Expresión neutra

2. **Videos**:
   - Buena calidad original
   - Rostros claramente visibles
   - Iluminación estable

3. **Procesamiento**:
   - No interrumpir el proceso
   - Un video a la vez para máxima calidad
   - Verificar resultados antes de procesar lotes grandes

## 🎉 ¡Disfruta de la MÁXIMA CALIDAD!

Esta configuración prioriza **CALIDAD sobre VELOCIDAD**. Los resultados serán de la más alta calidad posible con el hardware Tesla T4.