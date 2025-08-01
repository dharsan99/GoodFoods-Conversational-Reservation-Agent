#!/bin/bash

echo "Setting up GoodFoods development environment (simplified)..."

# Create virtual environments
echo "Creating virtual environments..."
python3 -m venv backend/venv
python3 -m venv frontend/venv

# Activate backend environment and install dependencies (without psycopg2 for local dev)
echo "Installing backend dependencies (development version)..."
source backend/venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements-dev.txt

# Install Prisma CLI globally (if not already installed)
if ! command -v prisma &> /dev/null; then
    echo "Installing Prisma CLI..."
    npm install -g prisma
fi

# Initialize Prisma (skip database push for local dev)
echo "Initializing Prisma..."
cd backend
python -m prisma generate
cd ..

# Activate frontend environment and install dependencies
echo "Installing frontend dependencies..."
source frontend/venv/bin/activate
pip install --upgrade pip
pip install -r frontend/requirements.txt

echo "Development environment setup complete!"
echo ""
echo "To start the services:"
echo "1. Backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "2. Frontend: cd frontend && source venv/bin/activate && streamlit run app.py --server.port 8501"
echo ""
echo "Or use the start_dev_simple.sh script to start both services." 