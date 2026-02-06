from flask import Blueprint, request, jsonify, session
import bcrypt
from database import create_user, get_user_by_email, get_user_by_id

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate input
    required_fields = ['email', 'password', 'full_name', 'phone']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    email = data['email']
    password = data['password']
    full_name = data['full_name']
    phone = data['phone']
    
    # Check if user already exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 409
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create user
    user_id = create_user(email, password_hash, full_name, phone)
    
    if user_id:
        # Create session
        session['user_id'] = user_id
        session['email'] = email
        session['is_admin'] = False
        
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user_id,
                'email': email,
                'full_name': full_name,
                'is_admin': False
            }
        }), 201
    else:
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/api/login', methods=['POST'])
def login():
    """Login user."""
    data = request.get_json()
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    email = data['email']
    password = data['password']
    
    # Get user
    user = get_user_by_email(email)
    
    if not user:
        return jsonify({'error': 'Invalid email or password'}), 401
    
    # Verify password
    if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        # Create session
        session['user_id'] = user['id']
        session['email'] = user['email']
        session['is_admin'] = bool(user['is_admin'])
        
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'full_name': user['full_name'],
                'phone': user['phone'],
                'is_admin': bool(user['is_admin'])
            }
        }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    """Logout user."""
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

@auth_bp.route('/api/user', methods=['GET'])
def get_current_user():
    """Get current logged-in user."""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user = get_user_by_id(session['user_id'])
    
    if user:
        return jsonify({
            'id': user['id'],
            'email': user['email'],
            'full_name': user['full_name'],
            'phone': user['phone'],
            'is_admin': bool(user['is_admin'])
        }), 200
    else:
        return jsonify({'error': 'User not found'}), 404

def login_required(f):
    """Decorator to require login."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    
    return decorated_function

def admin_required(f):
    """Decorator to require admin privileges."""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        if not session.get('is_admin'):
            return jsonify({'error': 'Admin privileges required'}), 403
        return f(*args, **kwargs)
    
    return decorated_function
