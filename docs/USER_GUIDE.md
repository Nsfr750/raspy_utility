# User Guide

Welcome to the Raspberry Pi Utility user guide. This document provides detailed instructions on how to use the application's features and functionality.

## Table of Contents
- [Getting Started](#getting-started)
- [User Interface](#user-interface)
- [GPIO Control](#gpio-control)
- [System Monitoring](#system-monitoring)
- [Scheduling Tasks](#scheduling-tasks)
- [Web Interface](#web-interface)
- [Command Line Interface](#command-line-interface)
- [Troubleshooting](#troubleshooting)

## Getting Started

### First Launch
1. After installation, start the application:
   ```bash
   python main.py
   ```
2. Open your web browser and navigate to `http://<your-pi-ip-address>:5000`
3. Log in with your credentials (default: admin/admin)

### Initial Setup
1. Change the default password immediately after first login
2. Configure your GPIO pins in the Settings menu
3. Set up any scheduled tasks or automations

## User Interface

### Dashboard
- **System Status**: CPU, memory, and disk usage
- **GPIO Overview**: Current state of all configured GPIO pins
- **Quick Actions**: Common tasks and shortcuts

### Navigation
- **Home**: Return to the dashboard
- **GPIO Control**: Manual control of GPIO pins
- **System**: System information and settings
- **Scheduler**: Set up timed events
- **Logs**: View application logs
- **Help**: Access documentation and support

## GPIO Control

### Manual Control
1. Navigate to **GPIO Control**
2. Select the pin you want to control
3. Choose the action (ON/OFF/PWM)
4. Click **Apply**

### Pin Configuration
1. Go to **Settings** > **GPIO Configuration**
2. Select a pin from the list
3. Configure:
   - Mode (Input/Output)
   - Pull-up/down resistors
   - Default state
   - Friendly name
4. Click **Save**

## System Monitoring

### Real-time Monitoring
- View CPU, memory, and disk usage
- Monitor network activity
- Check system temperature

### Alerts
Set up alerts for:
- High resource usage
- Temperature thresholds
- Disk space warnings
- Failed login attempts

## Scheduling Tasks

### Creating a Schedule
1. Go to **Scheduler**
2. Click **Add Schedule**
3. Configure:
   - Schedule name
   - Action (GPIO control, script execution, etc.)
   - Time/Date or interval
   - Recurrence (once, daily, weekly, etc.)
4. Click **Save**

### Example Schedules
- Turn on lights at sunset
- Water plants every morning
- Take temperature readings every hour
- Reboot system weekly

## Web Interface

### Accessing Remotely
1. Ensure your Raspberry Pi is connected to the network
2. Find your Pi's IP address:
   ```bash
   hostname -I
   ```
3. Open a web browser and go to `http://<your-pi-ip-address>:5000`

### Security
- Always use HTTPS in production
- Change default credentials
- Enable two-factor authentication
- Regularly update the application

## Command Line Interface

### Basic Commands
```bash
# Start the application
python main.py

# Start in debug mode
python main.py --debug

# Show help
python main.py --help

# Check version
python main.py --version
```

### Common Tasks
```bash
# List all GPIO pins
python main.py gpio list

# Set GPIO pin 17 to HIGH
python main.py gpio set 17 1

# Read GPIO pin 17
python main.py gpio read 17

# View system status
python main.py system status
```

## Troubleshooting

### Common Issues

#### Web Interface Not Loading
- Check if the service is running: `sudo systemctl status raspy_utility`
- Check the logs: `journalctl -u raspy_utility -f`
- Ensure port 5000 is open: `sudo ufw allow 5000`

#### GPIO Not Working
- Verify the pin is not in use by another process
- Check if the user has GPIO permissions
- Ensure the pin is configured correctly

#### High CPU Usage
- Check running processes: `top`
- Look for errors in the logs
- Consider increasing hardware resources

### Getting Help
- Check the [Troubleshooting Guide](TROUBLESHOOTING.md)
- Search the [GitHub Issues](https://github.com/Nsfr750/raspy_utility/issues)
- Join our [Discord](https://discord.gg/ryqNeuRYjD) for support

## Advanced Topics

### API Usage
For developers, the application provides a RESTful API. See the [API Reference](API_REFERENCE.md) for detailed documentation.

### Custom Scripts
You can extend functionality by adding custom scripts to the `scripts/` directory. These can be triggered via the web interface or scheduler.

### Backup and Restore
Regularly back up your configuration:
```bash
# Create a backup
python main.py config backup

# Restore from backup
python main.py config restore backup_file.json
```

## Support
For additional help, please refer to:
- [Documentation](README.md)
- [GitHub Repository](https://github.com/Nsfr750/raspy_utility)
- [Discord Support](https://discord.gg/ryqNeuRYjD)
