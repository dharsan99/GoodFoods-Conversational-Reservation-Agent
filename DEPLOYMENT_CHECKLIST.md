# 🚀 Deployment Checklist

## ✅ Pre-Deployment
- [ ] Code is pushed to GitHub
- [ ] Docker builds successfully locally
- [ ] Google Cloud service account created
- [ ] Service account has required permissions:
  - [ ] Vertex AI User
  - [ ] Service Usage Consumer
  - [ ] Storage Object Viewer
- [ ] Service account JSON key downloaded

## 🔧 Backend Deployment
- [ ] Create new Web Service in Render
- [ ] Connect GitHub repository
- [ ] Set configuration:
  - [ ] Name: `goodfoods-agent-api`
  - [ ] Environment: Docker
  - [ ] Dockerfile Path: `backend/Dockerfile`
  - [ ] Docker Context: `backend`
  - [ ] Plan: Starter
- [ ] Set environment variables:
  - [ ] `DEV_MODE=false`
  - [ ] `GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820`
  - [ ] `GOOGLE_CLOUD_LOCATION=us-central1`
  - [ ] `GOOGLE_APPLICATION_CREDENTIALS=<service-account-json>`
- [ ] Deploy and wait for completion
- [ ] Test health endpoint: `https://goodfoods-backend.onrender.com/health`

## 🎨 Frontend Deployment
- [ ] Create new Web Service in Render
- [ ] Connect same GitHub repository
- [ ] Set configuration:
  - [ ] Name: `goodfoods-frontend`
  - [ ] Environment: Docker
  - [ ] Dockerfile Path: `frontend/Dockerfile`
  - [ ] Docker Context: `frontend`
  - [ ] Plan: Starter
- [ ] Set environment variables:
  - [ ] `BACKEND_URL=https://goodfoods-agent-api.onrender.com`
- [ ] Deploy and wait for completion
- [ ] Test frontend: `https://goodfoods-agent-ui.onrender.com`

## 🧪 Testing
- [ ] Backend health check passes
- [ ] Frontend loads successfully
- [ ] Test conversation flow:
  - [ ] "Hello" → Proper greeting
  - [ ] "Find restaurants in HSR Layout" → Shows HSR restaurant
  - [ ] "Book a table for 2 people tomorrow at 7 PM" → Booking confirmation
  - [ ] "Show me menu specials" → Shows menu
  - [ ] "What's your name?" → Identifies as Samvaad

## 🎉 Post-Deployment
- [ ] Share frontend URL with users
- [ ] Monitor logs for any issues
- [ ] Set up monitoring alerts (optional)
- [ ] Document deployment process

## 🔗 URLs
- **Frontend**: `https://goodfoods-agent-ui.onrender.com`
- **Backend**: `https://goodfoods-agent-api.onrender.com`
- **Backend Health**: `https://goodfoods-agent-api.onrender.com/health`

## 📞 Support
If you encounter issues:
1. Check Render logs
2. Verify environment variables
3. Test locally with Docker
4. Check Google Cloud permissions 