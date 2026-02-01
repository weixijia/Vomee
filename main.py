"""
Vomee Multi-Modal Data Capture System

Main application entry point. Integrates TI IWR1843 mmWave radar,
webcam with optional MediaPipe skeleton overlay, and synchronized
recording capabilities.

Usage:
    python main.py
"""

import sys
import time
import argparse
from pathlib import Path

# IMPORTANT: Import MediaPipe FIRST before any GPU libraries (CuPy, PyTorch, etc.)
# This prevents module loading conflicts
try:
    import mediapipe
    # Pre-load solutions via attribute access (triggers __init__.py import)
    _ = mediapipe.solutions.pose
    _ = mediapipe.solutions.drawing_utils
    _ = mediapipe.solutions.drawing_styles
    print(f"[Init] MediaPipe {mediapipe.__version__} pre-loaded")
except ImportError as e:
    print(f"[Init] MediaPipe not installed: {e}")
except AttributeError as e:
    print(f"[Init] MediaPipe solutions not available: {e}")

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def setup_high_dpi():
    """Enable high DPI scaling for PyQt5."""
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Vomee Multi-Modal Data Capture System'
    )
    parser.add_argument(
        '--camera-only',
        action='store_true',
        help='Run in camera-only mode (no mmWave radar)'
    )
    parser.add_argument(
        '--no-camera',
        action='store_true',
        help='Run without camera (mmWave only)'
    )
    parser.add_argument(
        '--skeleton',
        action='store_true',
        help='Enable skeleton detection on startup'
    )
    parser.add_argument(
        '--recording-dir',
        type=str,
        default='./recordings',
        help='Base directory for recordings (default: ./recordings)'
    )
    parser.add_argument(
        '--camera-device',
        type=int,
        default=None,
        help='Camera device ID (default: from config, usually 0)'
    )
    return parser.parse_args()


def main():
    """Main application entry point."""
    args = parse_args()

    # Setup high DPI before creating QApplication
    setup_high_dpi()

    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Vomee")
    app.setOrganizationName("Vomee")

    # Import components
    from gui.main_window import MainWindow
    from core.mmwave_processor import MmWaveProcessor
    from recording.recorder import Recorder
    from recording.file_writer import FileWriter

    # Create main window
    window = MainWindow()

    # Initialize mmWave processor
    processor = MmWaveProcessor()
    window.set_mmwave_processor(processor)

    # Initialize recorder and file writer
    recorder = Recorder(args.recording_dir)
    window.set_recorder(recorder)

    file_writer = FileWriter()
    file_writer.start()
    window.set_file_writer(file_writer)

    # Initialize mmWave capture (unless camera-only mode)
    mmwave_capture = None
    if not args.camera_only:
        try:
            from core.mmwave_capture import MmWaveCapture
            mmwave_capture = MmWaveCapture()
            mmwave_capture.start()
            window.set_mmwave_capture(mmwave_capture)
            print("mmWave capture initialized")
        except Exception as e:
            print(f"Warning: Could not initialize mmWave capture: {e}")
            print("Running in camera-only mode")

    # Initialize camera capture (unless no-camera mode)
    camera_capture = None
    if not args.no_camera:
        try:
            print("Initializing camera capture...")
            from core.camera_capture import CameraCapture
            camera_capture = CameraCapture(
                device_id=args.camera_device,
                enable_skeleton=True  # Skeleton enabled by default
            )
            camera_capture.start()
            window.set_camera_capture(camera_capture)

            # Wait for camera to be ready
            timeout = 5.0
            start = time.time()
            while not camera_capture.is_ready and time.time() - start < timeout:
                time.sleep(0.1)

            if camera_capture.is_ready:
                print("Camera capture initialized successfully")
            else:
                print("Warning: Camera not ready within timeout")

        except Exception as e:
            import traceback
            print(f"Warning: Could not initialize camera: {e}")
            print("Full traceback:")
            traceback.print_exc()
            camera_capture = None

    # Log mode
    if mmwave_capture and camera_capture:
        print("Running with mmWave + camera")
    elif mmwave_capture:
        print("Running in mmWave-only mode")
    elif camera_capture:
        print("Running in camera-only mode")

    # Set initial skeleton state (enabled by default)
    if camera_capture:
        window.control_panel.set_skeleton_enabled(True)

    # Show window
    window.show()

    # Run application
    exit_code = app.exec_()

    # Cleanup
    print("Shutting down...")

    if mmwave_capture:
        mmwave_capture.stop()
    if camera_capture:
        camera_capture.stop()
    if file_writer:
        file_writer.stop()
        file_writer.join(timeout=2.0)

    print("Goodbye!")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
