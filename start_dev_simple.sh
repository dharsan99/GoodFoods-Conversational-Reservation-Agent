#!/bin/bash

echo "Starting GoodFoods development services (simplified)..."

# Function to start backend
start_backend() {
    echo "Starting backend service..."
    cd backend
    source venv/bin/activate
    export $(cat ../.env | xargs)
    # Skip database operations for local development
    export SKIP_DB_OPERATIONS=true
    python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend service..."
    cd frontend
    source venv/bin/activate
    export BACKEND_URL=http://localhost:8000
    streamlit run app.py --server.port 8501
}

# Check if virtual environments exist
if [ ! -d "backend/venv" ] || [ ! -d "frontend/venv" ]; then
    echo "Virtual environments not found. Running setup first..."
    chmod +x setup_dev_simple.sh
    ./setup_dev_simple.sh
fi

# Start services in background
echo "Starting backend in background..."
start_backend &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "Starting frontend in background..."
start_frontend &
FRONTEND_PID=$!

echo "Services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:8501"
echo ""
echo "To stop services, run: kill $BACKEND_PID $FRONTEND_PID"
echo "Or use: pkill -f 'uvicorn\|streamlit'"

# Wait for user to stop
wait 