"""
A PySide6-based dialog to view application log files with filtering by log level.
Logs are read from the logs/ directory and can be filtered by date and log level.
"""
import os
import glob
from datetime import datetime
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QPushButton, QTextEdit, QApplication, QSizePolicy, QFileDialog, QFrame
)
from PySide6.QtCore import Qt, QDateTime

LOG_DIR = 'logs'
LOG_LEVELS = ["ALL", "INFO", "DEBUG", "WARNING", "CRITICAL", "ERROR"]

class LogViewer(QDialog):
    """A dialog to view the application log file with filtering by log level."""
    
    def __init__(self, parent=None):
        """Initialize the LogViewer dialog."""
        super().__init__(parent)
        self.setWindowTitle("Log Viewer")
        self.setMinimumSize(1000, 700)
        
        # Create main layout
        layout = QVBoxLayout(self)
        
        # Create filter controls
        filter_layout = QHBoxLayout()
        
        # Log file selection
        filter_layout.addWidget(QLabel("Log File:"))
        self.file_combo = QComboBox()
        self.file_combo.setMinimumWidth(250)  # Wider to show full filenames
        self.file_combo.setMaxVisibleItems(10)  # Show 10 items in dropdown
        self.file_combo.currentTextChanged.connect(self.update_display)
        filter_layout.addWidget(self.file_combo)
        
        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        filter_layout.addWidget(separator)
        
        # Log level filter
        filter_layout.addWidget(QLabel("Level:"))
        self.level_combo = QComboBox()
        self.level_combo.addItems(LOG_LEVELS)
        self.level_combo.currentTextChanged.connect(self.update_display)
        filter_layout.addWidget(self.level_combo)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.update_display)
        filter_layout.addWidget(refresh_btn)
        
        # Open logs directory button
        open_dir_btn = QPushButton("📂 Open Logs")
        open_dir_btn.clicked.connect(self.open_logs_directory)
        filter_layout.addWidget(open_dir_btn)
        
        # Add stretch to push close button to the right
        filter_layout.addStretch()
        
        # Close button
        close_btn = QPushButton("❌ Close")
        close_btn.clicked.connect(self.accept)
        filter_layout.addWidget(close_btn)
        
        layout.addLayout(filter_layout)
        
        # Create log display with monospace font
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        self.log_display.setFontFamily("Consolas")
        self.log_display.setFontPointSize(10)
        self.log_display.setLineWrapMode(QTextEdit.NoWrap)
        
        # Set dark theme for better readability
        self.log_display.setStyleSheet(
            "QTextEdit { background-color: #1e1e1e; color: #e0e0e0; }"
        )
        
        # Add to layout with stretch
        layout.addWidget(self.log_display)
        
        # Load available log files
        self.update_log_file_list()
        
        # Initial update
        self.update_display()
    
    def update_log_file_list(self):
        """Update the list of available log files."""
        # Clear current items
        self.file_combo.clear()
        
        # Add 'All Logs' option first
        self.file_combo.addItem("All Logs", None)
        
        # Find all log files in logs directory
        if os.path.exists(LOG_DIR):
            log_files = glob.glob(os.path.join(LOG_DIR, 'raspy_utility_*.log'))
            
            # Extract dates from filenames and sort them
            file_info = []
            for log_file in log_files:
                try:
                    # Get file stats
                    file_stat = os.stat(log_file)
                    file_size = file_stat.st_size / (1024 * 1024)  # Size in MB
                    
                    # Extract date from filename: raspy_utility_YYYY-MM-DD.log
                    filename = os.path.basename(log_file)
                    date_str = filename.replace('raspy_utility_', '').replace('.log', '')
                    date = datetime.strptime(date_str, '%Y-%m-%d')
                    
                    # Format display text: YYYY-MM-DD (Day) - X.XX MB
                    display_text = f"{date.strftime('%Y-%m-%d (%A)')} - {file_size:.2f} MB"
                    
                    file_info.append({
                        'date': date,
                        'path': log_file,
                        'display': display_text,
                        'size': file_size
                    })
                except (ValueError, OSError) as e:
                    logger.warning(f"Error processing log file {log_file}: {e}")
                    continue
            
            # Sort by date (newest first)
            file_info.sort(key=lambda x: x['date'], reverse=True)
            
            # Add to combo box with formatted display text
            for info in file_info:
                self.file_combo.addItem(info['display'], info['path'])
    
    def get_selected_log_files(self):
        """Get the list of log files to read based on selection."""
        current_data = self.file_combo.currentData()
        
        # If 'All Logs' is selected, return all log files
        if current_data is None:
            if os.path.exists(LOG_DIR):
                log_files = glob.glob(os.path.join(LOG_DIR, 'raspy_utility_*.log'))
                # Sort by modification time (newest first)
                return sorted(log_files, key=os.path.getmtime, reverse=True)
            return []
        
        # Otherwise return only the selected log file if it exists
        if os.path.exists(current_data):
            return [current_data]
        
        # If selected file doesn't exist, refresh the list and try again
        self.update_log_file_list()
        return []
    
    def load_log_lines(self):
        """Load log lines from the selected log files."""
        log_files = self.get_selected_log_files()
        
        if not log_files:
            return ["No log files found in the logs/ directory.\n"]
        
        all_lines = []
        
        for log_file in log_files:
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    # Add a header with the log file name
                    file_name = os.path.basename(log_file)
                    all_lines.append(f"\n=== {file_name} ===\n\n")
                    all_lines.extend(f"{line}" for line in f.readlines())
            except Exception as e:
                all_lines.append(f"Error reading log file {log_file}: {str(e)}\n")
        
        return all_lines
    
    def filter_lines(self, lines, level):
        """Filter log lines by the specified level."""
        if level == "ALL":
            return lines
            
        return [line for line in lines if f"[{level}]" in line]
    
    def open_logs_directory(self):
        """Open the logs directory in the system file explorer."""
        if os.path.exists(LOG_DIR):
            os.startfile(os.path.abspath(LOG_DIR))
    
    def update_display(self):
        """Update the log display with filtered log entries."""
        level = self.level_combo.currentText()
        
        # Show loading message
        self.log_display.setPlainText("Loading logs...")
        QApplication.processEvents()  # Update UI
        
        try:
            # Load and filter lines
            lines = self.load_log_lines()
            filtered_lines = self.filter_lines(lines, level)
            
            # Update display
            self.log_display.clear()
            self.log_display.setPlainText(''.join(filtered_lines))
            
            # Auto-scroll to bottom
            scrollbar = self.log_display.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            
            # Show status in the log display
            status = f"\n\n=== Showing {len(filtered_lines)} log entries ===\n"
            self.log_display.append(status)
        except Exception as e:
            self.log_display.setPlainText(f"Error loading logs: {str(e)}")

# For testing
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    viewer = LogViewer()
    viewer.show()
    sys.exit(app.exec())
