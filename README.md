# Vomee: A Multimodal Sensing Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![MobiCom 2025](https://img.shields.io/badge/MobiCom-2025-green.svg)](https://sigmobile.org/mobicom/2025/)

**Official repository for the MobiCom 2025 paper: "Vomee -- A Multimodal Sensing Platform for Video, Audio, mmWave and Skeleton Data Capturing"**

## Overview

Vomee is a comprehensive multimodal sensing platform designed for synchronized data collection across multiple modalities:
- 📹 **Video** - High-resolution camera capture
- 🔊 **Audio** - Multi-channel audio recording
- 📡 **mmWave** - Millimeter wave radar sensing
- 🦴 **Skeleton** - Real-time skeleton tracking

This platform enables researchers and developers to collect rich, synchronized multimodal datasets for various applications including human activity recognition, gesture detection, and environmental sensing.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- CUDA-capable GPU (recommended)
- Compatible hardware sensors (see [Hardware Requirements](#hardware-requirements))

### Installation

```bash
# Clone the repository
git clone https://github.com/weixijia/Vomee.git
cd Vomee

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Basic Usage

```python
from vomee import VomeeCapture

# Initialize the platform
capture = VomeeCapture(
    video=True,
    audio=True,
    mmwave=True,
    skeleton=True
)

# Start synchronized capture
capture.start()

# Capture for 10 seconds
capture.record(duration=10)

# Stop and save data
data = capture.stop()
capture.save(data, 'output/session_001')
```

## 📊 Features

### Synchronized Data Capture
- **Temporal Alignment**: Precise timestamp synchronization across all modalities
- **Real-time Processing**: Live data streaming and processing capabilities
- **Flexible Configuration**: Customizable sensor parameters and recording settings

### Data Export Formats
- **Video**: MP4, AVI with configurable resolution and frame rates
- **Audio**: WAV, MP3 with multi-channel support
- **mmWave**: HDF5 format with radar point clouds and processing metadata
- **Skeleton**: JSON format with 3D joint coordinates and confidence scores

### Platform Integration
- **Cross-platform Support**: Windows, Linux, macOS
- **API Integration**: RESTful API for remote control and monitoring
- **Real-time Visualization**: Live data monitoring and visualization tools

## 🔧 Hardware Requirements

### Minimum Requirements
- **Camera**: USB 3.0 or higher (1080p @ 30fps)
- **Microphone**: USB or 3.5mm audio input
- **mmWave Radar**: Texas Instruments IWR series or equivalent
- **Depth Camera**: Intel RealSense, Azure Kinect, or similar

### Recommended Setup
- **Camera**: 4K capable webcam or industrial camera
- **Audio**: Multi-channel audio interface (≥4 channels)
- **mmWave**: TI IWR6843 or mmWave DevKit
- **Skeleton Tracking**: Azure Kinect DK or Intel RealSense D435i

## 📚 Documentation

- [Installation Guide](docs/installation.md)
- [Hardware Setup](docs/hardware_setup.md)
- [API Reference](docs/api_reference.md)
- [Data Format Specification](docs/data_formats.md)
- [Examples and Tutorials](docs/examples/)

## 🎯 Use Cases

### Research Applications
- **Human Activity Recognition**: Multimodal dataset collection for HAR research
- **Gesture Recognition**: Combined video-mmWave gesture analysis
- **Environmental Sensing**: Multi-sensor environmental monitoring
- **Social Interaction Analysis**: Group activity and interaction studies

### Industry Applications
- **Smart Home**: Presence detection and activity monitoring
- **Healthcare**: Patient monitoring and rehabilitation assessment
- **Security**: Multi-modal surveillance and intrusion detection
- **Automotive**: In-cabin sensing and driver monitoring

## 📖 Citation

If you use Vomee in your research, please cite our paper:

```bibtex
@inproceedings{vomee2025,
    title={Vomee: A Multimodal Sensing Platform for Video, Audio, mmWave and Skeleton Data Capturing},
    author={[Author Names]},
    booktitle={Proceedings of the 30th Annual International Conference on Mobile Computing and Networking},
    series={MobiCom '24},
    year={2025},
    publisher={ACM},
    doi={[DOI]},
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- MobiCom 2025 Program Committee
- [Institution/Lab Name]
- Hardware partners and sponsors

## 📧 Contact

- **Primary Contact**: [Your Name] - [email@domain.com]
- **Project Homepage**: [https://weixijia.github.io/Vomee](https://weixijia.github.io/Vomee)
- **Issues**: [GitHub Issues](https://github.com/weixijia/Vomee/issues)

---

<div align="center">
    <b>⭐ Star this repository if you find it useful! ⭐</b>
</div>
