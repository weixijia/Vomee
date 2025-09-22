"""
Audio capture module for Vomee platform.
"""

import pyaudio
import numpy as np
from typing import Optional, Any


class AudioCapture:
    """Audio capture handler using PyAudio."""
    
    def __init__(self, sample_rate: int = 44100, channels: int = 2, chunk_size: int = 1024):
        """
        Initialize audio capture.
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels
            chunk_size: Audio buffer chunk size
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.audio = None
        self.stream = None
        
    def start(self) -> bool:
        """Start audio capture."""
        try:
            self.audio = pyaudio.PyAudio()
            self.stream = self.audio.open(
                format=pyaudio.paFloat32,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size
            )
            return True
        except Exception as e:
            print(f"Failed to start audio capture: {e}")
            return False
    
    def capture(self) -> Optional[np.ndarray]:
        """Capture audio chunk."""
        if self.stream is None:
            return None
            
        try:
            data = self.stream.read(self.chunk_size)
            audio_data = np.frombuffer(data, dtype=np.float32)
            return audio_data
        except Exception as e:
            print(f"Audio capture error: {e}")
            return None
    
    def stop(self):
        """Stop audio capture."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
            
        if self.audio:
            self.audio.terminate()
            self.audio = None