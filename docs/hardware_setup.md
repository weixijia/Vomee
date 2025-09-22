# Hardware Setup Guide

This guide provides detailed instructions for setting up the hardware components of the Vomee multimodal sensing platform.

## Overview

The Vomee platform supports four main sensing modalities:
- **Video**: RGB cameras for visual data capture
- **Audio**: Microphones and audio interfaces for sound recording
- **mmWave**: Millimeter wave radar for motion and presence detection
- **Skeleton**: Depth cameras or RGB cameras for human pose tracking

## Video Setup

### Supported Cameras
- **USB Webcams**: Any USB Video Class (UVC) compatible camera
- **Industrial Cameras**: FLIR, Basler, Allied Vision cameras with USB3 Vision
- **Built-in Cameras**: Laptop/desktop integrated cameras

### Recommended Models
| Model | Resolution | Frame Rate | Price Range |
|-------|------------|------------|-------------|
| Logitech C920 | 1920x1080 | 30fps | $50-80 |
| Logitech BRIO | 3840x2160 | 30fps | $150-200 |
| FLIR Chameleon3 | 2048x1536 | 60fps | $300-500 |

### Setup Steps
1. **Physical Connection**
   - Connect camera to USB 3.0 port (USB 2.0 for lower resolutions)
   - Ensure stable mounting if needed

2. **Driver Installation**
   - Most USB cameras work with standard drivers
   - For industrial cameras, install manufacturer's SDK

3. **Configuration**
   ```python
   video_config = {
       "resolution": (1920, 1080),
       "fps": 30,
       "device_id": 0,  # Camera index
       "exposure": "auto",
       "gain": "auto"
   }
   ```

4. **Testing**
   ```bash
   # Test camera access
   python -c "import cv2; cap = cv2.VideoCapture(0); ret, frame = cap.read(); print('OK' if ret else 'Failed')"
   ```

## Audio Setup

### Audio Interfaces
- **USB Microphones**: Blue Yeti, Audio-Technica ATR2100x
- **Audio Interfaces**: Focusrite Scarlett, Behringer U-Phoria
- **Built-in Audio**: Computer's internal microphone (basic usage)

### Multi-Channel Setup
For advanced audio capture with multiple microphones:

#### Recommended Equipment
| Interface | Channels | Sample Rate | Price Range |
|-----------|----------|-------------|-------------|
| Focusrite Scarlett 2i2 | 2 | 192kHz | $150-200 |
| Focusrite Scarlett 18i20 | 18 | 192kHz | $400-500 |
| Behringer U-Phoria UMC404HD | 4 | 192kHz | $100-150 |

#### Setup Steps
1. **Hardware Connection**
   - Connect microphones to audio interface
   - Connect interface to computer via USB
   - Use XLR cables for professional microphones

2. **Software Configuration**
   ```python
   audio_config = {
       "sample_rate": 44100,
       "channels": 4,  # Number of input channels
       "chunk_size": 1024,
       "device_name": "Scarlett 2i2"  # Optional device selection
   }
   ```

3. **Testing**
   ```bash
   # List available audio devices
   python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"
   ```

## mmWave Radar Setup

### Supported Hardware
- **Texas Instruments IWR Series**
  - IWR6843: 60-64 GHz, long range
  - IWR1843: 76-81 GHz, short range, high resolution
  - IWR1642: 76-81 GHz, automotive grade

### Development Kits
| Kit | Range | Resolution | Price |
|-----|-------|------------|-------|
| IWR6843ISK | 0.4-10m | High | $199 |
| IWR1843BOOST | 0.1-4m | Very High | $199 |
| MMWAVEICBOOST | 0.1-6m | High | $149 |

### Setup Process

#### 1. Hardware Assembly
- Mount radar on evaluation board
- Connect to computer via micro-USB
- Ensure proper antenna orientation

#### 2. Driver Installation
```bash
# Install FTDI drivers for USB-to-UART communication
# Windows: Download from FTDI website
# Linux: Usually included in kernel
# macOS: Install using Homebrew
brew install libftdi
```

#### 3. Port Configuration
```python
mmwave_config = {
    "data_port": "/dev/ttyUSB0",    # Linux/macOS
    "config_port": "/dev/ttyUSB1",  # Linux/macOS
    # "data_port": "COM3",          # Windows
    # "config_port": "COM4",        # Windows
    "baud_rate": 921600
}
```

#### 4. Radar Configuration
The radar needs to be configured with specific parameters:
```python
# Example configuration commands
config_commands = [
    "flushCfg",
    "dfeDataOutputMode 1",
    "channelCfg 15 7 0",
    "adcCfg 2 1",
    "adcbufCfg -1 0 1 1 1",
    "profileCfg 0 77 429 90 1 0 0 70 1 256 5209 0 1 30",
    "chirpCfg 0 0 0 0 0 0 0 1",
    "frameCfg 0 0 16 0 100 1 0",
    "lowPower 0 0",
    "guiMonitor -1 1 1 0 0 0 1",
    "cfarCfg -1 0 2 8 4 3 0 15 1",
    "cfarCfg -1 1 0 4 2 3 1 15 1",
    "multiObjBeamForming -1 1 0.5",
    "clutterRemoval -1 0",
    "calibDcRangeSig -1 0 -5 8 256",
    "extendedMaxVelocity -1 0",
    "sensorStart"
]
```

## Skeleton Tracking Setup

### Option 1: Depth Cameras

#### Intel RealSense D435i
1. **Installation**
   ```bash
   # Install RealSense SDK
   # Ubuntu
   sudo apt-key adv --keyserver keys.gnupg.net --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
   sudo add-apt-repository "deb https://librealsense.ppa.launchpad.net/librealsense/main $(lsb_release -cs) main"
   sudo apt update
   sudo apt install librealsense2-dkms librealsense2-utils librealsense2-dev
   
   # Python bindings
   pip install pyrealsense2
   ```

2. **Testing**
   ```bash
   # Test camera
   realsense-viewer
   ```

#### Azure Kinect DK
1. **Installation**
   ```bash
   # Download Azure Kinect SDK from Microsoft
   # Install following official documentation
   pip install pyk4a
   ```

2. **Configuration**
   ```python
   kinect_config = {
       "color_resolution": "720p",
       "depth_mode": "WFOV_UNBINNED",
       "camera_fps": "30",
       "include_color": True,
       "include_depth": True,
       "include_ir": False
   }
   ```

### Option 2: RGB-based Tracking

#### MediaPipe Setup
```bash
# Install MediaPipe
pip install mediapipe
```

#### OpenPose Setup (Advanced)
```bash
# Download and compile OpenPose
git clone https://github.com/CMU-Perceptual-Computing-Lab/openpose.git
cd openpose
mkdir build && cd build
cmake ..
make -j`nproc`
```

## System Integration

### Multi-Device Synchronization
For precise temporal alignment across devices:

1. **Hardware Sync**: Use external trigger signals when available
2. **Software Sync**: Implement timestamp-based synchronization
3. **NTP Sync**: For distributed setups, use network time protocol

### Power Requirements
- **USB Hub**: Use powered USB 3.0 hub for multiple devices
- **Power Budget**: Calculate total USB power consumption
- **Backup Power**: Consider UPS for critical recordings

### Cable Management
- Use high-quality USB 3.0 cables (max 3m without repeater)
- Organize cables to prevent interference
- Label all connections for easy troubleshooting

## Performance Optimization

### System Settings
```bash
# Linux: Increase USB buffer sizes
echo 1000 | sudo tee /sys/module/usbcore/parameters/usbfs_memory_mb

# Disable power management for USB ports
echo 'SUBSYSTEM=="usb", ATTR{power/autosuspend}="-1"' | sudo tee /etc/udev/rules.d/50-usb-power.rules
```

### Monitoring
- Monitor CPU and memory usage during capture
- Check USB bandwidth utilization
- Verify stable frame rates across all devices

## Troubleshooting

### Common Issues
1. **Device Not Detected**: Check drivers and permissions
2. **Poor Performance**: Reduce resolution/frame rate
3. **Sync Issues**: Verify timestamp accuracy
4. **Data Loss**: Check storage speed and available space

### Diagnostics
```bash
# Check USB devices
lsusb

# Monitor system resources
htop

# Check audio devices
arecord -l

# Test camera capture
v4l2-ctl --list-devices
```

For additional support, consult the [troubleshooting guide](troubleshooting.md) or [contact support](mailto:support@vomee.io).