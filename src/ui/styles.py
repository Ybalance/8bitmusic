# Professional Light Theme for Audio Morph Studio
# High contrast, clean, and readable.

MODERN_STYLE = """
/* Global Reset */
QWidget {
    font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
    font-size: 14px;
    color: #333333;
    background-color: #f0f2f5;
}

/* Main Window & Tabs */
QMainWindow, QTabWidget::pane {
    background-color: #f0f2f5;
}

QTabBar::tab {
    background: #e0e0e0;
    color: #555555;
    padding: 10px 20px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    margin-right: 2px;
}

QTabBar::tab:selected {
    background: #ffffff;
    color: #0d47a1;
    font-weight: bold;
    border-bottom: 2px solid #0d47a1;
}

/* Panels & Containers */
QWidget#LeftPanel, QGroupBox, QScrollArea, QListWidget {
    background-color: #ffffff;
    border: 1px solid #dcdcdc;
    border-radius: 6px;
}

/* Group Boxes */
QGroupBox {
    margin-top: 24px;
    font-weight: bold;
    color: #1565c0; /* Blue Header */
}

QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}

/* Lists */
QListWidget {
    outline: none;
}

QListWidget::item {
    padding: 10px;
    border-bottom: 1px solid #f0f0f0;
}

QListWidget::item:selected {
    background-color: #e3f2fd; /* Light Blue */
    color: #0d47a1;
    border-left: 4px solid #0d47a1;
}

QListWidget::item:hover {
    background-color: #f5f5f5;
}

/* Inputs */
QLineEdit, QSpinBox, QComboBox, QTextEdit {
    background-color: #ffffff;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 6px;
    color: #333333;
    selection-background-color: #0d47a1;
}

QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QTextEdit:focus {
    border: 1px solid #0d47a1;
}

QLineEdit:read-only {
    background-color: #f8f9fa;
    color: #666666;
}

/* Buttons */
QPushButton {
    background-color: #ffffff;
    border: 1px solid #c0c0c0;
    border-radius: 4px;
    padding: 8px 16px;
    color: #333333;
    font-weight: 500;
}

QPushButton:hover {
    background-color: #f5f5f5;
    border-color: #a0a0a0;
}

QPushButton:pressed {
    background-color: #e0e0e0;
}

/* Primary Action Buttons */
QPushButton#ProcessButton {
    background-color: #0d47a1;
    color: #ffffff;
    border: none;
    font-weight: bold;
    font-size: 15px;
    padding: 12px;
}

QPushButton#ProcessButton:hover {
    background-color: #1565c0;
}

QPushButton#ProcessButton:disabled {
    background-color: #b0bec5;
    color: #f0f0f0;
}

/* Labels */
QLabel {
    background-color: transparent;
    color: #333333;
}

QLabel#HeaderLabel {
    font-size: 22px;
    font-weight: bold;
    color: #0d47a1;
    margin-bottom: 15px;
    padding-bottom: 10px;
    border-bottom: 2px solid #e0e0e0;
}

QLabel#DescriptionLabel {
    color: #666666;
    font-style: italic;
}

/* Scrollbars */
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0px 0px 0px 0px;
}
QScrollBar::handle:vertical {
    background: #c0c0c0;
    min-height: 20px;
    border-radius: 5px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}
"""
