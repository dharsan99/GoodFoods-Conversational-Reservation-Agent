# Local Development Guide

This guide shows you how to run GoodFoods locally without Docker for faster development.

## Prerequisites

- Python 3.11 or 3.12 (recommended for better compatibility)
- Node.js (for Prisma CLI)
- Git

## Quick Start (Minimal Setup)

### 1. Setup Environment

```bash
# Run the minimal setup script
./setup_minimal.sh
```

This will:
- Create virtual environments for both backend and frontend
- Install minimal dependencies that work with Python 3.13
- Skip problematic packages like `psycopg2-binary` and complex Prisma setup

### 2. Start Services

#### Option A: Using the start script
```bash
./start_minimal.sh
```

#### Option B: Manual start (recommended for development)

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
export $(cat ../.env | xargs)
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
source venv/bin/activate
export BACKEND_URL=http://localhost:8000
streamlit run app.py --server.port 8501
```

## Access Points

- **Backend API**: http://localhost:8000
- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs

## Development Workflow

### Backend Development

1. **Make changes** to files in `backend/app/`
2. **Save the file** - uvicorn will automatically reload
3. **Test API endpoints** at http://localhost:8000/docs

### Frontend Development

1. **Make changes** to `frontend/app.py`
2. **Save the file** - Streamlit will automatically reload
3. **View changes** at http://localhost:8501

### Database Operations (Production Only)

For local development, the minimal setup skips database operations. The full database functionality is available in:

- **Docker environment**: `docker-compose up`
- **Production deployment**: Render deployment

## Troubleshooting

### Python 3.13 Compatibility Issues

If you encounter issues with Python 3.13:

1. **Use Python 3.11 or 3.12**:
   ```bash
   # Install Python 3.11 via Homebrew
   brew install python@3.11
   
   # Create virtual environment with Python 3.11
   python3.11 -m venv backend/venv
   python3.11 -m venv frontend/venv
   ```

2. **Or use the minimal setup** (already configured for Python 3.13)

### Port Already in Use

If ports 8000 or 8501 are already in use:

```bash
# Kill processes using the ports
lsof -ti:8000 | xargs kill -9
lsof -ti:8501 | xargs kill -9

# Or use different ports
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
streamlit run app.py --server.port 8502
```

### Virtual Environment Issues

If virtual environments are corrupted:

```bash
# Remove and recreate
rm -rf backend/venv frontend/venv
./setup_minimal.sh
```

## File Structure

```
GoodFoods-Conversational-Reservation-Agent/
├── backend/
│   ├── venv/                    # Backend virtual environment
│   ├── app/                     # Backend application code
│   ├── requirements-minimal.txt # Minimal dependencies
│   └── requirements.txt         # Full dependencies (for production)
├── frontend/
│   ├── venv/                    # Frontend virtual environment
│   ├── app.py                   # Streamlit application
│   └── requirements.txt         # Frontend dependencies
├── .env                         # Environment variables
├── setup_minimal.sh            # Minimal setup script
├── start_minimal.sh            # Minimal start script
└── docker-compose.yml          # Docker setup (for production)
```

## Environment Variables

The `.env` file contains:

```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=...

# Database Configuration (for production)
DATABASE_URL=postgresql://...

# Backend Configuration
BACKEND_URL=http://localhost:8000
```

## Production vs Development

| Feature | Development | Production |
|---------|-------------|------------|
| Database | Skipped | PostgreSQL (Render) |
| AI Agent | Minimal | Full Llama 3.1 8B |
| Hot Reload | Yes | No |
| Environment | Local | Docker + Render |
| Dependencies | Minimal | Full |

## Next Steps

1. **Start with minimal setup** for UI/UX development
2. **Use Docker** for full functionality testing
3. **Deploy to Render** for production testing

## Support

- **Backend Issues**: Check `backend/app/` logs
- **Frontend Issues**: Check Streamlit logs in terminal
- **Database Issues**: Use Docker setup or production deployment 