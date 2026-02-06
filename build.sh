#!/bin/bash

# Build script for DriveNow Car Rental Website
# This script sets up the application for deployment

echo "========================================="
echo "DriveNow Car Rental - Build Script"
echo "========================================="
echo ""

# Step 1: Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Step 2: Initialize database
echo "🗄️  Initializing database..."
cd backend

python3 << EOF
from database import init_db
import os

db_path = os.path.join(os.path.dirname(__file__), 'car_rental.db')
if not os.path.exists(db_path):
    print("Creating database...")
    init_db()
    print("Database initialized with sample data!")
else:
    print("Database already exists, skipping initialization")
EOF

if [ $? -ne 0 ]; then
    echo "❌ Failed to initialize database"
    exit 1
fi

cd ..
echo "✅ Database ready"
echo ""

# Step 3: Verify installation
echo "🔍 Verifying installation..."

# Check if Flask is installed
python3 -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask not found"
    exit 1
fi

# Check if gunicorn is installed
python3 -c "import gunicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Gunicorn not found"
    exit 1
fi

echo "✅ All components verified"
echo ""

# Step 4: Build complete
echo "========================================="
echo "✅ Build completed successfully!"
echo "========================================="
echo ""
echo "To start the server:"
echo "  Development: cd backend && python app.py"
echo "  Production:  gunicorn --chdir backend --bind 0.0.0.0:8000 app:app"
echo ""
echo "Admin credentials:"
echo "  Email: admin@carrental.com"
echo "  Password: admin123"
echo ""

exit 0
