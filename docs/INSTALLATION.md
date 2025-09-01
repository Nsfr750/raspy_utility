# Installation Guide

This guide will walk you through the process of installing and setting up the Raspberry Pi Utility on your Raspberry Pi.

## Prerequisites

- Raspberry Pi (Model 3B+ or newer recommended)
- Raspberry Pi OS (64-bit) installed
- Internet connection
- Python 3.7 or higher
- `pip` package manager

## Step 1: Update System Packages

Before installation, ensure your system is up to date:

```bash
sudo apt update
sudo apt upgrade -y
```

## Step 2: Install Required System Dependencies

```bash
sudo apt install -y \
    python3-venv \
    python3-dev \
    python3-pip \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev \
    libopenjp2-7 \
    libtiff5 \
    libatlas-base-dev \
    libopenblas-dev \
    libxslt1-dev \
    libxml2-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libopenjp2-7 \
    libtiff5 \
    libatlas-base-dev \
    libopenblas-dev
```

## Step 3: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Nsfr750/raspy_utility.git
cd raspy_utility
```

## Step 4: Create and Activate Virtual Environment

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate
```

## Step 5: Install Python Dependencies

```bash
# Install required packages
pip install --upgrade pip
pip install -r requirements.txt

# If you're on a Raspberry Pi, install the Pi-specific requirements
if [ -f "requirements-rpi.txt" ]; then
    pip install -r requirements-rpi.txt
fi
```

## Step 6: Configure the Application

1. Copy the example configuration file:
   ```bash
   cp config.example.json config.json
   ```

2. Edit the configuration file with your preferred text editor:
   ```bash
   nano config.json
   ```

## Step 7: Set Up Systemd Service (Optional)

To run the application as a service that starts on boot:

1. Create a new systemd service file:
   ```bash
   sudo nano /etc/systemd/system/raspy_utility.service
   ```

2. Add the following content (adjust paths as needed):
   ```ini
   [Unit]
   Description=Raspberry Pi Utility
   After=network.target

   [Service]
   User=pi
   WorkingDirectory=/home/pi/raspy_utility
   Environment="PATH=/home/pi/raspy_utility/venv/bin"
   ExecStart=/home/pi/raspy_utility/venv/bin/python main.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable raspy_utility.service
   sudo systemctl start raspy_utility.service
   ```

## Step 8: Verify Installation

1. Check if the service is running:
   ```bash
   sudo systemctl status raspy_utility.service
   ```

2. Or run the application manually:
   ```bash
   python main.py
   ```

## Updating the Application

To update to the latest version:

```bash
# Navigate to the application directory
cd /path/to/raspy_utility

# Stop the service if it's running
sudo systemctl stop raspy_utility.service

# Pull the latest changes
git pull

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart the service
sudo systemctl start raspy_utility.service
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure the user has proper permissions to access GPIO
   - Add user to the `gpio` group:
     ```bash
     sudo usermod -a -G gpio $USER
     ```

2. **Missing Dependencies**
   - Make sure all system dependencies are installed
   - Check the error message for missing packages

3. **Service Fails to Start**
   - Check the logs:
     ```bash
     sudo journalctl -u raspy_utility.service -f
     ```

For additional help, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md) or open an issue on [GitHub](https://github.com/Nsfr750/raspy_utility/issues).

## Next Steps

- [Configuration Guide](CONFIGURATION.md)
- [API Reference](API_REFERENCE.md)
- [User Guide](USER_GUIDE.md)
