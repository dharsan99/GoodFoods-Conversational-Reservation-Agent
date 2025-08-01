# 🔄 Redeploy Backend to Fix Google Cloud Auth

## Issue
The Google Cloud credentials are properly configured in Render, but the backend is still getting `401 Unauthorized` errors. This usually means the backend service needs to be redeployed to pick up the environment variables.

## Solution: Redeploy Backend Service

### Step 1: Manual Redeploy
1. Go to your Render dashboard: https://dashboard.render.com
2. Navigate to the `goodfoods-agent-api` service
3. Click "Manual Deploy" in the top right corner
4. Select "Deploy latest commit"
5. Wait for deployment to complete (2-3 minutes)

### Step 2: Verify Environment Variables
After redeploy, check that the environment variables are loaded:
1. Go to the "Logs" section of your backend service
2. Look for any startup messages
3. The service should start without authentication errors

### Step 3: Test the Connection
1. Visit your frontend: https://goodfoods-agent-ui.onrender.com
2. Try sending a message like "Hello"
3. Check if you get a proper response instead of errors

## Alternative: Force Environment Variable Update
If redeploy doesn't work:

1. **Edit Environment Variables**:
   - Go to "Environment" section in the backend service
   - Click "Edit" next to `GOOGLE_APPLICATION_CREDENTIALS`
   - Re-paste the JSON content (even if it's the same)
   - Click "Save Changes"

2. **This should trigger an automatic redeploy**

## Expected Result
After successful redeploy:
- ✅ No more `401 Unauthorized` errors in logs
- ✅ Successful LLM responses from Vertex AI
- ✅ Chat functionality working properly
- ✅ Frontend can communicate with backend successfully

## Troubleshooting
If still getting 401 errors after redeploy:

1. **Check Service Account Permissions**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to IAM & Admin > IAM
   - Find your service account: `goodfoods-render-service@speechtotext-466820.iam.gserviceaccount.com`
   - Ensure it has these roles:
     - `Vertex AI User`
     - `Service Usage Consumer`

2. **Verify Model Access**:
   - Check if the model ID `7439580447044009984` is accessible
   - Ensure the model is deployed and active

3. **Check Render Logs**:
   - Look for any startup errors
   - Check if environment variables are being loaded correctly

## Quick Test
You can also test locally by running:
```bash
cd backend
python test_google_auth.py
```

This will verify if the credentials work in your local environment. 