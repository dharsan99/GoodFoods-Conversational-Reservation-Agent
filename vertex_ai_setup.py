#!/usr/bin/env python3
"""
Vertex AI Fine-Tuning Setup for GoodFoods AI Agent
Handles authentication, dataset upload, and fine-tuning job configuration
"""

import os
import subprocess
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class VertexAISetup:
    def __init__(self, project_id: str, location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        self.bucket_name = f"goodfoods-datasets-{project_id}"
        self.training_data_uri = f"gs://{self.bucket_name}/datasets/training_100.jsonl"
        self.validation_data_uri = f"gs://{self.bucket_name}/datasets/validation_100.jsonl"
        self.tuned_model_display_name = "llama3-1-8b-goodfoods-agent-v1"
        
    def check_gcloud_auth(self) -> bool:
        """Check if gcloud is authenticated and configured"""
        try:
            result = subprocess.run(
                ["gcloud", "auth", "list", "--filter=status:ACTIVE", "--format=value(account)"],
                capture_output=True, text=True, check=True
            )
            if result.stdout.strip():
                print(f"✅ Authenticated as: {result.stdout.strip()}")
                return True
            else:
                print("❌ No active gcloud authentication found")
                return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking gcloud auth: {e}")
            return False
    
    def check_project_access(self) -> bool:
        """Check if we have access to the specified project"""
        try:
            result = subprocess.run(
                ["gcloud", "config", "get-value", "project"],
                capture_output=True, text=True, check=True
            )
            current_project = result.stdout.strip()
            
            if current_project != self.project_id:
                print(f"🔄 Setting project to {self.project_id}")
                subprocess.run(
                    ["gcloud", "config", "set", "project", self.project_id],
                    check=True
                )
            else:
                print(f"✅ Project already set to {self.project_id}")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error setting project: {e}")
            return False
    
    def enable_apis(self) -> bool:
        """Enable required Google Cloud APIs"""
        apis = [
            "vertexai.googleapis.com",
            "storage.googleapis.com",
            "aiplatform.googleapis.com"
        ]
        
        print("🔧 Enabling required APIs...")
        for api in apis:
            try:
                subprocess.run(
                    ["gcloud", "services", "enable", api],
                    check=True, capture_output=True
                )
                print(f"✅ Enabled {api}")
            except subprocess.CalledProcessError as e:
                print(f"⚠️  API {api} may already be enabled or failed: {e}")
        
        return True
    
    def create_storage_bucket(self) -> bool:
        """Create Google Cloud Storage bucket for datasets"""
        try:
            # Check if bucket exists
            result = subprocess.run(
                ["gsutil", "ls", f"gs://{self.bucket_name}"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                print(f"✅ Bucket {self.bucket_name} already exists")
                return True
            
            # Create bucket
            print(f"🔄 Creating bucket {self.bucket_name}...")
            subprocess.run(
                ["gsutil", "mb", "-l", self.location, f"gs://{self.bucket_name}"],
                check=True
            )
            print(f"✅ Created bucket {self.bucket_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error creating bucket: {e}")
            return False
    
    def upload_datasets(self) -> bool:
        """Upload training and validation datasets to GCS"""
        try:
            # Check if files exist locally
            if not os.path.exists("training_100.jsonl"):
                print("❌ training_100.jsonl not found")
                return False
            
            if not os.path.exists("validation_100.jsonl"):
                print("❌ validation_100.jsonl not found")
                return False
            
            # Upload training data
            print("📤 Uploading training dataset...")
            subprocess.run(
                ["gsutil", "cp", "training_100.jsonl", self.training_data_uri],
                check=True
            )
            print(f"✅ Uploaded training data to {self.training_data_uri}")
            
            # Upload validation data
            print("📤 Uploading validation dataset...")
            subprocess.run(
                ["gsutil", "cp", "validation_100.jsonl", self.validation_data_uri],
                check=True
            )
            print(f"✅ Uploaded validation data to {self.validation_data_uri}")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error uploading datasets: {e}")
            return False
    
    def create_fine_tuning_script(self) -> str:
        """Create the fine-tuning Python script"""
        script_content = f'''#!/usr/bin/env python3
"""
Vertex AI Fine-Tuning Script for GoodFoods AI Agent
"""

import vertexai
from vertexai.preview import language_models
import time
from datetime import datetime

def main():
    # Configuration
    PROJECT_ID = "{self.project_id}"
    LOCATION = "{self.location}"
    BASE_MODEL_NAME = "meta/llama3-1-8b"
    TRAINING_DATA_URI = "{self.training_data_uri}"
    VALIDATION_DATA_URI = "{self.validation_data_uri}"
    TUNED_MODEL_DISPLAY_NAME = "{self.tuned_model_display_name}"
    
    print("🚀 Starting Vertex AI Fine-Tuning...")
    print(f"📊 Project: {{PROJECT_ID}}")
    print(f"📍 Location: {{LOCATION}}")
    print(f"🤖 Base Model: {{BASE_MODEL_NAME}}")
    print(f"📁 Training Data: {{TRAINING_DATA_URI}}")
    print(f"📁 Validation Data: {{VALIDATION_DATA_URI}}")
    print(f"🎯 Tuned Model Name: {{TUNED_MODEL_DISPLAY_NAME}}")
    
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    try:
        # Define tuning job
        tuning_job = language_models.SupervisedTuningJob(
            display_name=f"tune-{{TUNED_MODEL_DISPLAY_NAME}}",
            source_model=BASE_MODEL_NAME,
            train_dataset=TRAINING_DATA_URI,
            validation_dataset=VALIDATION_DATA_URI,
            epoch_count=5,
            adapter_size=8,
            learning_rate_multiplier=1.0
        )
        
        # Launch tuning job
        print("🔄 Launching fine-tuning job...")
        tuning_job.run()
        
        print(f"✅ Fine-tuning job launched successfully!")
        print(f"🔗 Job Resource Name: {{tuning_job.resource_name}}")
        print(f"📊 Monitor progress at: https://console.cloud.google.com/vertex-ai/training/tuning-jobs")
        
        # Save job details
        job_details = {{
            "resource_name": tuning_job.resource_name,
            "display_name": tuning_job.display_name,
            "start_time": datetime.now().isoformat(),
            "project_id": PROJECT_ID,
            "location": LOCATION,
            "base_model": BASE_MODEL_NAME,
            "training_data": TRAINING_DATA_URI,
            "validation_data": VALIDATION_DATA_URI,
            "tuned_model_name": TUNED_MODEL_DISPLAY_NAME
        }}
        
        with open("fine_tuning_job.json", "w") as f:
            json.dump(job_details, f, indent=2)
        
        print("💾 Job details saved to fine_tuning_job.json")
        
    except Exception as e:
        print(f"❌ Error launching fine-tuning job: {{e}}")
        raise

if __name__ == "__main__":
    main()
'''
        
        with open("run_fine_tuning.py", "w") as f:
            f.write(script_content)
        
        print("✅ Created fine-tuning script: run_fine_tuning.py")
        return "run_fine_tuning.py"
    
    def create_monitoring_script(self) -> str:
        """Create a script to monitor fine-tuning progress"""
        script_content = f'''#!/usr/bin/env python3
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
    
    print(f"🔍 Monitoring fine-tuning job: {{job_details['display_name']}}")
    print(f"🔗 Resource Name: {{job_details['resource_name']}}")
    
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
            print(f"📊 Status: {{status}}")
            
            if status in ["JOB_STATE_SUCCEEDED", "JOB_STATE_FAILED", "JOB_STATE_CANCELLED"]:
                if status == "JOB_STATE_SUCCEEDED":
                    print("🎉 Fine-tuning completed successfully!")
                    print(f"🤖 Tuned Model: {{tuning_job.tuned_model}}")
                else:
                    print(f"❌ Fine-tuning failed with status: {{status}}")
                break
            
            print("⏳ Waiting 60 seconds before next check...")
            time.sleep(60)
            
    except Exception as e:
        print(f"❌ Error monitoring job: {{e}}")

if __name__ == "__main__":
    monitor_job()
'''
        
        with open("monitor_fine_tuning.py", "w") as f:
            f.write(script_content)
        
        print("✅ Created monitoring script: monitor_fine_tuning.py")
        return "monitor_fine_tuning.py"
    
    def setup(self) -> bool:
        """Complete setup process"""
        print("🚀 Starting Vertex AI Fine-Tuning Setup...")
        print("=" * 50)
        
        # Step 1: Check authentication
        if not self.check_gcloud_auth():
            print("❌ Please run: gcloud auth login")
            return False
        
        # Step 2: Check project access
        if not self.check_project_access():
            print("❌ Project access failed")
            return False
        
        # Step 3: Enable APIs
        if not self.enable_apis():
            print("❌ API enablement failed")
            return False
        
        # Step 4: Create storage bucket
        if not self.create_storage_bucket():
            print("❌ Bucket creation failed")
            return False
        
        # Step 5: Upload datasets
        if not self.upload_datasets():
            print("❌ Dataset upload failed")
            return False
        
        # Step 6: Create scripts
        self.create_fine_tuning_script()
        self.create_monitoring_script()
        
        print("=" * 50)
        print("✅ Vertex AI Setup Complete!")
        print("\n📋 Next Steps:")
        print("1. Run fine-tuning: python run_fine_tuning.py")
        print("2. Monitor progress: python monitor_fine_tuning.py")
        print("3. Check console: https://console.cloud.google.com/vertex-ai/training/tuning-jobs")
        
        return True

def main():
    """Main setup function"""
    # Configuration
    PROJECT_ID = "speechtotext-466820"  # Your project ID
    
    setup = VertexAISetup(PROJECT_ID)
    success = setup.setup()
    
    if success:
        print("\n🎉 Ready to start fine-tuning!")
    else:
        print("\n❌ Setup failed. Please check the errors above.")

if __name__ == "__main__":
    main() 