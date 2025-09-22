# Installation Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, Ubuntu 18.04+, macOS 10.14+
- **Python**: 3.8 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 5GB free space for installation and data capture
- **USB Ports**: Multiple USB 3.0 ports for sensors

### Hardware Requirements

#### Video Capture
- USB 3.0 camera or webcam
- Minimum resolution: 1080p @ 30fps
- Recommended: 4K capable camera

#### Audio Capture
- USB microphone or audio interface
- Minimum: Single channel input
- Recommended: Multi-channel audio interface (4+ channels)

#### mmWave Radar
- Texas Instruments IWR series radar
- Supported models: IWR6843, IWR1843, IWR1642
- USB to UART bridge for serial communication

#### Skeleton Tracking
- Depth camera: Intel RealSense D435i, Azure Kinect DK, or compatible
- Alternative: Standard RGB camera with software-based tracking

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/weixijia/Vomee.git
cd Vomee
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv vomee_env
source vomee_env/bin/activate  # On Windows: vomee_env\Scripts\activate

# Or using conda
conda create -n vomee python=3.8
conda activate vomee
```

### 3. Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install optional dependencies based on your setup
pip install -e .[skeleton]  # For skeleton tracking
pip install -e .[mmwave]    # For mmWave processing
pip install -e .[audio]     # For advanced audio processing
pip install -e .[web]       # For web interface
```

### 4. Hardware Setup

#### Video Camera
1. Connect USB camera to USB 3.0 port
2. Test camera functionality:
```bash
python -c "import cv2; cap = cv2.VideoCapture(0); print('Camera OK' if cap.isOpened() else 'Camera Error')"
```

#### Audio Input
1. Connect microphone or audio interface
2. Test audio input:
```bash
python -c "import pyaudio; p = pyaudio.PyAudio(); print(f'Audio devices: {p.get_device_count()}')"
```

#### mmWave Radar (Optional)
1. Connect mmWave device via USB
2. Install device drivers if required
3. Check serial ports:
```bash
# Linux/macOS
ls /dev/tty*

# Windows
# Check Device Manager for COM ports
```

#### Depth Camera (Optional)
1. Install camera SDK:
   - **Intel RealSense**: Download from [Intel RealSense SDK](https://www.intelrealsense.com/sdk-2/)
   - **Azure Kinect**: Download from [Azure Kinect SDK](https://docs.microsoft.com/en-us/azure/kinect-dk/)
2. Connect camera and test

### 5. Verify Installation

Run the verification script:
```bash
python examples/verify_installation.py
```

This will test all components and provide a status report.

## Configuration

### Basic Configuration
Create a configuration file `config.json`:

```json
{
  "video": {
    "enabled": true,
    "resolution": [1920, 1080],
    "fps": 30,
    "device_id": 0
  },
  "audio": {
    "enabled": true,
    "sample_rate": 44100,
    "channels": 2
  },
  "mmwave": {
    "enabled": false,
    "device_port": "/dev/ttyUSB0",
    "config_port": "/dev/ttyUSB1"
  },
  "skeleton": {
    "enabled": true,
    "tracking_method": "mediapipe"
  }
}
```

### Advanced Configuration
For advanced users, see [Configuration Reference](configuration.md).

## Troubleshooting

### Common Issues

#### Camera Not Detected
- Check USB connection and drivers
- Try different USB ports
- Verify camera permissions on macOS/Linux

#### Audio Issues
- Check audio device permissions
- Verify correct audio input device
- Test with different sample rates

#### mmWave Connection Problems
- Verify serial port permissions
- Check device drivers
- Ensure correct baud rate

#### Performance Issues
- Close unnecessary applications
- Increase system RAM
- Use SSD for data storage
- Lower capture resolution/frame rate

### Getting Help

1. Check the [FAQ](faq.md)
2. Search [existing issues](https://github.com/weixijia/Vomee/issues)
3. Create a new issue with:
   - System information
   - Error messages
   - Configuration files
   - Steps to reproduce

## Next Steps

After successful installation:
1. Run the [basic example](../examples/basic_capture.py)
2. Explore [advanced examples](../examples/)
3. Read the [API documentation](api_reference.md)
4. Check out [use cases](use_cases.md)