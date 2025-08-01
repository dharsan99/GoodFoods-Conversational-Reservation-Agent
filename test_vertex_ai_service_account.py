#!/usr/bin/env python3
"""
Test script to verify Google Cloud Vertex AI setup with service account
"""

import os
import json
from openai import OpenAI
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

# Configuration
PROJECT_ID = "speechtotext-466820"
LOCATION = "us-central1"
MODEL_ID = "meta/llama-3.1-8b-instruct-maas"
SERVICE_ACCOUNT_KEY_FILE = "goodfoods-render-key.json"

def get_gcp_token_with_service_account():
    """Gets a short-lived access token using service account credentials."""
    try:
        # Load service account credentials
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_KEY_FILE,
            scopes=['https://www.googleapis.com/auth/cloud-platform']
        )
        
        # Get access token
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        return credentials.token
    except Exception as e:
        print(f"Error getting token with service account: {e}")
        return None

def test_vertex_ai_with_service_account():
    """Test Vertex AI with Llama 3.1 8B using service account"""
    print("🧪 Testing Google Cloud Vertex AI with Service Account...")
    
    try:
        # 1. Get the access token using service account
        print("🔐 Getting GCP access token with service account...")
        gcp_token = get_gcp_token_with_service_account()
        if not gcp_token:
            print("❌ Failed to get access token")
            return False
        print("✅ Access token obtained successfully!")
        
        # 2. Initialize the OpenAI client
        print("🔧 Initializing OpenAI client for Vertex AI...")
        client = OpenAI(
            api_key=gcp_token,
            base_url=f"https://{LOCATION}-aiplatform.googleapis.com/v1/projects/{PROJECT_ID}/locations/{LOCATION}/endpoints/openapi"
        )
        print("✅ OpenAI client initialized!")
        
        # 3. Test message
        test_message = "Hello! Can you help me find a restaurant in Bangalore?"
        
        # 4. Make the chat completion request
        print(f"📤 Sending test message: '{test_message}'")
        print("⏳ Waiting for Llama 3.1 8B response...")
        
        chat_completion = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant for restaurant recommendations."},
                {"role": "user", "content": test_message}
            ],
            temperature=0.7,
            max_tokens=250,
        )
        
        # 5. Print the response
        print("\n" + "="*50)
        print("🎉 SUCCESS! Llama 3.1 8B Response:")
        print("="*50)
        print(chat_completion.choices[0].message.content)
        print("="*50)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error testing Vertex AI: {e}")
        print("\n🔍 Troubleshooting tips:")
        print("1. Make sure Vertex AI API is enabled")
        print("2. Check if service account has correct permissions")
        print("3. Verify your project ID and location")
        print("4. Check if the service account key file exists")
        return False

if __name__ == "__main__":
    # Check if service account key file exists
    if not os.path.exists(SERVICE_ACCOUNT_KEY_FILE):
        print(f"❌ Service account key file '{SERVICE_ACCOUNT_KEY_FILE}' not found!")
        print("Please make sure you have created the service account key.")
        exit(1)
    
    success = test_vertex_ai_with_service_account()
    if success:
        print("\n✅ Vertex AI setup is working correctly!")
        print("🚀 Ready for GoodFoods deployment!")
    else:
        print("\n❌ Vertex AI setup needs attention.")
        exit(1) 