"""
Main capture module for Vomee multimodal sensing platform.

This module provides the core VomeeCapture class that orchestrates
synchronized data collection across multiple sensing modalities.
"""

import time
import threading
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

from .capture.video_capture import VideoCapture
from .capture.audio_capture import AudioCapture  
from .capture.mmwave_capture import mmWaveCapture
from .capture.skeleton_capture import SkeletonCapture
from .utils.sync_manager import SyncManager
from .utils.config_manager import ConfigManager


@dataclass
class CaptureConfig:
    """Configuration for capture session."""
    video_enabled: bool = True
    audio_enabled: bool = True
    mmwave_enabled: bool = True
    skeleton_enabled: bool = True
    
    video_resolution: tuple = (1920, 1080)
    video_fps: int = 30
    audio_sample_rate: int = 44100
    audio_channels: int = 2
    
    sync_tolerance_ms: float = 1.0
    output_format: str = "hdf5"


class VomeeCapture:
    """
    Main class for coordinating multimodal data capture.
    
    This class manages multiple sensor inputs and ensures synchronized
    data collection across video, audio, mmWave, and skeleton modalities.
    """
    
    def __init__(self, config: Optional[CaptureConfig] = None):
        """
        Initialize the Vomee capture system.
        
        Args:
            config: Configuration object with capture parameters
        """
        self.config = config or CaptureConfig()
        self.sync_manager = SyncManager(tolerance_ms=self.config.sync_tolerance_ms)
        
        # Initialize sensors
        self.sensors = {}
        self._initialize_sensors()
        
        # State management
        self.is_recording = False
        self.capture_thread = None
        self.data_buffer = []
        
    def _initialize_sensors(self):
        """Initialize all enabled sensors."""
        if self.config.video_enabled:
            self.sensors['video'] = VideoCapture(
                resolution=self.config.video_resolution,
                fps=self.config.video_fps
            )
            
        if self.config.audio_enabled:
            self.sensors['audio'] = AudioCapture(
                sample_rate=self.config.audio_sample_rate,
                channels=self.config.audio_channels
            )
            
        if self.config.mmwave_enabled:
            self.sensors['mmwave'] = mmWaveCapture()
            
        if self.config.skeleton_enabled:
            self.sensors['skeleton'] = SkeletonCapture()
    
    def start(self) -> bool:
        """
        Start the capture system.
        
        Returns:
            bool: True if all sensors started successfully
        """
        try:
            # Start sync manager
            self.sync_manager.start()
            
            # Start all sensors
            for sensor_name, sensor in self.sensors.items():
                if not sensor.start():
                    raise RuntimeError(f"Failed to start {sensor_name} sensor")
                    
            print("Vomee capture system started successfully")
            return True
            
        except Exception as e:
            print(f"Failed to start capture system: {e}")
            return False
    
    def record(self, duration: Optional[float] = None) -> Dict[str, Any]:
        """
        Start recording data from all sensors.
        
        Args:
            duration: Recording duration in seconds (None for manual stop)
            
        Returns:
            Dict containing captured data from all sensors
        """
        if self.is_recording:
            raise RuntimeError("Recording already in progress")
            
        self.is_recording = True
        self.data_buffer = []
        
        # Start recording thread
        self.capture_thread = threading.Thread(
            target=self._capture_loop,
            args=(duration,)
        )
        self.capture_thread.start()
        
        if duration:
            # Wait for recording to complete
            self.capture_thread.join()
            return self.get_captured_data()
        
        return {}
    
    def _capture_loop(self, duration: Optional[float]):
        """Main capture loop running in separate thread."""
        start_time = time.time()
        
        while self.is_recording:
            # Get synchronized timestamp
            timestamp = self.sync_manager.get_timestamp()
            
            # Capture from all sensors
            frame_data = {'timestamp': timestamp}
            
            for sensor_name, sensor in self.sensors.items():
                try:
                    data = sensor.capture()
                    if data is not None:
                        frame_data[sensor_name] = data
                except Exception as e:
                    print(f"Error capturing from {sensor_name}: {e}")
            
            self.data_buffer.append(frame_data)
            
            # Check duration
            if duration and (time.time() - start_time) >= duration:
                break
                
            # Small delay to prevent excessive CPU usage
            time.sleep(0.001)
    
    def stop(self) -> Dict[str, Any]:
        """
        Stop recording and return captured data.
        
        Returns:
            Dict containing all captured data
        """
        if not self.is_recording:
            return {}
            
        self.is_recording = False
        
        if self.capture_thread:
            self.capture_thread.join()
            
        return self.get_captured_data()
    
    def get_captured_data(self) -> Dict[str, Any]:
        """Get the captured data buffer."""
        return {
            'frames': self.data_buffer,
            'metadata': {
                'config': self.config,
                'capture_time': datetime.now().isoformat(),
                'num_frames': len(self.data_buffer)
            }
        }
    
    def save(self, data: Dict[str, Any], output_path: str):
        """
        Save captured data to file.
        
        Args:
            data: Data dictionary from capture
            output_path: Path to save the data
        """
        # Implementation would depend on the chosen format
        # For now, just a placeholder
        print(f"Saving data to {output_path}")
        # TODO: Implement actual saving logic
    
    def shutdown(self):
        """Gracefully shutdown the capture system."""
        if self.is_recording:
            self.stop()
            
        # Stop all sensors
        for sensor in self.sensors.values():
            sensor.stop()
            
        # Stop sync manager
        self.sync_manager.stop()
        
        print("Vomee capture system shutdown complete")