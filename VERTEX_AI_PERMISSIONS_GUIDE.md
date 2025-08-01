# Vertex AI Permissions Guide

## Current Issue
The fine-tuning job is failing due to insufficient permissions. The error message indicates:

```
403 Caller does not have required permission to use project speechtotext-466820. 
Grant the caller the roles/serviceusage.serviceUsageConsumer role, or a custom role 
with the serviceusage.services.use permission
```

## Solution Steps

### Step 1: Access Google Cloud Console IAM
1. Go to: https://console.developers.google.com/iam-admin/iam/project?project=speechtotext-466820
2. Or navigate to: Google Cloud Console → IAM & Admin → IAM

### Step 2: Add Required Role
1. Find your user account (the one you're using for authentication)
2. Click the "Edit" (pencil) icon next to your account
3. Click "Add another role"
4. Search for and select: `Service Usage Consumer` (`roles/serviceusage.serviceUsageConsumer`)
5. Click "Save"

### Step 3: Additional Recommended Roles
For full Vertex AI functionality, also add these roles:
- `Vertex AI User` (`roles/aiplatform.user`)
- `Vertex AI Service Agent` (`roles/aiplatform.serviceAgent`)
- `Storage Object Viewer` (`roles/storage.objectViewer`) - for accessing datasets

### Step 4: Wait for Propagation
- Permission changes may take 2-5 minutes to propagate
- You may need to re-authenticate: `gcloud auth login`

### Step 5: Verify Permissions
Run this command to verify your current permissions:
```bash
gcloud projects get-iam-policy speechtotext-466820 --flatten="bindings[].members" --format="table(bindings.role)" --filter="bindings.members:$(gcloud config get-value account)"
```

### Step 6: Re-run Fine-Tuning
After permissions are set up:
```bash
python run_fine_tuning.py
```

## Alternative: Use Service Account
If you prefer to use a service account instead of your user account:

1. Create a service account:
```bash
gcloud iam service-accounts create goodfoods-finetuning \
    --display-name="GoodFoods Fine-Tuning Service Account"
```

2. Grant the service account the required roles:
```bash
gcloud projects add-iam-policy-binding speechtotext-466820 \
    --member="serviceAccount:goodfoods-finetuning@speechtotext-466820.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding speechtotext-466820 \
    --member="serviceAccount:goodfoods-finetuning@speechtotext-466820.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"
```

3. Download and activate the service account key:
```bash
gcloud iam service-accounts keys create goodfoods-finetuning-key.json \
    --iam-account=goodfoods-finetuning@speechtotext-466820.iam.gserviceaccount.com

export GOOGLE_APPLICATION_CREDENTIALS="goodfoods-finetuning-key.json"
```

## Troubleshooting

### Common Issues:
1. **Permission Denied**: Ensure you have the correct roles assigned
2. **API Not Enabled**: Enable Vertex AI API in the Google Cloud Console
3. **Billing Not Enabled**: Ensure billing is enabled for the project
4. **Quota Exceeded**: Check Vertex AI quotas in the console

### Check API Status:
```bash
gcloud services list --enabled --filter="name:aiplatform.googleapis.com"
```

### Enable Vertex AI API:
```bash
gcloud services enable aiplatform.googleapis.com
```

## Next Steps
Once permissions are fixed:
1. Run `python run_fine_tuning.py` to start fine-tuning
2. Monitor progress with `python monitor_fine_tuning.py`
3. Check the Google Cloud Console for detailed progress

## Support
If you continue to have issues:
1. Check the Google Cloud Console for detailed error messages
2. Review the Vertex AI documentation: https://cloud.google.com/vertex-ai/docs
3. Contact Google Cloud support if needed 