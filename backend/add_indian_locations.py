import sqlite3

# Connect to database
conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

# Add Indian locations with all required fields
indian_locations = [
    ('Mumbai', 'Andheri Hub', 'Maharashtra', 'India', 'Shop 12, Andheri West, Mumbai, Maharashtra 400053'),
    ('Delhi', 'Connaught Place Center', 'Delhi', 'India', '15 Connaught Place, New Delhi, Delhi 110001'),
    ('Bangalore', 'Koramangala Station', 'Karnataka', 'India', '45 Koramangala 4th Block, Bangalore, Karnataka 560034'),
    ('Hyderabad', 'HITEC City Hub', 'Telangana', 'India', 'Cyber Towers, HITEC City, Hyderabad, Telangana 500081'),
    ('Chennai', 'Anna Nagar Center', 'Tamil Nadu', 'India', '23 Anna Nagar West, Chennai, Tamil Nadu 600040'),
    ('Pune', 'Hinjewadi Tech Park', 'Maharashtra', 'India', 'Rajiv Gandhi Infotech Park, Hinjewadi, Pune, Maharashtra 411057'),
]

print("Adding Indian locations to database...")
print("")

for city, name, state, country, address in indian_locations:
    cursor.execute("""
        INSERT INTO locations (city, name, state, country, address)
        VALUES (?, ?, ?, ?, ?)
    """, (city, name, state, country, address))
    print(f"Added: {city}, {state} - {name}")

conn.commit()
conn.close()

print("")
print("SUCCESS! All Indian locations added to database!")
print("Total locations added: 6")
print("")
print("Indian cities:")
print("- Mumbai (Maharashtra)")
print("- Delhi")
print("- Bangalore (Karnataka)")
print("- Hyderabad (Telangana)")
print("- Chennai (Tamil Nadu)")
print("- Pune (Maharashtra)")
