# GoodFoods Agent - Render Deployment Guide

This guide provides detailed steps for deploying the GoodFoods Conversational Reservation Agent to Render with PostgreSQL database and Prisma ORM.

## Prerequisites

- GitHub repository with the GoodFoods code
- Render account (free tier available)
- Google Cloud account with Vertex AI enabled
- Google Cloud Project ID

## Step 1: Set Up Google Cloud

1. **Create Google Cloud Project**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Note your **Project ID** (you'll need this)

2. **Enable Vertex AI API**
   - In Google Cloud Console, go to **APIs & Services > Library**
   - Search for "Vertex AI API"
   - Click **Enable**

3. **Set Up Authentication**
   - Go to **IAM & Admin > Service Accounts**
   - Create a new service account or use existing one
   - Add the **Vertex AI User** role
   - Create and download a JSON key file
   - **Important**: Keep this key file secure

## Step 2: Prepare Your Repository

Ensure your repository contains the following structure:
```
GoodFoods-Conversational-Reservation-Agent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── agent.py
│   │   ├── tool_functions.py
│   │   ├── tool_definitions.py
│   │   ├── database.py
│   │   └── generate_data.py
│   ├── prisma/
│   │   └── schema.prisma
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── init_prisma.py
│   └── seed_data.py
├── frontend/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── env_example.txt
└── README.md
```

## Step 3: Create PostgreSQL Database

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com/)
   - Sign in or create an account

2. **Create PostgreSQL Service**
   - Click **New > PostgreSQL**
   - Choose a plan:
     - **Free**: 1GB storage, suitable for development
     - **Starter**: 1GB storage, $7/month
     - **Standard**: 10GB storage, $20/month

3. **Configure Database**
   - **Name**: `goodfoods-db` (or your preferred name)
   - **Database**: `goodfoods` (or your preferred name)
   - **User**: Leave as default or customize
   - **Region**: Choose closest to your users

4. **Note Connection Details**
   - After creation, go to the database service
   - Copy the **Internal Connection URL**
   - It will look like: `postgresql://user:password@host:port/database`

## Step 4: Deploy Backend Service

1. **Create Web Service**
   - Go to **New > Web Service**
   - Connect your GitHub repository

2. **Configure Backend Service**
   - **Name**: `goodfoods-agent-api`
   - **Root Directory**: `backend`
   - **Environment**: Docker
   - **Branch**: `main`
   - **Region**: Same as your database

3. **Add Environment Variables**
   ```
   GOOGLE_CLOUD_PROJECT_ID=your_project_id_here
   GOOGLE_CLOUD_LOCATION=us-central1
   DATABASE_URL=your_postgres_internal_url_from_step_2
   ```

4. **Configure Build Settings**
   - **Build Command**: Leave empty (Docker handles this)
   - **Start Command**: Leave empty (Docker handles this)

5. **Choose Instance Type**
   - **Free**: 750 hours/month, suitable for development
   - **Starter**: $7/month, better performance
   - **Standard**: $25/month, production ready

6. **Deploy**
   - Click **Create Web Service**
   - Render will build and deploy your backend

## Step 5: Deploy Frontend Service

1. **Create Another Web Service**
   - Go to **New > Web Service**
   - Connect the same GitHub repository

2. **Configure Frontend Service**
   - **Name**: `goodfoods-agent-ui`
   - **Root Directory**: `frontend`
   - **Environment**: Docker
   - **Branch**: `main`
   - **Region**: Same as backend

3. **Add Environment Variables**
   ```
   BACKEND_URL=https://your-backend-service.onrender.com
   ```

4. **Choose Instance Type**
   - **Free**: 750 hours/month
   - **Starter**: $7/month

5. **Deploy**
   - Click **Create Web Service**
   - Render will build and deploy your frontend

## Step 6: Update CORS Settings

After both services are deployed:

1. **Get Frontend URL**
   - Note the URL of your frontend service
   - Example: `https://goodfoods-agent-ui.onrender.com`

2. **Update Backend CORS**
   - Go to your backend service in Render
   - Add environment variable:
   ```
   FRONTEND_URL=https://your-frontend-service.onrender.com
   ```

3. **Redeploy Backend**
   - Go to **Manual Deploy > Deploy latest commit**
   - This will apply the CORS changes

## Step 7: Verify Deployment

1. **Check Backend Health**
   - Visit: `https://your-backend-service.onrender.com/health`
   - Should return: `{"status": "healthy", "agent_ready": true}`

2. **Check API Documentation**
   - Visit: `https://your-backend-service.onrender.com/docs`
   - Should show FastAPI interactive docs

3. **Test Frontend**
   - Visit your frontend URL
   - Should show the GoodFoods chat interface

4. **Test Chat Functionality**
   - Try a simple query: "Find restaurants in Bangalore"
   - Should get a response from the AI agent

## Troubleshooting

### Common Issues

1. **Backend Build Fails**
   - Check build logs in Render dashboard
   - Ensure all files are in correct locations
   - Verify Dockerfile syntax

2. **Database Connection Fails**
   - Verify `DATABASE_URL` is correct
   - Check if database service is running
   - Ensure database credentials are correct

3. **Prisma Errors**
   - Check if Prisma schema is valid
   - Verify database URL format
   - Check build logs for Prisma generation errors

4. **Frontend Can't Connect to Backend**
   - Verify `BACKEND_URL` environment variable
   - Check CORS settings
   - Ensure backend service is running

### Debug Commands

```bash
# Check backend logs
# Go to your backend service > Logs

# Check database connection
# Go to your database service > Connect > External Connection

# Test API endpoints
curl https://your-backend-service.onrender.com/health
```

## Environment Variables Reference

### Backend Variables
- `GOOGLE_CLOUD_PROJECT_ID`: Your Google Cloud Project ID (required)
- `GOOGLE_CLOUD_LOCATION`: Google Cloud region (defaults to us-central1)
- `DATABASE_URL`: PostgreSQL connection string (required)
- `FRONTEND_URL`: Frontend service URL (for CORS)

### Frontend Variables
- `BACKEND_URL`: Backend service URL (required)

## Cost Estimation

### Free Tier (Development)
- **PostgreSQL**: Free (1GB storage)
- **Backend**: Free (750 hours/month)
- **Frontend**: Free (750 hours/month)
- **Total**: $0/month

### Production Tier
- **PostgreSQL**: $7/month (Starter)
- **Backend**: $7/month (Starter)
- **Frontend**: $7/month (Starter)
- **Total**: $21/month

## Security Considerations

1. **API Keys**: Never commit API keys to your repository
2. **Database**: Use Render's internal connection URLs
3. **CORS**: Configure specific origins, not wildcards
4. **HTTPS**: Render provides automatic HTTPS
5. **Environment Variables**: Use Render's secure environment variable storage

## Monitoring and Maintenance

1. **Health Checks**: Both services include health check endpoints
2. **Logs**: Monitor logs in Render dashboard
3. **Database**: Monitor database usage and performance
4. **Updates**: Set up automatic deployments from your main branch

## Support

For deployment issues:
1. Check Render's documentation: [render.com/docs](https://render.com/docs)
2. Review service logs in Render dashboard
3. Verify environment variables are set correctly
4. Test locally with Docker Compose first

For application issues:
1. Check the main README.md
2. Review API documentation at `/docs`
3. Open an issue in the repository 