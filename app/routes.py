"""
Routes for the Raspy Utility API.

This module defines the API endpoints for controlling GPIO pins.
"""
from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from .gpio_manager import gpio_manager

# Create a Blueprint for the main API endpoints
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the main application page."""
    return render_template('index.html', 
                         gpio_initialized=gpio_manager.initialized)

@main_bp.route('/api/status')
def status():
    """Get the current status of the GPIO system."""
    return jsonify({
        'initialized': gpio_manager.initialized,
        'pins': gpio_manager.get_all_pins(),
        'mode': gpio_manager.get_mode()
    })

@main_bp.route('/api/pins', methods=['GET'])
def get_pins():
    """Get the current state of all GPIO pins."""
    return jsonify(gpio_manager.get_all_pins())

@main_bp.route('/api/pins/<int:pin>', methods=['GET'])
def get_pin(pin):
    """Get the current state of a specific GPIO pin."""
    try:
        value = gpio_manager.get_pin(pin)
        return jsonify({'pin': pin, 'value': value})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@main_bp.route('/api/pins/<int:pin>', methods=['POST'])
def set_pin(pin):
    """Set the state of a GPIO pin."""
    data = request.get_json()
    if not data or 'value' not in data:
        return jsonify({'error': 'Missing value parameter'}), 400
    
    try:
        value = data['value']
        gpio_manager.set_pin(pin, value)
        return jsonify({'pin': pin, 'value': value})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@main_bp.route('/api/mode', methods=['GET'])
def get_mode():
    """Get the current GPIO mode."""
    return jsonify({'mode': gpio_manager.get_mode()})

@main_bp.route('/api/cleanup', methods=['POST'])
def cleanup():
    """Clean up GPIO resources."""
    gpio_manager.cleanup()
    return jsonify({'status': 'success'})
