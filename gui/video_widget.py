"""
Video Widget - Clean Camera Display

Minimal chrome, proper aspect ratio.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
import numpy as np

from .styles import COLORS, SPACING, HEADER_STYLE


class VideoWidget(QWidget):
    """
    Clean video display with minimal header.
    """

    def __init__(self, width: int = 1280, height: int = 720, parent=None):
        super().__init__(parent)
        self.native_width = width
        self.native_height = height
        self._last_frame = None
        self._skeleton_on = False
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = QLabel("CAMERA")
        self.header.setStyleSheet(HEADER_STYLE)
        self.header.setFixedHeight(28)
        layout.addWidget(self.header)

        # Video display
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet(f"background: {COLORS['bg_primary']};")
        # Use Ignored policy so the label doesn't affect layout when pixmap changes
        self.display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.display.setMinimumSize(320, 180)
        layout.addWidget(self.display)

        self._show_waiting()

    def _show_waiting(self):
        """Show waiting state."""
        size = self.display.size()
        w, h = max(320, size.width()), max(180, size.height())

        img = QPixmap(w, h)
        img.fill(QColor(COLORS['bg_primary']))

        painter = QPainter(img)
        painter.setPen(QColor(COLORS['text_muted']))
        painter.drawText(img.rect(), Qt.AlignCenter, "Waiting for camera...")
        painter.end()

        self.display.setPixmap(img)

    def update_frame(self, frame: np.ndarray):
        """Update with new RGB frame."""
        if frame is None:
            return

        self._last_frame = frame
        h, w, ch = frame.shape

        if not frame.flags['C_CONTIGUOUS']:
            frame = np.ascontiguousarray(frame)

        qimg = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)

        # Scale to fit while maintaining aspect ratio
        scaled = pixmap.scaled(
            self.display.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.display.setPixmap(scaled)

    def set_skeleton_visible(self, visible: bool):
        self._skeleton_on = visible
        if visible:
            self.header.setText("CAMERA  ·  SKELETON")
        else:
            self.header.setText("CAMERA")

    def clear(self):
        self._last_frame = None
        self._show_waiting()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self._last_frame is not None:
            self.update_frame(self._last_frame)
