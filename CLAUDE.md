# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Main Execution
- `python run.py` - Main entry point, delegates to roop.core
- `python batch_processor.py` - Batch process multiple videos with memory optimization
- `python colab_batch_processor.py` - Colab-specific batch processor
- `python run_simple.py` - Simplified execution with predefined settings
- `python run_optimized.py` - Optimized execution with memory management

### Setup and Configuration
- `python setup_folders.py` - Create necessary folder structure (source/, videos_input/, videos_output/)
- `python install_analyzer.py` - Install dependencies for automatic video analysis

### Diagnostic Tools
- `python test_cuda.py` - Test CUDA availability and GPU configuration
- `python debug_cuda.py` - Debug CUDA issues and GPU memory
- `python monitor_gpu.py` - Monitor GPU usage during processing
- `python show_config.py` - Display current configuration and available parameters

### Analysis Tools
- `python video_analyzer.py <video_file>` - Analyze specific video for face detection parameters
- `python face_config.py analyze` - Analyze all videos in videos_input/ directory

### Memory Management
- `python clear_cache.py` - Clear system and GPU memory cache

## Project Architecture

### Core Components
- **roop/core.py** - Main processing engine and argument parsing
- **roop/processors/frame/** - Frame processing modules (face_swapper, face_enhancer)
- **roop/face_analyser.py** - Face detection and analysis
- **roop/memory_optimizer.py** - Memory optimization utilities
- **roop/utilities.py** - Common utilities for file handling and video processing

### Processing Scripts
The project has evolved to include multiple processing approaches:
- **Standard processing** (`run.py`) - Basic single video processing
- **Batch processing** (`batch_processor.py`) - Optimized for multiple videos with automatic memory management
- **Automatic analysis** - Intelligent parameter detection based on video characteristics
- **Memory optimization** - Advanced memory management for large videos and limited RAM systems

### Folder Structure
```
roop2/
├── source/              # Source images (faces to swap)
├── videos_input/        # Input videos to process
├── videos_output/       # Processed output videos
├── roop/               # Main package
│   ├── processors/     # Frame processors
│   ├── core.py        # Main processing logic
│   └── ...
└── *.py               # Various processing and utility scripts
```

### Memory Management Features
The project includes sophisticated memory optimization:
- Automatic batch size adjustment based on available memory
- Real-time memory monitoring during processing
- GPU memory management for CUDA execution
- Fallback configurations for low-memory systems

### Key Arguments
- `--memory-optimization` - Enable memory optimization features
- `--batch-size <n>` - Control processing batch size (1-5)
- `--max-memory <GB>` - Limit maximum memory usage
- `--execution-threads <n>` - Control number of execution threads
- `--many-faces` - Process multiple faces in video
- `--similar-face-distance <float>` - Face matching threshold (0.75-0.85)

### Automatic Configuration
The project includes intelligent configuration based on video analysis:
- Automatic face detection and parameter optimization
- System memory profiling for optimal settings
- Video quality analysis for appropriate processing parameters

### Development Notes
- Project follows functional programming patterns (no OOP as per CONTRIBUTING.md)
- Uses ONNX Runtime with CUDA for GPU acceleration
- Memory optimization is critical for processing large videos
- Multiple processing scripts provide different optimization levels