# GoodFoods AI Agent - Render Deployment Guide

## 🚀 Quick Deployment

### Option 1: Automated Deployment (Recommended)
1. Push your code to GitHub
2. Connect your repository to Render
3. Render will automatically detect `render.yaml` and deploy both services

### Option 2: Manual Deployment
Follow the step-by-step guide below.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Render Account**: Sign up at [render.com](https://render.com)
3. **Google Cloud Service Account**: For Vertex AI access

## 🔧 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Ensure your repository has the following structure:
```
GoodFoods-Conversational-Reservation-Agent/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   └── .dockerignore
├── frontend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── .dockerignore
├── render.yaml
└── README.md
```

### Step 2: Create Google Cloud Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Navigate to IAM & Admin > Service Accounts
3. Create a new service account with these roles:
   - `Vertex AI User`
   - `Service Usage Consumer`
   - `Storage Object Viewer`
4. Create and download a JSON key file

### Step 3: Deploy Backend Service

1. **Go to Render Dashboard**
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click "New +" > "Web Service"

2. **Connect Repository**
   - Connect your GitHub repository
   - Select the repository

3. **Configure Backend Service**
   - **Name**: `goodfoods-agent-api`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Docker Context**: `backend`
   - **Plan**: `Starter` (Free tier)
   - **Region**: `Singapore` (or your preferred region)

4. **Set Environment Variables**
   ```
   DEV_MODE=false
   GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820
   GOOGLE_CLOUD_LOCATION=us-central1
   GOOGLE_APPLICATION_CREDENTIALS=<paste-your-service-account-json>
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

### Step 4: Deploy Frontend Service

1. **Create Another Web Service**
   - Click "New +" > "Web Service"
   - Connect the same repository

2. **Configure Frontend Service**
   - **Name**: `goodfoods-frontend`
   - **Environment**: `Docker`
   - **Dockerfile Path**: `frontend/Dockerfile`
   - **Docker Context**: `frontend`
   - **Plan**: `Starter` (Free tier)
   - **Region**: Same as backend

3. **Set Environment Variables**
   ```
   BACKEND_URL=https://goodfoods-agent-api.onrender.com
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete

## 🔍 Verification

### Check Backend Health
```bash
curl https://goodfoods-backend.onrender.com/health
```
Expected response: `{"status": "healthy"}`

### Check Frontend Health
```bash
curl https://goodfoods-frontend.onrender.com/_stcore/health
```
Expected response: Health status

### Test the Application
1. Visit your frontend URL: `https://goodfoods-frontend.onrender.com`
2. Try the conversation flow:
   - "Hello"
   - "Find restaurants in HSR Layout"
   - "Book a table for 2 people tomorrow at 7 PM"

## 🛠️ Troubleshooting

### Common Issues

1. **Backend Health Check Fails**
   - Check logs in Render dashboard
   - Verify Google Cloud credentials
   - Ensure all environment variables are set

2. **Frontend Can't Connect to Backend**
   - Verify BACKEND_URL is correct
   - Check CORS configuration
   - Ensure backend is healthy

3. **Google Cloud Authentication Issues**
   - Verify service account has correct permissions
   - Check GOOGLE_APPLICATION_CREDENTIALS format
   - Ensure project ID is correct

### View Logs
1. Go to your service in Render dashboard
2. Click on "Logs" tab
3. Check for error messages

### Restart Services
1. Go to service dashboard
2. Click "Manual Deploy" > "Deploy latest commit"

## 🔄 Continuous Deployment

Once deployed, Render will automatically:
- Deploy new versions when you push to GitHub
- Restart services if they crash
- Monitor health checks

## 📊 Monitoring

### Health Checks
- Backend: `/health` endpoint
- Frontend: `/_stcore/health` endpoint

### Metrics
- Response times
- Error rates
- Resource usage

## 🔐 Security

### Environment Variables
- Never commit sensitive data to Git
- Use Render's environment variable system
- Rotate service account keys regularly

### CORS Configuration
- Backend is configured to allow frontend domain
- Update CORS settings if needed

## 💰 Cost Optimization

### Free Tier Limits
- 750 hours/month per service
- Services sleep after 15 minutes of inactivity
- First request after sleep may be slow

### Upgrading
- Consider paid plans for production use
- Better performance and no sleep mode

## 🎉 Success!

Your GoodFoods AI Agent is now live at:
- **Frontend**: `https://goodfoods-agent-ui.onrender.com`
- **Backend**: `https://goodfoods-agent-api.onrender.com`

The AI agent is ready to help customers with restaurant reservations! 