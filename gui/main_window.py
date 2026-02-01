"""
Main Window - Clean Dashboard Layout

Fixed proportions, consistent spacing, no clutter.
"""

from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QSplitter, QMessageBox, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QCloseEvent
import numpy as np
import time

from .status_bar import StatusBar
from .video_widget import VideoWidget
from .heatmap_widget import DualHeatmapWidget
from .control_panel import ControlPanel
from .styles import MAIN_STYLE, COLORS, SPACING

import sys
sys.path.append('..')
from config import CAMERA_PARAMS, DISPLAY_PARAMS


class MainWindow(QMainWindow):
    """
    Clean dashboard layout with fixed proportions.

    ┌──────────────────────────────────────────────┐
    │ Status Bar                                   │
    ├─────────────────────────┬────────────────────┤
    │                         │   Range-Doppler    │
    │   Camera (16:9)         ├────────────────────┤
    │                         │   Range-Azimuth    │
    ├─────────────────────────┴────────────────────┤
    │ Controls                                     │
    └──────────────────────────────────────────────┘
    """

    update_video_signal = pyqtSignal(np.ndarray)
    update_rd_signal = pyqtSignal(np.ndarray)
    update_ra_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()

        self._mmwave_capture = None
        self._camera_capture = None
        self._mmwave_processor = None
        self._recorder = None
        self._file_writer = None
        self._timestamp_logger = None

        self._is_running = False
        self._frame_count = 0
        self._last_fps_time = time.time()
        self._fps_frame_count = 0

        self._setup_ui()
        self._setup_timer()
        self._connect_signals()

    def _setup_ui(self):
        self.setWindowTitle("Vomee")
        self.setStyleSheet(MAIN_STYLE)
        self.setMinimumSize(1024, 600)

        # Central widget
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Status bar
        self.status_bar = StatusBar()
        main_layout.addWidget(self.status_bar)

        # Content area
        content = QWidget()
        content.setStyleSheet(f"background: {COLORS['bg_primary']};")
        content_layout = QHBoxLayout(content)
        content_layout.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
        content_layout.setSpacing(SPACING['md'])

        # Video panel (left, ~65%)
        self.video_widget = VideoWidget(
            width=CAMERA_PARAMS['width'],
            height=CAMERA_PARAMS['height']
        )
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.video_widget, 65)

        # Heatmap panel (right, ~35%)
        self.heatmap_widget = DualHeatmapWidget()
        self.heatmap_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        content_layout.addWidget(self.heatmap_widget, 35)

        main_layout.addWidget(content, 1)

        # Control panel
        self.control_panel = ControlPanel()
        main_layout.addWidget(self.control_panel)

    def _setup_timer(self):
        self._update_timer = QTimer(self)
        self._update_timer.timeout.connect(self._on_update)
        interval = int(1000 / DISPLAY_PARAMS['update_rate_hz'])
        self._update_timer.setInterval(interval)

    def _connect_signals(self):
        self.control_panel.skeleton_toggled.connect(self._on_skeleton_toggle)
        self.control_panel.mode_changed.connect(self._on_mode_change)
        self.control_panel.start_clicked.connect(self._on_start)
        self.control_panel.stop_clicked.connect(self._on_stop)

        self.update_video_signal.connect(self.video_widget.update_frame)
        self.update_rd_signal.connect(self.heatmap_widget.update_rd)
        self.update_ra_signal.connect(self.heatmap_widget.update_ra)

    def showEvent(self, event):
        super().showEvent(event)
        if not hasattr(self, '_maximized'):
            self._maximized = True
            self.showMaximized()

    # ── Setters ──────────────────────────────────────────────────

    def set_mmwave_capture(self, c): self._mmwave_capture = c
    def set_camera_capture(self, c): self._camera_capture = c
    def set_mmwave_processor(self, p): self._mmwave_processor = p
    def set_recorder(self, r): self._recorder = r
    def set_file_writer(self, w): self._file_writer = w

    # ── Event Handlers ───────────────────────────────────────────

    def _on_skeleton_toggle(self, enabled: bool):
        if self._camera_capture:
            self._camera_capture.set_skeleton_enabled(enabled)
        self.video_widget.set_skeleton_visible(enabled)

    def _on_mode_change(self, mode: str):
        self.status_bar.update_mode(mode)

    def _on_start(self):
        mode = self.control_panel.get_mode()

        if mode == "Recording" and self._recorder:
            skeleton = self.control_panel.is_skeleton_enabled()
            path = self._recorder.start_session(skeleton)
            print(f"[Rec] {path}")

            if self._recorder.session_path:
                from recording.recorder import TimestampLogger
                self._timestamp_logger = TimestampLogger(self._recorder.get_timestamps_path())
                self._timestamp_logger.open()

            self.status_bar.start_recording()

        self._is_running = True
        self._frame_count = 0
        self._last_fps_time = time.time()
        self._fps_frame_count = 0
        self._update_timer.start()

    def _on_stop(self):
        self._is_running = False
        self._update_timer.stop()

        if self._recorder and self._recorder.is_recording:
            if self._timestamp_logger:
                self._timestamp_logger.close()
                self._timestamp_logger = None
            info = self._recorder.stop_session()
            print(f"[Rec] Done: {info.get('frame_count', 0)} frames")
            if self._file_writer:
                self._file_writer.wait_completion(timeout=5.0)

        # Clear all displays
        self.video_widget.clear()
        self.heatmap_widget.clear()
        self.status_bar.reset()

    def _on_update(self):
        if not self._is_running:
            return

        cam_updated = False
        mmw_updated = False
        sync_ms = -1.0
        cam_ts = 0
        frame = None
        landmarks = None

        # Camera
        if self._camera_capture:
            if self.control_panel.is_skeleton_enabled():
                frame, cam_ts, landmarks = self._camera_capture.get_frame_with_overlay()
            else:
                frame, cam_ts, landmarks = self._camera_capture.get_frame()

            if frame is not None:
                self.update_video_signal.emit(frame)
                cam_updated = True

        # mmWave
        if self._mmwave_capture:
            result = self._mmwave_capture.get_frame()

            if not isinstance(result[0], str):
                data, mmw_ts, fnum, lost = result

                if cam_updated and cam_ts > 0 and mmw_ts > 0:
                    sync_ms = abs(mmw_ts - cam_ts) * 1000

                if self._mmwave_processor:
                    try:
                        rd, ra, _ = self._mmwave_processor.process(data)
                        self.update_rd_signal.emit(rd)
                        self.update_ra_signal.emit(ra)
                        mmw_updated = True

                        if self._recorder and self._recorder.is_recording:
                            self._record(data, rd, ra, fnum, mmw_ts,
                                        cam_ts if cam_updated else 0,
                                        frame, landmarks)
                    except Exception as e:
                        print(f"[Err] {e}")

        # Status
        if mmw_updated and cam_updated:
            self.status_bar.update_sync_status(sync_ms)
        elif cam_updated:
            self.status_bar.update_sync_status(-1)
        elif mmw_updated:
            self.status_bar.update_sync_status(-2)

        if cam_updated or mmw_updated:
            self._frame_count += 1
            self._fps_frame_count += 1
            self.status_bar.update_frame_count(self._frame_count)

        # FPS
        now = time.time()
        if now - self._last_fps_time >= 1.0:
            fps = self._fps_frame_count / (now - self._last_fps_time)
            self.status_bar.update_fps(fps)
            self._last_fps_time = now
            self._fps_frame_count = 0

    def _record(self, data, rd, ra, fnum, mmw_ts, cam_ts, frame, landmarks):
        if not self._file_writer or not self._recorder:
            return

        self._recorder.increment_frame_count()

        raw_path = self._recorder.get_raw_path()
        if raw_path:
            self._file_writer.write_raw_mmwave(raw_path, data, fnum)

        rd_path = self._recorder.get_frame_path(fnum, 'rd')
        if rd_path:
            self._file_writer.write_rd_heatmap(rd_path, rd, fnum)

        ra_path = self._recorder.get_frame_path(fnum, 'ra')
        if ra_path:
            self._file_writer.write_ra_heatmap(ra_path, ra, fnum)

        if frame is not None:
            cam_path = self._recorder.get_frame_path(fnum, 'camera')
            if cam_path:
                self._file_writer.write_camera_frame(cam_path, frame, fnum)

        if landmarks:
            skel_path = self._recorder.get_frame_path(fnum, 'skeleton')
            if skel_path:
                self._file_writer.write_skeleton(skel_path, landmarks, fnum)

        if self._timestamp_logger:
            self._timestamp_logger.log(fnum, mmw_ts, cam_ts)

    def closeEvent(self, event: QCloseEvent):
        if self._is_running:
            reply = QMessageBox.question(
                self, 'Exit', 'Stop capture and exit?',
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
            self._on_stop()

        if self._mmwave_capture: self._mmwave_capture.stop()
        if self._camera_capture: self._camera_capture.stop()
        if self._file_writer: self._file_writer.stop()
        event.accept()

    @property
    def is_running(self) -> bool:
        return self._is_running
