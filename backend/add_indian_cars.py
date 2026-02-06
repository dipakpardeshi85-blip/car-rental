import sqlite3

# Connect to database
conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

# Indian location IDs: 7=Mumbai, 8=Delhi, 9=Bangalore, 10=Hyderabad, 11=Chennai, 12=Pune

# Add cars to Indian locations (distributing existing cars across Indian cities)
# We'll add 2 cars per Indian city for a total of 12 new cars

indian_cars = [
    # Mumbai (ID: 7) - 2 cars
    ('Tata Nexon EV', 'Tata', 'Nexon', 2024, 'Electric SUV', 5, 'Automatic', 'Electric', 85.00, 7, '/images/cars/tesla_model_3_1769942219589.png', 'Popular Indian electric SUV with great range and features.', 'Connected Car Tech, Sunroof, Fast Charging, Safety Features'),
    ('Mahindra XUV700', 'Mahindra', 'XUV700', 2024, 'SUV', 7, 'Automatic', 'Diesel', 95.00, 7, '/images/cars/bmw_x5_1769942238426.png', 'Premium Indian SUV with advanced features and spacious interior.', 'ADAS, Panoramic Sunroof, Premium Audio, 7 Seats'),
    
    # Delhi (ID: 8) - 2 cars
    ('Honda City Hybrid', 'Honda', 'City', 2024, 'Sedan', 5, 'Automatic', 'Hybrid', 70.00, 8, '/images/cars/toyota_camry_1769942308962.png', 'Fuel-efficient hybrid sedan perfect for city driving.', 'Honda Sensing, Sunroof, Cruise Control, Premium Interior'),
    ('Hyundai Creta', 'Hyundai', 'Creta', 2024, 'SUV', 5, 'Automatic', 'Petrol', 80.00, 8, '/images/cars/honda_crv_1769942411079.png', 'Best-selling compact SUV with modern features.', 'Ventilated Seats, Wireless Charging, Panoramic Sunroof, BlueLink'),
    
    # Bangalore (ID: 9) - 2 cars
    ('MG Hector', 'MG', 'Hector', 2024, 'SUV', 5, 'Automatic', 'Hybrid', 90.00, 9, '/images/cars/range_rover_1769942357466.png', 'Tech-loaded SUV with internet connectivity.', 'AI Assistant, Panoramic Sunroof, Premium Sound, Connected Features'),
    ('Skoda Octavia', 'Skoda', 'Octavia', 2024, 'Sedan', 5, 'Automatic', 'Petrol', 85.00, 9, '/images/cars/audi_a4_1769942377766.png', 'European sedan with premium features and comfort.', 'Virtual Cockpit, Ambient Lighting, Sunroof, Premium Audio'),
    
    # Hyderabad (ID: 10) - 2 cars
    ('Kia Seltos', 'Kia', 'Seltos', 2024, 'SUV', 5, 'Automatic', 'Petrol', 75.00, 10, '/images/cars/volkswagen_atlas_1769942444489.png', 'Stylish compact SUV with great features.', 'UVO Connect, Sunroof, Ventilated Seats, Wireless Charging'),
    ('Volkswagen Virtus', 'Volkswagen', 'Virtus', 2024, 'Sedan', 5, 'Automatic', 'Petrol', 72.00, 10, '/images/cars/mercedes_c_class_1769942256490.png', 'Premium German sedan with excellent build quality.', 'Digital Cockpit, Sunroof, Cruise Control, Premium Interior'),
    
    # Chennai (ID: 11) - 2 cars
    ('Maruti Suzuki Grand Vitara', 'Maruti Suzuki', 'Grand Vitara', 2024, 'SUV', 5, 'Automatic', 'Hybrid', 78.00, 11, '/images/cars/jeep_wrangler_1769942275065.png', 'Strong hybrid SUV with excellent fuel efficiency.', 'Panoramic Sunroof, 360 Camera, Wireless Charging, ADAS'),
    ('Toyota Fortuner', 'Toyota', 'Fortuner', 2024, 'SUV', 7, 'Automatic', 'Diesel', 120.00, 11, '/images/cars/bmw_x5_1769942238426.png', 'Premium 7-seater SUV, perfect for family trips.', '4WD, Leather Seats, Premium Audio, Safety Features'),
    
    # Pune (ID: 12) - 2 cars
    ('Jeep Compass', 'Jeep', 'Compass', 2024, 'SUV', 5, 'Automatic', 'Diesel', 95.00, 12, '/images/cars/jeep_wrangler_1769942275065.png', 'American SUV with off-road capability.', '4x4, Panoramic Sunroof, Premium Interior, Safety Features'),
    ('BMW 3 Series', 'BMW', '3 Series', 2024, 'Luxury Sedan', 5, 'Automatic', 'Petrol', 150.00, 12, '/images/cars/mercedes_c_class_1769942256490.png', 'Luxury German sedan with sporty performance.', 'iDrive, Sunroof, Premium Audio, Sport Mode'),
]

print("Adding cars to Indian locations...")
print("")

for car_data in indian_cars:
    cursor.execute("""
        INSERT INTO cars (name, brand, model, year, car_type, seats, transmission, 
                         fuel_type, price_per_day, location_id, image_url, description, features)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, car_data)
    print(f"Added: {car_data[0]} to location ID {car_data[9]}")

conn.commit()
conn.close()

print("")
print("SUCCESS! Added 12 cars to Indian locations!")
print("Distribution:")
print("  Mumbai: 2 cars")
print("  Delhi: 2 cars")
print("  Bangalore: 2 cars")
print("  Hyderabad: 2 cars")
print("  Chennai: 2 cars")
print("  Pune: 2 cars")
