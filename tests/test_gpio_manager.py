"""
Tests for the GPIO Manager module.

These tests verify the core functionality of the GPIO manager,
including pin setup, state management, and cleanup.
"""
import pytest
from unittest.mock import MagicMock, patch

from struttura.gpio_manager import GPIOManager, PinMode, PinState, PinInfo

class TestGPIOManager:
    """Test cases for the GPIOManager class."""
    
    @pytest.fixture
    def mock_gpio(self):
        """Mock the RPi.GPIO module."""
        with patch('struttura.gpio_manager.GPIO') as mock_gpio:
            yield mock_gpio
    
    @pytest.fixture
    def gpio_manager(self, mock_gpio):
        """Create a GPIOManager instance for testing."""
        return GPIOManager(simulation_mode=False)
    
    def test_initialization(self, gpio_manager, mock_gpio):
        """Test that the GPIO manager initializes correctly."""
        # Verify GPIO setup
        mock_gpio.setmode.assert_called_once_with(mock_gpio.BCM)
        mock_gpio.setwarnings.assert_called_once_with(False)
        assert gpio_manager.simulation_mode is False
    
    def test_setup_pin_output(self, gpio_manager, mock_gpio):
        """Test setting up a pin in output mode."""
        # Setup a pin in output mode
        gpio_manager.setup_pin(
            pin=17,
            mode=PinMode.OUTPUT,
            initial=PinState.HIGH,
            description="Test Output"
        )
        
        # Verify pin was set up correctly
        mock_gpio.setup.assert_called_once_with(
            17, mock_gpio.OUT, initial=mock_gpio.HIGH
        )
        
        # Verify pin info was stored
        pin_info = gpio_manager.get_pin_info(17)
        assert pin_info is not None
        assert pin_info.pin_number == 17
        assert pin_info.mode == PinMode.OUTPUT
        assert pin_info.state == PinState.HIGH
        assert pin_info.description == "Test Output"
    
    def test_setup_pin_input(self, gpio_manager, mock_gpio):
        """Test setting up a pin in input mode."""
        # Setup a pin in input mode
        gpio_manager.setup_pin(
            pin=18,
            mode=PinMode.INPUT,
            description="Test Input"
        )
        
        # Verify pin was set up correctly
        mock_gpio.setup.assert_called_once_with(18, mock_gpio.IN)
        
        # Verify pin info was stored
        pin_info = gpio_manager.get_pin_info(18)
        assert pin_info is not None
        assert pin_info.mode == PinMode.INPUT
    
    def test_set_pin_state(self, gpio_manager, mock_gpio):
        """Test setting the state of an output pin."""
        # Setup a pin in output mode
        gpio_manager.setup_pin(17, PinMode.OUTPUT)
        
        # Set pin state to HIGH
        gpio_manager.set_pin_state(17, PinState.HIGH)
        
        # Verify the state was set
        mock_gpio.output.assert_called_once_with(17, mock_gpio.HIGH)
        assert gpio_manager.get_pin_info(17).state == PinState.HIGH
        
        # Set pin state to LOW
        gpio_manager.set_pin_state(17, PinState.LOW)
        
        # Verify the state was updated
        assert mock_gpio.output.call_count == 2
        mock_gpio.output.assert_called_with(17, mock_gpio.LOW)
        assert gpio_manager.get_pin_info(17).state == PinState.LOW
    
    def test_set_pwm_duty_cycle(self, gpio_manager, mock_gpio):
        """Test setting the duty cycle of a PWM pin."""
        # Setup a pin in PWM mode
        gpio_manager.setup_pin(
            pin=18,
            mode=PinMode.PWM,
            pwm_frequency=1000,
            description="PWM Test"
        )
        
        # Set duty cycle
        gpio_manager.set_pwm_duty_cycle(18, 50.0)
        
        # Verify PWM was configured
        pin_info = gpio_manager.get_pin_info(18)
        assert pin_info.pwm_duty_cycle == 50.0
        
        # The PWM object should be created and duty cycle set
        assert hasattr(pin_info, 'pwm')
        pin_info.pwm.ChangeDutyCycle.assert_called_once_with(50.0)
    
    def test_cleanup_pin(self, gpio_manager, mock_gpio):
        """Test cleaning up a single pin."""
        # Setup a pin
        gpio_manager.setup_pin(17, PinMode.OUTPUT)
        
        # Clean up the pin
        gpio_manager.cleanup_pin(17)
        
        # Verify cleanup was called
        mock_gpio.cleanup.assert_called_once_with(17)
        assert gpio_manager.get_pin_info(17) is None
    
    def test_cleanup_all(self, gpio_manager, mock_gpio):
        """Test cleaning up all pins."""
        # Setup multiple pins
        gpio_manager.setup_pin(17, PinMode.OUTPUT)
        gpio_manager.setup_pin(18, PinMode.INPUT)
        
        # Clean up all pins
        gpio_manager.cleanup_all()
        
        # Verify cleanup was called
        mock_gpio.cleanup.assert_called_once()
        assert gpio_manager.get_pin_info(17) is None
        assert gpio_manager.get_pin_info(18) is None
    
    def test_simulation_mode(self):
        """Test operation in simulation mode."""
        # Create a manager in simulation mode
        manager = GPIOManager(simulation_mode=True)
        
        # Setup a pin
        manager.setup_pin(17, PinMode.OUTPUT, initial=PinState.HIGH)
        
        # Verify pin was set up (no GPIO calls should be made)
        pin_info = manager.get_pin_info(17)
        assert pin_info is not None
        assert pin_info.state == PinState.HIGH
        
        # Change pin state
        manager.set_pin_state(17, PinState.LOW)
        assert manager.get_pin_info(17).state == PinState.LOW
        
        # Clean up (should not raise exceptions)
        manager.cleanup_all()
    
    def test_error_handling(self, gpio_manager, mock_gpio):
        """Test error handling for invalid operations."""
        # Try to set state on a pin that's not set up
        with pytest.raises(ValueError, match="Pin 99 not found"):
            gpio_manager.set_pin_state(99, PinState.HIGH)
        
        # Try to set PWM duty cycle on a non-PWM pin
        gpio_manager.setup_pin(17, PinMode.OUTPUT)
        with pytest.raises(ValueError, match="Pin 17 is not in PWM mode"):
            gpio_manager.set_pwm_duty_cycle(17, 50.0)
        
        # Try to set up a pin that's already set up
        gpio_manager.setup_pin(18, PinMode.INPUT)
        with pytest.raises(ValueError, match="Pin 18 is already configured"):
            gpio_manager.setup_pin(18, PinMode.OUTPUT)
