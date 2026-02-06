from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from database import init_db
from auth import auth_bp
from api import api_bp

app = Flask(__name__, static_folder='../frontend')

# Use environment variable for secret key in production, fallback for development
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# Enable CORS for frontend communication
# In production, Render will serve both frontend and backend from same origin
allowed_origins = [
    'http://localhost:5000',
    'http://127.0.0.1:5000',
    os.environ.get('RENDER_EXTERNAL_URL', '')
]
CORS(app, supports_credentials=True, origins=[origin for origin in allowed_origins if origin])

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

# Initialize database on startup (for both development and production)
db_path = os.path.join(os.path.dirname(__file__), 'car_rental.db')
if not os.path.exists(db_path):
    print("Initializing database...")
    init_db()
    print("Database initialized with sample data!")

if __name__ == '__main__':
    print("Starting Car Rental Server...")
    print("Access the website at: http://localhost:5000")
    print("Admin credentials: admin@carrental.com / admin123")
    
    # Use PORT environment variable for production (Render), default to 5000 for development
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') != 'production'
    
    app.run(debug=debug, host='0.0.0.0', port=port)
