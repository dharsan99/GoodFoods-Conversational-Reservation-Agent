#!/bin/bash

echo "Setting up GoodFoods minimal development environment..."

# Create virtual environments
echo "Creating virtual environments..."
python3 -m venv backend/venv
python3 -m venv frontend/venv

# Activate backend environment and install minimal dependencies
echo "Installing backend dependencies (minimal)..."
source backend/venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements-minimal.txt

# Activate frontend environment and install dependencies
echo "Installing frontend dependencies..."
source frontend/venv/bin/activate
pip install --upgrade pip
pip install -r frontend/requirements.txt

echo "Minimal development environment setup complete!"
echo ""
echo "To start the services:"
echo "1. Backend: cd backend && source venv/bin/activate && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo "2. Frontend: cd frontend && source venv/bin/activate && streamlit run app.py --server.port 8501"
echo ""
echo "Or use the start_minimal.sh script to start both services." 