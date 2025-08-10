"""
Help Dialog Module (PySide6 Version)

This module provides the Help dialog for the Project.
Displays usage instructions and feature highlights in a tabbed interface.

License: GPL v3.0 (see LICENSE)
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QTabWidget, QLabel, 
    QTextBrowser, QDialogButtonBox, QWidget
)
from PySide6.QtCore import Qt
from .lang import tr

class Help(QDialog):
    """Help dialog with tabbed interface for different help topics."""
    
    def __init__(self, parent=None):
        """Initialize the Help dialog."""
        super().__init__(parent)
        self.setWindowTitle(tr('help_title'))
        self.setMinimumSize(600, 500)
        
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self._add_welcome_tab()
        self._add_features_tab()
        self._add_shortcuts_tab()
        
        layout.addWidget(self.tabs)
        
        # Add close button
        self.button_box = QDialogButtonBox(QDialogButtonBox.Close)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)
    
    def _add_welcome_tab(self):
        """Add the welcome tab with basic information."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setReadOnly(True)
        text.setHtml("""
        <h1>Welcome to Raspy Utility</h1>
        <p>This application provides a user-friendly interface for managing your Raspberry Pi.</p>
        <p>Use the tabs above to learn more about the available features and how to use them.</p>
        """)
        
        layout.addWidget(text)
        self.tabs.addTab(widget, tr('welcome_tab'))
    
    def _add_features_tab(self):
        """Add the features tab with an overview of main features."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setReadOnly(True)
        text.setHtml("""
        <h1>Features</h1>
        <h2>Web Interface</h2>
        <p>Access the application from any device on your network using the built-in web server.</p>
        
        <h2>GPIO Control</h2>
        <p>Control and monitor your Raspberry Pi's GPIO pins directly from the application.</p>
        
        <h2>System Monitoring</h2>
        <p>Monitor system resources like CPU, memory, and disk usage in real-time.</p>
        """)
        
        layout.addWidget(text)
        self.tabs.addTab(widget, tr('features_tab'))
    
    def _add_shortcuts_tab(self):
        """Add the keyboard shortcuts tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        text = QTextBrowser()
        text.setOpenExternalLinks(True)
        text.setReadOnly(True)
        text.setHtml("""
        <h1>Keyboard Shortcuts</h1>
        <table border="1">
            <tr><th>Action</th><th>Shortcut</th></tr>
            <tr><td>Start Web Server</td><td>Ctrl+S</td></tr>
            <tr><td>Stop Web Server</td><td>Ctrl+Q</td></tr>
            <tr><td>Open in Browser</td><td>Ctrl+B</td></tr>
            <tr><td>View Logs</td><td>Ctrl+L</td></tr>
            <tr><td>Exit Application</td><td>Alt+F4</td></tr>
        </table>
        """)
        
        layout.addWidget(text)
        self.tabs.addTab(widget, tr('shortcuts_tab'))

# For testing
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = Help()
    dialog.exec()
    sys.exit()
