#!/usr/bin/env python3
"""
Analizador automático de videos para configurar parámetros óptimos de detección de rostros
"""

import cv2
import numpy as np
from pathlib import Path
import subprocess
import json
import os

class VideoAnalyzer:
    def __init__(self):
        self.analysis_results = {}
    
    def analyze_video(self, video_path):
        """
        Analiza un video y determina la configuración óptima
        """
        print(f"🔍 Analizando video: {Path(video_path).name}")
        
        # Obtener información básica del video
        video_info = self.get_video_info(video_path)
        
        # Analizar frames para detectar rostros
        face_analysis = self.analyze_faces(video_path)
        
        # Analizar calidad del video
        quality_analysis = self.analyze_quality(video_path)
        
        # Combinar análisis
        analysis = {
            "video_info": video_info,
            "face_analysis": face_analysis,
            "quality_analysis": quality_analysis,
            "recommended_config": self.get_recommended_config(video_info, face_analysis, quality_analysis)
        }
        
        self.analysis_results[video_path] = analysis
        return analysis
    
    def get_video_info(self, video_path):
        """Obtiene información básica del video usando ffprobe"""
        try:
            cmd = [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            data = json.loads(result.stdout)
            
            # Extraer información relevante
            format_info = data.get("format", {})
            video_stream = None
            
            for stream in data.get("streams", []):
                if stream.get("codec_type") == "video":
                    video_stream = stream
                    break
            
            return {
                "duration": float(format_info.get("duration", 0)),
                "width": int(video_stream.get("width", 0)) if video_stream else 0,
                "height": int(video_stream.get("height", 0)) if video_stream else 0,
                "fps": eval(video_stream.get("r_frame_rate", "0/1")) if video_stream else 0,
                "bitrate": int(format_info.get("bit_rate", 0)),
                "size_mb": float(format_info.get("size", 0)) / (1024 * 1024)
            }
        except Exception as e:
            print(f"⚠️  Error obteniendo información del video: {e}")
            return {}
    
    def analyze_faces(self, video_path):
        """Analiza la presencia y características de rostros en el video"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return {"error": "No se pudo abrir el video"}
        
        # Cargar detector de rostros
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps > 0 else 0
        
        # Analizar frames espaciados
        sample_frames = min(50, total_frames)  # Máximo 50 frames
        frame_interval = max(1, total_frames // sample_frames)
        
        face_counts = []
        face_sizes = []
        face_positions = []
        
        print(f"   📊 Analizando {sample_frames} frames de {total_frames} totales...")
        
        for i in range(0, total_frames, frame_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                continue
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detectar rostros
            faces = face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.1, 
                minNeighbors=5, 
                minSize=(30, 30)
            )
            
            face_counts.append(len(faces))
            
            # Analizar cada rostro detectado
            for (x, y, w, h) in faces:
                # Tamaño relativo del rostro
                face_size = (w * h) / (frame.shape[0] * frame.shape[1])
                face_sizes.append(face_size)
                
                # Posición del rostro
                center_x = x + w/2
                center_y = y + h/2
                face_positions.append((center_x, center_y))
        
        cap.release()
        
        # Calcular estadísticas
        avg_faces_per_frame = np.mean(face_counts) if face_counts else 0
        max_faces_per_frame = max(face_counts) if face_counts else 0
        avg_face_size = np.mean(face_sizes) if face_sizes else 0
        min_face_size = min(face_sizes) if face_sizes else 0
        
        return {
            "avg_faces_per_frame": avg_faces_per_frame,
            "max_faces_per_frame": max_faces_per_frame,
            "avg_face_size": avg_face_size,
            "min_face_size": min_face_size,
            "total_frames_analyzed": len(face_counts),
            "frames_with_faces": sum(1 for count in face_counts if count > 0),
            "duration_seconds": duration
        }
    
    def analyze_quality(self, video_path):
        """Analiza la calidad del video"""
        video_info = self.get_video_info(video_path)
        
        if not video_info:
            return {"quality_level": "unknown"}
        
        width = video_info.get("width", 0)
        height = video_info.get("height", 0)
        bitrate = video_info.get("bitrate", 0)
        size_mb = video_info.get("size_mb", 0)
        
        # Determinar calidad basada en resolución
        if width >= 1920 and height >= 1080:
            resolution_quality = "high"
        elif width >= 1280 and height >= 720:
            resolution_quality = "medium"
        else:
            resolution_quality = "low"
        
        # Determinar calidad basada en bitrate
        if bitrate > 5000000:  # 5 Mbps
            bitrate_quality = "high"
        elif bitrate > 2000000:  # 2 Mbps
            bitrate_quality = "medium"
        else:
            bitrate_quality = "low"
        
        # Calidad general
        if resolution_quality == "high" and bitrate_quality == "high":
            overall_quality = "high"
        elif resolution_quality == "low" or bitrate_quality == "low":
            overall_quality = "low"
        else:
            overall_quality = "medium"
        
        return {
            "resolution": f"{width}x{height}",
            "resolution_quality": resolution_quality,
            "bitrate_kbps": bitrate // 1000 if bitrate else 0,
            "bitrate_quality": bitrate_quality,
            "size_mb": size_mb,
            "overall_quality": overall_quality
        }
    
    def get_recommended_config(self, video_info, face_analysis, quality_analysis):
        """Genera configuración recomendada basada en el análisis"""
        config = {
            "similar_face_distance": "0.85",
            "reference_face_position": "0",
            "temp_frame_quality": "100",
            "many_faces": False,
            "reasoning": []
        }
        
        # Configurar basado en número de rostros
        avg_faces = face_analysis.get("avg_faces_per_frame", 0)
        max_faces = face_analysis.get("max_faces_per_frame", 0)
        
        if max_faces > 1:
            config["many_faces"] = True
            config["similar_face_distance"] = "0.80"
            config["reasoning"].append("Múltiples rostros detectados")
        
        # Configurar basado en tamaño de rostros
        avg_face_size = face_analysis.get("avg_face_size", 0)
        min_face_size = face_analysis.get("min_face_size", 0)
        
        if avg_face_size < 0.01:  # Rostros muy pequeños
            config["similar_face_distance"] = "0.75"
            config["temp_frame_quality"] = "100"
            config["reasoning"].append("Rostros pequeños detectados")
        elif avg_face_size > 0.1:  # Rostros muy grandes
            config["similar_face_distance"] = "0.90"
            config["reasoning"].append("Rostros grandes detectados")
        
        # Configurar basado en calidad del video
        quality = quality_analysis.get("overall_quality", "medium")
        
        if quality == "low":
            config["similar_face_distance"] = "0.75"
            config["temp_frame_quality"] = "90"
            config["reasoning"].append("Video de baja calidad")
        elif quality == "high":
            config["temp_frame_quality"] = "100"
            config["reasoning"].append("Video de alta calidad")
        
        # Configurar basado en duración
        duration = face_analysis.get("duration_seconds", 0)
        if duration > 300:  # Más de 5 minutos
            config["temp_frame_quality"] = "95"  # Reducir ligeramente para videos largos
            config["reasoning"].append("Video largo detectado")
        
        return config
    
    def print_analysis_report(self, video_path):
        """Imprime un reporte detallado del análisis"""
        if video_path not in self.analysis_results:
            print(f"❌ No hay análisis disponible para {video_path}")
            return
        
        analysis = self.analysis_results[video_path]
        video_info = analysis["video_info"]
        face_analysis = analysis["face_analysis"]
        quality_analysis = analysis["quality_analysis"]
        config = analysis["recommended_config"]
        
        print(f"\n📊 REPORTE DE ANÁLISIS: {Path(video_path).name}")
        print("=" * 60)
        
        # Información del video
        print("📹 INFORMACIÓN DEL VIDEO:")
        print(f"   • Resolución: {quality_analysis.get('resolution', 'N/A')}")
        print(f"   • Duración: {face_analysis.get('duration_seconds', 0):.1f} segundos")
        print(f"   • FPS: {video_info.get('fps', 0):.1f}")
        print(f"   • Tamaño: {quality_analysis.get('size_mb', 0):.1f} MB")
        print(f"   • Calidad: {quality_analysis.get('overall_quality', 'N/A')}")
        
        # Análisis de rostros
        print("\n👥 ANÁLISIS DE ROSTROS:")
        print(f"   • Rostros promedio por frame: {face_analysis.get('avg_faces_per_frame', 0):.2f}")
        print(f"   • Máximo rostros en un frame: {face_analysis.get('max_faces_per_frame', 0)}")
        print(f"   • Tamaño promedio de rostros: {face_analysis.get('avg_face_size', 0):.4f}")
        print(f"   • Frames con rostros: {face_analysis.get('frames_with_faces', 0)}/{face_analysis.get('total_frames_analyzed', 0)}")
        
        # Configuración recomendada
        print("\n⚙️  CONFIGURACIÓN RECOMENDADA:")
        for key, value in config.items():
            if key != "reasoning":
                print(f"   • {key}: {value}")
        
        if config["reasoning"]:
            print("\n💡 RAZONES:")
            for reason in config["reasoning"]:
                print(f"   • {reason}")
        
        print("\n" + "=" * 60)

def analyze_video_auto(video_path):
    """Función simple para análisis automático"""
    analyzer = VideoAnalyzer()
    analysis = analyzer.analyze_video(video_path)
    analyzer.print_analysis_report(video_path)
    return analysis["recommended_config"]

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        if Path(video_path).exists():
            analyze_video_auto(video_path)
        else:
            print(f"❌ El archivo {video_path} no existe")
    else:
        print("Uso: python video_analyzer.py <ruta_del_video>") 