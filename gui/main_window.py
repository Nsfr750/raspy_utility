"""
Main window for the Raspy Utility GUI using PySide6.
"""
import logging
import os
import webbrowser
from datetime import datetime
from threading import Thread
from typing import Optional

# PySide6 imports
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QToolBar, QStatusBar, QMessageBox, QSplitter,
    QFrame, QTextEdit
)
from PySide6.QtCore import QTimer, Qt, QThread, Signal, QObject
from PySide6.QtGui import QAction, QIcon, QPixmap

# Import language support
from struttura.lang import tr

# Import menu handler and other UI components
from struttura import About, Help, Sponsor, LogViewer, show_version

logger = logging.getLogger(__name__)

class WebServerThread(QThread):
    """Thread for running the Flask web server with proper shutdown handling."""
    def __init__(self, port=5000):
        super().__init__()
        self.port = port
        self._is_running = False
        self.server = None
        
    def run(self):
        """Run the Flask web server."""
        try:
            from app.app import create_app
            from werkzeug.serving import make_server
            
            # Create the Flask app
            app = create_app()
            
            # Create the server
            self.server = make_server('0.0.0.0', self.port, app, threaded=True)
            self._is_running = True
            
            # Serve until shutdown is requested
            self.server.serve_forever()
            
        except Exception as e:
            logger.error(f"Error in web server thread: {e}")
            self._is_running = False
            raise
            
    def stop(self):
        """Stop the web server gracefully."""
        if self.server:
            try:
                # Shutdown the server
                self.server.shutdown()
                # Wait for the server to stop
                self.wait(2000)  # Wait up to 2 seconds
            except Exception as e:
                logger.error(f"Error stopping server: {e}")
            finally:
                self.server = None
                self._is_running = False

class MainWindow(QMainWindow):
    """Main application window for the Raspy Utility."""
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        # Web server thread
        self.web_server_thread: Optional[WebServerThread] = None
        self.web_server_running = False
        
        # Set window properties
        self.setWindowTitle(tr('app_title'))
        self.resize(650, 600)
        
        # Set application icon with error handling
        try:
            icon_path = os.path.abspath(os.path.join('assets', 'icon.ico'))
            if os.path.exists(icon_path):
                # Use QPixmap to load the icon with validation
                pixmap = QPixmap(icon_path)
                if not pixmap.isNull():
                    self.setWindowIcon(QIcon(pixmap))
                else:
                    logger.warning(f"Invalid icon file: {icon_path}")
            else:
                logger.debug(f"Icon file not found: {icon_path}")
        except Exception as e:
            logger.warning(f"Error loading application icon: {e}")
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        
        # Create menu bar using the centralized menu system
        from struttura.menu import create_menu_bar
        menubar = create_menu_bar(self)
        self.setMenuBar(menubar)
        
        # Create toolbars
        self._create_toolbars()
        
        # Create main content area
        self._create_main_content(main_layout)
        
        # Create status bar
        self.statusBar().showMessage(tr('ready_status'))
        
        # Setup UI components
        self._setup_ui()
    
    def _create_toolbars(self):
        """Create the application toolbars."""
        # Main toolbar
        self.toolbar = QToolBar("Main Toolbar")
        self.addToolBar(self.toolbar)
        
        # Add actions to toolbar
        self.start_server_action = QAction("Start Server", self)
        self.start_server_action.triggered.connect(self._start_web_server)
        self.toolbar.addAction(self.start_server_action)
        
        self.stop_server_action = QAction("Stop Server", self)
        self.stop_server_action.triggered.connect(self._stop_web_server)
        self.stop_server_action.setEnabled(False)  # Initially disabled
        self.toolbar.addAction(self.stop_server_action)
        
        self.toolbar.addSeparator()
        
        self.open_browser_action = QAction("Open in Browser", self)
        self.open_browser_action.triggered.connect(self._open_web_interface)
        self.open_browser_action.setEnabled(False)  # Disabled until server starts
        self.toolbar.addAction(self.open_browser_action)
    
    def _create_main_content(self, parent_layout):
        """Create the main content area."""
        # Create main splitter
        splitter = QSplitter(Qt.Vertical)
        
        # Create a container for the banner (full width)
        banner_container = QWidget()
        banner_layout = QVBoxLayout(banner_container)
        banner_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add banner (full width)
        banner_frame = QFrame()
        banner_frame.setFixedHeight(151)  # Fixed height for the banner
        banner_frame_layout = QVBoxLayout(banner_frame)
        banner_frame_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create banner label
        banner_label = QLabel()
        banner_label.setFixedHeight(151)
        banner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        banner_frame_layout.addWidget(banner_label)
        
        # Load banner asynchronously to prevent UI freezing
        def load_banner():
            try:
                banner_path = os.path.join('Assets', 'banner.png')
                if os.path.exists(banner_path):
                    banner_pixmap = QPixmap(banner_path)
                    if not banner_pixmap.isNull():
                        # Scale the pixmap to fit the banner height while maintaining aspect ratio
                        scaled_pixmap = banner_pixmap.scaledToHeight(
                            151,  # Fixed height
                            Qt.TransformationMode.SmoothTransformation
                        )
                        banner_label.setPixmap(scaled_pixmap)
            except Exception as e:
                logger.warning(f"Failed to load banner: {e}")
        
        # Schedule banner loading
        QTimer.singleShot(100, load_banner)
        
        # Add banner to container
        banner_layout.addWidget(banner_frame)
        
        # Create container for GPIO controls (full width, below banner)
        gpio_container = QWidget()
        gpio_layout = QVBoxLayout(gpio_container)
        gpio_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add GPIO title
        gpio_title = QLabel("GPIO Controls")
        gpio_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        gpio_layout.addWidget(gpio_title)
        
        # Create a fixed grid layout for GPIO buttons (5x8)
        gpio_grid = QGridLayout()
        gpio_grid.setSpacing(2)
        gpio_grid.setContentsMargins(2, 2, 2, 2)
        
        # Add GPIO buttons in a 5x8 grid (5 rows x 8 columns)
        self.gpio_buttons = {}
        
        # Set fixed size for buttons (20x5)
        button_width = 20
        button_height = 5
        
        # Create buttons for GPIO 0-39
        for pin in range(40):  # 0 to 39
            row = pin // 8  # 5 rows (40 pins / 8 columns = 5 rows)
            col = pin % 8   # 8 columns
            
            btn = QPushButton(f"{pin}")
            btn.setCheckable(True)
            btn.setFixedSize(button_width * 5, button_height * 5)  # 100x25 pixels
            
            # Store the original style for toggling
            btn.original_style = btn.styleSheet()
            
            # Connect the toggled signal with the pin number
            btn.toggled.connect(lambda checked, p=pin: self._gpio_toggled(p, checked))
            
            # Add button to grid and dictionary
            gpio_grid.addWidget(btn, row, col)
            self.gpio_buttons[pin] = btn
            
            # Disable stretching to maintain fixed button sizes
            gpio_grid.setRowStretch(row, 0)
            gpio_grid.setColumnStretch(col, 0)
            gpio_grid.setRowMinimumHeight(row, button_height * 5)
            gpio_grid.setColumnMinimumWidth(col, button_width * 5)
        
        # Set grid spacing and stretch
        gpio_grid.setSpacing(5)
        gpio_grid.setContentsMargins(5, 5, 5, 5)
        
        gpio_layout.addLayout(gpio_grid)
        
        # Create main content area with fixed sections
        main_container = QWidget()
        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # 1. Fixed banner section (non-resizable)
        banner_container.setFixedHeight(151)
        main_layout.addWidget(banner_container, stretch=0)
        
        # 2. Fixed GPIO section (non-resizable, 5x8 grid)
        gpio_container.setFixedHeight(250)  # 5 rows * 50px (40px button + 5px spacing)
        main_layout.addWidget(gpio_container, stretch=0)
        
        # 3. Commands section (resizable)
        commands_container = QWidget()
        commands_layout = QVBoxLayout(commands_container)
        commands_title = QLabel("Commands")
        commands_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        commands_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        commands_layout.addWidget(commands_title)
        
        # Add command buttons
        cmd_button_layout = QHBoxLayout()
        
        # Start All button
        self.start_all_btn = QPushButton("Start All")
        self.start_all_btn.setFixedHeight(30)
        self.start_all_btn.clicked.connect(self._on_start_all_clicked)
        cmd_button_layout.addWidget(self.start_all_btn)
        
        # Stop All button
        self.stop_all_btn = QPushButton("Stop All")
        self.stop_all_btn.setFixedHeight(30)
        self.stop_all_btn.clicked.connect(self._on_stop_all_clicked)
        cmd_button_layout.addWidget(self.stop_all_btn)
        
        # Reset button
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedHeight(30)
        self.reset_btn.clicked.connect(self._on_reset_clicked)
        cmd_button_layout.addWidget(self.reset_btn)
        
        commands_layout.addLayout(cmd_button_layout)
        
        main_layout.addWidget(commands_container, stretch=1)
        
        # 4. Log section (resizable)
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_title = QLabel("Logs")
        log_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        log_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        log_layout.addWidget(log_title)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        log_layout.addWidget(self.log_area)
        
        main_layout.addWidget(log_container, stretch=2)
        
        # Add main container to window
        splitter.addWidget(main_container)
        
        # Add a small separator after banner/GPIO section
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.HLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        
        # GPIO Command States section
        states_container = QWidget()
        states_layout = QVBoxLayout(states_container)
        states_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add GPIO states title
        states_title = QLabel("GPIO Command States")
        states_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        states_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        states_layout.addWidget(states_title)
        
        # Create a text area for command states with proper sizing
        self.states_area = QTextEdit()
        self.states_area.setMinimumHeight(150)  # Ensure minimum height for visibility
        self.states_area.setReadOnly(True)
        self.states_area.setReadOnly(True)
        self.states_area.setMinimumHeight(100)
        self.states_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        states_layout.addWidget(self.states_area)
        
        # Add a small separator before log area
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.HLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        
        # Log area
        log_container = QWidget()
        log_container_layout = QVBoxLayout(log_container)
        log_container_layout.setContentsMargins(5, 5, 5, 5)
        
        # Add log title
        log_title = QLabel("Log Messages")
        log_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        log_title.setStyleSheet("font-weight: bold; font-size: 14px;")
        log_container_layout.addWidget(log_title)
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(100)
        self.log_area.setStyleSheet("""
            QTextEdit {
                background-color: #2d2d2d;
                color: #e0e0e0;
                border: 1px solid #3e3e3e;
                border-radius: 4px;
                padding: 5px;
                font-family: 'Consolas', 'Courier New', monospace;
            }
        """)
        log_container_layout.addWidget(self.log_area)
        
        # Add all sections to the main splitter
        splitter.addWidget(separator1)
        splitter.addWidget(states_container)
        splitter.addWidget(separator2)
        splitter.addWidget(log_container)
        
        # Configure splitter stretch factors
        splitter.setStretchFactor(0, 2)  # Banner/GPIO section
        splitter.setStretchFactor(1, 1)  # States section
        splitter.setStretchFactor(2, 1)  # Log section
        
        # Set initial sizes
        splitter.setSizes([self.height() * 2 // 3, self.height() // 3])
        
        # Add splitter to the parent layout
        parent_layout.addWidget(splitter)
    
    def _setup_ui(self):
        """Set up the main UI components."""
        # Add any additional UI setup here
        pass
    
    def _start_web_server(self):
        """Start the web server in a separate thread."""
        if self.web_server_running:
            QMessageBox.information(self, "Info", "Web server is already running")
            return
        
        try:
            # Disable start button and update status
            self.start_server_action.setEnabled(False)
            self.statusBar().showMessage("Starting web server...")
            
            # Create and configure the web server thread
            self.web_server_thread = WebServerThread(port=5000)
            self.web_server_thread.finished.connect(self._on_web_server_finished)
            
            # Start the thread
            self.web_server_thread.start()
            
            # Small delay to let the thread start
            if not self.web_server_thread.wait(500):  # Wait up to 500ms for thread to start
                logger.warning("Web server thread is taking longer than expected to start")
            
            # Update state and UI
            self.web_server_running = True
            self.stop_server_action.setEnabled(True)
            self.open_browser_action.setEnabled(True)
            
            logger.info("Web server started successfully")
            self.statusBar().showMessage("Web server started on http://localhost:5000", 3000)
                    
        except Exception as e:
            logger.error(f"Failed to start web server: {e}", exc_info=True)
            QMessageBox.critical(
                self, 
                "Error", 
                f"Failed to start web server: {str(e)}\n\nCheck the logs for more details."
            )
            self._on_web_server_finished()  # Clean up if there was an error
    
    def _stop_web_server(self):
        """Stop the web server gracefully without blocking the UI."""
        if not self.web_server_running or not self.web_server_thread:
            QMessageBox.information(self, "Info", "Web server is not running")
            return
        
        # Update UI immediately
        self.stop_server_action.setEnabled(False)
        self.statusBar().showMessage("Stopping web server...")
        
        # Use a timer to check the server status
        from PySide6.QtCore import QTimer
        
        def check_server_stopped():
            if not self.web_server_thread.isRunning():
                self._on_web_server_finished()
                logger.info("Web server stopped successfully")
            else:
                # Check again in 100ms
                QTimer.singleShot(100, check_server_stopped)
        
        # Request the server to stop in a separate thread
        def request_stop():
            try:
                if hasattr(self.web_server_thread, 'stop'):
                    self.web_server_thread.stop()
                else:
                    self.web_server_thread.quit()
                
                # Start checking if the server has stopped
                QTimer.singleShot(100, check_server_stopped)
                
            except Exception as e:
                logger.error(f"Error stopping web server: {e}")
                # Force termination if stop fails
                self.web_server_thread.terminate()
                self._on_web_server_finished()
        
        # Start the stop request in a separate thread
        import threading
        stop_thread = threading.Thread(target=request_stop, daemon=True)
        stop_thread.start()
    
    def _on_web_server_finished(self):
        """Handle web server thread finishing."""
        self.web_server_running = False
        
        # Update UI state
        self.start_server_action.setEnabled(True)
        self.stop_server_action.setEnabled(False)
        self.open_browser_action.setEnabled(False)
                
        # Clean up the thread
        if self.web_server_thread:
            if self.web_server_thread.isRunning():
                self.web_server_thread.terminate()
            self.web_server_thread = None
            
        self.statusBar().showMessage("Web server stopped", 3000)
    
    def _open_web_interface(self):
        """Open the web interface in the default browser."""
        if not self.web_server_running:
            QMessageBox.warning(self, "Warning", "Web server is not running")
            return
        
        webbrowser.open("http://localhost:5000")
    
    def _show_settings(self):
        """Show the settings dialog."""
        from gui.settings_dialog_qt import SettingsDialog
        settings_dialog = SettingsDialog(self)
        settings_dialog.settings_saved.connect(self._on_settings_saved)
        settings_dialog.exec()
    
    def _on_settings_saved(self):
        """Handle settings saved event."""
        # Reload any settings that affect the UI
        self.statusBar().showMessage(tr('settings_saved_message'), 3000)
    
    def _show_about(self):
        """Show the about dialog."""
        about = About(self)
        about.exec()
    
    def _show_help(self):
        """Show the help dialog."""
        help_dialog = Help(self)
        help_dialog.exec()
    
    def _show_sponsor(self):
        """Show the sponsor dialog."""
        sponsor_dialog = Sponsor(self)
        sponsor_dialog.exec()
    
    def _gpio_toggled(self, pin, state):
        """Handle GPIO button toggled event.
        
        Args:
            pin (int): The GPIO pin number (0-39)
            state (bool): The new state (True = on, False = off)
        """
        status = 'ON' if state else 'OFF'
        message = f"GPIO {pin} {status}"
        logger.info(message)
        
        # Update button style based on state
        button = self.gpio_buttons.get(pin)
        if button:
            # Common button styles
            base_style = (
                "QPushButton { "
                "font-weight: bold; "
                "border: 2px solid #2c3e50; "
                "border-radius: 6px; "
                "padding: 8px; "
                "margin: 2px; "
                "min-width: 20px; "
                "min-height: 5px; "
                "}"
                "QPushButton:hover { "
                "border: 2px solid #3498db; "
                "}"
            )
            
            if state:
                # Green gradient for ON state
                button.setStyleSheet(
                    base_style +
                    "QPushButton { "
                    "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
                    "stop:0 #2ecc71, stop:1 #27ae60); "  # Green gradient
                    "color: white; "
                    "font-size: 10pt; "
                    "}"
                    "QPushButton:pressed { "
                    "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
                    "stop:0 #27ae60, stop:1 #219653); "  # Darker green when pressed
                    "}"
                )
            else:
                # Red gradient for OFF state
                button.setStyleSheet(
                    base_style +
                    "QPushButton { "
                    "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
                    "stop:0 #e74c3c, stop:1 #c0392b); "  # Red gradient
                    "color: white; "
                    "font-size: 10pt; "
                    "opacity: 0.7; "
                    "}"
                    "QPushButton:pressed { "
                    "background: qlineargradient(x1:0, y1:0, x2:0, y2:1, "
                    "stop:0 #c0392b, stop:1 #a93226); "  # Darker red when pressed
                    "}"
                )
            
            # Add a tooltip with pin information
            button.setToolTip(f"GPIO {pin}\nClick to toggle state\nCurrent: {status}")
        
        # Update GPIO command states view with timestamp
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Format: HH:MM:SS.mmm
        state_text = self.states_area.toPlainText()
        
        # Add or update the pin state in the states area
        lines = state_text.split('\n') if state_text else []
        pin_found = False
        
        for i, line in enumerate(lines):
            if line.startswith(f"GPIO {pin}:"):
                lines[i] = f"GPIO {pin}: {status} (Last changed: {timestamp})"
                pin_found = True
                break
        
        if not pin_found:
            lines.append(f"GPIO {pin}: {status} (Last changed: {timestamp})")
        
        # Keep only the most recent 20 pin states
        if len(lines) > 20:
            lines = lines[-20:]
        
        # Update the states area
        self.states_area.setPlainText('\n'.join(lines))
        
        # Auto-scroll to bottom
        self.states_area.verticalScrollBar().setValue(
            self.states_area.verticalScrollBar().maximum()
        )
        
        # TODO: Implement actual GPIO control here
        
    def _show_gpio_control(self):
        """Show the GPIO control window."""
        from .gpio_window import GPIOWindow
        
        # Check if window already exists
        if not hasattr(self, 'gpio_window') or not self.gpio_window:
            self.gpio_window = GPIOWindow(self)
        
        self.gpio_window.show()
        self.gpio_window.raise_()
        self.gpio_window.activateWindow()
    
    def _view_logs(self):
        """Show the log viewer dialog."""
        log_viewer = LogViewer(self)
        log_viewer.exec()
        
    def _on_start_all_clicked(self):
        """Handle Start All button click - turn on all GPIO pins."""
        logger.info("Turning ON all GPIO pins")
        for pin, button in self.gpio_buttons.items():
            if not button.isChecked():
                button.setChecked(True)
                self._gpio_toggled(pin, True)
        
    def _on_stop_all_clicked(self):
        """Handle Stop All button click - turn off all GPIO pins."""
        logger.info("Turning OFF all GPIO pins")
        for pin, button in self.gpio_buttons.items():
            if button.isChecked():
                button.setChecked(False)
                self._gpio_toggled(pin, False)
    
    def _on_reset_clicked(self):
        """Handle Reset button click - reset all GPIO pins to default state (off)."""
        logger.info("Resetting all GPIO pins to default state")
        for pin, button in self.gpio_buttons.items():
            button.setChecked(False)
            self._gpio_toggled(pin, False)
        
        # Clear the states area
        self.states_area.clear()
        logger.info("All GPIO pins have been reset")
    
    def append_log(self, message):
        """Append a message to the log area."""
        self.log_area.append(message)
        # Auto-scroll to bottom
        self.log_area.verticalScrollBar().setValue(
            self.log_area.verticalScrollBar().maximum()
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.web_server_running:
            reply = QMessageBox.question(
                self, 
                'Confirm Exit',
                'Web server is still running. Are you sure you want to quit?',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self._stop_web_server()
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
