# GoodFoods Agent Deployment Guide

This guide covers deploying the GoodFoods Conversational Reservation Agent using the new containerized architecture with separate frontend and backend services.

## Architecture Overview

The application is now split into two containerized services:

- **Backend**: FastAPI service handling AI logic, database operations, and tool-calling
- **Frontend**: Streamlit service providing the user interface
- **Database**: PostgreSQL database managed with Prisma ORM

### Database Architecture

The application uses **Prisma** as the ORM with **PostgreSQL** for production deployments:

- **Prisma Schema**: Located in `backend/prisma/schema.prisma`
- **Database Models**: Restaurant, Table, User, Booking
- **Automatic Migrations**: Schema is automatically applied on deployment
- **Data Seeding**: Initial data is populated automatically

## Local Development Setup

### Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ (for local development without containers)
- API key for Llama 3.1 8B (DeepInfra, Ollama, etc.)

### Quick Start with Docker Compose

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd GoodFoods-Conversational-Reservation-Agent
   ```

2. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   # Edit .env and add your API_KEY
   ```

3. **Initialize the database:**
   ```bash
   # Run the data generation script locally first
   python backend/app/generate_data.py
   ```

4. **Start the services:**
   ```bash
   docker-compose up --build
   ```

5. **Access the application:**
   - Frontend: http://localhost:8501
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Local Development (Without Docker)

#### Backend Setup
```bash
cd backend
pip install -r requirements.txt
cd app
python generate_data.py  # Initialize database
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## Cloud Deployment

### Render Deployment (Recommended)

Render provides a simple, unified platform for deploying both services and databases.

#### Step 1: Prepare Your Repository

Ensure your repository contains:
- `backend/` directory with Dockerfile
- `frontend/` directory with Dockerfile
- `docker-compose.yml` for local testing
- `.env` file with your API key

#### Step 2: Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New > PostgreSQL**
3. Choose a plan (free tier available for development)
4. Note the **Internal Connection URL** - this will be your `DATABASE_URL`
5. The database will be automatically created with the Prisma schema when the backend deploys

#### Step 3: Deploy Backend Service

1. Go to **New > Web Service**
2. Connect your GitHub repository
3. Configure the service:
   - **Name**: `goodfoods-agent-api`
   - **Root Directory**: `backend`
   - **Environment**: Docker
   - **Branch**: `main`

4. Add environment variables:
   ```
   API_KEY=your_llama_api_key_here
   DATABASE_URL=your_postgres_internal_url
   ```
   
   **Important**: The `DATABASE_URL` should be the Internal Connection URL from your PostgreSQL service. It will look like:
   ```
   postgresql://username:password@host:port/database
   ```

5. Choose instance type (free tier available)
6. Click **Create Web Service**

#### Step 4: Deploy Frontend Service

1. Go to **New > Web Service**
2. Connect the same GitHub repository
3. Configure the service:
   - **Name**: `goodfoods-agent-ui`
   - **Root Directory**: `frontend`
   - **Environment**: Docker
   - **Branch**: `main`

4. Add environment variables:
   ```
   BACKEND_URL=https://your-backend-service.onrender.com
   ```

5. Choose instance type (free tier available)
6. Click **Create Web Service**

#### Step 5: Update CORS Settings

After deployment, update the CORS origins in `backend/app/main.py` to include your frontend URL:

```python
origins = [
    "https://your-frontend-service.onrender.com",
    # ... other origins
]
```

Redeploy the backend service after making this change.

### Alternative Cloud Platforms

#### Railway
Railway offers similar simplicity to Render with good free tier options.

#### Heroku
Heroku supports containerized deployments but requires a paid plan for production use.

#### AWS/GCP/Azure
For enterprise deployments, use container orchestration services:
- AWS: ECS or EKS
- GCP: Cloud Run or GKE
- Azure: Container Instances or AKS

## Environment Variables

### Backend Variables
- `API_KEY`: Your Llama 3.1 8B API key
- `DATABASE_URL`: PostgreSQL connection string (required for production)
- `BACKEND_URL`: Backend service URL

### Frontend Variables
- `BACKEND_URL`: URL of the backend API service

## Health Checks

Both services include health check endpoints:

- Backend: `GET /health`
- Frontend: Built-in Streamlit health check

## Monitoring and Logs

### Render Dashboard
- View service logs in the Render dashboard
- Monitor resource usage and performance
- Set up alerts for service failures

### Custom Monitoring
For production deployments, consider:
- Application Performance Monitoring (APM)
- Log aggregation (ELK stack, Datadog)
- Error tracking (Sentry)

## Scaling Considerations

### Horizontal Scaling
- Backend: Can be scaled horizontally behind a load balancer
- Frontend: Stateless, can be scaled easily
- Database: Consider managed database services for production

### Performance Optimization
- Implement caching for frequently accessed data
- Use CDN for static assets
- Optimize database queries
- Consider async processing for heavy operations

## Security Best Practices

### Production Checklist
- [ ] Use HTTPS for all communications
- [ ] Implement proper authentication/authorization
- [ ] Secure API keys and secrets
- [ ] Enable CORS with specific origins only
- [ ] Use managed database services
- [ ] Implement rate limiting
- [ ] Regular security updates

### API Security
- Implement API key validation
- Add request rate limiting
- Use proper HTTP status codes
- Validate all input data

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Check if backend service is running
   - Verify API key configuration
   - Check CORS settings

2. **Database Connection Issues**
   - Verify database URL format
   - Check network connectivity
   - Ensure database is accessible

3. **Container Build Failures**
   - Check Dockerfile syntax
   - Verify requirements.txt dependencies
   - Check for missing files

### Debug Commands

```bash
# Check container logs
docker-compose logs backend
docker-compose logs frontend

# Access container shell
docker-compose exec backend bash
docker-compose exec frontend bash

# Check service health
curl http://localhost:8000/health
curl http://localhost:8501
```

## Support

For deployment issues:
1. Check the service logs
2. Verify environment variables
3. Test locally with Docker Compose
4. Review the troubleshooting section above

For application issues:
1. Check the API documentation at `/docs`
2. Review the main README.md
3. Open an issue in the repository 