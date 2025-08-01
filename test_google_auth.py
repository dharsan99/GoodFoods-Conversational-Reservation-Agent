#!/usr/bin/env python3
"""
Test Google Cloud authentication for the GoodFoods AI Agent
"""

import os
import json
from google.auth import default
from google.auth.transport.requests import Request
from google.cloud import aiplatform

def test_google_auth():
    """Test Google Cloud authentication"""
    
    print("🔍 Testing Google Cloud Authentication...")
    print("=" * 50)
    
    # Check environment variables
    print("📋 Environment Variables:")
    print(f"GOOGLE_CLOUD_PROJECT_ID: {os.getenv('GOOGLE_CLOUD_PROJECT_ID', 'NOT SET')}")
    print(f"GOOGLE_CLOUD_LOCATION: {os.getenv('GOOGLE_CLOUD_LOCATION', 'NOT SET')}")
    
    credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    if credentials_json:
        print(f"GOOGLE_APPLICATION_CREDENTIALS: {'SET' if credentials_json else 'NOT SET'}")
        
        # Try to parse the JSON
        try:
            if credentials_json.startswith('{'):
                # It's a JSON string
                creds_data = json.loads(credentials_json)
                print(f"✅ JSON parsed successfully")
                print(f"   Service Account: {creds_data.get('client_email', 'Unknown')}")
                print(f"   Project ID: {creds_data.get('project_id', 'Unknown')}")
            else:
                # It's a file path
                print(f"📁 Credentials file path: {credentials_json}")
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return False
    else:
        print("❌ GOOGLE_APPLICATION_CREDENTIALS not set")
        return False
    
    print("\n🔐 Testing Authentication...")
    
    try:
        # Initialize Vertex AI
        aiplatform.init(
            project=os.getenv('GOOGLE_CLOUD_PROJECT_ID'),
            location=os.getenv('GOOGLE_CLOUD_LOCATION')
        )
        print("✅ Vertex AI initialized successfully")
        
        # Test getting default credentials
        credentials, project = default()
        print(f"✅ Default credentials obtained")
        print(f"   Project: {project}")
        
        # Test making a simple API call
        print("\n🧪 Testing API Access...")
        
        # Try to list models (this should work with proper permissions)
        try:
            from vertexai.preview import language_models
            models = language_models.TextGenerationModel.list_models()
            print(f"✅ Successfully listed {len(models)} models")
        except Exception as e:
            print(f"⚠️  Could not list models: {e}")
            print("   This might be a permissions issue")
        
        print("\n✅ Authentication test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return False

def test_model_access():
    """Test specific model access"""
    
    print("\n🤖 Testing Model Access...")
    print("=" * 30)
    
    try:
        from vertexai.preview import language_models
        
        # Test the specific model we're using
        model_name = "7439580447044009984"  # Your trained model ID
        
        print(f"Testing access to model: {model_name}")
        
        # Try to get the model
        model = language_models.TextGenerationModel.from_pretrained(f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT_ID')}/locations/{os.getenv('GOOGLE_CLOUD_LOCATION')}/models/{model_name}")
        print("✅ Model access successful!")
        
        return True
        
    except Exception as e:
        print(f"❌ Model access failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 GoodFoods AI Agent - Google Cloud Auth Test")
    print("=" * 60)
    
    # Test basic authentication
    auth_success = test_google_auth()
    
    if auth_success:
        # Test model access
        model_success = test_model_access()
        
        if model_success:
            print("\n🎉 All tests passed! Google Cloud is properly configured.")
        else:
            print("\n⚠️  Authentication works but model access failed.")
            print("   Check if the model ID is correct and accessible.")
    else:
        print("\n❌ Authentication failed. Check your credentials and permissions.")
    
    print("\n📋 Next Steps:")
    print("1. If tests pass: Redeploy the backend service")
    print("2. If tests fail: Check service account permissions")
    print("3. Verify the model ID is correct") 