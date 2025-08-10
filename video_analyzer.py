#!/usr/bin/env python3
"""
Analizador automático de videos para configuración óptima de detección de rostros
"""

import cv2
import numpy as np
from pathlib import Path
import json
import os
from typing import Dict, List, Tuple, Optional

class VideoAnalyzer:
    def __init__(self):
        self.face_cascade = None
        self.eye_cascade = None
        self.analysis_cache = {}
        self.cache_file = "video_analysis_cache.json"
        self.load_cache()
        
        # Intentar cargar cascadas de OpenCV
        try:
            self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        except:
            print("⚠️  OpenCV no disponible, usando análisis básico")
    
    def load_cache(self):
        """Carga el cache de análisis previos"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    self.analysis_cache = json.load(f)
        except:
            self.analysis_cache = {}
    
    def save_cache(self):
        """Guarda el cache de análisis"""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.analysis_cache, f, indent=2)
        except:
            pass
    
    def analyze_video_auto(self, video_path: str) -> Dict:
        """
        Analiza automáticamente un video y retorna la configuración óptima
        """
        video_path = str(video_path)
        
        # Verificar cache
        if video_path in self.analysis_cache:
            print(f"📋 Usando análisis cacheado para {Path(video_path).name}")
            return self.analysis_cache[video_path]
        
        print(f"🔍 Analizando video: {Path(video_path).name}")
        
        try:
            # Abrir video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("No se pudo abrir el video")
            
            # Obtener información básica
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            duration = frame_count / fps if fps > 0 else 0
            
            # Analizar frames clave
            face_count, face_sizes, quality_score = self.analyze_frames(cap, frame_count)
            
            cap.release()
            
            # Determinar configuración óptima
            config = self.determine_optimal_config(
                width, height, fps, duration, face_count, face_sizes, quality_score
            )
            
            # Guardar en cache
            self.analysis_cache[video_path] = config
            self.save_cache()
            
            return config
            
        except Exception as e:
            print(f"❌ Error analizando {Path(video_path).name}: {e}")
            # Configuración por defecto
            return self.get_default_config()
    
    def analyze_frames(self, cap: cv2.VideoCapture, total_frames: int) -> Tuple[int, List[float], float]:
        """
        Analiza frames del video para detectar rostros y calidad
        """
        face_count = 0
        face_sizes = []
        quality_scores = []
        
        # Analizar frames espaciados uniformemente
        sample_frames = min(20, total_frames)  # Máximo 20 frames
        frame_indices = np.linspace(0, total_frames-1, sample_frames, dtype=int)
        
        for frame_idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if not ret:
                continue
            
            # Analizar calidad del frame
            quality = self.analyze_frame_quality(frame)
            quality_scores.append(quality)
            
            # Detectar rostros si OpenCV está disponible
            if self.face_cascade is not None:
                faces = self.detect_faces_in_frame(frame)
                face_count = max(face_count, len(faces))
                
                for face in faces:
                    face_size = (face[2] * face[3]) / (frame.shape[0] * frame.shape[1])
                    face_sizes.append(face_size)
        
        avg_quality = np.mean(quality_scores) if quality_scores else 0.5
        return face_count, face_sizes, avg_quality
    
    def detect_faces_in_frame(self, frame: np.ndarray) -> List:
        """
        Detecta rostros en un frame usando OpenCV
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            return faces.tolist()
        except:
            return []
    
    def analyze_frame_quality(self, frame: np.ndarray) -> float:
        """
        Analiza la calidad de un frame basado en nitidez y contraste
        """
        try:
            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Calcular nitidez usando Laplaciano
            laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            # Calcular contraste
            contrast = gray.std()
            
            # Normalizar y combinar métricas
            sharpness_score = min(laplacian_var / 1000, 1.0)  # Normalizar
            contrast_score = min(contrast / 100, 1.0)  # Normalizar
            
            quality = (sharpness_score + contrast_score) / 2
            return max(0.1, min(1.0, quality))  # Limitar entre 0.1 y 1.0
            
        except:
            return 0.5
    
    def determine_optimal_config(self, width: int, height: int, fps: float, 
                               duration: float, face_count: int, 
                               face_sizes: List[float], quality_score: float) -> Dict:
        """
        Determina la configuración óptima basada en el análisis del video
        """
        config = {
            "many_faces": False,
            "similar_face_distance": "0.85",
            "reference_face_position": "0",
            "temp_frame_quality": "100",
            "analysis_info": {}
        }
        
        # Configurar según número de rostros
        if face_count > 1:
            config["many_faces"] = True
            config["similar_face_distance"] = "0.80"
            print(f"   👥 Detectados {face_count} rostros - Activando procesamiento múltiple")
        
        # Configurar según tamaño de rostros
        if face_sizes:
            avg_face_size = np.mean(face_sizes)
            if avg_face_size < 0.01:  # Rostros muy pequeños
                config["similar_face_distance"] = "0.75"
                config["temp_frame_quality"] = "100"
                print(f"   🔍 Rostros pequeños detectados - Ajustando sensibilidad")
            elif avg_face_size > 0.1:  # Rostros muy grandes
                config["similar_face_distance"] = "0.90"
                print(f"   📸 Rostros grandes detectados - Ajustando para mejor detección")
        
        # Configurar según calidad del video
        if quality_score < 0.4:
            config["temp_frame_quality"] = "100"
            config["similar_face_distance"] = "0.75"
            print(f"   📉 Video de baja calidad detectado - Optimizando parámetros")
        elif quality_score > 0.8:
            config["similar_face_distance"] = "0.90"
            print(f"   ✨ Video de alta calidad detectado - Usando parámetros estándar")
        
        # Configurar según resolución
        if width < 720 or height < 480:
            config["temp_frame_quality"] = "100"
            print(f"   📱 Resolución baja detectada ({width}x{height}) - Maximizando calidad")
        elif width > 1920 or height > 1080:
            print(f"   🎬 Resolución alta detectada ({width}x{height}) - Usando configuración estándar")
        
        # Guardar información del análisis
        config["analysis_info"] = {
            "resolution": f"{width}x{height}",
            "fps": round(fps, 2),
            "duration": round(duration, 2),
            "face_count": face_count,
            "avg_face_size": round(np.mean(face_sizes), 4) if face_sizes else 0,
            "quality_score": round(quality_score, 3)
        }
        
        return config
    
    def get_default_config(self) -> Dict:
        """
        Retorna configuración por defecto
        """
        return {
            "many_faces": True,
            "similar_face_distance": "0.85",
            "reference_face_position": "0",
            "temp_frame_quality": "100",
            "analysis_info": {"error": "Configuración por defecto"}
        }
    
    def print_analysis_report(self, video_path: str):
        """
        Imprime un reporte detallado del análisis
        """
        if video_path not in self.analysis_cache:
            print(f"❌ No hay análisis disponible para {Path(video_path).name}")
            return
        
        config = self.analysis_cache[video_path]
        info = config.get("analysis_info", {})
        
        print(f"\n📊 REPORTE DE ANÁLISIS: {Path(video_path).name}")
        print("=" * 50)
        
        if "error" not in info:
            print(f"📐 Resolución: {info.get('resolution', 'N/A')}")
            print(f"🎬 FPS: {info.get('fps', 'N/A')}")
            print(f"⏱️  Duración: {info.get('duration', 'N/A')} segundos")
            print(f"👥 Rostros detectados: {info.get('face_count', 'N/A')}")
            print(f"🔍 Tamaño promedio de rostros: {info.get('avg_face_size', 'N/A')}")
            print(f"✨ Puntuación de calidad: {info.get('quality_score', 'N/A')}")
        else:
            print("⚠️  Análisis no disponible")
        
        print(f"\n⚙️  CONFIGURACIÓN APLICADA:")
        print(f"  • Múltiples rostros: {config['many_faces']}")
        print(f"  • Distancia de rostros: {config['similar_face_distance']}")
        print(f"  • Posición de referencia: {config['reference_face_position']}")
        print(f"  • Calidad de frames: {config['temp_frame_quality']}")
    
    def analyze_all_videos_in_folder(self, folder_path: str = "videos_input"):
        """
        Analiza automáticamente todos los videos en una carpeta
        """
        folder = Path(folder_path)
        if not folder.exists():
            print(f"❌ La carpeta {folder_path} no existe")
            return
        
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(folder.glob(ext))
        
        if not video_files:
            print(f"⚠️  No se encontraron videos en {folder_path}")
            return
        
        print(f"🔍 Analizando {len(video_files)} videos automáticamente...")
        print("=" * 60)
        
        for video_file in video_files:
            try:
                self.analyze_video_auto(str(video_file))
                self.print_analysis_report(str(video_file))
                print("-" * 40)
            except Exception as e:
                print(f"❌ Error analizando {video_file.name}: {e}")
        
        print("\n✅ Análisis automático completado")
        print("💡 Los resultados se usarán automáticamente en el procesamiento")

def analyze_video_auto(video_path: str) -> List[str]:
    """
    Función de conveniencia para obtener argumentos de configuración
    """
    analyzer = VideoAnalyzer()
    config = analyzer.analyze_video_auto(video_path)
    
    # Convertir configuración a argumentos de línea de comandos
    args = []
    
    if config.get("many_faces", False):
        args.append("--many-faces")
    
    args.extend([
        "--similar-face-distance", config.get("similar_face_distance", "0.85"),
        "--reference-face-position", config.get("reference_face_position", "0"),
        "--temp-frame-format", "jpg",
        "--temp-frame-quality", config.get("temp_frame_quality", "100")
    ])
    
    return args

if __name__ == "__main__":
    import sys
    
    analyzer = VideoAnalyzer()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "analyze":
            # Analizar todos los videos en la carpeta
            folder = sys.argv[2] if len(sys.argv) > 2 else "videos_input"
            analyzer.analyze_all_videos_in_folder(folder)
        else:
            # Analizar video específico
            video_path = sys.argv[1]
            if os.path.exists(video_path):
                config = analyzer.analyze_video_auto(video_path)
                analyzer.print_analysis_report(video_path)
            else:
                print(f"❌ El archivo {video_path} no existe")
    else:
        print("🔍 ANALIZADOR AUTOMÁTICO DE VIDEOS")
        print("=" * 40)
        print("Uso:")
        print("  python video_analyzer.py <video_path>     - Analizar video específico")
        print("  python video_analyzer.py analyze          - Analizar todos los videos en videos_input")
        print("  python video_analyzer.py analyze <folder> - Analizar videos en carpeta específica")
