@echo off
REM Build script for DriveNow Car Rental Website (Windows)
REM This script sets up the application for deployment

echo =========================================
echo DriveNow Car Rental - Build Script
echo =========================================
echo.

REM Step 1: Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies
    exit /b 1
)

echo Dependencies installed successfully
echo.

REM Step 2: Initialize database
echo Initializing database...
cd backend

python -c "from database import init_db; import os; db_path = os.path.join(os.path.dirname(__file__), 'car_rental.db'); init_db() if not os.path.exists(db_path) else print('Database already exists')"

if %ERRORLEVEL% NEQ 0 (
    echo Failed to initialize database
    exit /b 1
)

cd ..
echo Database ready
echo.

REM Step 3: Verify installation
echo Verifying installation...

python -c "import flask" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Flask not found
    exit /b 1
)

python -c "import gunicorn" 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Gunicorn not found
    exit /b 1
)

echo All components verified
echo.

REM Step 4: Build complete
echo =========================================
echo Build completed successfully!
echo =========================================
echo.
echo To start the server:
echo   Development: cd backend ^&^& python app.py
echo   Production:  gunicorn --chdir backend --bind 0.0.0.0:8000 app:app
echo.
echo Admin credentials:
echo   Email: admin@carrental.com
echo   Password: admin123
echo.

exit /b 0
