"""
Logger module for the application with daily log rotation.
Creates a new log file each day in the logs/ directory.
"""
import os
import sys
import threading
import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

# Ensure logs directory exists
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs'))
try:
    os.makedirs(LOG_DIR, exist_ok=True)
    print(f"Logs will be saved in: {LOG_DIR}")
except Exception as e:
    print(f"Error creating logs directory: {e}")
    # Fallback to current directory if we can't create the logs directory
    LOG_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"Falling back to: {LOG_DIR}")

# Configure logging
LOG_FORMAT = '%(asctime)s [%(levelname)s] %(message)s'
LOG_LEVELS = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

# Create a lock for thread-safe logging
_log_lock = threading.Lock()

class DailyRotatingFileHandler(TimedRotatingFileHandler):
    """Custom handler that rotates logs at midnight and keeps a backup of old logs.
    Creates files with names like 'raspy_utility_YYYY-MM-DD.log'.
    """
    def __init__(self, filename, **kwargs):
        self.filename = filename
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.baseFilename = os.path.join(LOG_DIR, f"{filename}_{self.current_date}.log")
        
        # Initialize with a long rotation interval since we handle the date in the filename
        super().__init__(
            self.baseFilename,
            when='midnight',
            interval=3650,  # 10 years (effectively disable rotation since we handle it)
            backupCount=30,  # Keep logs for 30 days
            encoding='utf-8',
            **kwargs
        )
        
    def shouldRollover(self, record):
        """Determine if the log should roll over to a new file."""
        # Check if the date has changed
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        if current_date != self.current_date:
            return True
        return False
        
    def doRollover(self):
        """Create a new log file with the current date."""
        # Close the old file
        if self.stream:
            self.stream.close()
            self.stream = None
            
        # Update the current date and base filename
        self.current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        self.baseFilename = os.path.join(LOG_DIR, f"{self.filename}_{self.current_date}.log")
        
        # Create the new log file
        if not self.delay:
            self.stream = self._open()
            
        # Clean up old log files
        self._clean_old_logs()
    
    def _clean_old_logs(self):
        """Remove log files older than backupCount days."""
        import time
        from datetime import datetime, timedelta
        
        if self.backupCount <= 0:
            return
            
        # Get all log files for this logger
        log_dir = os.path.dirname(self.baseFilename)
        base_name = os.path.basename(self.filename)
        log_files = []
        
        for f in os.listdir(log_dir):
            if f.startswith(base_name) and f.endswith('.log'):
                try:
                    # Extract date from filename
                    date_str = f.replace(f"{base_name}_", "").replace(".log", "")
                    file_date = datetime.strptime(date_str, "%Y-%m-%d")
                    log_files.append((file_date, os.path.join(log_dir, f)))
                except ValueError:
                    continue
        
        # Sort by date (oldest first)
        log_files.sort()
        
        # Remove old files if we have more than backupCount
        while len(log_files) > self.backupCount:
            _, old_file = log_files.pop(0)
            try:
                os.remove(old_file)
            except OSError:
                pass

# Configure the root logger
def setup_logger(name='raspy_utility'):
    """Set up and return a logger with daily rotation.
    
    Args:
        name (str): Name of the logger
        
    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Don't propagate to root logger
    logger.propagate = False
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    
    # Add file handler with daily rotation
    file_handler = DailyRotatingFileHandler(name)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    
    # Add console handler for errors and above
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    
    # Remove any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add the handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Create the main application logger
logger = setup_logger()

# Convenience functions
def log_debug(message):
    """Log a debug message."""
    logger.debug(message)

def log_info(message):
    """Log an info message."""
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)

def log_error(message):
    """Log an error message."""
    logger.error(message)

def log_critical(message):
    """Log a critical message."""
    logger.critical(message)

def log_exception(exception, message=None):
    """Log an exception with an optional message."""
    if message:
        logger.error(message, exc_info=exception)
    else:
        logger.exception(exception)

def setup_global_exception_logging():
    """Set up global exception handling to log all uncaught exceptions."""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            # Call the default handler for keyboard interrupts
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
            
        logger.critical("Uncaught exception", 
                      exc_info=(exc_type, exc_value, exc_traceback))
    
    sys.excepthook = handle_exception

# Set up global exception handling when the module is imported
setup_global_exception_logging()

# Add a startup message
log_info("Logger initialized")

# For backward compatibility
log_all = log_debug
