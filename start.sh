#!/bin/bash

# GoodFoods Conversational Agent Startup Script

echo "🍽️  GoodFoods Conversational Reservation Agent"
echo "================================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    if [ -f "env_example.txt" ]; then
        cp env_example.txt .env
        echo "✅ .env file created from template"
        echo "📝 Please edit .env file and add your API_KEY"
        echo "   Then run this script again"
        exit 1
    else
        echo "❌ env_example.txt not found"
        exit 1
    fi
fi

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  DATABASE_URL not set. Please add it to your .env file"
    echo "   Format: postgresql://username:password@host:port/database"
    exit 1
fi

echo "🗄️  Using PostgreSQL database: ${DATABASE_URL}"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."
echo "   This may take a few minutes on first run..."

# Start the services
docker-compose up --build

echo ""
echo "🎉 Services started successfully!"
echo "   Frontend: http://localhost:8501"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the services" 