from flask import Blueprint, request, jsonify, session
from database import (
    get_all_locations, get_all_cars, get_car_by_id,
    create_booking, get_user_bookings, cancel_booking,
    check_car_availability, add_car, update_car, get_all_bookings
)
from auth import login_required, admin_required
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all locations."""
    locations = get_all_locations()
    return jsonify(locations), 200

@api_bp.route('/api/cars', methods=['GET'])
def get_cars():
    """Get cars with optional filters."""
    location_id = request.args.get('location_id', type=int)
    car_type = request.args.get('car_type')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    
    cars = get_all_cars(
        location_id=location_id,
        car_type=car_type,
        min_price=min_price,
        max_price=max_price
    )
    
    return jsonify(cars), 200

@api_bp.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    """Get car details by ID."""
    car = get_car_by_id(car_id)
    
    if car:
        return jsonify(car), 200
    else:
        return jsonify({'error': 'Car not found'}), 404

@api_bp.route('/api/cars/check-availability', methods=['POST'])
def check_availability():
    """Check if a car is available for given dates."""
    data = request.get_json()
    
    required_fields = ['car_id', 'pickup_date', 'return_date']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    car_id = data['car_id']
    pickup_date = data['pickup_date']
    return_date = data['return_date']
    
    # Validate dates
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        
        if pickup >= return_dt:
            return jsonify({'error': 'Return date must be after pickup date'}), 400
        
        if pickup < datetime.now():
            return jsonify({'error': 'Pickup date cannot be in the past'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    available = check_car_availability(car_id, pickup_date, return_date)
    
    return jsonify({'available': available}), 200

@api_bp.route('/api/bookings', methods=['POST'])
@login_required
def create_new_booking():
    """Create a new booking."""
    data = request.get_json()
    
    required_fields = ['car_id', 'pickup_date', 'return_date', 
                      'pickup_location_id', 'return_location_id', 'total_price']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    car_id = data['car_id']
    pickup_date = data['pickup_date']
    return_date = data['return_date']
    pickup_location_id = data['pickup_location_id']
    return_location_id = data['return_location_id']
    total_price = data['total_price']
    
    # Validate dates
    try:
        pickup = datetime.strptime(pickup_date, '%Y-%m-%d')
        return_dt = datetime.strptime(return_date, '%Y-%m-%d')
        
        if pickup >= return_dt:
            return jsonify({'error': 'Return date must be after pickup date'}), 400
        
        if pickup < datetime.now():
            return jsonify({'error': 'Pickup date cannot be in the past'}), 400
    except ValueError:
        return jsonify({'error': 'Invalid date format'}), 400
    
    # Check availability
    if not check_car_availability(car_id, pickup_date, return_date):
        return jsonify({'error': 'Car not available for selected dates'}), 409
    
    # Create booking
    user_id = session['user_id']
    booking_id = create_booking(
        user_id, car_id, pickup_date, return_date,
        pickup_location_id, return_location_id, total_price
    )
    
    if booking_id:
        return jsonify({
            'message': 'Booking created successfully',
            'booking_id': booking_id
        }), 201
    else:
        return jsonify({'error': 'Failed to create booking'}), 500

@api_bp.route('/api/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Get user's bookings."""
    user_id = session['user_id']
    bookings = get_user_bookings(user_id)
    return jsonify(bookings), 200

@api_bp.route('/api/bookings/<int:booking_id>', methods=['DELETE'])
@login_required
def delete_booking(booking_id):
    """Cancel a booking."""
    user_id = session['user_id']
    
    if cancel_booking(booking_id, user_id):
        return jsonify({'message': 'Booking cancelled successfully'}), 200
    else:
        return jsonify({'error': 'Booking not found or unauthorized'}), 404

# Admin routes
@api_bp.route('/api/admin/cars', methods=['POST'])
@admin_required
def create_car():
    """Add a new car (admin only)."""
    data = request.get_json()
    
    required_fields = ['name', 'brand', 'model', 'year', 'car_type', 'seats',
                      'transmission', 'fuel_type', 'price_per_day', 'location_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    car_id = add_car(
        name=data['name'],
        brand=data['brand'],
        model=data['model'],
        year=data['year'],
        car_type=data['car_type'],
        seats=data['seats'],
        transmission=data['transmission'],
        fuel_type=data['fuel_type'],
        price_per_day=data['price_per_day'],
        location_id=data['location_id'],
        image_url=data.get('image_url', ''),
        description=data.get('description', ''),
        features=data.get('features', '')
    )
    
    return jsonify({
        'message': 'Car added successfully',
        'car_id': car_id
    }), 201

@api_bp.route('/api/admin/cars/<int:car_id>', methods=['PUT'])
@admin_required
def update_car_details(car_id):
    """Update car details (admin only)."""
    data = request.get_json()
    
    # Remove id from data if present
    data.pop('id', None)
    
    if update_car(car_id, **data):
        return jsonify({'message': 'Car updated successfully'}), 200
    else:
        return jsonify({'error': 'Failed to update car'}), 500

@api_bp.route('/api/admin/bookings', methods=['GET'])
@admin_required
def get_all_bookings_admin():
    """Get all bookings (admin only)."""
    bookings = get_all_bookings()
    return jsonify(bookings), 200
