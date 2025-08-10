#!/usr/bin/env python3
"""
Main entry point for the Raspy Utility application.
"""
import os
import sys
import logging
import threading
from typing import Optional

# PySide6 imports
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QObject, Signal, QThread, Slot, Qt
from PySide6.QtGui import QPalette, QColor

def configure_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('raspy_utility.log')
        ]
    )

class WebServerThread(QThread):
    """Thread for running the Flask web server."""
    def __init__(self, port=5000):
        super().__init__()
        self.port = port
        
    def run(self):
        """Run the Flask web server."""
        from app.app import create_app
        app = create_app()
        app.run(host='0.0.0.0', port=self.port, threaded=True, use_reloader=False)

class MainApplication(QObject):
    """Main application class for PySide6."""
    def _setup_dark_theme(self):
        """Apply a dark theme to the application."""
        self.app.setStyle("Fusion")
        
        # Create a dark color palette
        dark_palette = QPalette()
        
        # Base colors
        dark_gray = QColor(53, 53, 53)
        darker_gray = QColor(35, 35, 35)
        
        # Set the color roles
        dark_palette.setColor(QPalette.Window, dark_gray)
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, darker_gray)
        dark_palette.setColor(QPalette.AlternateBase, dark_gray)
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, dark_gray)
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))  # Blue
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))  # Blue
        dark_palette.setColor(QPalette.HighlightedText, Qt.white)
        
        self.app.setPalette(dark_palette)
        
        # Apply a dark stylesheet for additional styling
        self.app.setStyleSheet("""
            QToolTip {
                color: #ffffff;
                background-color: #2a82da;
                border: 1px solid white;
            }
            
            QMenuBar::item:selected {
                background: #555555;
            }
            
            QMenu::item:selected {
                background: #2a82da;
            }
        """)
        
    def __init__(self):
        super().__init__()
        self.app = QApplication.instance() or QApplication(sys.argv)
        
        # Setup dark theme
        self._setup_dark_theme()
        
        # Use the new PySide6-based MainWindow
        from gui.main_window import MainWindow
        self.main_window = MainWindow()
        
    def run(self):
        """Run the application."""
        self.main_window.show()
        return self.app.exec()

def start_gui():
    """Start the GUI application."""
    logger = logging.getLogger(__name__)
    try:
        app = MainApplication()
        return app.run()
    except Exception as e:
        logger.error(f"Failed to start GUI: {e}", exc_info=True)
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"Failed to start application: {str(e)}"
        )
        return 1

def open_browser(url: str):
    """Open a URL in the default web browser."""
    import webbrowser
    webbrowser.open(url)

def main():
    """Main entry point for the application."""
    # Configure logging
    configure_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Start the application
        return start_gui()
            
    except Exception as e:
        logger.error(f"Failed to start application: {e}", exc_info=True)
        QMessageBox.critical(
            None,
            "Fatal Error",
            f"Failed to start application: {str(e)}"
        )
        return 1

if __name__ == '__main__':
    main()
