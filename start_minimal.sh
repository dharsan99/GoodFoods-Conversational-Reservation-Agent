#!/bin/bash

echo "Starting GoodFoods minimal development services..."

# Function to start backend (minimal)
start_backend() {
    echo "Starting backend service (minimal)..."
    cd backend
    source venv/bin/activate
    export $(cat ../.env | xargs)
    # Skip database operations for local development
    export SKIP_DB_OPERATIONS=true
    # Use a simpler approach without pydantic for now
    python -c "
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title='GoodFoods API', version='1.0.0')

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8501'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
async def root():
    return {'message': 'GoodFoods API is running!'}

@app.get('/health')
async def health():
    return {'status': 'healthy'}

@app.post('/chat')
async def chat(message: dict):
    return {
        'response': 'Hello! This is a minimal version of GoodFoods. The full AI agent is available in production.',
        'message': message.get('message', '')
    }

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000, reload=True)
"
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
    echo "Virtual environments not found. Please run setup_dev_simple.sh first."
    exit 1
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