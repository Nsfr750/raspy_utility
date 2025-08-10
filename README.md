# Raspberry Pi GPIO Control Center

**Version:** 1.0.0  
**License:** GNU General Public License v3.0 (GPLv3)  
**Python:** 3.8+  
**Platform:** Windows, Linux, Raspberry Pi

![Application Screenshot](assets/screenshot.png)

## 🚀 Features

- Modern PySide6-based GUI with dark/light theme support
- Complete GPIO control interface with visual feedback
- Daily log rotation with log viewer
- System tray integration
- Multi-language support
- Command buttons for bulk GPIO operations
- Real-time status updates
- Cross-platform compatibility

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Nsfr750/raspy-utility.git
   cd raspy-utility
   ```

2. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   For Windows (without RPi.GPIO):

   ```bash
   pip install -r requirements-windows.txt
   ```

## 🛠 Usage

1. Run the application:

   ```bash
   python main.py
   ```

2. Use the interface to control GPIO pins:

   - Toggle individual pins with the GPIO buttons
   - Use "Start All" to set all GPIOs to HIGH
   - Use "Stop All" to set all GPIOs to LOW
   - Use "Reset" to reset all GPIOs and clear the log

3. Access logs:

   - Click on "View Logs" in the menu
   - Select a log file from the dropdown
   - Filter logs by level if needed

## 📝 Logging

Logs are stored in the `logs/` directory with daily rotation. Each log file is named `raspy_utility_YYYY-MM-DD.log`.

## 🤝 Contributing

Contributions are welcome! Please read our [contributing guidelines](CONTRIBUTING.md) before submitting pull requests.

A comprehensive application for controlling and monitoring Raspberry Pi GPIO pins through a user-friendly interface or REST API.

## ✨ Features

- 🖥️ **Graphical User Interface**
  - Modern, responsive interface
  - Real-time GPIO status monitoring
  - Intuitive pin control (on/off)
  - Multi-language support (English/Italiano)
  - System tray integration
  - Integrated web browser control

- 🔌 **GPIO Support**
  - Control digital I/O pins
  - Built-in GPIO simulator for development
  - Automatic hardware detection
  - Safe pin management
  - Remote GPIO support

- 🌐 **Web Interface**
  - Built-in web server
  - Responsive design for mobile/desktop
  - Real-time updates
  - REST API integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Raspberry Pi (optional, simulator available)
- Internet connection (for package installation)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Nsfr750/raspy-utility.git
   cd raspy-utility
   ```

2. **Create and activate virtual environment** (recommended)
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Unix or MacOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

## 📦 Features in Detail

### GUI Features
- Modern interface with dark/light theme support
- Real-time GPIO status visualization
- Integrated log viewer
- System tray integration for quick access
- Multi-window support

### GPIO Control
- Support for all Raspberry Pi GPIO pins
- Input/Output configuration
- Pull-up/down resistor control
- PWM support
- Hardware-accelerated operations

### Web Interface
- Accessible from any device on the network
- Mobile-responsive design
- Real-time updates using WebSocket
- Secure authentication
- API documentation

## 🌍 Internationalization
- Built-in support for multiple languages
- Easy to add new translations
- Automatic language detection
- Right-to-left (RTL) language support

## 🤝 Contributing
Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on how to contribute to this project.

## 📄 License
This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- Thanks to all contributors who have helped improve this project
- Special thanks to the Raspberry Pi Foundation for their amazing hardware
- Inspired by various open-source GPIO control projects
