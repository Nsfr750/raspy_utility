"""
Menu handling utilities for PySide6 applications.

This module provides menu creation and management functionality
for the main application window.
"""

import os
import sys
import subprocess
from typing import Optional, Dict, Any, TYPE_CHECKING

from PySide6.QtWidgets import QMenuBar, QMenu, QMessageBox, QFileDialog
from PySide6.QtCore import Qt, Signal, QObject, QProcess
from PySide6.QtGui import QIcon, QPixmap, QAction, QKeySequence

# Import local modules
from .lang import tr, set_language
from .version import show_version

# Import dialogs from the new structure
try:
    from struttura.about import About
    from struttura.help import Help
    from struttura.sponsor import Sponsor
    from struttura.log_viewer import LogViewer
    from gui.settings_dialog import SettingsDialog
    from gui.gpio_window import GPIOWindow
    
    # Check if all required modules are available
    MODULES_AVAILABLE = all([
        About, Help, Sponsor, LogViewer, 
        SettingsDialog, GPIOWindow
    ])
except ImportError as e:
    MODULES_AVAILABLE = False
    print(f"Warning: Could not import all required modules: {e}")

# Language options
LANG_OPTIONS = {'English': 'en', 'Italiano': 'it'}


class GPIOMenuHandler(QObject):
    """Handler for GPIO-related menu actions."""
    
    # Signals
    simulator_started = Signal()
    simulator_stopped = Signal()
    
    def __init__(self, parent=None):
        """Initialize the GPIO menu handler."""
        super().__init__(parent)
        self.gpio_process: Optional[QProcess] = None
        self.gpio_menu: Optional[QMenu] = None
        self.gpio_start_action: Optional[QAction] = None
        self.gpio_stop_action: Optional[QAction] = None
    
    def create_gpio_menu(self, parent_menu: QMenu) -> Optional[QMenu]:
        """Create the GPIO menu.
        
        Args:
            parent_menu: The parent menu to add the GPIO menu to
            
        Returns:
            QMenu: The created GPIO menu, or None if not available
        """
        if not MODULES_AVAILABLE or 'GPIOWindow' not in globals():
            return None
            
        self.gpio_menu = QMenu(tr('menu_gpio'), parent_menu)
        
        # GPIO Control action
        gpio_control = QAction(tr('gpio_control'), self.gpio_menu)
        gpio_control.triggered.connect(self._show_gpio_control)
        self.gpio_menu.addAction(gpio_control)
        
        # Add separator
        self.gpio_menu.addSeparator()
        
        # GPIO Simulator actions
        self.gpio_start_action = QAction(tr('gpio_start_simulator'), self.gpio_menu)
        self.gpio_start_action.triggered.connect(self._start_gpio_simulator)
        
        self.gpio_stop_action = QAction(tr('gpio_stop_simulator'), self.gpio_menu)
        self.gpio_stop_action.triggered.connect(self._stop_gpio_simulator)
        self.gpio_stop_action.setEnabled(False)
        
        self.gpio_menu.addAction(self.gpio_start_action)
        self.gpio_menu.addAction(self.gpio_stop_action)
        
        return self.gpio_menu
    
    def _show_gpio_control(self):
        """Show the GPIO control window."""
        if 'GPIOWindow' in globals():
            gpio_window = GPIOWindow()
            gpio_window.exec()
    
    def _start_gpio_simulator(self):
        """Start the GPIO simulator."""
        try:
            self.gpio_process = QProcess()
            self.gpio_process.finished.connect(self._on_simulator_finished)
            
            # Start the simulator process
            script_path = os.path.join('app', 'gpio_simulator.py')
            if os.path.exists(script_path):
                self.gpio_process.start('python', [script_path])
                
                if self.gpio_start_action:
                    self.gpio_start_action.setEnabled(False)
                if self.gpio_stop_action:
                    self.gpio_stop_action.setEnabled(True)
                
                QMessageBox.information(
                    None,
                    tr('gpio_simulator'),
                    tr('gpio_simulator_started')
                )
                self.simulator_started.emit()
            else:
                QMessageBox.critical(
                    None,
                    tr('error'),
                    tr('simulator_script_not_found')
                )
                
        except Exception as e:
            QMessageBox.critical(
                None,
                tr('error'),
                f"{tr('error_starting_simulator')}: {str(e)}"
            )
    
    def _stop_gpio_simulator(self):
        """Stop the GPIO simulator."""
        if self.gpio_process and self.gpio_process.state() == QProcess.Running:
            self.gpio_process.terminate()
            self.gpio_process.waitForFinished(2000)  # Wait up to 2 seconds
            
            if self.gpio_start_action:
                self.gpio_start_action.setEnabled(True)
            if self.gpio_stop_action:
                self.gpio_stop_action.setEnabled(False)
            
            QMessageBox.information(
                None,
                tr('gpio_simulator'),
                tr('gpio_simulator_stopped')
            )
            self.simulator_stopped.emit()
        else:
            QMessageBox.warning(
                None,
                tr('warning'),
                tr('no_simulator_running')
            )
    
    def _on_simulator_finished(self, exit_code, exit_status):
        """Handle simulator process finished."""
        if self.gpio_start_action:
            self.gpio_start_action.setEnabled(True)
        if self.gpio_stop_action:
            self.gpio_stop_action.setEnabled(False)
        
        if exit_code != 0 or exit_status != QProcess.NormalExit:
            QMessageBox.critical(
                None,
                tr('error'),
                tr('simulator_crashed')
            )
        
        self.simulator_stopped.emit()


def create_menu_bar(parent) -> QMenuBar:
    """Create the main menu bar.
    
    Args:
        parent: The parent widget
        
    Returns:
        QMenuBar: The created menu bar
    """
    menubar = QMenuBar(parent)
    
    # File menu
    file_menu = menubar.addMenu(tr('menu_file'))
    
    # Exit action
    exit_action = QAction(tr('menu_exit'), parent)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.triggered.connect(parent.close)
    file_menu.addAction(exit_action)
    
    # View menu
    view_menu = menubar.addMenu(tr('menu_view'))

    # Log action
    log_action = QAction(tr('menu_view_log'), parent)
    log_action.triggered.connect(lambda: LogViewer(parent).exec())
    view_menu.addAction(log_action)
    
    # Tools menu
    tools_menu = menubar.addMenu(tr('menu_tools'))
    
    # Add GPIO menu if available
    gpio_handler = GPIOMenuHandler(parent)
    gpio_menu = gpio_handler.create_gpio_menu(tools_menu)
    if gpio_menu:
        tools_menu.addMenu(gpio_menu)
    
    # Add Settings action if available
    if MODULES_AVAILABLE and 'SettingsDialog' in globals():
        settings_action = QAction(tr('menu_settings'), parent)
        settings_action.triggered.connect(lambda: SettingsDialog(parent).exec())
        tools_menu.addAction(settings_action)
    
    # Help menu
    help_menu = menubar.addMenu(tr('menu_help'))
    
    # Help action
    if MODULES_AVAILABLE and 'Help' in globals():
        help_action = QAction(tr('menu_help'), parent)
        help_action.triggered.connect(lambda: Help(parent).exec())
        help_menu.addAction(help_action)
    
    # About action
    if MODULES_AVAILABLE and 'About' in globals():
        about_action = QAction(tr('menu_about'), parent)
        about_action.triggered.connect(lambda: About(parent).exec())
        help_menu.addAction(about_action)
    
    # Sponsor action
    if MODULES_AVAILABLE and 'Sponsor' in globals():
        sponsor_action = QAction(tr('menu_sponsor'), parent)
        sponsor_action.triggered.connect(lambda: Sponsor(parent).exec())
        help_menu.addAction(sponsor_action)
    
    help_menu.addSeparator()
    
    # Version action
    version_action = QAction(tr('menu_version'), parent)
    version_action.triggered.connect(lambda: show_version(parent))
    help_menu.addAction(version_action)
    
    # Language menu
    lang_menu = menubar.addMenu(tr('menu_language'))
    
    def set_lang_and_restart(lang_code):
        """Set language and restart the application."""
        set_language(lang_code)
        QMessageBox.information(
            parent,
            tr('restart_required'),
            tr('restart_to_apply_language')
        )
    
    for label, code in LANG_OPTIONS.items():
        action = QAction(label, parent)
        action.triggered.connect(
            lambda checked, c=code: set_lang_and_restart(c)
        )
        lang_menu.addAction(action)

    return menubar
