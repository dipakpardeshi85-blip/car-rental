import sqlite3

conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

# Count cars in Indian locations
cursor.execute('SELECT COUNT(*) FROM cars WHERE location_id BETWEEN 7 AND 12')
total = cursor.fetchone()[0]
print(f'Total cars in Indian locations: {total}')

# Cars per city
cursor.execute('''
    SELECT l.city, COUNT(c.id) 
    FROM locations l 
    LEFT JOIN cars c ON l.id = c.location_id 
    WHERE l.country="India" 
    GROUP BY l.city
''')

print('\nCars per Indian city:')
for city, count in cursor.fetchall():
    print(f'  {city}: {count} cars')

conn.close()
