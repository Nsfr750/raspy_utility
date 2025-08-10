"""
Network client for remote GPIO control.

This module provides a client to control GPIO pins on a remote Raspberry Pi
over a network connection using HTTP/HTTPS.
"""
import requests
from typing import Optional, Dict, Any
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class PinMode(str, Enum):
    """GPIO pin modes."""
    INPUT = "input"
    OUTPUT = "output"

class PinState(str, Enum):
    """GPIO pin states."""
    LOW = "low"
    HIGH = "high"

class NetworkGPIOClient:
    """Client for controlling GPIO pins on a remote Raspberry Pi."""
    
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initialize the network GPIO client.
        
        Args:
            base_url: Base URL of the remote API (e.g., 'http://raspberrypi:8000')
            api_key: Optional API key for authentication
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        if api_key:
            self.headers['X-API-Key'] = api_key
    
    def setup_pin(
        self, 
        pin: int, 
        mode: PinMode, 
        initial: Optional[PinState] = None,
        pull_up_down: Optional[str] = None,
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """Set up a GPIO pin on the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            mode: Pin mode (input/output)
            initial: Initial pin state (for output mode)
            pull_up_down: Pull up/down configuration
            description: Optional pin description
            
        Returns:
            Dictionary containing the pin configuration
        """
        url = f"{self.base_url}/pins/{pin}/setup"
        data = {
            'mode': mode.value,
        }
        if initial:
            data['initial'] = initial.value
        if pull_up_down:
            data['pull_up_down'] = pull_up_down
        if description:
            data['description'] = description
            
        try:
            response = self.session.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to setup pin {pin}: {e}")
            raise
    
    def set_pin_state(self, pin: int, state: PinState) -> Dict[str, Any]:
        """Set the state of a GPIO pin on the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            state: Desired pin state (high/low)
            
        Returns:
            Dictionary containing the updated pin state
        """
        url = f"{self.base_url}/pins/{pin}/state"
        data = {'state': state.value}
        
        try:
            response = self.session.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to set pin {pin} to {state}: {e}")
            raise
    
    def get_pin_state(self, pin: int) -> Dict[str, Any]:
        """Get the current state of a GPIO pin from the remote Raspberry Pi.
        
        Args:
            pin: GPIO pin number
            
        Returns:
            Dictionary containing the pin state and configuration
        """
        url = f"{self.base_url}/pins/{pin}"
        
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get state for pin {pin}: {e}")
            raise
    
    def get_all_pins(self) -> Dict[str, Any]:
        """Get the state of all configured GPIO pins from the remote Raspberry Pi.
        
        Returns:
            Dictionary containing all configured pins and their states
        """
        url = f"{self.base_url}/pins"
        
        try:
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get all pins: {e}")
            raise
    
    def cleanup(self, pin: Optional[int] = None) -> Dict[str, Any]:
        """Clean up GPIO resources on the remote Raspberry Pi.
        
        Args:
            pin: Optional pin number to clean up. If None, clean up all pins.
            
        Returns:
            Dictionary containing the cleanup status
        """
        if pin is not None:
            url = f"{self.base_url}/pins/{pin}/cleanup"
        else:
            url = f"{self.base_url}/cleanup"
        
        try:
            response = self.session.post(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to clean up {f'pin {pin}' if pin else 'all pins'}: {e}")
            raise
    
    def close(self):
        """Close the network session."""
        self.session.close()
        
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
