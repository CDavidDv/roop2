# 🚀 Configuración ROOP para Google Colab

## 🛠️ Solución al Error de onnxruntime

### Problema Identificado
```
ModuleNotFoundError: No module named 'onnxruntime'
```

### ✅ Solución Rápida

**1. Instalar dependencias correctamente:**
```python
# En tu celda de Colab, ejecuta esto PRIMERO:
!python colab_install.py
```

**2. Verificar instalación:**
```python
# Verificar que todo está instalado
!python -c "import onnxruntime; print('✅ ONNX OK:', onnxruntime.get_available_providers())"
```

**3. Ejecutar el procesador:**
```python
# Ahora sí puedes usar el batch processor
!python colab_batch_processor.py
```

## 📦 Instalación Manual (alternativa)

Si `colab_install.py` no funciona, ejecuta estos comandos en celdas separadas:

```python
# Celda 1: Actualizar pip y PyTorch
!pip install --upgrade pip
!pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

```python
# Celda 2: ONNX Runtime GPU (IMPORTANTE)
!pip install onnxruntime-gpu==1.15.1
```

```python
# Celda 3: Dependencias principales
!pip install numpy==1.24.3 opencv-python==4.8.0.74 onnx==1.14.0
!pip install insightface==0.7.3 psutil==5.9.5 pillow==10.0.0
```

```python
# Celda 4: Dependencias adicionales
!pip install tensorflow==2.13.0 opennsfw2==0.10.2 protobuf==4.23.4
!pip install tqdm==4.65.0 gfpgan==1.3.8 moviepy matplotlib
```

## 🔍 Verificación de Tesla T4

```python
# Verificar GPU
!nvidia-smi

# Verificar CUDA en Python
import torch
print("🚀 CUDA disponible:", torch.cuda.is_available())
print("🎯 GPU actual:", torch.cuda.get_device_name(0))

# Verificar ONNX Runtime
import onnxruntime
providers = onnxruntime.get_available_providers()
print("🔧 ONNX Providers:", providers)
if 'CUDAExecutionProvider' in providers:
    print("✅ ¡GPU Tesla T4 lista para ROOP!")
else:
    print("⚠️ Solo CPU disponible")
```

## 📁 Estructura de Archivos en Colab

```python
# Crear estructura de carpetas
!mkdir -p source videos_input videos_output

# Verificar estructura
!ls -la
```

## 🎬 Uso Completo en Colab

```python
# 1. Clonar repositorio
!git clone https://tu-repo.git
%cd roop2

# 2. Instalar dependencias
!python colab_install.py

# 3. Crear carpetas
!python setup_folders.py

# 4. Subir archivos (usar interfaz de Colab)
# - Subir imagen fuente a source/
# - Subir videos a videos_input/

# 5. Procesar
!python colab_batch_processor.py

# 6. Descargar resultados
from google.colab import files
import zipfile

# Comprimir resultados
!zip -r resultados.zip videos_output/
files.download('resultados.zip')
```

## 🚨 Solución de Problemas

### Error: "Command returned non-zero exit status 1"
```python
# Verificar dependencias específicas
!python -c "
try:
    import onnxruntime
    print('✅ onnxruntime OK')
except ImportError:
    print('❌ onnxruntime FALTA - ejecuta: pip install onnxruntime-gpu==1.15.1')

try:
    import cv2
    print('✅ opencv OK')
except ImportError:
    print('❌ opencv FALTA - ejecuta: pip install opencv-python==4.8.0.74')

try:
    import insightface
    print('✅ insightface OK')
except ImportError:
    print('❌ insightface FALTA - ejecuta: pip install insightface==0.7.3')
"
```

### Error de memoria en Tesla T4
```python
# Usar configuración de memoria baja
!python colab_batch_processor.py --batch-size 1 --max-memory 6
```

### Error de permisos
```python
# Dar permisos a los scripts
!chmod +x *.py
```

## 💡 Tips para Colab

1. **Reinicia el runtime** después de instalar dependencias
2. **Usa configuraciones de memoria baja** para videos grandes
3. **Procesa videos cortos** primero para probar
4. **Guarda resultados frecuentemente** en Google Drive

## 📞 Debug Avanzado

```python
# Script de diagnóstico completo
!python -c "
import sys
print('🐍 Python:', sys.version)

try:
    import torch
    print('🔥 PyTorch:', torch.__version__)
    print('🚀 CUDA:', torch.cuda.is_available())
    if torch.cuda.is_available():
        print('🎯 GPU:', torch.cuda.get_device_name(0))
except:
    print('❌ PyTorch no disponible')

try:
    import onnxruntime
    print('🔧 ONNX Runtime:', onnxruntime.__version__)
    providers = onnxruntime.get_available_providers()
    print('📋 Providers:', providers)
except:
    print('❌ ONNX Runtime no disponible')

try:
    import cv2
    print('📸 OpenCV:', cv2.__version__)
except:
    print('❌ OpenCV no disponible')

try:
    import insightface
    print('👤 InsightFace: OK')
except:
    print('❌ InsightFace no disponible')
"
```