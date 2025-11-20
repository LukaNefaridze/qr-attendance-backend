@echo off
REM Database Setup Script for QR Attendance System
REM This script helps set up the MySQL database and run migrations

echo ========================================
echo QR Attendance System - Database Setup
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not found in PATH
    echo Please ensure Python is installed and added to PATH
    echo Or activate your virtual environment first
    pause
    exit /b 1
)

echo Step 1: Creating migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo.
echo Step 2: Applying migrations to database...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Failed to apply migrations
    echo Make sure:
    echo   1. MySQL server is running
    echo   2. Database 'attendance_db' exists
    echo   3. Database credentials in settings.py are correct
    pause
    exit /b 1
)

echo.
echo Step 3: Creating superuser (optional)...
echo Do you want to create a superuser? (y/n)
set /p create_superuser=
if /i "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

echo.
echo ========================================
echo Database setup completed successfully!
echo ========================================
echo.
echo You can now:
echo   - Access Django admin at http://127.0.0.1:8000/admin
echo   - Start the development server: python manage.py runserver
echo.
pause


