@echo off
echo ==============================
echo Setting up Authentication App (PostgreSQL)
echo ==============================

REM Create virtual environment
echo Creating virtual environment...
python -m venv .venv

REM Activate environment
echo Activating virtual environment...
call .venv\Scripts\activate

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo Installing dependencies...
python -m pip install -r requirements.txt

echo ==============================
echo Setup Complete!
echo ==============================

echo IMPORTANT:
echo 1. Install PostgreSQL if not installed
echo 2. Create database: auth_system_pg
echo 3. Update credentials in database.py (user, password)

echo.
echo To run the project:
echo .venv\Scripts\activate
echo python app.py

pause