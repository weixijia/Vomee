"""
Video capture module for Vomee platform.
"""

import cv2
import numpy as np
from typing import Optional, Tuple, Any


class VideoCapture:
    """Video capture handler using OpenCV."""
    
    def __init__(self, resolution: Tuple[int, int] = (1920, 1080), fps: int = 30, device_id: int = 0):
        """
        Initialize video capture.
        
        Args:
            resolution: Video resolution (width, height)
            fps: Frames per second
            device_id: Camera device ID
        """
        self.resolution = resolution
        self.fps = fps
        self.device_id = device_id
        self.cap = None
        
    def start(self) -> bool:
        """Start video capture."""
        try:
            self.cap = cv2.VideoCapture(self.device_id)
            if not self.cap.isOpened():
                return False
                
            # Set capture properties
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.cap.set(cv2.CAP_PROP_FPS, self.fps)
            
            return True
        except Exception as e:
            print(f"Failed to start video capture: {e}")
            return False
    
    def capture(self) -> Optional[np.ndarray]:
        """Capture a single frame."""
        if self.cap is None:
            return None
            
        ret, frame = self.cap.read()
        if ret:
            return frame
        return None
    
    def stop(self):
        """Stop video capture."""
        if self.cap:
            self.cap.release()
            self.cap = None