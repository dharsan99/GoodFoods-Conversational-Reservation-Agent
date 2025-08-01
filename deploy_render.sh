#!/bin/bash

# GoodFoods AI Agent - Render Deployment Script

echo "🚀 GoodFoods AI Agent - Render Deployment"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose are available"

# Build and test locally
echo ""
echo "🔨 Building Docker images..."
docker-compose build

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed"
    exit 1
fi

echo "✅ Docker images built successfully"

# Test the services locally
echo ""
echo "🧪 Testing services locally..."
docker-compose up -d

# Wait for services to start
echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are healthy
echo "🔍 Checking service health..."

# Check backend
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "❌ Backend health check failed"
    docker-compose logs backend
    docker-compose down
    exit 1
fi

# Check frontend
if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
    echo "✅ Frontend is healthy"
else
    echo "❌ Frontend health check failed"
    docker-compose logs frontend
    docker-compose down
    exit 1
fi

echo ""
echo "🎉 Local testing successful!"
echo ""
echo "📋 Next Steps for Render Deployment:"
echo "1. Push your code to GitHub"
echo "2. Connect your repository to Render"
echo "3. Create two services:"
echo "   - Backend: Use backend/Dockerfile"
echo "   - Frontend: Use frontend/Dockerfile"
echo "4. Set environment variables in Render:"
echo "   - GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820"
echo "   - GOOGLE_CLOUD_LOCATION=us-central1"
echo "   - GOOGLE_APPLICATION_CREDENTIALS=<your-service-account-key>"
echo "   - DEV_MODE=false"
echo ""
echo "🌐 Services will be available at:"
echo "   - Backend: https://your-backend-service.onrender.com"
echo "   - Frontend: https://your-frontend-service.onrender.com"

# Stop local services
echo ""
echo "🛑 Stopping local services..."
docker-compose down

echo "✅ Deployment script completed!" 