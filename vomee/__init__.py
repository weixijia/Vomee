"""
Vomee: A Multimodal Sensing Platform

This package provides a comprehensive platform for synchronized multimodal data capture
including video, audio, mmWave radar, and skeleton tracking.
"""

__version__ = "1.0.0"
__author__ = "Vomee Research Team"
__email__ = "contact@vomee.io"

# Import main classes from their respective modules
from .capture_main import VomeeCapture, CaptureConfig
from .processing import DataProcessor
from .utils import SyncManager, ConfigManager
from .visualization import Visualizer

__all__ = [
    "VomeeCapture",
    "CaptureConfig",
    "DataProcessor", 
    "SyncManager",
    "ConfigManager",
    "Visualizer"
]