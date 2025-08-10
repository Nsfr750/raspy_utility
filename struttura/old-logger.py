import datetime
import sys
import threading
import os

# Ensure logs directory exists
LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR, exist_ok=True)

def get_log_file():
    """Generate log file path with current date."""
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    return os.path.join(LOG_DIR, f'raspy_utility_{date_str}.log')
LOG_LEVELS = ("ALL", "INFO", "DEBUG", "WARNING", "CRITICAL","ERROR")

_log_lock = threading.Lock()

def _write_log(level, message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    log_file = get_log_file()
    with _log_lock:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry)

def log_all(message):
    _write_log("ALL", message)
def log_info(message):
    _write_log("INFO", message)
def log_debug(message):
    _write_log("DEBUG", message)
def log_warning(message):
    _write_log("WARNING", message)
def log_critical(message):
    _write_log("CRITICAL", message)
def log_error(message):
    _write_log("ERROR", message)

def log_exception(exc_type, exc_value, exc_tb):
    import traceback
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_file = get_log_file()
    with _log_lock:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[{timestamp}] [ERROR] Uncaught exception:\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)

def setup_global_exception_logging():
    sys.excepthook = log_exception
