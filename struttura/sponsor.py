"""
Sponsor Dialog Module (PySide6 Version)

This module provides the Sponsor dialog for the Project.
Displays various sponsorship/donation options.

License: GPL v3.0 (see LICENSE)
"""

import webbrowser
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
)
from PySide6.QtCore import Qt
from .lang import tr

class Sponsor(QDialog):
    """Sponsor dialog with donation/support options."""
    
    def __init__(self, parent=None):
        """Initialize the Sponsor dialog."""
        super().__init__(parent)
        self.setWindowTitle(tr('sponsor'))
        self.setMinimumSize(500, 150)
        
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Add message
        message = QLabel(tr('support_message'))
        message.setAlignment(Qt.AlignCenter)
        message.setWordWrap(True)
        layout.addWidget(message)
        
        # Create button layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Sponsor buttons
        buttons = [
            (tr('sponsor_on_github'), "https://github.com/sponsors/Nsfr750"),
            (tr('join_discord'), "https://discord.gg/BvvkUEP9"),
            (tr('buy_me_a_coffee'), "https://paypal.me/3dmega"),
            (tr('join_the_patreon'), "https://www.patreon.com/Nsfr750")
        ]
        
        for text, url in buttons:
            btn = QPushButton(text)
            btn.clicked.connect(lambda checked, u=url: webbrowser.open(u))
            button_layout.addWidget(btn)
        
        # Add stretch to center buttons
        layout.addStretch()
        layout.addLayout(button_layout)
        layout.addStretch()
        
        # Add close button
        close_btn = QPushButton(tr('close'))
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

# For testing
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = Sponsor()
    dialog.exec()
    sys.exit()
