"""
Modern UI Styles - Clean, Minimal Dashboard Design

Based on 2024 dashboard design principles:
- Minimal color palette (2-3 colors)
- Consistent spacing (12px base unit)
- No unnecessary borders/boxes
- Clear visual hierarchy
"""

# Spacing system - 12px base unit
SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 12,
    'lg': 16,
    'xl': 24,
}

# Minimal color palette
COLORS = {
    # Backgrounds - subtle gradient of grays
    'bg_primary': '#0d0d0d',       # Darkest - main bg
    'bg_secondary': '#161616',     # Cards/panels
    'bg_elevated': '#1f1f1f',      # Hover states

    # Text - high contrast
    'text_primary': '#f5f5f5',
    'text_secondary': '#888888',
    'text_muted': '#555555',

    # Accent - minimal, only for actions
    'accent': '#3b82f6',           # Blue - primary action
    'success': '#22c55e',          # Green - start/active
    'danger': '#ef4444',           # Red - stop/recording

    # Borders - very subtle
    'border': '#262626',
}

# Main window - clean, no borders
MAIN_STYLE = f"""
QMainWindow, QWidget {{
    background-color: {COLORS['bg_primary']};
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', system-ui, sans-serif;
    font-size: 13px;
}}
QSplitter::handle {{
    background: {COLORS['bg_primary']};
    width: 12px;
}}
"""

# Status bar - minimal, no boxes
STATUS_STYLE = f"""
QWidget#statusBar {{
    background-color: {COLORS['bg_secondary']};
    padding: 0 {SPACING['lg']}px;
}}
QLabel {{
    background: transparent;
    color: {COLORS['text_secondary']};
    font-size: 12px;
    padding: 0;
}}
QLabel#mainStatus {{
    color: {COLORS['text_primary']};
    font-weight: 600;
}}
QLabel#timer {{
    font-family: 'Consolas', 'SF Mono', monospace;
    font-size: 13px;
    color: {COLORS['text_primary']};
    letter-spacing: 1px;
}}
"""

# Control panel - clean buttons
CONTROL_STYLE = f"""
QWidget#controlPanel {{
    background-color: {COLORS['bg_secondary']};
}}
QPushButton {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['text_primary']};
    border: none;
    border-radius: 6px;
    padding: 10px 28px;
    font-size: 13px;
    font-weight: 500;
}}
QPushButton:hover {{
    background-color: #2a2a2a;
}}
QPushButton#btnStart {{
    background-color: {COLORS['success']};
    color: #000;
}}
QPushButton#btnStart:hover {{
    background-color: #16a34a;
}}
QPushButton#btnStart:disabled {{
    background-color: #1a2e1a;
    color: #555;
}}
QPushButton#btnStop {{
    background-color: {COLORS['danger']};
    color: #fff;
}}
QPushButton#btnStop:hover {{
    background-color: #dc2626;
}}
QPushButton#btnStop:disabled {{
    background-color: #2e1a1a;
    color: #555;
}}
QCheckBox {{
    color: {COLORS['text_primary']};
    spacing: 8px;
    background: transparent;
}}
QCheckBox::indicator {{
    width: 18px;
    height: 18px;
    border-radius: 4px;
    border: 2px solid {COLORS['text_muted']};
    background: transparent;
}}
QCheckBox::indicator:checked {{
    background-color: {COLORS['accent']};
    border-color: {COLORS['accent']};
}}
QComboBox {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['text_primary']};
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    min-width: 120px;
}}
QComboBox::drop-down {{
    border: none;
    width: 20px;
}}
QComboBox QAbstractItemView {{
    background-color: {COLORS['bg_elevated']};
    color: {COLORS['text_primary']};
    selection-background-color: {COLORS['accent']};
}}
QLabel {{
    background: transparent;
    color: {COLORS['text_secondary']};
}}
"""

# Panel headers - subtle
HEADER_STYLE = f"""
QLabel {{
    background: transparent;
    color: {COLORS['text_muted']};
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: {SPACING['sm']}px {SPACING['md']}px;
}}
"""
