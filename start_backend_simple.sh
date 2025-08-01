#!/bin/bash

echo "Starting GoodFoods Backend (Simple Mode)..."

cd backend
source venv/bin/activate

echo "Backend virtual environment activated"
echo "Starting server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python simple_server.py 