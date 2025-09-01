# Raspberry Pi Utility - Documentation

Welcome to the official documentation for the Raspberry Pi Utility application. This documentation provides all the necessary information to install, configure, and use the application effectively.

## Table of Contents

1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [API Reference](#api-reference)
5. [Development](#development)
6. [Troubleshooting](#troubleshooting)
7. [Contributing](#contributing)
8. [License](#license)

## Installation

### Prerequisites
- Raspberry Pi OS (Raspbian)
- Python 3.7 or higher
- Required system packages

### Setup Instructions
1. Clone the repository
2. Install dependencies
3. Configure the application

## Configuration

### Configuration Files
- `config.py` - Main configuration file
- `config.json` - User-specific settings

### Environment Variables
- `RASPY_UTILITY_DEBUG` - Enable debug mode
- `RASPY_UTILITY_CONFIG` - Path to custom config file

## Usage

### Basic Commands
```bash
python main.py
```

### Command Line Options
- `--help` - Show help message
- `--version` - Show version information
- `--config` - Specify config file

## API Reference

### GPIO Control
- `gpio_setup()` - Initialize GPIO
- `gpio_cleanup()` - Cleanup GPIO
- `set_pin()` - Set pin state

## Development

### Setting Up Development Environment
1. Create virtual environment
2. Install development dependencies
3. Run tests

### Testing
```bash
pytest tests/
```

## Troubleshooting

### Common Issues
1. **GPIO Access Denied**
   - Solution: Add user to gpio group
   
2. **Missing Dependencies**
   - Solution: Run `pip install -r requirements.txt`

## Contributing

We welcome contributions! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

---
© 2025 Nsfr750 | [GitHub](https://github.com/Nsfr750) | [Discord](https://discord.gg/ryqNeuRYjD)
