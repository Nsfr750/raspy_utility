"""
Flask application factory for the Raspy Utility web interface.
"""
import os
from flask import Flask, send_from_directory
from flask_cors import CORS

def create_app():
    """Create and configure the Flask application."""
    # Create and configure the app
    app = Flask(__name__, 
                instance_relative_config=True,
                static_url_path='',
                static_folder='static',
                template_folder='templates')
    
    # Enable CORS
    CORS(app)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Register blueprints
    from . import routes
    app.register_blueprint(routes.main_bp)
    
    # Serve static files from the root
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)
    
    # Import the GPIO manager (it initializes itself)
    from .gpio_manager import gpio_manager
    
    # Register teardown handler to clean up GPIO on app shutdown
    @app.teardown_appcontext
    def cleanup_gpio(exception):
        """Clean up GPIO resources when the app context is torn down."""
        if gpio_manager.initialized:
            gpio_manager.cleanup()
    
    return app
