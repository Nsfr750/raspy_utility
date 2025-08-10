"""
GPIO Manager for handling both local and remote GPIO operations.

This module provides a unified interface for GPIO operations that can work
with both local GPIO (RPi.GPIO) and remote GPIO (over network) interfaces.
"""
import logging
import importlib
from typing import Optional, Dict, Any, Union, Type, Tuple

# Import configuration
from config import Config

logger = logging.getLogger(__name__)

class GPIOManager:
    """Manager for GPIO operations that supports both local and remote GPIO."""
    
    def __init__(self):
        """Initialize the GPIO manager."""
        self.gpio = None
        self.gpio_type = None
        self.initialized = False
        self._setup_gpio()
    
    def _setup_gpio(self):
        """Set up the appropriate GPIO interface based on configuration."""
        if Config.REMOTE_GPIO_ENABLED:
            self._setup_remote_gpio()
        else:
            self._setup_local_gpio()
    
    def _setup_local_gpio(self):
        """Set up local GPIO interface."""
        try:
            # Try to import RPi.GPIO
            import RPi.GPIO as GPIO
            self.gpio = GPIO
            self.gpio_type = 'rpi'
            logger.info("Using RPi.GPIO for local GPIO access")
        except (ImportError, RuntimeError):
            # Fall back to GPIO simulator
            self.setup_local_gpio()
        
        # Initialize GPIO
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)
        self.initialized = True
    
    def setup_local_gpio(self) -> None:
        """Set up local GPIO using the simulator."""
        try:
            from .gpio_simulator import GPIOSimulator, BCM, BOARD
            self.gpio = GPIOSimulator()
            # Set the default mode to BCM (same as RPi.GPIO)
            self.gpio.setmode(BCM)
            self.initialized = True
            logger.info("Initialized GPIO Simulator in BCM mode")
        except Exception as e:
            logger.error(f"Failed to initialize GPIO Simulator: {e}")
            self.initialized = False
            raise
    
    def _setup_remote_gpio(self):
        """Set up remote GPIO interface."""
        from .network_client import NetworkGPIOClient
        from .network_gpio import NetworkGPIO
        
        try:
            client = NetworkGPIOClient(
                base_url=Config.REMOTE_GPIO_HOST,
                api_key=Config.REMOTE_GPIO_API_KEY,
                timeout=Config.REMOTE_GPIO_TIMEOUT
            )
            self.gpio = NetworkGPIO(client)
            self.gpio_type = 'remote'
            logger.info(f"Using remote GPIO at {Config.REMOTE_GPIO_HOST}")
            self.initialized = True
        except Exception as e:
            logger.error(f"Failed to initialize remote GPIO: {e}")
            # Fall back to local GPIO if remote fails
            logger.info("Falling back to local GPIO")
            self._setup_local_gpio()
    
    def setup(self, pin: int, mode: str, pull_up_down: Optional[str] = None, initial: Optional[Union[int, str]] = None) -> None:
        """Set up a GPIO pin.
        
        Args:
            pin: The pin number to set up
            mode: Either 'input' or 'output'
            pull_up_down: Optional pull up/down resistor setting ('PUD_UP' or 'PUD_DOWN')
            initial: Initial value for output pins (0/1 or 'low'/'high')
        """
        if not self.initialized:
            raise RuntimeError("GPIO manager not initialized")
        
        # Convert mode to GPIO constant
        gpio_mode = self.gpio.IN if mode.lower() == 'input' else self.gpio.OUT
        
        # Convert pull_up_down to GPIO constant if needed
        gpio_pud = None
        if pull_up_down:
            gpio_pud = getattr(self.gpio, pull_up_down.upper(), None)
        
        # Convert initial value if needed
        gpio_initial = None
        if initial is not None:
            if isinstance(initial, str):
                gpio_initial = self.gpio.HIGH if initial.lower() == 'high' else self.gpio.LOW
            else:
                gpio_initial = self.gpio.HIGH if initial else self.gpio.LOW
        
        # Call the appropriate setup method
        if gpio_initial is not None and gpio_mode == self.gpio.OUT:
            self.gpio.setup(pin, gpio_mode, initial=gpio_initial, pull_up_down=gpio_pud)
        else:
            self.gpio.setup(pin, gpio_mode, pull_up_down=gpio_pud)
    
    def output(self, pin: int, value: Union[int, str, bool]) -> None:
        """Set the output value of a GPIO pin.
        
        Args:
            pin: The pin number to set
            value: The value to set (0/1, 'high'/'low', or boolean)
        """
        if not self.initialized:
            raise RuntimeError("GPIO manager not initialized")
        
        # Convert value to GPIO constant if needed
        if isinstance(value, str):
            gpio_value = self.gpio.HIGH if value.lower() == 'high' else self.gpio.LOW
        else:
            gpio_value = self.gpio.HIGH if bool(value) else self.gpio.LOW
        
        self.gpio.output(pin, gpio_value)
    
    def input(self, pin: int) -> bool:
        """Read the input value of a GPIO pin.
        
        Args:
            pin: The pin number to read
            
        Returns:
            bool: True if pin is high, False if low
        """
        if not self.initialized:
            raise RuntimeError("GPIO manager not initialized")
            
        return bool(self.gpio.input(pin))
    
    def cleanup(self, pin: Optional[int] = None) -> None:
        """Clean up GPIO resources.
        
        Args:
            pin: Optional pin number to clean up, or None to clean up all pins
        """
        if not self.initialized:
            return
            
        self.gpio.cleanup(pin)
    
    def is_remote(self) -> bool:
        """Check if using remote GPIO.
        
        Returns:
            bool: True if using remote GPIO, False otherwise
        """
        return self.gpio_type == 'remote'
    
    def get_mode(self) -> str:
        """
        Get the current GPIO mode.
        
        Returns:
            str: The current mode ('BCM' or 'BOARD' or 'UNKNOWN' if not initialized).
        """
        if not self.initialized or not self.gpio:
            return "UNKNOWN"
        
        mode = self.gpio.get_mode()  # Get the global mode (BCM/BOARD)
        if mode == self.gpio.BCM:
            return 'BCM'
        elif mode == self.gpio.BOARD:
            return 'BOARD'
        return 'UNKNOWN'
    
    def get_pin(self, pin: int) -> Optional[Dict[str, Any]]:
        """Get information about a pin.
        
        Args:
            pin: The pin number
            
        Returns:
            Optional[Dict]: Pin information, or None if pin is not configured
        """
        if not self.initialized:
            return None
            
        # This is a simplified implementation - in a real application, you would
        # need to track pin states in the manager
        return {
            'pin': pin,
            'mode': 'input' if self.gpio.gpio_function(pin) == self.gpio.IN else 'output',
            'value': bool(self.gpio.input(pin))
        }
    
    def get_pins(self) -> Dict[int, Dict[str, Any]]:
        """Get information about all configured pins.
        
        Returns:
            Dict[int, Dict]: Dictionary mapping pin numbers to their information
        """
        if not self.initialized:
            return {}
            
        # This is a simplified implementation - in a real application, you would
        # need to track which pins have been configured
        return {}
    
    def get_all_pins(self) -> Dict[int, int]:
        """
        Get the current state of all GPIO pins.
        
        Returns:
            Dict[int, int]: A dictionary mapping pin numbers to their current values.
        """
        if not self.initialized or not self.gpio:
            return {}
            
        # For the simulator, we'll return all pins we're tracking
        # with their current states, defaulting to 0 (LOW) for pins we haven't seen
        pins = {}
        for pin in range(40):  # Standard Raspberry Pi has 40 GPIO pins
            try:
                pins[pin] = self.gpio.input(pin)
            except:
                pins[pin] = 0  # Default to LOW for uninitialized pins
        return pins
    
# Create a global instance of the GPIO manager
gpio_manager = GPIOManager()
