import sqlite3

# Connect to database
conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

# Get Indian location IDs
cursor.execute("SELECT id, city, name FROM locations WHERE country='India'")
indian_locations = cursor.fetchall()

print("Indian Locations:")
for loc_id, city, name in indian_locations:
    print(f"  ID {loc_id}: {city} - {name}")

conn.close()
