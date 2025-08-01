#!/usr/bin/env python3
"""
Fine-Tuning Monitoring Script
"""

import json
import time
import vertexai
from vertexai.preview import language_models

def load_job_details():
    try:
        with open("fine_tuning_job.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ fine_tuning_job.json not found. Run fine-tuning first.")
        return None

def monitor_job():
    job_details = load_job_details()
    if not job_details:
        return
    
    print(f"🔍 Monitoring fine-tuning job: {job_details['display_name']}")
    print(f"🔗 Resource Name: {job_details['resource_name']}")
    
    # Initialize Vertex AI
    vertexai.init(project=job_details['project_id'], location=job_details['location'])
    
    try:
        # Get the tuning job
        tuning_job = language_models.SupervisedTuningJob(
            job_details['resource_name']
        )
        
        while True:
            # Get job status
            status = tuning_job.state
            print(f"📊 Status: {status}")
            
            if status in ["JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"]:
                if status == "JOB_STATE_SUCCEEDED":
                    print("🎉 Fine-tuning completed successfully!")
                    print(f"🤖 Tuned Model: {tuning_job.tuned_model}")
                else:
                    print(f"❌ Fine-tuning failed with status: {status}")
                break
            
            print("⏳ Waiting 60 seconds before next check...")
            time.sleep(60)
            
    except Exception as e:
        print(f"❌ Error monitoring job: {e}")

if __name__ == "__main__":
    monitor_job()
