# Vertex AI Fine-Tuning Deployment Guide

This guide walks you through deploying the GoodFoods AI Agent fine-tuning on Google Cloud Vertex AI.

## 🎯 Overview

We'll be fine-tuning Llama 3.1 8B model with our 100-example dataset to create a specialized restaurant reservation agent.

## 📋 Prerequisites

### 1. Google Cloud Account
- Active Google Cloud account with billing enabled
- Project ID: `speechtotext-466820`

### 2. Local Setup
- Python 3.8+ installed
- Google Cloud SDK (`gcloud`) installed and configured
- Required Python packages (see `requirements_vertex_ai.txt`)

### 3. Authentication
```bash
# Login to Google Cloud
gcloud auth login

# Set the project
gcloud config set project speechtotext-466820

# Verify authentication
gcloud auth list
```

## 🚀 Step-by-Step Deployment

### Step 1: Install Dependencies
```bash
# Install Vertex AI requirements
pip install -r requirements_vertex_ai.txt

# Verify installation
python -c "import vertexai; print('Vertex AI installed successfully')"
```

### Step 2: Run Setup Script
```bash
# Run the automated setup
python vertex_ai_setup.py
```

This script will:
- ✅ Check gcloud authentication
- ✅ Set project configuration
- ✅ Enable required APIs
- ✅ Create GCS bucket
- ✅ Upload datasets
- ✅ Generate fine-tuning scripts

### Step 3: Start Fine-Tuning
```bash
# Launch the fine-tuning job
python run_fine_tuning.py
```

**Expected Output:**
```
🚀 Starting Vertex AI Fine-Tuning...
📊 Project: speechtotext-466820
📍 Location: us-central1
🤖 Base Model: meta/llama3-1-8b
📁 Training Data: gs://goodfoods-datasets-speechtotext-466820/datasets/training_100.jsonl
📁 Validation Data: gs://goodfoods-datasets-speechtotext-466820/datasets/validation_100.jsonl
🎯 Tuned Model Name: llama3-1-8b-goodfoods-agent-v1
🔄 Launching fine-tuning job...
✅ Fine-tuning job launched successfully!
🔗 Job Resource Name: projects/speechtotext-466820/locations/us-central1/tuningJobs/1234567890123456789
📊 Monitor progress at: https://console.cloud.google.com/vertex-ai/training/tuning-jobs
💾 Job details saved to fine_tuning_job.json
```

### Step 4: Monitor Progress
```bash
# Monitor fine-tuning progress
python monitor_fine_tuning.py
```

**Expected Output:**
```
🔍 Monitoring fine-tuning job: tune-llama3-1-8b-goodfoods-agent-v1
🔗 Resource Name: projects/speechtotext-466820/locations/us-central1/tuningJobs/1234567890123456789
📊 Status: JOB_STATE_RUNNING
⏳ Waiting 60 seconds before next check...
📊 Status: JOB_STATE_SUCCEEDED
🎉 Fine-tuning completed successfully!
🤖 Tuned Model: projects/speechtotext-466820/locations/us-central1/models/1234567890123456789
```

## 📊 Fine-Tuning Configuration

### Model Settings
- **Base Model**: `meta/llama3-1-8b`
- **Epochs**: 5
- **Adapter Size**: 8
- **Learning Rate Multiplier**: 1.0

### Dataset Configuration
- **Training Examples**: 100
- **Validation Examples**: 1
- **Format**: Vertex AI JSONL
- **Total Size**: ~72KB

### Expected Training Time
- **Duration**: 2-4 hours
- **Cost**: ~$50-100 USD
- **Region**: us-central1

## 🔍 Monitoring Options

### 1. Command Line Monitoring
```bash
python monitor_fine_tuning.py
```

### 2. Google Cloud Console
Visit: https://console.cloud.google.com/vertex-ai/training/tuning-jobs

### 3. Check Job Status
```bash
# Get job details
gcloud ai custom-jobs describe JOB_ID --region=us-central1

# List all jobs
gcloud ai custom-jobs list --region=us-central1
```

## 📈 Expected Results

### Training Metrics to Monitor
- **Training Loss**: Should decrease over epochs
- **Validation Loss**: Should decrease but not overfit
- **Tool Accuracy**: Correct tool selection rate
- **Response Quality**: Natural, helpful responses

### Success Criteria
After fine-tuning, the model should demonstrate:
- ✅ Better conversation flow
- ✅ Context-aware "yes" responses
- ✅ Accurate tool selection
- ✅ Graceful error handling
- ✅ Consistent "Samvaad" personality

## 🚀 Post-Training Deployment

### 1. Get Tuned Model
```python
import vertexai
from vertexai.preview import language_models

# Initialize Vertex AI
vertexai.init(project="speechtotext-466820", location="us-central1")

# Get the tuned model
tuned_model = language_models.TextGenerationModel.from_tuned_model(
    "projects/speechtotext-466820/locations/us-central1/models/MODEL_ID"
)
```

### 2. Update Agent Configuration
Update `backend/app/agent.py` to use the tuned model:
```python
# Replace the base model with tuned model
MODEL_NAME = "projects/speechtotext-466820/locations/us-central1/models/MODEL_ID"
```

### 3. Test the Tuned Model
```bash
# Test with curl
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Find restaurants in Koramangala"}'
```

## 💰 Cost Estimation

### Fine-Tuning Costs
- **Base Model**: Llama 3.1 8B
- **Training Time**: 2-4 hours
- **Estimated Cost**: $50-100 USD
- **Storage**: ~$1-2 USD/month

### Runtime Costs
- **Inference**: ~$0.01-0.05 per request
- **Monthly**: ~$10-50 USD for moderate usage

## 🔧 Troubleshooting

### Common Issues

#### 1. Authentication Errors
```bash
# Re-authenticate
gcloud auth login
gcloud auth application-default login
```

#### 2. API Not Enabled
```bash
# Enable required APIs
gcloud services enable vertexai.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com
```

#### 3. Insufficient Quotas
- Check quotas in Google Cloud Console
- Request quota increase if needed
- Use different region if quota exceeded

#### 4. Dataset Format Issues
```bash
# Validate dataset
python validate_dataset.py
```

### Error Messages

#### "Permission Denied"
- Check IAM roles
- Ensure project access
- Verify billing enabled

#### "Model Not Found"
- Check model name
- Verify region
- Ensure model is available

#### "Dataset Upload Failed"
- Check file existence
- Verify bucket permissions
- Check network connectivity

## 📞 Support

### Google Cloud Support
- **Documentation**: https://cloud.google.com/vertex-ai/docs
- **Support**: https://cloud.google.com/support
- **Community**: https://stackoverflow.com/questions/tagged/google-cloud-ai-platform

### Project-Specific Issues
- Check logs in Google Cloud Console
- Review fine_tuning_job.json for job details
- Monitor training metrics

## 🎉 Success Checklist

- [ ] gcloud authenticated and configured
- [ ] APIs enabled successfully
- [ ] Dataset uploaded to GCS
- [ ] Fine-tuning job launched
- [ ] Training completed successfully
- [ ] Tuned model accessible
- [ ] Agent updated with tuned model
- [ ] Performance tested and validated

---

**Generated**: August 2024  
**Project**: GoodFoods AI Agent  
**Model**: Llama 3.1 8B Fine-tuned  
**Dataset**: 100 examples (72KB) 