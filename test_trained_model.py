#!/usr/bin/env python3
"""
Test script to verify the trained model is working correctly
"""

import sys
import os
sys.path.append('backend')

from app.agent import GoodFoodsAgent

def test_trained_model():
    """Test the trained model with various scenarios"""
    
    print("🧪 Testing Trained Model...")
    print("=" * 50)
    
    # Initialize the agent
    agent = GoodFoodsAgent()
    
    # Test scenarios
    test_cases = [
        "Hello",
        "Find restaurants in HSR Layout",
        "I need to book a table for 2 people",
        "Show me menu specials",
        "What's your name?"
    ]
    
    for i, test_input in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{test_input}'")
        print("-" * 30)
        
        try:
            response = agent.get_response(test_input)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")

if __name__ == "__main__":
    test_trained_model() 