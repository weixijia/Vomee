"""
Camera Capture Module

Webcam capture with MediaPipe Pose skeleton detection.
"""

import threading
import numpy as np
import cv2
from datetime import datetime
from typing import Tuple, Optional, Dict
import time

import sys
sys.path.append('..')
from config import CAMERA_PARAMS, MEDIAPIPE_PARAMS


def _init_mediapipe():
    """Initialize MediaPipe components."""
    try:
        import mediapipe

        # Try multiple import paths - MediaPipe package structure varies by version
        mp_pose = None
        mp_drawing = None
        mp_drawing_styles = None

        # Method 1: Access through mediapipe.solutions attribute (set by __init__.py)
        if hasattr(mediapipe, 'solutions'):
            try:
                mp_pose = mediapipe.solutions.pose
                mp_drawing = mediapipe.solutions.drawing_utils
                mp_drawing_styles = mediapipe.solutions.drawing_styles
                print(f"[Camera] MediaPipe {mediapipe.__version__} ready (via attribute)")
                return True, mediapipe, mp_pose, mp_drawing, mp_drawing_styles
            except Exception as e:
                print(f"[Camera] solutions attribute failed: {e}")

        # Method 2: Direct import from mediapipe.python.solutions (actual package location)
        try:
            import mediapipe.python.solutions.pose as mp_pose
            import mediapipe.python.solutions.drawing_utils as mp_drawing
            import mediapipe.python.solutions.drawing_styles as mp_drawing_styles
            print(f"[Camera] MediaPipe {mediapipe.__version__} ready (via python.solutions)")
            return True, mediapipe, mp_pose, mp_drawing, mp_drawing_styles
        except ImportError as e:
            print(f"[Camera] python.solutions import failed: {e}")

        # Method 3: Direct import (older versions)
        try:
            import mediapipe.solutions.pose as mp_pose
            import mediapipe.solutions.drawing_utils as mp_drawing
            import mediapipe.solutions.drawing_styles as mp_drawing_styles
            print(f"[Camera] MediaPipe {mediapipe.__version__} ready (direct import)")
            return True, mediapipe, mp_pose, mp_drawing, mp_drawing_styles
        except ImportError as e:
            print(f"[Camera] direct solutions import failed: {e}")

        print("[Camera] MediaPipe solutions not available")
        print("[Camera] Try: pip uninstall mediapipe && pip install mediapipe")
        return False, None, None, None, None

    except ImportError:
        print("[Camera] MediaPipe not installed")
        return False, None, None, None, None
    except Exception as e:
        print(f"[Camera] MediaPipe error: {e}")
        import traceback
        traceback.print_exc()
        return False, None, None, None, None


class CameraCapture(threading.Thread):
    """
    Camera capture with MediaPipe Pose skeleton overlay.
    """

    def __init__(self,
                 device_id: int = None,
                 width: int = None,
                 height: int = None,
                 fps: int = None,
                 enable_skeleton: bool = False):
        threading.Thread.__init__(self, daemon=True)

        self.device_id = device_id if device_id is not None else CAMERA_PARAMS['device']
        self.width = width or CAMERA_PARAMS['width']
        self.height = height or CAMERA_PARAMS['height']
        self.fps = fps or CAMERA_PARAMS['fps']

        self._running = True
        self._lock = threading.Lock()
        self._enable_skeleton = False
        self._frame = None
        self._frame_with_skeleton = None
        self._timestamp = 0.0
        self._landmarks = None
        self._frame_count = 0

        self.cap = None
        self.pose = None

        # MediaPipe components (lazy loaded)
        self._mediapipe_available = False
        self._mp = None
        self._mp_pose = None
        self._mp_drawing = None
        self._mp_drawing_styles = None

        # Init MediaPipe (lazy)
        self._load_mediapipe()

        # Init camera
        self._init_camera()

        # Set skeleton state after init
        if enable_skeleton and self._mediapipe_available and self.pose:
            self._enable_skeleton = True

    def _load_mediapipe(self):
        """Lazy load MediaPipe to avoid import order issues."""
        result = _init_mediapipe()
        self._mediapipe_available = result[0]
        self._mp = result[1]
        self._mp_pose = result[2]
        self._mp_drawing = result[3]
        self._mp_drawing_styles = result[4]

        if self._mediapipe_available:
            self._init_pose()
            print(f"[Camera] Skeleton support: mediapipe={self._mediapipe_available}, pose={self.pose is not None}")
        else:
            print("[Camera] Skeleton support: DISABLED (MediaPipe failed to load)")

    def _init_camera(self):
        """Initialize camera."""
        backends = [
            (cv2.CAP_DSHOW, "DirectShow"),
            (cv2.CAP_MSMF, "MSMF"),
            (cv2.CAP_ANY, "Auto"),
        ]

        for backend, name in backends:
            try:
                self.cap = cv2.VideoCapture(self.device_id, backend)
                if self.cap.isOpened():
                    self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                    self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                    self.cap.set(cv2.CAP_PROP_FPS, self.fps)
                    self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

                    ret, test = self.cap.read()
                    if ret:
                        print(f"[Camera] {name}: {test.shape[1]}x{test.shape[0]}")
                        return
                    self.cap.release()
            except:
                pass

        raise RuntimeError(f"Cannot open camera {self.device_id}")

    def _init_pose(self):
        """Initialize MediaPipe Pose model."""
        try:
            self.pose = self._mp_pose.Pose(
                model_complexity=MEDIAPIPE_PARAMS['model_complexity'],
                min_detection_confidence=MEDIAPIPE_PARAMS['min_detection_confidence'],
                min_tracking_confidence=MEDIAPIPE_PARAMS['min_tracking_confidence'],
                static_image_mode=False,
                enable_segmentation=False
            )
            print("[Camera] MediaPipe Pose ready")
        except Exception as e:
            print(f"[Camera] MediaPipe Pose failed: {e}")
            self.pose = None

    def run(self):
        """Main capture loop."""
        while self._running:
            if not self.cap or not self.cap.isOpened():
                time.sleep(0.1)
                continue

            ret, frame_bgr = self.cap.read()
            if not ret:
                continue

            # Mirror horizontally for natural mirror effect
            frame_bgr = cv2.flip(frame_bgr, 1)

            # Convert BGR -> RGB
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            timestamp = datetime.now().timestamp()

            frame_with_skeleton = frame_rgb.copy()
            landmarks_dict = None

            # Process skeleton if enabled
            if self._enable_skeleton and self.pose and self._mp_drawing:
                # MediaPipe needs RGB
                results = self.pose.process(frame_rgb)

                if results.pose_landmarks:
                    # Draw on BGR image (MediaPipe drawing expects BGR)
                    frame_bgr_draw = frame_bgr.copy()

                    self._mp_drawing.draw_landmarks(
                        frame_bgr_draw,
                        results.pose_landmarks,
                        self._mp_pose.POSE_CONNECTIONS,
                        landmark_drawing_spec=self._mp_drawing_styles.get_default_pose_landmarks_style()
                    )

                    # Convert back to RGB for display
                    frame_with_skeleton = cv2.cvtColor(frame_bgr_draw, cv2.COLOR_BGR2RGB)

                    # Extract landmarks for recording
                    landmarks_dict = self._extract_landmarks(results)

                    if self._frame_count % 90 == 0:
                        print("[Camera] Skeleton detected")

            # Store
            with self._lock:
                self._frame = frame_rgb
                self._frame_with_skeleton = frame_with_skeleton
                self._timestamp = timestamp
                self._landmarks = landmarks_dict
                self._frame_count += 1

    def _extract_landmarks(self, results) -> Dict:
        """Extract landmarks to dict for recording."""
        landmarks = {'landmarks': [], 'visibility': []}

        for lm in results.pose_landmarks.landmark:
            landmarks['landmarks'].append({
                'x': lm.x * self.width,
                'y': lm.y * self.height,
                'z': lm.z,
                'visibility': lm.visibility
            })
            landmarks['visibility'].append(lm.visibility)

        return landmarks

    def get_frame(self) -> Tuple[Optional[np.ndarray], float, Optional[Dict]]:
        """Get frame without skeleton."""
        with self._lock:
            if self._frame is None:
                return None, 0.0, None
            return self._frame.copy(), self._timestamp, self._landmarks

    def get_frame_with_overlay(self) -> Tuple[Optional[np.ndarray], float, Optional[Dict]]:
        """Get frame with skeleton overlay."""
        with self._lock:
            if self._frame is None:
                return None, 0.0, None

            frame = self._frame_with_skeleton if self._enable_skeleton else self._frame
            return frame.copy(), self._timestamp, self._landmarks

    def set_skeleton_enabled(self, enabled: bool):
        """Enable/disable skeleton."""
        with self._lock:
            can_enable = enabled and self._mediapipe_available and self.pose is not None
            self._enable_skeleton = can_enable
            if enabled and not can_enable:
                print(f"[Camera] Skeleton OFF (mediapipe={self._mediapipe_available}, pose={self.pose is not None})")
            else:
                print(f"[Camera] Skeleton {'ON' if can_enable else 'OFF'}")

    def is_skeleton_enabled(self) -> bool:
        return self._enable_skeleton

    def stop(self):
        """Stop capture."""
        self._running = False
        if self.pose:
            try:
                self.pose.close()
            except ValueError:
                pass  # Already closed
        if self.cap:
            self.cap.release()

    @property
    def is_running(self) -> bool:
        return self._running and self.is_alive()

    @property
    def is_ready(self) -> bool:
        with self._lock:
            return self._frame is not None
