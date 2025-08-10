"""
GPIO Control Window (PySide6 Version)

This module provides a window for controlling GPIO pins.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QComboBox, QGroupBox, QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon

from struttura.logger import log_info, log_error
from struttura.lang import tr
from config import Config

class GPIOWindow(QDialog):
    """Window for controlling GPIO pins."""
    
    def __init__(self, parent=None):
        """Initialize the GPIO window.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(tr('gpio_control'))
        self.setMinimumSize(400, 300)
        
        # Load config
        self.config = Config()
        
        # Initialize GPIO state
        self.gpio_initialized = False
        self.pin_states = {}
        
        # Create UI
        self.setup_ui()
        
        # Set window modality
        self.setWindowModality(Qt.ApplicationModal)
    
    def setup_ui(self):
        """Set up the user interface."""
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # GPIO Control Group
        control_group = QGroupBox(tr('gpio_control'))
        control_layout = QFormLayout(control_group)
        
        # Pin selection
        self.pin_selector = QSpinBox()
        self.pin_selector.setRange(1, 40)
        self.pin_selector.setValue(17)
        control_layout.addRow(tr('select_pin') + ':', self.pin_selector)
        
        # Direction selection
        self.direction_combo = QComboBox()
        self.direction_combo.addItems([tr('input'), tr('output')])
        control_layout.addRow(tr('direction') + ':', self.direction_combo)
        
        # Initial state (for output)
        self.initial_state_combo = QComboBox()
        self.initial_state_combo.addItems([tr('low'), tr('high')])
        control_layout.addRow(tr('initial_state') + ':', self.initial_state_combo)
        
        # Setup button
        self.setup_button = QPushButton(tr('setup_gpio'))
        self.setup_button.clicked.connect(self.toggle_gpio_setup)
        control_layout.addRow(self.setup_button)
        
        # Status label
        self.status_label = QLabel(tr('gpio_not_initialized'))
        control_layout.addRow(self.status_label)
        
        # Add control group to main layout
        main_layout.addWidget(control_group)
        
        # Pin Control Group (shown after GPIO is initialized)
        self.pin_control_group = QGroupBox(tr('pin_control'))
        self.pin_control_layout = QVBoxLayout(self.pin_control_group)
        self.pin_control_group.setVisible(False)
        
        # Toggle button for output pins
        self.toggle_button = QPushButton(tr('toggle_pin'))
        self.toggle_button.clicked.connect(self.toggle_pin)
        self.pin_control_layout.addWidget(self.toggle_button)
        
        # Read button for input pins
        self.read_button = QPushButton(tr('read_pin'))
        self.read_button.clicked.connect(self.read_pin)
        self.pin_control_layout.addWidget(self.read_button)
        
        # Status display
        self.pin_status = QLabel()
        self.pin_control_layout.addWidget(self.pin_status)
        
        # Add pin control group to main layout
        main_layout.addWidget(self.pin_control_group)
        
        # Close button
        close_button = QPushButton(tr('close'))
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button, alignment=Qt.AlignRight)
        
        # Connect signals
        self.direction_combo.currentTextChanged.connect(self.update_ui_for_direction)
        self.update_ui_for_direction()
    
    def update_ui_for_direction(self):
        """Update UI based on selected direction."""
        is_output = self.direction_combo.currentText() == tr('output')
        self.initial_state_combo.setVisible(is_output)
        
        if self.gpio_initialized:
            self.toggle_button.setVisible(is_output)
            self.read_button.setVisible(not is_output)
    
    @Slot()
    def toggle_gpio_setup(self):
        """Toggle GPIO setup for the selected pin."""
        if not self.gpio_initialized:
            self.setup_gpio()
        else:
            self.cleanup_gpio()
    
    def setup_gpio(self):
        """Set up the selected GPIO pin."""
        try:
            pin = self.pin_selector.value()
            direction = self.direction_combo.currentText()
            
            # Here you would initialize the actual GPIO
            # For example:
            # import RPi.GPIO as GPIO
            # GPIO.setmode(GPIO.BCM if self.config.GPIO_MODE == 'BCM' else GPIO.BOARD)
            # if direction == tr('output'):
            #     initial_state = GPIO.HIGH if self.initial_state_combo.currentText() == tr('high') else GPIO.LOW
            #     GPIO.setup(pin, GPIO.OUT, initial=initial_state)
            # else:
            #     GPIO.setup(pin, GPIO.IN)
            
            self.gpio_initialized = True
            self.pin_states[pin] = False
            
            # Update UI
            self.setup_button.setText(tr('cleanup_gpio'))
            self.status_label.setText(tr('gpio_initialized').format(pin=pin, direction=direction))
            self.pin_control_group.setVisible(True)
            self.update_ui_for_direction()
            
            log_info(f"GPIO pin {pin} set up as {direction}")
            
        except Exception as e:
            log_error(f"Error setting up GPIO: {e}")
            QMessageBox.critical(self, tr('error'), tr('gpio_setup_error').format(error=str(e)))
    
    def cleanup_gpio(self):
        """Clean up GPIO resources."""
        try:
            # Here you would clean up the actual GPIO
            # For example:
            # import RPi.GPIO as GPIO
            # GPIO.cleanup()
            
            self.gpio_initialized = False
            
            # Update UI
            self.setup_button.setText(tr('setup_gpio'))
            self.status_label.setText(tr('gpio_not_initialized'))
            self.pin_control_group.setVisible(False)
            
            log_info("GPIO cleaned up")
            
        except Exception as e:
            log_error(f"Error cleaning up GPIO: {e}")
            QMessageBox.critical(self, tr('error'), tr('gpio_cleanup_error').format(error=str(e)))
    
    @Slot()
    def toggle_pin(self):
        """Toggle the state of an output pin."""
        if not self.gpio_initialized:
            return
            
        try:
            pin = self.pin_selector.value()
            new_state = not self.pin_states.get(pin, False)
            
            # Here you would toggle the actual GPIO pin
            # For example:
            # import RPi.GPIO as GPIO
            # GPIO.output(pin, GPIO.HIGH if new_state else GPIO.LOW)
            
            self.pin_states[pin] = new_state
            state_text = tr('high') if new_state else tr('low')
            self.pin_status.setText(tr('pin_state').format(pin=pin, state=state_text))
            
            log_info(f"Toggled pin {pin} to {state_text}")
            
        except Exception as e:
            log_error(f"Error toggling pin: {e}")
            QMessageBox.critical(self, tr('error'), tr('gpio_toggle_error').format(error=str(e)))
    
    @Slot()
    def read_pin(self):
        """Read the state of an input pin."""
        if not self.gpio_initialized:
            return
            
        try:
            pin = self.pin_selector.value()
            
            # Here you would read the actual GPIO pin
            # For example:
            # import RPi.GPIO as GPIO
            # state = GPIO.input(pin)
            state = False  # Placeholder
            
            state_text = tr('high') if state else tr('low')
            self.pin_status.setText(tr('pin_state').format(pin=pin, state=state_text))
            
            log_info(f"Read pin {pin}: {state_text}")
            
        except Exception as e:
            log_error(f"Error reading pin: {e}")
            QMessageBox.critical(self, tr('error'), tr('gpio_read_error').format(error=str(e)))
    
    def closeEvent(self, event):
        """Handle window close event."""
        if self.gpio_initialized:
            self.cleanup_gpio()
        event.accept()

# For testing
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    window = GPIOWindow()
    window.show()
    sys.exit(app.exec())
