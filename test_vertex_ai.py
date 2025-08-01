#!/usr/bin/env python3
"""
Test script to verify Google Cloud Vertex AI setup with Llama 3.1 8B
"""

import os
from openai import OpenAI
import google.auth
import google.auth.transport.requests

# Configuration
PROJECT_ID = "speechtotext-466820"
LOCATION = "us-central1"
MODEL_ID = "meta/llama-3.1-8b-instruct-maas"

def get_gcp_token():
    """Gets a short-lived access token from Google Cloud credentials."""
    credentials, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)
    return credentials.token

def test_vertex_ai():
    """Test Vertex AI with Llama 3.1 8B"""
    print("🧪 Testing Google Cloud Vertex AI with Llama 3.1 8B...")
    
    try:
        # 1. Get the access token
        print("🔐 Getting GCP access token...")
        gcp_token = get_gcp_token()
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
        print("2. Check if you have the correct permissions")
        print("3. Verify your project ID and location")
        return False

if __name__ == "__main__":
    success = test_vertex_ai()
    if success:
        print("\n✅ Vertex AI setup is working correctly!")
        print("🚀 Ready for GoodFoods deployment!")
    else:
        print("\n❌ Vertex AI setup needs attention.")
        exit(1) 