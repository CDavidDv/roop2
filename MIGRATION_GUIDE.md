# 🎬 ROOP - Guía de Migración a Python 3.12

Esta guía te ayuda a migrar ROOP a Python 3.12 con dependencias actualizadas.

## 📋 Resumen de Cambios

### ✅ Dependencias Actualizadas
- **ONNX Runtime**: `1.15.1` → `≥1.17.0` (compatible con Python 3.12)
- **TensorFlow**: `2.13.0` → `≥2.13.0` (versiones flexibles)
- **Protobuf**: `4.23.4` → `≥4.21.0,<5.0.0` (rango compatible)
- **NumPy**: `1.24.3` → `≥1.24.0` (evita problemas de compilación)

### 🔧 Archivos Modificados
- `requirements.txt` - Dependencias principales actualizadas
- `requirements-colab.txt` - Versión específica para Colab
- `requirements-python312.txt` - Versión completa para Python 3.12

### 🆕 Archivos Nuevos
- `colab_setup.py` - Setup automático para Colab
- `install_colab.py` - Instalador simple
- `test_installation.py` - Pruebas de verificación
- `MIGRATION_GUIDE.md` - Esta guía

## 🚀 Instalación en Google Colab

### Opción 1: Setup Automático (Recomendado)
```python
# Clonar el repositorio (si es necesario)
!git clone https://github.com/tu-usuario/roop2.git
%cd roop2

# Ejecutar setup automático
!python colab_setup.py
```

### Opción 2: Instalación Manual
```python
# Instalar dependencias actualizadas
!pip install numpy opencv-python pillow psutil tqdm torch torchvision tensorflow onnx "onnxruntime-gpu>=1.17.0" insightface gfpgan "protobuf>=4.21.0,<5.0.0" opennsfw2

# Verificar instalación
!python test_installation.py
```

### Opción 3: Usando requirements
```python
# Usar requirements específicos para Colab
!pip install -r requirements-colab.txt

# O requirements generales actualizados
!pip install -r requirements.txt
```

## 🔍 Verificación de la Instalación

```python
# Ejecutar pruebas de verificación
!python test_installation.py
```

Las pruebas verifican:
- ✅ Importaciones de todas las librerías
- 🚀 Funcionalidad CUDA/GPU
- 👤 Librerías de procesamiento facial
- 💾 Optimización de memoria
- 🎬 Módulos específicos de ROOP

## 📁 Estructura de Carpetas

El setup crea automáticamente:
```
roop2/
├── source/          # Imágenes fuente aquí
├── videos_input/    # Videos a procesar aquí  
├── videos_output/   # Videos procesados aquí
├── models/          # Modelos de IA aquí
└── ...
```

## 🎯 Uso Después de la Instalación

### Procesamiento por Lotes
```python
# Colocar imagen fuente en source/
# Colocar videos en videos_input/
# Ejecutar procesamiento automático
!python batch_processor.py --auto
```

### Procesamiento Individual
```python
!python run.py -s source/imagen.jpg -t video.mp4 -o resultado.mp4
```

## 🐛 Solución de Problemas Comunes

### Error: "No matching distribution found for onnxruntime"
```python
# Instalar versión específica compatible
!pip install "onnxruntime-gpu>=1.17.0"
```

### Error: "Getting requirements to build wheel"
```python
# Usar solo binarios precompilados
!pip install --only-binary=all numpy opencv-python
```

### Error: "CUDA not available"
```python
# Verificar runtime de Colab
import torch
print("CUDA disponible:", torch.cuda.is_available())
print("Dispositivo:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU")

# En Colab, ir a: Runtime → Change runtime type → Hardware accelerator → GPU
```

### Error: "InsightFace model not found"
```python
# Los modelos se descargan automáticamente en el primer uso
# Si hay problemas, reinicia el runtime y vuelve a intentar
```

## 🔧 Variables de Entorno

El setup configura automáticamente:
```python
import os
os.environ['OMP_NUM_THREADS'] = '1'          # Optimización CPU
os.environ['MKL_NUM_THREADS'] = '1'          # Intel MKL
os.environ['OPENBLAS_NUM_THREADS'] = '1'     # OpenBLAS  
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'     # Menos logs TF
```

## 📊 Rendimiento Esperado

### Con GPU (T4/V100):
- ✅ Procesamiento 10-20x más rápido
- ✅ Uso de memoria optimizado
- ✅ Modelos de IA acelerados

### Solo CPU:
- ⚠️ Procesamiento más lento
- ✅ Funcionalidad completa
- ⚠️ Mayor uso de memoria RAM

## 🆕 Nuevas Características

### Optimización Automática de Memoria
- Detección automática de recursos del sistema
- Ajuste dinámico de batch size
- Limpieza automática de memoria

### Configuración Adaptativa
- Perfiles de memoria (low/medium/high)
- Ajuste automático de threads
- Optimización de calidad de frames

## 🔄 Migración desde Versión Anterior

1. **Respaldar configuración actual**
2. **Ejecutar `colab_setup.py`**
3. **Verificar con `test_installation.py`** 
4. **Probar con `batch_processor.py --dry-run`**
5. **Procesamiento normal**

## 📞 Soporte

Si tienes problemas:

1. Ejecuta `test_installation.py` y comparte los resultados
2. Verifica que uses Python 3.10+ en Colab
3. Asegúrate que el runtime tenga GPU activada
4. Reinicia el runtime si hay errores persistentes

## 🎉 ¡Listo!

Con esta migración tendrás:
- ✅ Compatibilidad con Python 3.12
- ✅ Dependencias actualizadas
- ✅ Mejor rendimiento
- ✅ Setup automatizado
- ✅ Verificación completa