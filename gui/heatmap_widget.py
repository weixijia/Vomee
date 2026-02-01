"""
Heatmap Widget - Clean, Fixed Display

No zoom/pan, fixed aspect ratio, minimal chrome.
"""

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
import numpy as np

from .styles import COLORS, SPACING, HEADER_STYLE


class HeatmapWidget(QWidget):
    """
    Simple heatmap display - no interactivity, just clean visualization.
    """

    def __init__(self, title: str = "Heatmap", parent=None):
        super().__init__(parent)
        self.title = title
        self._colormap = self._create_viridis_lut()
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Header
        self.header = QLabel(self.title.upper())
        self.header.setStyleSheet(HEADER_STYLE)
        self.header.setFixedHeight(28)
        layout.addWidget(self.header)

        # Display area - simple QLabel
        self.display = QLabel()
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setStyleSheet(f"background: {COLORS['bg_primary']};")
        # Use Ignored policy so the label doesn't affect layout when pixmap changes
        self.display.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.display.setMinimumSize(100, 100)
        layout.addWidget(self.display)

        self._show_empty()

    def _create_viridis_lut(self) -> np.ndarray:
        """Create viridis colormap LUT."""
        # Viridis key colors
        colors = np.array([
            [68, 1, 84],
            [72, 35, 116],
            [64, 67, 135],
            [52, 94, 141],
            [41, 120, 142],
            [32, 144, 140],
            [34, 167, 132],
            [68, 190, 112],
            [121, 209, 81],
            [189, 222, 38],
            [253, 231, 36]
        ], dtype=np.uint8)

        # Interpolate to 256 values
        lut = np.zeros((256, 3), dtype=np.uint8)
        for i in range(256):
            t = i / 255.0 * (len(colors) - 1)
            idx = int(t)
            frac = t - idx
            if idx >= len(colors) - 1:
                lut[i] = colors[-1]
            else:
                lut[i] = (colors[idx] * (1 - frac) + colors[idx + 1] * frac).astype(np.uint8)
        return lut

    def _show_empty(self):
        """Show empty state."""
        size = self.display.size()
        w, h = max(100, size.width()), max(100, size.height())

        img = QPixmap(w, h)
        img.fill(QColor(COLORS['bg_primary']))

        painter = QPainter(img)
        painter.setPen(QColor(COLORS['text_muted']))
        painter.drawText(img.rect(), Qt.AlignCenter, "No data")
        painter.end()

        self.display.setPixmap(img)

    def update_heatmap(self, data: np.ndarray):
        """Update with new data (normalized 0-1)."""
        if data is None:
            self._show_empty()
            return

        # Ensure float and clamp
        data = np.clip(data.astype(np.float32), 0, 1)

        # Map to colormap indices
        indices = (data * 255).astype(np.uint8)

        # Apply colormap
        h, w = data.shape
        rgb = self._colormap[indices.flatten()].reshape(h, w, 3)

        # Convert to QImage
        rgb = np.ascontiguousarray(rgb)
        qimg = QImage(rgb.data, w, h, 3 * w, QImage.Format_RGB888)

        # Scale to fit display
        pixmap = QPixmap.fromImage(qimg)
        scaled = pixmap.scaled(
            self.display.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.display.setPixmap(scaled)

    def clear(self):
        self._show_empty()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Don't re-render on resize to avoid flicker


class DualHeatmapWidget(QWidget):
    """
    Two stacked heatmaps for Range-Doppler and Range-Azimuth.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING['md'])

        self.rd_widget = HeatmapWidget("Range-Doppler")
        layout.addWidget(self.rd_widget, 1)

        self.ra_widget = HeatmapWidget("Range-Azimuth")
        layout.addWidget(self.ra_widget, 1)

    def update_rd(self, data: np.ndarray):
        self.rd_widget.update_heatmap(data)

    def update_ra(self, data: np.ndarray):
        self.ra_widget.update_heatmap(data)

    def clear(self):
        self.rd_widget.clear()
        self.ra_widget.clear()
