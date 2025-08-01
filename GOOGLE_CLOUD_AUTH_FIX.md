# 🔐 Fix Google Cloud Authentication

## Issue
The backend is successfully deployed and receiving requests, but it's getting a `401 Unauthorized` error when trying to access Google Cloud Vertex AI.

## Root Cause
The `GOOGLE_APPLICATION_CREDENTIALS` environment variable is not properly configured in the backend service on Render.

## Solution

### Step 1: Check Backend Environment Variables
1. Go to your Render dashboard: https://dashboard.render.com
2. Navigate to the `goodfoods-agent-api` service
3. Click on "Environment" in the left sidebar
4. Check if `GOOGLE_APPLICATION_CREDENTIALS` is set

### Step 2: Add Google Cloud Service Account
If the environment variable is missing or incorrect:

1. **Create/Download Service Account Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Navigate to IAM & Admin > Service Accounts
   - Find or create a service account with these roles:
     - `Vertex AI User`
     - `Service Usage Consumer`
   - Create a new key (JSON format)
   - Download the JSON file

2. **Add to Render Backend Service**:
   - In the Render dashboard for `goodfoods-agent-api`
   - Go to "Environment" section
   - Add/Update these environment variables:
     ```
     GOOGLE_APPLICATION_CREDENTIALS=<paste-the-entire-json-content>
     GOOGLE_CLOUD_PROJECT_ID=speechtotext-466820
     GOOGLE_CLOUD_LOCATION=us-central1
     ```

### Step 3: Alternative - Use Secret Files
If the JSON is too large for environment variables:

1. **Upload as Secret File**:
   - In Render dashboard, go to "Secret Files" section
   - Upload your service account JSON file
   - Name it something like `google-credentials.json`

2. **Update Environment Variable**:
   - Set `GOOGLE_APPLICATION_CREDENTIALS=/etc/secrets/google-credentials.json`

### Step 4: Redeploy Backend
After adding the credentials:
1. Click "Manual Deploy" in the backend service
2. Select "Deploy latest commit"
3. Wait for deployment to complete

## Verification
After fixing:
1. Check the backend logs for authentication errors
2. Try sending a message in the frontend
3. Look for successful LLM responses instead of 401 errors

## Expected Result
- ✅ No more `401 Unauthorized` errors
- ✅ Successful LLM responses from Vertex AI
- ✅ Chat functionality working properly

## Troubleshooting
If still getting 401 errors:
1. Verify the service account has correct permissions
2. Check if the project ID matches your Google Cloud project
3. Ensure the JSON key is valid and not expired
4. Check Render logs for more detailed error messages 