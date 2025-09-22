"""
Configuration manager for Vomee platform.
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class SensorConfig:
    """Base configuration for sensors."""
    enabled: bool = True
    device_id: Optional[str] = None


@dataclass
class VideoConfig(SensorConfig):
    """Video capture configuration."""
    resolution: tuple = (1920, 1080)
    fps: int = 30
    codec: str = "mp4v"


@dataclass
class AudioConfig(SensorConfig):
    """Audio capture configuration."""
    sample_rate: int = 44100
    channels: int = 2
    chunk_size: int = 1024


@dataclass
class mmWaveConfig(SensorConfig):
    """mmWave radar configuration."""
    device_port: str = "/dev/ttyUSB0"
    config_port: str = "/dev/ttyUSB1"
    range_max: float = 10.0
    velocity_max: float = 5.0


@dataclass
class SkeletonConfig(SensorConfig):
    """Skeleton tracking configuration."""
    tracking_method: str = "mediapipe"
    confidence_threshold: float = 0.5


@dataclass
class SystemConfig:
    """Overall system configuration."""
    output_dir: str = "./output"
    session_name: str = "vomee_session"
    sync_tolerance_ms: float = 1.0
    
    video: VideoConfig = VideoConfig()
    audio: AudioConfig = AudioConfig()
    mmwave: mmWaveConfig = mmWaveConfig()
    skeleton: SkeletonConfig = SkeletonConfig()


class ConfigManager:
    """Manages configuration for the Vomee platform."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path
        self.config = SystemConfig()
        
        if config_path and os.path.exists(config_path):
            self.load_config(config_path)
    
    def load_config(self, config_path: str):
        """Load configuration from file."""
        try:
            with open(config_path, 'r') as f:
                config_dict = json.load(f)
            
            # Update configuration with loaded values
            self._update_config_from_dict(config_dict)
            
        except Exception as e:
            print(f"Failed to load config from {config_path}: {e}")
    
    def save_config(self, config_path: str):
        """Save current configuration to file."""
        try:
            config_dict = asdict(self.config)
            with open(config_path, 'w') as f:
                json.dump(config_dict, f, indent=2)
                
        except Exception as e:
            print(f"Failed to save config to {config_path}: {e}")
    
    def _update_config_from_dict(self, config_dict: Dict[str, Any]):
        """Update configuration from dictionary."""
        # This would recursively update the configuration
        # For now, just a placeholder
        pass
    
    def get_config(self) -> SystemConfig:
        """Get current configuration."""
        return self.config