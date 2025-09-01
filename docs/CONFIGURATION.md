# Configuration Guide

This guide explains how to configure the Raspberry Pi Utility to suit your specific needs.

## Table of Contents
- [Configuration Files](#configuration-files)
- [Environment Variables](#environment-variables)
- [GPIO Configuration](#gpio-configuration)
- [Web Interface Settings](#web-interface-settings)
- [Security Settings](#security-settings)
- [Logging Configuration](#logging-configuration)
- [Backup and Restore](#backup-and-restore)

## Configuration Files

The application uses the following configuration files:

1. `config.json` - Main configuration file
2. `gpio_config.json` - GPIO pin configurations
3. `schedules.json` - Scheduled tasks
4. `users.json` - User accounts and permissions

## Environment Variables

You can override configuration settings using environment variables:

```bash
# Application settings
export RASPY_UTILITY_DEBUG=true
export RASPY_UTILITY_CONFIG=/path/to/config.json

# Web server settings
export FLASK_APP=app.py
export FLASK_ENV=production

# Database settings
export DATABASE_URL=sqlite:///instance/raspy_utility.db

# Security settings
export SECRET_KEY=your-secret-key-here
export JWT_SECRET_KEY=your-jwt-secret-here
```

## GPIO Configuration

### Pin Configuration

Edit `gpio_config.json` to configure your GPIO pins:

```json
{
  "pins": [
    {
      "pin": 17,
      "name": "Living Room Light",
      "mode": "OUT",
      "initial_state": 0,
      "pull_up_down": "PUD_OFF",
      "pwm": {
        "enabled": false,
        "frequency": 100,
        "duty_cycle": 0
      },
      "safety": {
        "max_on_time": 3600,
        "cooldown": 300
      }
    },
    {
      "pin": 18,
      "name": "Temperature Sensor",
      "mode": "IN",
      "pull_up_down": "PUD_UP"
    }
  ]
}
```

### Configuration Options

| Setting | Type | Description |
|---------|------|-------------|
| `pin` | integer | BCM pin number |
| `name` | string | Friendly name for the pin |
| `mode` | string | `IN` or `OUT` |
| `initial_state` | integer | `0` (LOW) or `1` (HIGH) |
| `pull_up_down` | string | `PUD_UP`, `PUD_DOWN`, or `PUD_OFF` |
| `pwm.enabled` | boolean | Enable PWM for this pin |
| `pwm.frequency` | integer | PWM frequency in Hz |
| `pwm.duty_cycle` | integer | Initial duty cycle (0-100) |
| `safety.max_on_time` | integer | Maximum time in seconds the pin can stay on (0 = unlimited) |
| `safety.cooldown` | integer | Cooldown period in seconds after max_on_time is reached |

## Web Interface Settings

Configure the web interface in `config.json`:

```json
{
  "web": {
    "host": "0.0.0.0",
    "port": 5000,
    "debug": false,
    "secret_key": "your-secret-key-here",
    "session_timeout": 3600,
    "theme": {
      "primary_color": "#4a6fa5",
      "secondary_color": "#6c757d",
      "dark_mode": false
    },
    "features": {
      "registration": false,
      "password_reset": true,
      "two_factor_auth": true,
      "api_docs": true
    }
  }
}
```

## Security Settings

### User Authentication

```json
{
  "security": {
    "secret_key": "your-secret-key-here",
    "password_salt_rounds": 10,
    "jwt_secret_key": "your-jwt-secret-here",
    "jwt_expiration": 3600,
    "password_policy": {
      "min_length": 8,
      "require_uppercase": true,
      "require_lowercase": true,
      "require_digits": true,
      "require_special_chars": true,
      "max_age_days": 90
    },
    "login_attempts": 5,
    "lockout_time": 900
  }
}
```

### API Security

```json
{
  "api": {
    "enabled": true,
    "rate_limiting": {
      "enabled": true,
      "max_requests": 1000,
      "per_seconds": 3600
    },
    "cors": {
      "enabled": true,
      "origins": ["*"],
      "methods": ["GET", "POST", "PUT", "DELETE"],
      "allow_credentials": true
    }
  }
}
```

## Logging Configuration

Configure logging in `config.json`:

```json
{
  "logging": {
    "level": "INFO",
    "file": "logs/raspy_utility.log",
    "max_size_mb": 10,
    "backup_count": 5,
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S"
  }
}
```

## Backup and Restore

### Creating a Backup

```bash
# Create a backup of all configurations
python main.py config backup

# Create a backup to a specific file
python main.py config backup --output backup_$(date +%Y%m%d).tar.gz
```

### Restoring from Backup

```bash
# Restore from the latest backup
python main.py config restore

# Restore from a specific backup file
python main.py config restore --input backup_20230901.tar.gz
```

## Advanced Configuration

### Custom Scripts

You can add custom scripts to the `scripts/` directory. These can be triggered via the web interface or scheduler.

### Plugins

To enable plugins, add them to the `plugins` directory and update the configuration:

```json
{
  "plugins": {
    "enabled": true,
    "directory": "plugins",
    "autoload": true,
    "load_order": [
      "my_custom_plugin"
    ]
  }
}
```

### Systemd Service Configuration

Edit the systemd service file at `/etc/systemd/system/raspy_utility.service`:

```ini
[Unit]
Description=Raspberry Pi Utility
After=network.target

[Service]
User=pi
WorkingDirectory=/home/pi/raspy_utility
Environment="PATH=/home/pi/raspy_utility/venv/bin"
Environment="FLASK_APP=app.py"
Environment="FLASK_ENV=production"
Environment="SECRET_KEY=your-secret-key-here"
ExecStart=/home/pi/raspy_utility/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Troubleshooting Configuration Issues

1. **Configuration Not Loading**
   - Check file permissions
   - Verify JSON syntax is valid
   - Check application logs for errors

2. **GPIO Configuration Errors**
   - Verify pin numbers are correct for your Raspberry Pi model
   - Check for pin conflicts
   - Ensure the user has GPIO permissions

3. **Web Interface Not Starting**
   - Check if the port is in use: `sudo lsof -i :5000`
   - Verify the host and port in the configuration
   - Check firewall settings

For additional help, refer to the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on [GitHub](https://github.com/Nsfr750/raspy_utility/issues).
