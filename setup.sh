#!/bin/bash

echo "=============================="
echo "Setting up Authentication App (PostgreSQL)"
echo "=============================="

echo "Creating virtual environment..."
python3 -m venv .venv

echo "Activating environment..."
source .venv/bin/activate

echo "Upgrading pip..."
python -m pip install --upgrade pip

echo "Installing dependencies..."
python -m pip install -r requirements.txt

echo "=============================="
echo "Setup Complete!"
echo "=============================="

echo "IMPORTANT:"
echo "1. Make sure PostgreSQL is installed"
echo "2. Create database: auth_system_pg"
echo "3. Update credentials in database.py"

echo ""
echo "Running app..."
python app.py