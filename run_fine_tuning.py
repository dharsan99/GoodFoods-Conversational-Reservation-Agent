#!/usr/bin/env python3
"""
Vertex AI Fine-Tuning Script for GoodFoods AI Agent
Updated for correct Vertex AI API and dataset format
"""

import vertexai
from vertexai.preview import language_models
import time
from datetime import datetime
import json

def main():
    # Configuration
    PROJECT_ID = "speechtotext-466820"
    LOCATION = "us-central1"
    BASE_MODEL_NAME = "meta/llama3-1-8b"
    TRAINING_DATA_URI = "gs://goodfoods-datasets-speechtotext-466820/datasets/training_vertex_ai.jsonl"
    VALIDATION_DATA_URI = "gs://goodfoods-datasets-speechtotext-466820/datasets/validation_vertex_ai.jsonl"
    TUNED_MODEL_DISPLAY_NAME = "llama3-1-8b-goodfoods-agent-v1"
    
    print("🚀 Starting Vertex AI Fine-Tuning...")
    print(f"📊 Project: {PROJECT_ID}")
    print(f"📍 Location: {LOCATION}")
    print(f"🤖 Base Model: {BASE_MODEL_NAME}")
    print(f"📁 Training Data: {TRAINING_DATA_URI}")
    print(f"📁 Validation Data: {VALIDATION_DATA_URI}")
    print(f"🎯 Tuned Model Name: {TUNED_MODEL_DISPLAY_NAME}")
    
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    try:
        # Create the fine-tuning job using the correct API
        print("🔄 Creating fine-tuning job...")
        
        # First, get the base model
        base_model = language_models.TextGenerationModel.from_pretrained(BASE_MODEL_NAME)
        
        # Use the correct method for fine-tuning
        tuning_job = base_model.tune_model(
            training_data=TRAINING_DATA_URI,
            validation_data=VALIDATION_DATA_URI,
            model_display_name=TUNED_MODEL_DISPLAY_NAME,
            # Fine-tuning parameters
            tuning_method="supervised",
            hyperparameters={
                "epoch_count": 5,
                "learning_rate_multiplier": 1.0,
                "adapter_size": 8
            }
        )
        
        print(f"✅ Fine-tuning job created successfully!")
        print(f"🔗 Job Resource Name: {tuning_job.resource_name}")
        print(f"📊 Monitor progress at: https://console.cloud.google.com/vertex-ai/training/tuning-jobs")
        
        # Save job details
        job_details = {
            "resource_name": tuning_job.resource_name,
            "display_name": TUNED_MODEL_DISPLAY_NAME,
            "start_time": datetime.now().isoformat(),
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "base_model": BASE_MODEL_NAME,
            "training_data": TRAINING_DATA_URI,
            "validation_data": VALIDATION_DATA_URI,
            "tuned_model_name": TUNED_MODEL_DISPLAY_NAME,
            "status": "created"
        }
        
        with open("fine_tuning_job.json", "w") as f:
            json.dump(job_details, f, indent=2)
        
        print("💾 Job details saved to fine_tuning_job.json")
        print("\n📋 Next Steps:")
        print("1. Monitor progress: python monitor_fine_tuning.py")
        print("2. Check console: https://console.cloud.google.com/vertex-ai/training/tuning-jobs")
        print("3. Wait for completion (2-4 hours)")
        
    except Exception as e:
        print(f"❌ Error creating fine-tuning job: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if Vertex AI API is enabled")
        print("2. Verify dataset format is correct")
        print("3. Ensure billing is enabled")
        print("4. Check quotas and permissions")
        raise

if __name__ == "__main__":
    main()
