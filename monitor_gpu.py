#!/usr/bin/env python3

import time
import subprocess
import threading
import psutil

def monitor_gpu_usage():
    """Monitorea el uso de GPU en tiempo real"""
    print("🔍 Monitoreando uso de GPU...")
    print("=" * 50)
    
    def get_gpu_info():
        try:
            # Usar nvidia-smi para obtener info de GPU
            result = subprocess.run(['nvidia-smi', '--query-gpu=memory.used,memory.total,utilization.gpu', '--format=csv,noheader,nounits'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                for line in lines:
                    if line.strip():
                        used, total, util = line.split(', ')
                        return {
                            'memory_used': int(used),
                            'memory_total': int(total),
                            'utilization': int(util)
                        }
        except Exception as e:
            print(f"Error obteniendo info GPU: {e}")
        return None
    
    def get_system_memory():
        memory = psutil.virtual_memory()
        return {
            'used': memory.used / (1024**3),  # GB
            'total': memory.total / (1024**3),  # GB
            'percent': memory.percent
        }
    
    print("⏱️  Monitoreo iniciado. Presiona Ctrl+C para detener.")
    print("=" * 50)
    
    try:
        while True:
            gpu_info = get_gpu_info()
            sys_memory = get_system_memory()
            
            if gpu_info:
                gpu_memory_gb = gpu_info['memory_used'] / 1024
                gpu_total_gb = gpu_info['memory_total'] / 1024
                gpu_percent = (gpu_info['memory_used'] / gpu_info['memory_total']) * 100
                
                print(f"🖥️  GPU: {gpu_memory_gb:.1f}GB / {gpu_total_gb:.1f}GB ({gpu_percent:.1f}%) | Util: {gpu_info['utilization']}%")
            else:
                print("🖥️  GPU: No disponible")
            
            print(f"💾 RAM: {sys_memory['used']:.1f}GB / {sys_memory['total']:.1f}GB ({sys_memory['percent']:.1f}%)")
            print("-" * 50)
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n⏹️  Monitoreo detenido.")

if __name__ == "__main__":
    monitor_gpu_usage() 