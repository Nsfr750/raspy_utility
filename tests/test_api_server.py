"""
Tests for the API server module.

These tests verify the functionality of the REST API endpoints
using FastAPI's TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from fastapi import status
from unittest.mock import MagicMock, patch

from app.api_server import app
from struttura.gpio_manager import GPIOManager, PinMode, PinState, PinInfo

# Mock the GPIO manager for testing
@pytest.fixture
def mock_gpio_manager():
    """Create a mock GPIO manager."""
    with patch('app.api_server.gpio_manager') as mock_manager:
        # Set up mock manager with some test data
        mock_manager.get_pin_info.return_value = None
        mock_manager.get_all_pins.return_value = []
        mock_manager.simulation_mode = True
        yield mock_manager

@pytest.fixture
def api_client(mock_gpio_manager):
    """Create a test client for the API."""
    with TestClient(app) as client:
        yield client

class TestAPIServer:
    """Test cases for the API server endpoints."""
    
    def test_root_endpoint(self, api_client):
        """Test the root endpoint returns API information."""
        response = api_client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert data["status"] == "success"
        assert "version" in data["data"]
    
    def test_setup_pin(self, api_client, mock_gpio_manager):
        """Test setting up a new pin."""
        # Mock the pin info to return after setup
        pin_info = PinInfo(
            pin_number=17,
            mode=PinMode.OUTPUT,
            state=PinState.LOW,
            description="Test Pin"
        )
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request
        response = api_client.post(
            "/pins/17/setup",
            json={
                "mode": "output",
                "initial": "low",
                "description": "Test Pin"
            }
        )
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pin"] == 17
        assert data["mode"] == "OUTPUT"
        assert data["state"] == "LOW"
        assert data["description"] == "Test Pin"
        
        # Verify the GPIO manager was called
        mock_gpio_manager.setup_pin.assert_called_once()
    
    def test_set_pin_state(self, api_client, mock_gpio_manager):
        """Test setting the state of a pin."""
        # Mock the pin info
        pin_info = PinInfo(
            pin_number=17,
            mode=PinMode.OUTPUT,
            state=PinState.LOW,
            description="Test Pin"
        )
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request to set pin HIGH
        response = api_client.post(
            "/pins/17/state",
            json={"state": "high"}
        )
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pin"] == 17
        assert data["state"] == "HIGH"
        
        # Verify the GPIO manager was called
        mock_gpio_manager.set_pin_state.assert_called_once_with(17, PinState.HIGH)
    
    def test_get_pin_info(self, api_client, mock_gpio_manager):
        """Test getting information about a pin."""
        # Mock the pin info
        pin_info = PinInfo(
            pin_number=17,
            mode=PinMode.OUTPUT,
            state=PinState.HIGH,
            description="Test Pin"
        )
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request
        response = api_client.get("/pins/17")
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pin"] == 17
        assert data["mode"] == "OUTPUT"
        assert data["state"] == "HIGH"
        assert data["description"] == "Test Pin"
    
    def test_get_nonexistent_pin(self, api_client, mock_gpio_manager):
        """Test getting information about a non-existent pin."""
        # Mock the pin info to return None (pin not found)
        mock_gpio_manager.get_pin_info.return_value = None
        
        # Make the API request
        response = api_client.get("/pins/99")
        
        # Verify the response
        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()
    
    def test_set_pwm_duty_cycle(self, api_client, mock_gpio_manager):
        """Test setting the PWM duty cycle of a pin."""
        # Mock the pin info for a PWM pin
        pin_info = PinInfo(
            pin_number=18,
            mode=PinMode.PWM,
            state=PinState.LOW,
            pwm_frequency=1000,
            pwm_duty_cycle=0.0,
            description="PWM Test"
        )
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request to set duty cycle to 75%
        response = api_client.post(
            "/pins/18/pwm",
            json={"duty_cycle": 75.0}
        )
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["pin"] == 18
        assert data["pwm_duty_cycle"] == 75.0
        
        # Verify the GPIO manager was called
        mock_gpio_manager.set_pwm_duty_cycle.assert_called_once_with(18, 75.0)
    
    def test_list_pins(self, api_client, mock_gpio_manager):
        """Test listing all configured pins."""
        # Mock the list of pins
        pins = [
            (17, PinInfo(17, PinMode.OUTPUT, PinState.HIGH, description="LED 1")),
            (18, PinInfo(18, PinMode.INPUT, PinState.LOW, description="Button 1")),
        ]
        mock_gpio_manager.get_all_pins.return_value = pins
        
        # Make the API request
        response = api_client.get("/pins")
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["pin"] == 17
        assert data[1]["pin"] == 18
    
    def test_cleanup_pin(self, api_client, mock_gpio_manager):
        """Test cleaning up a pin."""
        # Mock the pin info
        pin_info = PinInfo(17, PinMode.OUTPUT, PinState.LOW)
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request to clean up the pin
        response = api_client.delete("/pins/17")
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        assert "17" in data["message"]
        
        # Verify the GPIO manager was called
        mock_gpio_manager.cleanup_pin.assert_called_once_with(17)
    
    def test_cleanup_all_pins(self, api_client, mock_gpio_manager):
        """Test cleaning up all pins."""
        # Make the API request to clean up all pins
        response = api_client.delete("/pins")
        
        # Verify the response
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "success"
        
        # Verify the GPIO manager was called
        mock_gpio_manager.cleanup_all.assert_called_once()
    
    def test_invalid_pin_mode(self, api_client, mock_gpio_manager):
        """Test setting up a pin with an invalid mode."""
        # Make the API request with an invalid mode
        response = api_client.post(
            "/pins/17/setup",
            json={"mode": "invalid_mode"}
        )
        
        # Verify the response indicates an error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_invalid_pin_state(self, api_client, mock_gpio_manager):
        """Test setting a pin to an invalid state."""
        # Mock the pin info
        pin_info = PinInfo(17, PinMode.OUTPUT, PinState.LOW)
        mock_gpio_manager.get_pin_info.return_value = pin_info
        
        # Make the API request with an invalid state
        response = api_client.post(
            "/pins/17/state",
            json={"state": "invalid_state"}
        )
        
        # Verify the response indicates an error
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
