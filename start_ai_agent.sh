#!/bin/bash

echo "🚀 Starting GoodFoods AI Agent..."

# Check if we're in the right directory
if [ ! -f "backend/app/agent.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    exit 1
fi

# Setup database
echo "📊 Setting up database..."
cd backend
python setup_database.py

if [ $? -eq 0 ]; then
    echo "✅ Database setup complete"
else
    echo "❌ Database setup failed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Start the backend server
echo "🌐 Starting AI Agent backend..."
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 