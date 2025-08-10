"""
GPIO Simulator for development and testing.

This module provides a simulated GPIO interface that can be used for development
and testing when a real Raspberry Pi is not available. It also includes a simple
HTTP server that can be used to control the GPIO pins remotely.
"""
import sys
import os
import logging
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Dict, Any, Optional, Tuple

logger = logging.getLogger(__name__)

# GPIO modes
BCM = 11
BOARD = 10

# Pin modes
IN = 1
OUT = 0

# Pin states
LOW = 0
HIGH = 1

# Pull up/down
PUD_UP = 31
PUD_DOWN = 32
PUD_OFF = 33

class GPIOSimulator:
    """Simulates RPi.GPIO for testing without hardware."""
    
    # Define constants as class attributes for easy access
    BCM = BCM
    BOARD = BOARD
    IN = IN
    OUT = OUT
    LOW = LOW
    HIGH = HIGH
    PUD_UP = PUD_UP
    PUD_DOWN = PUD_DOWN
    PUD_OFF = PUD_OFF
    
    def __init__(self):
        """Initialize the GPIO simulator."""
        self._mode = None
        self._warnings = True
        self._setup = False
        self._pins = {}
        self._modes = {}  # Track pin modes (IN/OUT)
        self._pull_ups = {}  # Track pull up/down states
        logger.info("GPIO Simulator initialized")
    
    def setmode(self, mode):
        """Set the numbering mode (BCM or BOARD)."""
        if mode not in (self.BCM, self.BOARD):
            if self._warnings:
                logger.warning("An invalid mode was passed to setmode()")
            return
        self._mode = mode
        logger.debug(f"GPIO mode set to {'BCM' if mode == self.BCM else 'BOARD'}")
    
    def getmode(self):
        """Get the current numbering mode."""
        return self._mode
    
    def setwarnings(self, flag):
        """Enable or disable warnings."""
        self._warnings = bool(flag)
    
    def setup(self, channel, direction, pull_up_down=None, initial=None):
        """Set up a GPIO channel or list of channels."""
        if isinstance(channel, list):
            for ch in channel:
                self.setup(ch, direction, pull_up_down, initial)
            return
            
        if direction not in (self.IN, self.OUT):
            if self._warnings:
                logger.warning("Invalid direction for setup")
            return
            
        self._modes[channel] = direction
        
        if pull_up_down is not None:
            self._pull_ups[channel] = pull_up_down
        
        if direction == self.OUT and initial is not None:
            self.output(channel, initial)
        else:
            self._pins[channel] = 0  # Default to LOW for inputs
    
    def output(self, channel, value):
        """Set output to a channel or list of channels."""
        if isinstance(channel, list):
            for i, ch in enumerate(channel):
                self.output(ch, value[i] if isinstance(value, (list, tuple)) else value)
            return
            
        if channel not in self._modes or self._modes[channel] != self.OUT:
            if self._warnings:
                logger.warning("Channel is not set up as output")
            return
            
        self._pins[channel] = 1 if value else 0
        logger.debug(f"GPIO {channel} set to {'HIGH' if value else 'LOW'}")
    
    def input(self, channel):
        """Read from a channel."""
        if channel not in self._modes:
            if self._warnings:
                logger.warning(f"Channel {channel} is not set up")
            return 0
            
        # Return the current state or default to LOW
        return self._pins.get(channel, 0)
    
    def cleanup(self, channel=None):
        """Clean up GPIO channels."""
        if channel is None:
            self._pins.clear()
            self._modes.clear()
            self._pull_ups.clear()
        else:
            if isinstance(channel, list):
                for ch in channel:
                    self.cleanup(ch)
            else:
                self._pins.pop(channel, None)
                self._modes.pop(channel, None)
                self._pull_ups.pop(channel, None)
        
        logger.debug(f"GPIO cleanup on channel {channel if channel is not None else 'all'}")
    
    def get_pin(self, channel):
        """Get the current value of a pin."""
        return self.input(channel)
    
    def get_mode(self, channel=None):
        """
        Get the current GPIO mode or a pin's mode.
        
        Args:
            channel: If None, returns the global mode (BCM/BOARD).
                    If specified, returns the mode of the pin (IN/OUT).
        """
        if channel is None:
            return self._mode
        return self._modes.get(channel)
    
    def get_pull_up_down(self, channel):
        """Get the pull up/down state of a pin."""
        return self._pull_ups.get(channel, self.PUD_OFF)
    
    def get_all_pins(self):
        """Get the state of all pins."""
        return dict(self._pins)
    
    # Add compatibility with RPi.GPIO
    def set_high(self, channel):
        """Set a channel to HIGH."""
        self.output(channel, self.HIGH)
    
    def set_low(self, channel):
        """Set a channel to LOW."""
        self.output(channel, self.LOW)
    
    def is_high(self, channel):
        """Check if a channel is HIGH."""
        return self.input(channel) == self.HIGH
    
    def is_low(self, channel):
        """Check if a channel is LOW."""
        return self.input(channel) == self.LOW


class GPIORequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the GPIO simulator API."""
    
    def __init__(self, *args, **kwargs):
        self.gpio = kwargs.pop('gpio')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests."""
        try:
            if self.path == '/':
                self._send_response(200, {
                    'status': 'success',
                    'data': {
                        'name': 'GPIO Simulator',
                        'version': '1.0.0',
                        'description': 'A simple GPIO simulator with HTTP API'
                    }
                })
            elif self.path == '/pins':
                self._send_response(200, {
                    'status': 'success',
                    'data': self.gpio.get_all_pins()
                })
            elif self.path.startswith('/pins/'):
                try:
                    pin = int(self.path.split('/')[2])
                    pin_info = {
                        'mode': self.gpio.get_mode(pin),
                        'pull_up_down': self.gpio.get_pull_up_down(pin),
                        'value': self.gpio.get_pin(pin)
                    }
                    if pin_info['mode'] is not None:
                        self._send_response(200, {
                            'status': 'success',
                            'data': pin_info
                        })
                    else:
                        self._send_response(404, {
                            'status': 'error',
                            'message': f'Pin {pin} not found'
                        })
                except (ValueError, IndexError):
                    self._send_response(400, {
                        'status': 'error',
                        'message': 'Invalid pin number'
                    })
            else:
                self._send_response(404, {
                    'status': 'error',
                    'message': 'Not found'
                })
        except Exception as e:
            logger.error(f"Error handling GET request: {e}")
            self._send_response(500, {
                'status': 'error',
                'message': 'Internal server error'
            })
    
    def do_POST(self):
        """Handle POST requests."""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode('utf-8')) if content_length > 0 else {}
            
            if self.path.startswith('/pins/') and '/setup' in self.path:
                # Handle pin setup
                try:
                    pin = int(self.path.split('/')[2])
                    mode = data.get('mode')
                    initial = data.get('initial')
                    pull_up_down = data.get('pull_up_down')
                    
                    if mode not in ('input', 'output'):
                        self._send_response(400, {
                            'status': 'error',
                            'message': 'Invalid mode. Must be "input" or "output"'
                        })
                        return
                    
                    self.gpio.setup(pin, self.gpio.IN if mode == 'input' else self.gpio.OUT, pull_up_down, initial)
                    
                    pin_info = {
                        'mode': self.gpio.get_mode(pin),
                        'pull_up_down': self.gpio.get_pull_up_down(pin),
                        'value': self.gpio.get_pin(pin)
                    }
                    self._send_response(200, {
                        'status': 'success',
                        'data': pin_info
                    })
                except (ValueError, IndexError):
                    self._send_response(400, {
                        'status': 'error',
                        'message': 'Invalid pin number'
                    })
            
            elif self.path.startswith('/pins/') and '/state' in self.path:
                # Handle pin state change
                try:
                    pin = int(self.path.split('/')[2])
                    state = data.get('state')
                    
                    if state not in ('high', 'low'):
                        self._send_response(400, {
                            'status': 'error',
                            'message': 'Invalid state. Must be "high" or "low"'
                        })
                        return
                    
                    self.gpio.output(pin, 1 if state == 'high' else 0)
                    
                    pin_info = {
                        'mode': self.gpio.get_mode(pin),
                        'pull_up_down': self.gpio.get_pull_up_down(pin),
                        'value': self.gpio.get_pin(pin)
                    }
                    self._send_response(200, {
                        'status': 'success',
                        'data': pin_info
                    })
                except (ValueError, IndexError):
                    self._send_response(400, {
                        'status': 'error',
                        'message': 'Invalid pin number'
                    })
            
            elif self.path.startswith('/pins/') and '/cleanup' in self.path:
                # Handle pin cleanup
                try:
                    pin = int(self.path.split('/')[2])
                    self.gpio.cleanup(pin)
                    self._send_response(200, {
                        'status': 'success',
                        'message': f'Pin {pin} cleaned up'
                    })
                except (ValueError, IndexError):
                    self._send_response(400, {
                        'status': 'error',
                        'message': 'Invalid pin number'
                    })
            
            elif self.path == '/cleanup':
                # Handle cleanup of all pins
                self.gpio.cleanup()
                self._send_response(200, {
                    'status': 'success',
                    'message': 'All pins cleaned up'
                })
            
            else:
                self._send_response(404, {
                    'status': 'error',
                    'message': 'Not found'
                })
        
        except json.JSONDecodeError:
            self._send_response(400, {
                'status': 'error',
                'message': 'Invalid JSON'
            })
        except Exception as e:
            logger.error(f"Error handling POST request: {e}")
            self._send_response(500, {
                'status': 'error',
                'message': 'Internal server error'
            })
    
    def _send_response(self, status_code, data):
        """Send a JSON response."""
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))


def start_simulator(host='0.0.0.0', port=5000):
    """Start the GPIO simulator server.
    
    Args:
        host: The host to bind to
        port: The port to listen on
        
    Returns:
        The server thread
    """
    gpio = GPIOSimulator()
    
    def handler(*args, **kwargs):
        return GPIORequestHandler(*args, gpio=gpio, **kwargs)
    
    server = HTTPServer((host, port), handler)
    
    def run_server():
        logger.info(f"Starting GPIO simulator on http://{host}:{port}")
        try:
            server.serve_forever()
        except Exception as e:
            logger.error(f"GPIO simulator error: {e}")
        finally:
            server.server_close()
    
    thread = threading.Thread(target=run_server, daemon=True)
    thread.start()
    
    # Return the GPIO instance and the server thread
    return gpio, thread


# Create a global instance of the GPIO simulator
GPIO = GPIOSimulator()

# Create aliases for the GPIO class
setmode = GPIO.setmode
setwarnings = GPIO.setwarnings
setup = GPIO.setup
output = GPIO.output
input = GPIO.input
cleanup = GPIO.cleanup

# Constants
BCM = "BCM"
BOARD = "BOARD"
OUT = "out"
IN = "in"
HIGH = 1
LOW = 0
PUD_UP = "PUD_UP"
PUD_DOWN = "PUD_DOWN"
