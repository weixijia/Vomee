"""
Control Panel - Clean, Minimal Controls
"""

from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QPushButton, QComboBox,
                             QLabel, QCheckBox)
from PyQt5.QtCore import Qt, pyqtSignal

from .styles import COLORS, SPACING, CONTROL_STYLE


class ControlPanel(QWidget):
    """
    Minimal control panel with clean button styling.
    """

    skeleton_toggled = pyqtSignal(bool)
    mode_changed = pyqtSignal(str)
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("controlPanel")
        self._is_running = False
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        self.setStyleSheet(CONTROL_STYLE)
        self.setFixedHeight(64)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING['xl'], 0, SPACING['xl'], 0)
        layout.setSpacing(SPACING['lg'])

        # Skeleton toggle (enabled by default)
        self.skeleton_cb = QCheckBox("Skeleton")
        self.skeleton_cb.setChecked(True)
        layout.addWidget(self.skeleton_cb)

        layout.addSpacing(SPACING['xl'])

        # Mode
        mode_label = QLabel("Mode")
        layout.addWidget(mode_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Preview", "Recording"])
        layout.addWidget(self.mode_combo)

        # Spacer
        layout.addStretch()

        # Buttons
        self.btn_start = QPushButton("Start")
        self.btn_start.setObjectName("btnStart")
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setFixedWidth(100)
        layout.addWidget(self.btn_start)

        self.btn_stop = QPushButton("Stop")
        self.btn_stop.setObjectName("btnStop")
        self.btn_stop.setCursor(Qt.PointingHandCursor)
        self.btn_stop.setFixedWidth(100)
        self.btn_stop.setEnabled(False)
        layout.addWidget(self.btn_stop)

    def _connect_signals(self):
        self.skeleton_cb.toggled.connect(self.skeleton_toggled.emit)
        self.mode_combo.currentTextChanged.connect(self.mode_changed.emit)
        self.btn_start.clicked.connect(self._on_start)
        self.btn_stop.clicked.connect(self._on_stop)

    def _on_start(self):
        self._is_running = True
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.mode_combo.setEnabled(False)
        self.start_clicked.emit()

    def _on_stop(self):
        self._is_running = False
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.mode_combo.setEnabled(True)
        self.stop_clicked.emit()

    def is_skeleton_enabled(self) -> bool:
        return self.skeleton_cb.isChecked()

    def get_mode(self) -> str:
        return self.mode_combo.currentText()

    def set_mode(self, mode: str):
        idx = self.mode_combo.findText(mode)
        if idx >= 0:
            self.mode_combo.setCurrentIndex(idx)

    def set_skeleton_enabled(self, enabled: bool):
        self.skeleton_cb.setChecked(enabled)

    def reset(self):
        self._is_running = False
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)
        self.mode_combo.setEnabled(True)
        self.mode_combo.setCurrentIndex(0)
        self.skeleton_cb.setChecked(True)  # Keep skeleton on by default

    @property
    def is_running(self) -> bool:
        return self._is_running
