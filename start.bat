@echo off
REM GoodFoods Conversational Agent Startup Script for Windows

echo 🍽️  GoodFoods Conversational Reservation Agent
echo ================================================

REM Check if .env file exists
if not exist ".env" (
    echo ⚠️  .env file not found. Creating from template...
    if exist "env_example.txt" (
        copy env_example.txt .env
        echo ✅ .env file created from template
        echo 📝 Please edit .env file and add your API_KEY
        echo    Then run this script again
        pause
        exit /b 1
    ) else (
        echo ❌ env_example.txt not found
        pause
        exit /b 1
    )
)

REM Check if DATABASE_URL is set
if "%DATABASE_URL%"=="" (
    echo ⚠️  DATABASE_URL not set. Please add it to your .env file
    echo    Format: postgresql://username:password@host:port/database
    pause
    exit /b 1
)

echo 🗄️  Using PostgreSQL database: %DATABASE_URL%

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not running. Please start Docker and try again.
    pause
    exit /b 1
)

echo 🐳 Starting services with Docker Compose...
echo    This may take a few minutes on first run...

REM Start the services
docker-compose up --build

echo.
echo 🎉 Services started successfully!
echo    Frontend: http://localhost:8501
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the services
pause 