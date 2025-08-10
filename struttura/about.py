"""
About Dialog Module (PySide6 Version)

This module provides the About dialog for the Project.
Displays application information and version details.

License: GPL v3.0 (see LICENSE)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QIcon
from .version import get_version
from .lang import tr

class About(QDialog):
    """About dialog showing application information."""
    
    def __init__(self, parent=None):
        """Initialize the About dialog."""
        super().__init__(parent)
        self.setWindowTitle(tr('about'))
        self.setMinimumSize(400, 300)
        
        # Create main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add application title
        title = QLabel(tr('app_title'))
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        
        # Add version information
        version = QLabel(f"{tr('version')} {get_version()}")
        version.setAlignment(Qt.AlignCenter)
        
        # Add description
        description = QLabel('Raspy Utility')
        description.setAlignment(Qt.AlignCenter)
        
        # Add copyright information
        copyright = QLabel('© 2025 Nsfr750')
        copyright.setAlignment(Qt.AlignCenter)
        
        # Add close button
        button_box = QHBoxLayout()
        close_button = QPushButton(tr('close'))
        close_button.clicked.connect(self.accept)
        button_box.addStretch()
        button_box.addWidget(close_button)
        button_box.addStretch()
        
        # Add widgets to layout
        layout.addStretch()
        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(description)
        layout.addStretch()
        layout.addWidget(copyright)
        layout.addLayout(button_box)
        
        # Set window properties
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

# For testing
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = About()
    dialog.exec()
    sys.exit()
