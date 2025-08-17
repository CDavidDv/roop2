# 🚀 Optimización de Memoria para ROOP

Este documento explica cómo usar las nuevas optimizaciones de memoria implementadas en ROOP para evitar errores de memoria sin reducir la calidad de la imagen.

## 🎯 Problema Resuelto

El error original:
```
numpy.core._exceptions._ArrayMemoryError: Unable to allocate 43.5 MiB for an array with shape (1760, 1080, 3) and data type float64
```

Ocurre cuando el sistema no tiene suficiente memoria para procesar frames grandes durante la mejora facial.

## ✨ Nuevas Características

### 1. Modo de Optimización de Memoria
- **`--memory-optimization`**: Habilita todas las optimizaciones de memoria
- **`--batch-size <número>`**: Controla el tamaño del lote de procesamiento
- **`--max-memory <GB>`**: Limita el uso máximo de memoria del sistema

### 2. Optimizaciones Automáticas
- Redimensionamiento inteligente de caras para procesamiento
- Limpieza automática de memoria cada 10 frames
- Gestión optimizada de memoria GPU
- Procesamiento en lotes más pequeños

### 3. Monitoreo de Memoria
- Visualización en tiempo real del uso de memoria
- Información de memoria del sistema y GPU
- Alertas automáticas cuando la memoria es alta

## 🚀 Uso Básico

### Comando Simple con Optimizaciones
```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4 --memory-optimization
```

### Comando Avanzado con Configuración Personalizada
```bash
python run.py \
  -s source.jpg \
  -t target.mp4 \
  -o output.mp4 \
  --memory-optimization \
  --batch-size 2 \
  --execution-threads 10 \
  --max-memory 6
```

## ⚙️ Parámetros de Memoria

| Parámetro | Descripción | Valor Recomendado |
|-----------|-------------|-------------------|
| `--memory-optimization` | Habilita optimizaciones | Siempre usar |
| `--batch-size` | Frames por lote | 1-5 (menor = menos memoria) |
| `--max-memory` | Límite de RAM en GB | 6-8 para sistemas con 16GB |
| `--execution-threads` | Número de threads | 10-15 (reducir si hay problemas) |

## 🔧 Configuraciones por Tipo de Sistema

### Sistema con 8GB RAM
```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4 \
  --memory-optimization \
  --batch-size 1 \
  --max-memory 6 \
  --execution-threads 8
```

### Sistema con 16GB RAM
```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4 \
  --memory-optimization \
  --batch-size 3 \
  --max-memory 12 \
  --execution-threads 15
```

### Sistema con 32GB+ RAM
```bash
python run.py -s source.jpg -t target.mp4 -o output.mp4 \
  --memory-optimization \
  --batch-size 5 \
  --max-memory 24 \
  --execution-threads 25
```

## 🎬 Para Videos Largos

### Procesamiento en Segmentos
Si tienes un video muy largo (más de 5 minutos), considera dividirlo:

```bash
# Dividir video en segmentos de 2 minutos
ffmpeg -i long_video.mp4 -c copy -map 0 -segment_time 120 -f segment segment_%03d.mp4

# Procesar cada segmento
for segment in segment_*.mp4; do
  python run.py -s source.jpg -t "$segment" -o "output_$segment" \
    --memory-optimization \
    --batch-size 1 \
    --max-memory 6
done

# Combinar segmentos procesados
ffmpeg -f concat -safe 0 -i segments.txt -c copy final_output.mp4
```

## 🐛 Solución de Problemas

### Error de Memoria Persiste
1. **Reduce batch-size a 1**:
   ```bash
   --batch-size 1
   ```

2. **Reduce threads de ejecución**:
   ```bash
   --execution-threads 5
   ```

3. **Reduce límite de memoria**:
   ```bash
   --max-memory 4
   ```

4. **Cierra otras aplicaciones** que usen mucha memoria

### Rendimiento Lento
1. **Aumenta batch-size** gradualmente:
   ```bash
   --batch-size 2  # Luego 3, 4, 5
   ```

2. **Aumenta threads** si hay memoria disponible:
   ```bash
   --execution-threads 20
   ```

## 📊 Monitoreo de Rendimiento

Durante la ejecución, verás información como:
```
Processing: 71%|███████   | 1276/1793 [23:16<09:25, 1.09s/frame, memory_usage=6.45GB (S:78%, G:65%), execution_providers=['CUDAExecutionProvider'], execution_threads=15, batch_size=3]
```

- `memory_usage`: Uso total de memoria
- `S:78%`: Uso de memoria del sistema (78%)
- `G:65%`: Uso de memoria GPU (65%)
- `batch_size:3`: Tamaño del lote actual

## 💡 Consejos Adicionales

### Antes de Ejecutar
1. **Cierra aplicaciones innecesarias** (navegador, editores, etc.)
2. **Reinicia el sistema** si ha estado funcionando por mucho tiempo
3. **Verifica espacio en disco** (necesitas al menos 2x el tamaño del video)

### Durante la Ejecución
1. **No uses el sistema** para tareas intensivas
2. **Monitorea la memoria** con el Task Manager/htop
3. **Si ves errores**, reduce los parámetros gradualmente

### Para Mejor Calidad
1. **Mantén `--memory-optimization`** habilitado
2. **Usa `--temp-frame-format png`** para máxima calidad
3. **Evita `--temp-frame-quality`** muy baja

## 🔍 Scripts de Ejemplo

### Script Automático (Windows)
```batch
@echo off
echo Iniciando ROOP con optimizaciones de memoria...
python run.py -s source.jpg -t target.mp4 -o output.mp4 ^
  --memory-optimization ^
  --batch-size 2 ^
  --max-memory 8 ^
  --execution-threads 12
pause
```

### Script Automático (Linux/Mac)
```bash
#!/bin/bash
echo "🚀 Iniciando ROOP con optimizaciones de memoria..."
python run.py -s source.jpg -t target.mp4 -o output.mp4 \
  --memory-optimization \
  --batch-size 2 \
  --max-memory 8 \
  --execution-threads 12
```

## 📞 Soporte

Si sigues teniendo problemas:

1. **Revisa los logs** de error completos
2. **Prueba con batch-size 1** y threads reducidos
3. **Verifica la memoria disponible** en tu sistema
4. **Considera procesar en segmentos** para videos largos

## 🎉 Resultado

Con estas optimizaciones, deberías poder procesar videos sin errores de memoria, manteniendo la calidad original de la imagen. El sistema automáticamente:

- ✅ Optimiza el uso de memoria
- ✅ Limpia memoria cuando es necesario
- ✅ Procesa en lotes eficientes
- ✅ Monitorea el rendimiento
- ✅ Mantiene la calidad de imagen

¡Disfruta procesando tus videos sin preocupaciones de memoria! 🎬✨
