"""
Pytest configuration and fixtures for the test suite.
"""
import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Generator, Dict, Any

import pytest
from _pytest.config import Config

# Add the project root to the Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test configuration
TEST_CONFIG = {
    "app": {
        "name": "Test App",
        "version": "1.0.0",
        "debug": True,
    },
    "server": {
        "host": "127.0.0.1",
        "port": 8000,
        "reload": False,
    },
    "gpio": {
        "simulation_mode": True,
        "warnings": False,
        "default_mode": "output",
    },
    "logging": {
        "level": "DEBUG",
        "file": "test.log",
        "max_size": 1048576,  # 1MB
        "backup_count": 3,
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "datefmt": "%Y-%m-%d %H:%M:%S",
    },
    "ui": {
        "theme": "dark",
        "language": "en",
    },
}

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Return the project root directory."""
    return PROJECT_ROOT

@pytest.fixture(scope="session")
def test_config() -> Dict[str, Any]:
    """Return the test configuration."""
    return TEST_CONFIG

@pytest.fixture(scope="function")
def temp_dir() -> Generator[Path, None, None]:
    """Create and clean up a temporary directory for tests."""
    temp_dir = Path(tempfile.mkdtemp(prefix="pytest_"))
    yield temp_dir
    if temp_dir.exists():
        shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture(scope="function")
def test_log_file(temp_dir: Path) -> Path:
    """Return a path to a test log file."""
    log_file = temp_dir / "test.log"
    if log_file.exists():
        log_file.unlink()
    return log_file

def pytest_configure(config: Config) -> None:
    """Configure pytest with custom settings."""
    # Register custom markers
    config.addinivalue_line(
        "markers",
        "integration: mark test as an integration test (deselect with '-m "
        "not integration')",
    )
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test (deselect with '-m unit')"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test (deselect with '-m not e2e')"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow (deselect with '-m "
        "not slow')",
    )

# Skip tests that require hardware if not on a Raspberry Pi
try:
    import RPi.GPIO as GPIO  # noqa: F401
    ON_RASPBERRY_PI = True
except (ImportError, RuntimeError):
    ON_RASPBERRY_PI = False

def pytest_runtest_setup(item: pytest.Item) -> None:
    """Skip tests that require hardware if not on a Raspberry Pi."""
    if any(marker.name == "hardware" for marker in item.iter_markers()):
        if not ON_RASPBERRY_PI:
            pytest.skip("Test requires Raspberry Pi hardware")

# Add a command-line option to run hardware tests
def pytest_addoption(parser: pytest.Parser) -> None:
    """Add custom command-line options to pytest."""
    parser.addoption(
        "--run-hardware",
        action="store_true",
        default=False,
        help="run tests that require hardware (Raspberry Pi)",
    )

# Configure test collection
def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """Modify test collection based on command-line options."""
    if not config.getoption("--run-hardware"):
        skip_hardware = pytest.mark.skip(
            reason="need --run-hardware option to run"
        )
        for item in items:
            if "hardware" in item.keywords:
                item.add_marker(skip_hardware)

# Configure logging for tests
@pytest.fixture(autouse=True)
def setup_logging() -> None:
    """Configure logging for tests."""
    import logging
    
    # Set up basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # Disable logging for external libraries
    for logger_name in ["urllib3", "asyncio"]:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
