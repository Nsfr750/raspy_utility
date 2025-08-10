"""
Settings Dialog (PySide6 Version)

This module provides a settings dialog for configuring the application.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTabWidget, QWidget, QFormLayout, QLineEdit, QSpinBox,
    QComboBox, QCheckBox, QDialogButtonBox, QMessageBox, QFileDialog,
    QGroupBox
)
from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QIcon

from config import Config
from struttura.logger import log_info, log_error
from struttura.lang import tr

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""
    
    settings_saved = Signal()  # Signal emitted when settings are saved
    
    def __init__(self, parent=None):
        """Initialize the settings dialog.
        
        Args:
            parent: The parent widget
        """
        super().__init__(parent)
        self.setWindowTitle(tr('settings_title'))
        self.setMinimumSize(500, 400)
        
        # Load current settings
        self.config = Config()
        
        # Get current settings from config class attributes
        self.settings = {
            'general': {
                'start_minimized': False,  # Default value
                'check_updates': True,     # Default value
            },
            'server': {
                'host': self.config.HOST,
                'port': self.config.PORT,
            },
            'appearance': {
                'theme': 'system',  # Default value
                'language': 'en',   # Default value
            },
            'gpio': {
                'mode': self.config.GPIO_MODE,
                'led_pin': self.config.DEFAULT_PINS.get('LED', 17),
                'button_pin': self.config.DEFAULT_PINS.get('BUTTON', 27),
                'remote_enabled': self.config.REMOTE_GPIO_ENABLED,
                'remote_host': self.config.REMOTE_GPIO_HOST,
                'remote_api_key': self.config.REMOTE_GPIO_API_KEY or ''
            }
        }
        
        # Create UI
        self.setup_ui()
        
        # Set window modality
        self.setWindowModality(Qt.ApplicationModal)
    
    def setup_ui(self):
        """Set up the user interface."""
        # Create main layout
        main_layout = QVBoxLayout(self)
        
        # Create tab widget
        self.tabs = QTabWidget()
        
        # Add tabs
        self.general_tab = self.create_general_tab()
        self.network_tab = self.create_network_tab()
        self.gpio_tab = self.create_gpio_tab()
        self.appearance_tab = self.create_appearance_tab()
        
        self.tabs.addTab(self.general_tab, tr('general'))
        self.tabs.addTab(self.network_tab, tr('network'))
        self.tabs.addTab(self.gpio_tab, tr('gpio_settings'))
        self.tabs.addTab(self.appearance_tab, tr('appearance'))
        
        main_layout.addWidget(self.tabs)
        
        # Add buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.Apply).clicked.connect(self.apply_settings)
        
        main_layout.addWidget(button_box)
    
    def create_general_tab(self) -> QWidget:
        """Create the general settings tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        
        # Add general settings widgets here
        self.start_minimized = QCheckBox(tr('start_minimized'))
        self.start_minimized.setChecked(self.settings.get('general.start_minimized', False))
        layout.addRow(tr('start_minimized') + ':', self.start_minimized)
        
        self.check_updates = QCheckBox(tr('check_updates_on_startup'))
        self.check_updates.setChecked(self.settings.get('general.check_updates', True))
        layout.addRow(tr('check_updates') + ':', self.check_updates)
        
        # Add more settings as needed
        
        return tab
    
    def create_network_tab(self) -> QWidget:
        """Create the network settings tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        
        # Server host
        self.server_host = QLineEdit(self.settings['server']['host'])
        layout.addRow(tr('server_host') + ':', self.server_host)
        
        # Server port
        self.server_port = QSpinBox()
        self.server_port.setRange(1024, 65535)
        self.server_port.setValue(self.settings['server']['port'])
        layout.addRow(tr('server_port') + ':', self.server_port)
        
        return tab
    
    def create_gpio_tab(self) -> QWidget:
        """Create the GPIO settings tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        
        # GPIO Mode
        self.gpio_mode = QComboBox()
        self.gpio_mode.addItems(['BCM', 'BOARD'])
        self.gpio_mode.setCurrentText(self.settings['gpio']['mode'])
        layout.addRow(tr('gpio_mode') + ':', self.gpio_mode)
        
        # LED Pin
        self.led_pin = QSpinBox()
        self.led_pin.setRange(1, 40)
        self.led_pin.setValue(self.settings['gpio']['led_pin'])
        layout.addRow(tr('led_pin') + ':', self.led_pin)
        
        # Button Pin
        self.button_pin = QSpinBox()
        self.button_pin.setRange(1, 40)
        self.button_pin.setValue(self.settings['gpio']['button_pin'])
        layout.addRow(tr('button_pin') + ':', self.button_pin)
        
        # Remote GPIO Group
        remote_group = QGroupBox(tr('remote_gpio'))
        remote_layout = QFormLayout(remote_group)
        
        # Remote GPIO Enabled
        self.remote_enabled = QCheckBox(tr('enable_remote_gpio'))
        self.remote_enabled.setChecked(self.settings['gpio']['remote_enabled'])
        remote_layout.addRow(self.remote_enabled)
        
        # Remote Host
        self.remote_host = QLineEdit(self.settings['gpio']['remote_host'])
        remote_layout.addRow(tr('remote_host') + ':', self.remote_host)
        
        # Remote API Key
        self.remote_api_key = QLineEdit(self.settings['gpio']['remote_api_key'] or '')
        self.remote_api_key.setEchoMode(QLineEdit.Password)
        remote_layout.addRow(tr('api_key') + ':', self.remote_api_key)
        
        layout.addRow(remote_group)
        
        # Connect signals
        self.remote_enabled.toggled.connect(self._update_remote_controls)
        self._update_remote_controls()
        
        return tab
    
    def _update_remote_controls(self):
        """Update the enabled state of remote controls based on checkbox."""
        enabled = self.remote_enabled.isChecked()
        self.remote_host.setEnabled(enabled)
        self.remote_api_key.setEnabled(enabled)
    
    def create_appearance_tab(self) -> QWidget:
        """Create the appearance settings tab."""
        tab = QWidget()
        layout = QFormLayout(tab)
        
        # Theme selection
        self.theme = QComboBox()
        self.theme.addItems(['light', 'dark', 'system'])
        current_theme = self.settings.get('appearance.theme', 'system')
        self.theme.setCurrentText(current_theme)
        layout.addRow(tr('theme') + ':', self.theme)
        
        # Language selection
        self.language = QComboBox()
        self.language.addItems(['en', 'it'])  # Add more languages as needed
        current_lang = self.settings.get('appearance.language', 'en')
        self.language.setCurrentText(current_lang)
        layout.addRow(tr('language') + ':', self.language)
        
        # Add more appearance settings as needed
        
        return tab
    
    def get_settings(self) -> dict:
        """Get the current settings from the UI."""
        settings = {
            'general': {
                'start_minimized': self.start_minimized.isChecked(),
                'check_updates': self.check_updates.isChecked(),
            },
            'server': {
                'host': self.server_host.text(),
                'port': self.server_port.value(),
            },
            'gpio': {
                'mode': self.gpio_mode.currentText(),
                'led_pin': self.led_pin.value(),
                'button_pin': self.button_pin.value(),
                'remote_enabled': self.remote_enabled.isChecked(),
                'remote_host': self.remote_host.text(),
                'remote_api_key': self.remote_api_key.text()
            },
            'appearance': {
                'theme': self.theme.currentText(),
                'language': self.language.currentText(),
            }
        }
        return settings
    
    @Slot()
    def apply_settings(self):
        """Apply the current settings."""
        try:
            settings = self.get_settings()
            
            # Save settings to config
            # Update config attributes directly
            if 'server' in settings:
                server = settings['server']
                if 'host' in server:
                    self.config.HOST = server['host']
                if 'port' in server:
                    self.config.PORT = int(server['port'])
            
            if 'gpio' in settings:
                gpio = settings['gpio']
                if 'mode' in gpio:
                    self.config.GPIO_MODE = gpio['mode']
                if 'led_pin' in gpio:
                    self.config.DEFAULT_PINS['LED'] = int(gpio['led_pin'])
                if 'button_pin' in gpio:
                    self.config.DEFAULT_PINS['BUTTON'] = int(gpio['button_pin'])
                if 'remote_enabled' in gpio:
                    self.config.REMOTE_GPIO_ENABLED = bool(gpio['remote_enabled'])
                if 'remote_host' in gpio:
                    self.config.REMOTE_GPIO_HOST = gpio['remote_host']
                if 'remote_api_key' in gpio:
                    self.config.REMOTE_GPIO_API_KEY = gpio['remote_api_key'] or None
            
            # Save settings to a file if needed
            # Note: The current Config class doesn't have a save method
            # You might want to implement this in the future
            log_info("Settings updated in memory")
            
            # Note: To persist settings, you'll need to implement a save method in the Config class
            # that writes the settings to a configuration file.
            
            # Emit signal that settings were saved
            self.settings_saved.emit()
            
            QMessageBox.information(
                self,
                tr('settings_saved'),
                tr('settings_saved_message'),
                QMessageBox.Ok
            )
            
        except Exception as e:
            log_error(f"Error saving settings: {e}")
            QMessageBox.critical(
                self,
                tr('error'),
                tr('error_saving_settings').format(error=str(e)),
                QMessageBox.Ok
            )
    
    def accept(self):
        """Handle OK button click."""
        self.apply_settings()
        super().accept()

# For testing
if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    dialog = SettingsDialog()
    if dialog.exec() == QDialog.Accepted:
        print("Settings saved")
    sys.exit()
