"""
Status Bar - Minimal, Non-Flashing

Rate-limited updates to prevent visual noise.
"""

from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from datetime import datetime
import time

from .styles import COLORS, SPACING, STATUS_STYLE


class StatusBar(QWidget):
    """
    Clean status bar with rate-limited updates.

    Updates sync/FPS only every 500ms to prevent flashing.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusBar")

        self._fps = 0.0
        self._frame_count = 0
        self._mode = "Preview"
        self._start_time = None
        self._is_recording = False

        # Rate limiting
        self._last_sync_update = 0
        self._last_sync_value = "--"
        self._pending_sync = None

        self._setup_ui()
        self._setup_timers()

    def _setup_ui(self):
        self.setStyleSheet(STATUS_STYLE)
        self.setFixedHeight(40)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], 0, SPACING['lg'], 0)
        layout.setSpacing(SPACING['xl'])

        # Status indicator (dot)
        self.dot = QLabel("●")
        self.dot.setStyleSheet(f"color: {COLORS['success']}; font-size: 10px;")
        layout.addWidget(self.dot)

        # Status text
        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("mainStatus")
        layout.addWidget(self.status_label)

        # Separator
        layout.addSpacing(SPACING['lg'])

        # FPS
        self.fps_label = QLabel("-- FPS")
        layout.addWidget(self.fps_label)

        # Frames
        self.frame_label = QLabel("0 frames")
        layout.addWidget(self.frame_label)

        # Mode
        self.mode_label = QLabel("Preview")
        layout.addWidget(self.mode_label)

        # Spacer
        layout.addStretch()

        # Timer
        self.timer_label = QLabel("00:00:00")
        self.timer_label.setObjectName("timer")
        layout.addWidget(self.timer_label)

        # Sync (rate-limited)
        self.sync_label = QLabel("--")
        layout.addWidget(self.sync_label)

    def _setup_timers(self):
        # Timer for elapsed time (1 sec)
        self._elapsed_timer = QTimer(self)
        self._elapsed_timer.timeout.connect(self._update_elapsed)
        self._elapsed_timer.start(1000)

        # Timer for sync display update (500ms)
        self._sync_timer = QTimer(self)
        self._sync_timer.timeout.connect(self._flush_sync)
        self._sync_timer.start(500)

    def _update_elapsed(self):
        if self._start_time and self._is_recording:
            elapsed = datetime.now() - self._start_time
            h, rem = divmod(int(elapsed.total_seconds()), 3600)
            m, s = divmod(rem, 60)
            self.timer_label.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def _flush_sync(self):
        """Apply pending sync update (rate limited)."""
        if self._pending_sync is not None:
            text, color = self._pending_sync
            self.sync_label.setText(text)
            self.sync_label.setStyleSheet(f"color: {color}; background: transparent;")
            self._pending_sync = None

    def update_fps(self, fps: float):
        self._fps = fps
        self.fps_label.setText(f"{fps:.1f} FPS")

    def update_frame_count(self, count: int):
        self._frame_count = count
        # Only update every 10 frames to reduce redraws
        if count % 10 == 0:
            self.frame_label.setText(f"{count:,} frames")

    def update_mode(self, mode: str):
        self._mode = mode
        self.mode_label.setText(mode)

        if mode == "Recording":
            self.dot.setStyleSheet(f"color: {COLORS['danger']}; font-size: 10px;")
            self.status_label.setText("Recording")
        else:
            self.dot.setStyleSheet(f"color: {COLORS['success']}; font-size: 10px;")
            self.status_label.setText("Ready")

    def update_sync_status(self, diff_ms: float):
        """Queue sync update (will be applied every 500ms)."""
        if diff_ms == -2:
            self._pending_sync = ("No camera", COLORS['text_muted'])
        elif diff_ms == -1:
            self._pending_sync = ("Waiting", COLORS['text_muted'])
        elif diff_ms < 30:
            self._pending_sync = (f"{diff_ms:.0f}ms", COLORS['success'])
        elif diff_ms < 50:
            self._pending_sync = (f"{diff_ms:.0f}ms", "#f59e0b")  # Amber
        else:
            self._pending_sync = (f"{diff_ms:.0f}ms", COLORS['danger'])

    def start_recording(self):
        self._is_recording = True
        self._start_time = datetime.now()
        self.update_mode("Recording")

    def stop_recording(self):
        self._is_recording = False
        self.update_mode("Preview")

    def reset(self):
        self._fps = 0.0
        self._frame_count = 0
        self._start_time = None
        self._is_recording = False
        self.fps_label.setText("-- FPS")
        self.frame_label.setText("0 frames")
        self.timer_label.setText("00:00:00")
        self.sync_label.setText("--")
        self.update_mode("Preview")
