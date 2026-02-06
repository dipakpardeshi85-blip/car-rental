import sqlite3
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'car_rental.db')

def get_db_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema."""
    conn = get_db_connection()
    
    # Read and execute schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        conn.executescript(f.read())
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# User operations
def create_user(email, password_hash, full_name, phone, is_admin=0):
    """Create a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO users (email, password_hash, full_name, phone, is_admin) VALUES (?, ?, ?, ?, ?)',
            (email, password_hash, full_name, phone, is_admin)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def get_user_by_email(email):
    """Get user by email."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    return dict(user) if user else None

def get_user_by_id(user_id):
    """Get user by ID."""
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None

# Location operations
def get_all_locations():
    """Get all locations."""
    conn = get_db_connection()
    locations = conn.execute('SELECT * FROM locations ORDER BY city').fetchall()
    conn.close()
    return [dict(loc) for loc in locations]

def get_location_by_id(location_id):
    """Get location by ID."""
    conn = get_db_connection()
    location = conn.execute('SELECT * FROM locations WHERE id = ?', (location_id,)).fetchone()
    conn.close()
    return dict(location) if location else None

# Car operations
def get_all_cars(location_id=None, car_type=None, min_price=None, max_price=None, available_only=True):
    """Get cars with optional filters."""
    conn = get_db_connection()
    
    query = '''
        SELECT cars.*, locations.name as location_name, locations.city 
        FROM cars 
        JOIN locations ON cars.location_id = locations.id 
        WHERE 1=1
    '''
    params = []
    
    if available_only:
        query += ' AND cars.available = 1'
    
    if location_id:
        query += ' AND cars.location_id = ?'
        params.append(location_id)
    
    if car_type:
        query += ' AND cars.car_type = ?'
        params.append(car_type)
    
    if min_price is not None:
        query += ' AND cars.price_per_day >= ?'
        params.append(min_price)
    
    if max_price is not None:
        query += ' AND cars.price_per_day <= ?'
        params.append(max_price)
    
    query += ' ORDER BY cars.price_per_day'
    
    cars = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(car) for car in cars]

def get_car_by_id(car_id):
    """Get car by ID with location info."""
    conn = get_db_connection()
    car = conn.execute('''
        SELECT cars.*, locations.name as location_name, locations.city, locations.address 
        FROM cars 
        JOIN locations ON cars.location_id = locations.id 
        WHERE cars.id = ?
    ''', (car_id,)).fetchone()
    conn.close()
    return dict(car) if car else None

def add_car(name, brand, model, year, car_type, seats, transmission, fuel_type, 
            price_per_day, location_id, image_url, description, features):
    """Add a new car."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cars (name, brand, model, year, car_type, seats, transmission, 
                         fuel_type, price_per_day, location_id, image_url, description, features)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, brand, model, year, car_type, seats, transmission, fuel_type, 
          price_per_day, location_id, image_url, description, features))
    conn.commit()
    car_id = cursor.lastrowid
    conn.close()
    return car_id

def update_car(car_id, **kwargs):
    """Update car details."""
    conn = get_db_connection()
    
    # Build dynamic update query
    fields = []
    values = []
    for key, value in kwargs.items():
        if value is not None:
            fields.append(f"{key} = ?")
            values.append(value)
    
    if not fields:
        conn.close()
        return False
    
    values.append(car_id)
    query = f"UPDATE cars SET {', '.join(fields)} WHERE id = ?"
    
    conn.execute(query, values)
    conn.commit()
    conn.close()
    return True

def check_car_availability(car_id, pickup_date, return_date):
    """Check if a car is available for the given dates."""
    conn = get_db_connection()
    
    # Check for overlapping bookings
    overlapping = conn.execute('''
        SELECT COUNT(*) as count FROM bookings 
        WHERE car_id = ? 
        AND status = 'confirmed'
        AND (
            (pickup_date <= ? AND return_date >= ?) OR
            (pickup_date <= ? AND return_date >= ?) OR
            (pickup_date >= ? AND return_date <= ?)
        )
    ''', (car_id, pickup_date, pickup_date, return_date, return_date, pickup_date, return_date)).fetchone()
    
    conn.close()
    return overlapping['count'] == 0

# Booking operations
def create_booking(user_id, car_id, pickup_date, return_date, pickup_location_id, 
                   return_location_id, total_price):
    """Create a new booking."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO bookings (user_id, car_id, pickup_date, return_date, 
                            pickup_location_id, return_location_id, total_price)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, car_id, pickup_date, return_date, pickup_location_id, 
          return_location_id, total_price))
    
    conn.commit()
    booking_id = cursor.lastrowid
    conn.close()
    return booking_id

def get_user_bookings(user_id):
    """Get all bookings for a user."""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT bookings.*, 
               cars.name as car_name, cars.brand, cars.model, cars.image_url,
               pl.name as pickup_location_name, pl.city as pickup_city,
               rl.name as return_location_name, rl.city as return_city
        FROM bookings
        JOIN cars ON bookings.car_id = cars.id
        JOIN locations pl ON bookings.pickup_location_id = pl.id
        JOIN locations rl ON bookings.return_location_id = rl.id
        WHERE bookings.user_id = ?
        ORDER BY bookings.created_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return [dict(booking) for booking in bookings]

def get_booking_by_id(booking_id):
    """Get booking by ID."""
    conn = get_db_connection()
    booking = conn.execute('''
        SELECT bookings.*, 
               cars.name as car_name, cars.brand, cars.model,
               pl.name as pickup_location_name,
               rl.name as return_location_name
        FROM bookings
        JOIN cars ON bookings.car_id = cars.id
        JOIN locations pl ON bookings.pickup_location_id = pl.id
        JOIN locations rl ON bookings.return_location_id = rl.id
        WHERE bookings.id = ?
    ''', (booking_id,)).fetchone()
    conn.close()
    return dict(booking) if booking else None

def cancel_booking(booking_id, user_id):
    """Cancel a booking."""
    conn = get_db_connection()
    
    # Verify booking belongs to user
    booking = conn.execute(
        'SELECT * FROM bookings WHERE id = ? AND user_id = ?', 
        (booking_id, user_id)
    ).fetchone()
    
    if not booking:
        conn.close()
        return False
    
    conn.execute(
        "UPDATE bookings SET status = 'cancelled' WHERE id = ?", 
        (booking_id,)
    )
    conn.commit()
    conn.close()
    return True

def get_all_bookings():
    """Get all bookings (admin only)."""
    conn = get_db_connection()
    bookings = conn.execute('''
        SELECT bookings.*, 
               users.full_name as user_name, users.email as user_email,
               cars.name as car_name
        FROM bookings
        JOIN users ON bookings.user_id = users.id
        JOIN cars ON bookings.car_id = cars.id
        ORDER BY bookings.created_at DESC
    ''').fetchall()
    conn.close()
    return [dict(booking) for booking in bookings]
