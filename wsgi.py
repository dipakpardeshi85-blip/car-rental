"""
WSGI Entry Point for Render Deployment

This file serves as the entry point for the Flask application when deployed on Render.
It imports the Flask app from the backend directory and exposes it for gunicorn.
"""

import sys
import os

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

# Import the Flask app from backend/app.py
from app import app

# Expose the app for gunicorn
if __name__ == "__main__":
    app.run()
