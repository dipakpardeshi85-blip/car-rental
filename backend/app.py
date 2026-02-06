from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from database import init_db
from auth import auth_bp
from api import api_bp

app = Flask(__name__, static_folder='../frontend')
app.secret_key = 'your-secret-key-change-in-production-12345'

# Enable CORS for frontend communication
CORS(app, supports_credentials=True, origins=['http://localhost:5000', 'http://127.0.0.1:5000'])

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(api_bp)

# Serve frontend files
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        # For client-side routing, return index.html
        return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # Initialize database if it doesn't exist
    db_path = os.path.join(os.path.dirname(__file__), 'car_rental.db')
    if not os.path.exists(db_path):
        print("Initializing database...")
        init_db()
    
    print("Starting Car Rental Server...")
    print("Access the website at: http://localhost:5000")
    print("Admin credentials: admin@carrental.com / admin123")
    app.run(debug=True, host='0.0.0.0', port=5000)
