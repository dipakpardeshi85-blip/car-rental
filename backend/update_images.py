import sqlite3

# Connect to database
conn = sqlite3.connect('car_rental.db')
cursor = conn.cursor()

# Update ALL car images with web-accessible paths
updates = [
    ("/images/cars/tesla_model_3_1769942219589.png", "Tesla Model 3 Performance"),
    ("/images/cars/bmw_x5_1769942238426.png", "BMW X5 M Sport"),
    ("/images/cars/mercedes_c_class_1769942256490.png", "Mercedes-Benz C-Class"),
    ("/images/cars/jeep_wrangler_1769942275065.png", "Jeep Wrangler Unlimited"),
    ("/images/cars/porsche_911_1769942293189.png", "Porsche 911 Carrera"),
    ("/images/cars/toyota_camry_1769942308962.png", "Toyota Camry Hybrid"),
    ("/images/cars/range_rover_1769942357466.png", "Range Rover Sport"),
    ("/images/cars/audi_a4_1769942377766.png", "Audi A4 Quattro"),
    ("/images/cars/ford_mustang_1769942395914.png", "Ford Mustang GT"),
    ("/images/cars/honda_crv_1769942411079.png", "Honda CR-V Hybrid"),
    ("/images/cars/chevrolet_corvette_1769942427514.png", "Chevrolet Corvette"),
    ("/images/cars/volkswagen_atlas_1769942444489.png", "Volkswagen Atlas"),
]

print("Updating car images with web paths...")
print("")
for image_url, car_name in updates:
    cursor.execute("UPDATE cars SET image_url = ? WHERE name = ?", (image_url, car_name))
    print(f"Updated {car_name} -> {image_url}")

conn.commit()
conn.close()

print("")
print("SUCCESS! All car images updated with web-accessible paths!")
print("Images are now served from /images/cars/ directory")
