import sqlite3
import json

# Connect to database
conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

print("=" * 80)
print("CAR RENTAL DATABASE - COMPLETE DATA OVERVIEW")
print("=" * 80)

# Get all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print(f"\nTotal Tables: {len(tables)}")
for table in tables:
    print(f"   - {table[0]}")

# Users table
print("\n" + "=" * 80)
print("1. USERS TABLE")
print("=" * 80)
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]
print(f"Total Users: {user_count}")

cursor.execute("SELECT id, email, full_name, phone, created_at FROM users LIMIT 5")
users = cursor.fetchall()
print("\nSample Users:")
for user in users:
    print(f"  ID: {user[0]} | Email: {user[1]} | Name: {user[2]} | Phone: {user[3]}")

# Locations table
print("\n" + "=" * 80)
print("2. LOCATIONS TABLE")
print("=" * 80)
cursor.execute("SELECT COUNT(*) FROM locations")
location_count = cursor.fetchone()[0]
print(f"Total Locations: {location_count}")

cursor.execute("SELECT country, COUNT(*) FROM locations GROUP BY country")
country_stats = cursor.fetchall()
print("\nLocations by Country:")
for country, count in country_stats:
    print(f"  {country}: {count} locations")

cursor.execute("SELECT id, city, name, state, country FROM locations ORDER BY country, city")
locations = cursor.fetchall()
print("\nAll Locations:")
for loc in locations:
    print(f"  ID {loc[0]}: {loc[1]}, {loc[3]} ({loc[4]}) - {loc[2]}")

# Cars table
print("\n" + "=" * 80)
print("3. CARS TABLE")
print("=" * 80)
cursor.execute("SELECT COUNT(*) FROM cars")
car_count = cursor.fetchone()[0]
print(f"Total Cars: {car_count}")

cursor.execute("SELECT car_type, COUNT(*) FROM cars GROUP BY car_type ORDER BY COUNT(*) DESC")
type_stats = cursor.fetchall()
print("\nCars by Type:")
for car_type, count in type_stats:
    print(f"  {car_type}: {count} cars")

cursor.execute("SELECT fuel_type, COUNT(*) FROM cars GROUP BY fuel_type")
fuel_stats = cursor.fetchall()
print("\nCars by Fuel Type:")
for fuel, count in fuel_stats:
    print(f"  {fuel}: {count} cars")

cursor.execute("SELECT MIN(price_per_day), MAX(price_per_day), AVG(price_per_day) FROM cars")
price_stats = cursor.fetchone()
print(f"\nPrice Range:")
print(f"  Minimum: ${price_stats[0]:.2f}/day")
print(f"  Maximum: ${price_stats[1]:.2f}/day")
print(f"  Average: ${price_stats[2]:.2f}/day")

cursor.execute("""
    SELECT c.name, c.brand, c.car_type, c.price_per_day, l.city, l.country 
    FROM cars c 
    JOIN locations l ON c.location_id = l.id 
    ORDER BY l.country, l.city, c.name
""")
cars = cursor.fetchall()
print(f"\nAll {len(cars)} Cars:")
current_country = None
current_city = None
for car in cars:
    if car[5] != current_country:
        current_country = car[5]
        print(f"\n  [{current_country}]:")
    if car[4] != current_city:
        current_city = car[4]
        print(f"    {current_city}:")
    print(f"      - {car[0]} ({car[1]}) - {car[2]} - ${car[3]}/day")

# Bookings table
print("\n" + "=" * 80)
print("4. BOOKINGS TABLE")
print("=" * 80)
cursor.execute("SELECT COUNT(*) FROM bookings")
booking_count = cursor.fetchone()[0]
print(f"Total Bookings: {booking_count}")

if booking_count > 0:
    cursor.execute("SELECT status, COUNT(*) FROM bookings GROUP BY status")
    status_stats = cursor.fetchall()
    print("\nBookings by Status:")
    for status, count in status_stats:
        print(f"  {status}: {count} bookings")

    cursor.execute("""
        SELECT b.id, u.email, c.name, b.pickup_date, b.return_date, b.total_price, b.status
        FROM bookings b
        JOIN users u ON b.user_id = u.id
        JOIN cars c ON b.car_id = c.id
        ORDER BY b.created_at DESC
        LIMIT 10
    """)
    bookings = cursor.fetchall()
    print("\nRecent Bookings:")
    for booking in bookings:
        print(f"  Booking #{booking[0]}: {booking[1]} | {booking[2]} | {booking[3]} to {booking[4]} | ${booking[5]} | {booking[6]}")
else:
    print("No bookings yet.")

print("\n" + "=" * 80)
print("DATABASE SUMMARY")
print("=" * 80)
print(f"[+] {user_count} Users")
print(f"[+] {location_count} Locations")
print(f"[+] {car_count} Cars")
print(f"[+] {booking_count} Bookings")
print("=" * 80)

conn.close()
