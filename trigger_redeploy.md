# 🔄 Trigger Frontend Redeploy

## Issue
The frontend is still trying to connect to `localhost:8000` instead of the deployed backend URL, even though the environment variable is correctly set in Render.

## Solution: Trigger Redeploy

### Option 1: Manual Redeploy (Recommended)
1. Go to your Render dashboard: https://dashboard.render.com
2. Navigate to the `goodfoods-agent-ui` service
3. Click on "Manual Deploy" in the top right
4. Select "Deploy latest commit"
5. Wait for the deployment to complete (2-3 minutes)

### Option 2: Force Environment Variable Update
1. Go to the Environment Variables page for `goodfoods-agent-ui`
2. Click "Edit" next to `BACKEND_URL`
3. Change the value to: `https://goodfoods-agent-api.onrender.com`
4. Click "Save Changes"
5. This should trigger an automatic redeploy

### Option 3: Push a Small Change
If the above doesn't work, we can push a small change to trigger redeploy:
```bash
# Add a comment to trigger redeploy
echo "# Trigger redeploy" >> frontend/app.py
git add frontend/app.py
git commit -m "Trigger frontend redeploy"
git push origin main
```

## Verification
After redeploy:
1. Visit: https://goodfoods-agent-ui.onrender.com
2. Check if the connection error is gone
3. Try sending a message like "Hello" to test the connection

## Expected Result
- ✅ No more "Cannot connect to backend server" error
- ✅ Backend status should show "✅ Backend Connected"
- ✅ Chat interface should work properly
- ✅ Auto-scroll should work for new messages

## Troubleshooting
If it still doesn't work:
1. Check the Render logs for any errors
2. Verify the backend is still healthy at: https://goodfoods-agent-api.onrender.com/health
3. Clear browser cache and try again 