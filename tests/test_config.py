"""
Tests for the configuration manager module.

These tests verify the functionality of the configuration manager,
including loading from files, environment variables, and defaults.
"""
import os
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open

from struttura.config import ConfigManager

class TestConfigManager:
    """Test cases for the ConfigManager class."""
    
    @pytest.fixture
    def sample_config(self):
        """Return a sample configuration dictionary."""
        return {
            "app": {
                "name": "Test App",
                "version": "1.0.0",
                "debug": False
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
                "reload": False
            },
            "gpio": {
                "simulation_mode": True,
                "warnings": False,
                "default_mode": "output"
            },
            "logging": {
                "level": "INFO",
                "file": "gpio_control.log"
            },
            "ui": {
                "theme": "dark",
                "language": "en"
            }
        }
    
    @pytest.fixture
    def config_file(self, sample_config):
        """Create a temporary config file with sample data."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            json.dump(sample_config, f, indent=2)
            f.flush()
            yield Path(f.name)
        
        # Clean up after test
        if os.path.exists(f.name):
            os.unlink(f.name)
    
    def test_load_from_file(self, config_file, sample_config):
        """Test loading configuration from a file."""
        # Create a config manager and load from file
        config = ConfigManager(config_file=config_file)
        
        # Verify the config was loaded correctly
        assert config.get("app.name") == sample_config["app"]["name"]
        assert config.get("server.port") == sample_config["server"]["port"]
        assert config.get("gpio.simulation_mode") == sample_config["gpio"]["simulation_mode"]
    
    def test_load_nonexistent_file(self):
        """Test loading configuration from a non-existent file with defaults."""
        # Try to load from a non-existent file
        config = ConfigManager(config_file=Path("/nonexistent/config.json"))
        
        # Should not raise an exception and should use defaults
        assert config is not None
        assert config.get("app.name") is not None
    
    def test_environment_variables(self, monkeypatch, sample_config):
        """Test overriding config with environment variables."""
        # Set up environment variables
        monkeypatch.setenv("GPIO_APP_NAME", "Test From Env")
        monkeypatch.setenv("GPIO_SERVER_PORT", "9000")
        monkeypatch.setenv("GPIO_GPIO_SIMULATION_MODE", "True")
        
        # Create a config manager
        config = ConfigManager()
        
        # Verify environment variables take precedence
        assert config.get("app.name") == "Test From Env"
        assert config.get("server.port") == 9000  # Should be converted to int
        assert config.get("gpio.simulation_mode") is True  # Should be converted to bool
    
    def test_default_values(self):
        """Test that default values are used when no config is provided."""
        # Create a config manager with no config file
        config = ConfigManager()
        
        # Verify some default values
        assert isinstance(config.get("app.name"), str)
        assert isinstance(config.get("server.port"), int)
        assert isinstance(config.get("gpio.simulation_mode"), bool)
    
    def test_nested_keys(self, sample_config):
        """Test accessing nested configuration values."""
        # Create a config manager with sample config
        config = ConfigManager(config_dict=sample_config)
        
        # Test getting nested values
        assert config.get("app.name") == sample_config["app"]["name"]
        assert config.get("server.host") == sample_config["server"]["host"]
        
        # Test getting a section
        app_config = config.get_section("app")
        assert app_config["name"] == sample_config["app"]["name"]
        assert app_config["version"] == sample_config["app"]["version"]
    
    def test_nonexistent_key(self, sample_config):
        """Test accessing non-existent keys."""
        # Create a config manager with sample config
        config = ConfigManager(config_dict=sample_config)
        
        # Test getting non-existent keys with and without default
        assert config.get("nonexistent.key") is None
        assert config.get("nonexistent.key", default="default") == "default"
        
        # Test getting non-existent section
        assert config.get_section("nonexistent") is None
    
    def test_save_config(self, sample_config, tmp_path):
        """Test saving configuration to a file."""
        # Create a temporary file path
        config_path = tmp_path / "test_config.json"
        
        # Create a config manager and save to file
        config = ConfigManager(config_dict=sample_config)
        config.save(config_path)
        
        # Verify the file was created and contains the correct data
        assert config_path.exists()
        with open(config_path, 'r') as f:
            saved_config = json.load(f)
        
        assert saved_config == sample_config
    
    def test_update_config(self, sample_config):
        """Test updating configuration values."""
        # Create a config manager with sample config
        config = ConfigManager(config_dict=sample_config)
        
        # Update some values
        config.update("app.name", "Updated Name")
        config.update("server.port", 8080)
        config.update("new.setting", "value")
        
        # Verify the updates
        assert config.get("app.name") == "Updated Name"
        assert config.get("server.port") == 8080
        assert config.get("new.setting") == "value"
    
    def test_update_nested_section(self, sample_config):
        """Test updating a nested section of the config."""
        # Create a config manager with sample config
        config = ConfigManager(config_dict=sample_config)
        
        # Update a nested section
        new_ui_config = {
            "theme": "light",
            "language": "it",
            "new_setting": True
        }
        config.update_section("ui", new_ui_config)
        
        # Verify the updates
        assert config.get("ui.theme") == "light"
        assert config.get("ui.language") == "it"
        assert config.get("ui.new_setting") is True
        
        # Verify existing values not in the update are preserved
        assert "theme" in config.get_section("ui")
    
    def test_environment_variable_parsing(self, monkeypatch):
        """Test parsing of different environment variable types."""
        # Set up environment variables with different types
        monkeypatch.setenv("GPIO_TEST_INT", "42")
        monkeypatch.setenv("GPIO_TEST_FLOAT", "3.14")
        monkeypatch.setenv("GPIO_TEST_BOOL_TRUE1", "true")
        monkeypatch.setenv("GPIO_TEST_BOOL_TRUE2", "True")
        monkeypatch.setenv("GPIO_TEST_BOOL_FALSE1", "false")
        monkeypatch.setenv("GPIO_TEST_BOOL_FALSE2", "False")
        monkeypatch.setenv("GPIO_TEST_STRING", "hello world")
        monkeypatch.setenv("GPIO_TEST_EMPTY", "")
        
        # Create a config manager
        config = ConfigManager()
        
        # Test type conversion
        assert config._parse_value("42") == 42
        assert config._parse_value("3.14") == 3.14
        assert config._parse_value("true") is True
        assert config._parse_value("True") is True
        assert config._parse_value("false") is False
        assert config._parse_value("False") is False
        assert config._parse_value("hello") == "hello"
        assert config._parse_value("") == ""
        
        # Test with environment variables
        assert config.get("test.int") == 42
        assert config.get("test.float") == 3.14
        assert config.get("test.bool_true1") is True
        assert config.get("test.bool_true2") is True
        assert config.get("test.bool_false1") is False
        assert config.get("test.bool_false2") is False
        assert config.get("test.string") == "hello world"
        assert config.get("test.empty") == ""
    
    def test_config_merging(self):
        """Test that configs are merged correctly with precedence."""
        # Default config
        default_config = {
            "app": {
                "name": "Default App",
                "version": "1.0.0",
                "debug": False
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000
            }
        }
        
        # User config (overrides some defaults)
        user_config = {
            "app": {
                "name": "User App",
                "debug": True
            },
            "new_setting": "value"
        }
        
        # Create config with both
        config = ConfigManager(
            default_config=default_config,
            config_dict=user_config
        )
        
        # Verify merging
        assert config.get("app.name") == "User App"  # Overridden
        assert config.get("app.version") == "1.0.0"  # From default
        assert config.get("app.debug") is True  # Overridden
        assert config.get("server.host") == "0.0.0.0"  # From default
        assert config.get("new_setting") == "value"  # New setting
    
    def test_config_repr(self, sample_config):
        """Test the string representation of the config."""
        config = ConfigManager(config_dict=sample_config)
        config_str = str(config)
        
        # Should contain some expected keys
        assert "app" in config_str
        assert "server" in config_str
        assert "gpio" in config_str
        
        # Should not contain the actual values (for security)
        assert "password" not in config_str.lower()
        assert "secret" not in config_str.lower()
    
    def test_sensitive_data_handling(self):
        """Test that sensitive data is handled properly."""
        # Create a config with sensitive data
        sensitive_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "username": "user",
                "password": "s3cr3t",
                "api_key": "12345-67890-abcde"
            },
            "secret_key": "very-secret-key"
        }
        
        config = ConfigManager(config_dict=sensitive_config)
        config_str = str(config)
        
        # Sensitive data should be redacted
        assert "s3cr3t" not in config_str
        assert "12345-67890-abcde" not in config_str
        assert "very-secret-key" not in config_str
        
        # But the keys should still be visible
        assert "password" in config_str
        assert "api_key" in config_str
        assert "secret_key" in config_str
        
        # The actual values should still be accessible
        assert config.get("database.password") == "s3cr3t"
        assert config.get("database.api_key") == "12345-67890-abcde"
        assert config.get("secret_key") == "very-secret-key"
