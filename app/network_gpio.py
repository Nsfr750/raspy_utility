"""
Network-based GPIO interface for remote Raspberry Pi control.

This module provides a drop-in replacement for RPi.GPIO that communicates
with a remote Raspberry Pi over the network.
"""
import logging
from typing import Optional, Dict, Any
from .network_client import NetworkGPIOClient, PinMode, PinState

logger = logging.getLogger(__name__)

class NetworkGPIO:
    """Network-based GPIO interface that mimics RPi.GPIO."""
    
    # Constants that match RPi.GPIO
    BCM = "BCM"
    BOARD = "BOARD"
    OUT = "OUT"
    IN = "IN"
    HIGH = 1
    LOW = 0
    PUD_UP = "PUD_UP"
    PUD_DOWN = "PUD_DOWN"
    
    _mode = None
    _client = None
    _initialized = False
    
    @classmethod
    def initialize(cls, base_url: str, api_key: Optional[str] = None):
        """Initialize the network GPIO client.
        
        Args:
            base_url: Base URL of the remote API (e.g., 'http://raspberrypi:8000')
            api_key: Optional API key for authentication
        """
        if cls._client is not None:
            cls.cleanup()
            
        cls._client = NetworkGPIOClient(base_url, api_key)
        cls._initialized = True
        logger.info(f"Initialized NetworkGPIO with base URL: {base_url}")
    
    @classmethod
    def setmode(cls, mode):
        """Set the pin numbering mode (BCM or BOARD)."""
        if mode not in (cls.BCM, cls.BOARD):
            raise ValueError("Mode must be either BCM or BOARD")
        cls._mode = mode
        logger.info(f"Set pin numbering mode to {mode}")
    
    @classmethod
    def setup(cls, pin, mode, pull_up_down=None):
        """Set up a GPIO pin on the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            mode: Pin mode (IN or OUT)
            pull_up_down: Optional pull up/down configuration (PUD_UP or PUD_DOWN)
        """
        if not cls._initialized:
            raise RuntimeError("NetworkGPIO not initialized. Call initialize() first.")
            
        pin_mode = PinMode.INPUT if mode == cls.IN else PinMode.OUTPUT
        initial = None
        
        # Convert pull up/down
        pud = None
        if pull_up_down == cls.PUD_UP:
            pud = "up"
            initial = PinState.HIGH if mode == cls.IN else None
        elif pull_up_down == cls.PUD_DOWN:
            pud = "down"
            initial = PinState.LOW if mode == cls.IN else None
        
        try:
            cls._client.setup_pin(
                pin=pin,
                mode=pin_mode,
                initial=initial,
                pull_up_down=pud
            )
            logger.info(f"Set up pin {pin} as {mode} (pull_up_down: {pull_up_down})")
        except Exception as e:
            logger.error(f"Failed to set up pin {pin}: {e}")
            raise
    
    @classmethod
    def output(cls, pin, value):
        """Set the output state of a GPIO pin on the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            value: Pin state (HIGH/1/True or LOW/0/False)
        """
        if not cls._initialized:
            raise RuntimeError("NetworkGPIO not initialized. Call initialize() first.")
            
        state = PinState.HIGH if value else PinState.LOW
        
        try:
            cls._client.set_pin_state(pin, state)
            logger.debug(f"Set pin {pin} to {state}")
        except Exception as e:
            logger.error(f"Failed to set pin {pin} to {value}: {e}")
            raise
    
    @classmethod
    def input(cls, pin):
        """Read the input state of a GPIO pin from the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            
        Returns:
            int: The current state of the pin (HIGH/1 or LOW/0)
        """
        if not cls._initialized:
            raise RuntimeError("NetworkGPIO not initialized. Call initialize() first.")
            
        try:
            pin_info = cls._client.get_pin_state(pin)
            state = pin_info.get('state', 'LOW')
            return cls.HIGH if state.upper() == 'HIGH' else cls.LOW
        except Exception as e:
            logger.error(f"Failed to read pin {pin}: {e}")
            return cls.LOW  # Return LOW as a safe default
    
    @classmethod
    def cleanup(cls, pin=None):
        """Clean up GPIO resources on the remote Raspberry Pi.
        
        Args:
            pin: Optional pin number to clean up. If None, clean up all pins.
        """
        if cls._client is None:
            return
            
        try:
            cls._client.cleanup(pin)
            logger.info(f"Cleaned up {f'pin {pin}' if pin else 'all pins'}")
        except Exception as e:
            logger.error(f"Failed to clean up {f'pin {pin}' if pin else 'all pins'}: {e}")
    
    @classmethod
    def setwarnings(cls, flag):
        """Enable or disable warning messages."""
        level = logging.WARNING if flag else logging.ERROR
        logger.setLevel(level)
        logger.debug(f"Set warnings to {'on' if flag else 'off'}")

# Create aliases for backward compatibility
setmode = NetworkGPIO.setmode
setup = NetworkGPIO.setup
output = NetworkGPIO.output
input = NetworkGPIO.input
cleanup = NetworkGPIO.cleanup
setwarnings = NetworkGPIO.setwarnings
BCM = NetworkGPIO.BCM
BOARD = NetworkGPIO.BOARD
OUT = NetworkGPIO.OUT
IN = NetworkGPIO.IN
HIGH = NetworkGPIO.HIGH
LOW = NetworkGPIO.LOW
PUD_UP = NetworkGPIO.PUD_UP
PUD_DOWN = NetworkGPIO.PUD_DOWN
