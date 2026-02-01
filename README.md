# Vomee

A Multi-Modal Data Capture System for synchronized Video, mmWave Radar, and Skeleton Data Capturing.

> **Paper**: Vomee -- A Multimodal Sensing Platform for Video, Audio, mmWave and Skeleton Data Capturing

## Overview

Vomee is a real-time multi-modal data capture platform that integrates:

- **TI IWR1843 mmWave Radar** - FMCW radar for range-doppler and range-azimuth sensing
- **Webcam Capture** - Video capture with optional skeleton detection
- **MediaPipe Pose** - Real-time human pose estimation with 33 body landmarks
- **GPU-Accelerated Processing** - CuPy/CUDA-based FFT for radar signal processing

The system provides synchronized recording of all sensor modalities with precise timestamps for multi-modal research applications.

## Features

- **Real-time Visualization**
  - Live camera feed with skeleton overlay
  - Range-Doppler and Range-Azimuth heatmaps
  - FPS and synchronization status display

- **Synchronized Multi-Modal Recording**
  - Raw mmWave ADC data (binary format)
  - Processed radar heatmaps (NumPy arrays)
  - Camera frames (NumPy arrays)
  - Skeleton landmarks (JSON format)
  - Frame-level timestamps with sync metrics

- **GPU-Accelerated Signal Processing**
  - 3D FFT for radar data processing
  - Automatic CPU fallback when GPU unavailable

- **Clean Dashboard Interface**
  - PyQt5-based GUI with modern styling
  - Adjustable skeleton detection toggle
  - Preview and Recording modes

## System Requirements

### Hardware
- TI IWR1843 mmWave Radar (for radar functionality)
- Webcam (for video/skeleton capture)
- NVIDIA GPU with CUDA support (recommended for radar processing)

### Software
- Python 3.8+
- CUDA Toolkit 11.x or 12.x (for GPU acceleration)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/weixijia/Vomee.git
   cd Vomee
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure network settings** (for mmWave radar)
   
   Edit `config.py` to match your network setup:
   ```python
   NETWORK_PARAMS = {
       'pc_ip': '192.168.33.30',       # Your PC's static IP
       'radar_ip': '192.168.33.180',   # Radar ADC IP
       'data_port': 4098,              # UDP data port
       'config_port': 4096             # UDP config port
   }
   ```

## Usage

### Basic Usage

```bash
python main.py
```

### Command-Line Options

| Option | Description |
|--------|-------------|
| `--camera-only` | Run in camera-only mode (no mmWave radar) |
| `--no-camera` | Run without camera (mmWave only) |
| `--skeleton` | Enable skeleton detection on startup |
| `--recording-dir PATH` | Base directory for recordings (default: `./recordings`) |
| `--camera-device ID` | Camera device ID (default: from config) |

### Examples

```bash
# Camera-only mode with skeleton detection
python main.py --camera-only --skeleton

# mmWave radar only
python main.py --no-camera

# Custom recording directory
python main.py --recording-dir /path/to/recordings
```

## Project Structure

```
Vomee/
├── main.py                 # Application entry point
├── config.py               # Configuration parameters
├── requirements.txt        # Python dependencies
├── core/                   # Core capture and processing modules
│   ├── camera_capture.py   # Webcam capture with MediaPipe skeleton
│   ├── mmwave_capture.py   # UDP-based radar data reception
│   └── mmwave_processor.py # GPU-accelerated FFT processing
├── gui/                    # PyQt5 GUI components
│   ├── main_window.py      # Main application window
│   ├── video_widget.py     # Camera display widget
│   ├── heatmap_widget.py   # Radar heatmap display
│   ├── control_panel.py    # Recording controls
│   ├── status_bar.py       # Status display
│   └── styles.py           # UI styling
└── recording/              # Recording and file management
    ├── recorder.py         # Session management
    └── file_writer.py      # Async file I/O
```

## Configuration

### Radar Parameters (`config.py`)

```python
ADC_PARAMS = {
    'chirps': 255,      # Number of chirps per frame
    'rx': 4,            # Number of receive antennas
    'tx': 2,            # Number of transmit antennas
    'samples': 256,     # Range samples per chirp
    'IQ': 2,            # I and Q components
    'bytes': 2          # 16-bit integers
}
```

### Camera Parameters

```python
CAMERA_PARAMS = {
    'device': 0,        # Camera device ID
    'width': 1280,      # Frame width
    'height': 720,      # Frame height
    'fps': 30           # Target frame rate
}
```

### MediaPipe Parameters

```python
MEDIAPIPE_PARAMS = {
    'model_complexity': 1,          # 0=Lite, 1=Full, 2=Heavy
    'min_detection_confidence': 0.5,
    'min_tracking_confidence': 0.5,
    'process_width': 640,           # Downscale for processing
    'process_height': 480
}
```

## Recording Output

Each recording session creates a timestamped directory with the following structure:

```
recordings/
└── session_YYYYMMDD_HHMMSS/
    ├── metadata.json       # Session metadata
    ├── timestamps.csv      # Frame timestamps
    ├── raw/
    │   └── mmwave.bin      # Raw ADC data
    ├── heatmaps/
    │   ├── rd/             # Range-Doppler heatmaps (.npy)
    │   └── ra/             # Range-Azimuth heatmaps (.npy)
    ├── camera/             # Camera frames (.npy)
    └── skeleton/           # Skeleton landmarks (.json)
```

## Dependencies

| Package | Purpose |
|---------|---------|
| numpy | Array operations |
| opencv-python | Camera capture and image processing |
| PyQt5 | GUI framework |
| pyqtgraph | Real-time plotting |
| cupy-cuda11x/12x | GPU-accelerated FFT |
| mediapipe | Pose estimation |

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use Vomee in your research, please cite:

```bibtex
@article{vomee2025,
  title={Vomee: A Multimodal Sensing Platform for Video, Audio, mmWave and Skeleton Data Capturing},
  author={...},
  year={2025}
}
```
