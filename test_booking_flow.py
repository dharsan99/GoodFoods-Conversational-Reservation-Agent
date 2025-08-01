#!/usr/bin/env python3
"""
Test the complete booking flow with the trained model
"""

import sys
import os
sys.path.append('backend')

from app.agent import GoodFoodsAgent

def test_booking_flow():
    """Test the complete booking flow"""
    
    print("🧪 Testing Complete Booking Flow...")
    print("=" * 60)
    
    # Initialize the agent
    agent = GoodFoodsAgent()
    
    # Simulate a complete booking conversation
    conversation = [
        "Hi",
        "Find restaurants near me",
        "Yes, I want to book at HSR Layout",
        "Book for 2 people tomorrow at 7 PM. My name is John and phone is 9876543210"
    ]
    
    for i, user_input in enumerate(conversation, 1):
        print(f"\n👤 User {i}: '{user_input}'")
        print("-" * 40)
        
        try:
            response = agent.get_response(user_input)
            print(f"🤖 Samvaad: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Booking flow test completed!")

def test_tool_calling():
    """Test specific tool calling scenarios"""
    
    print("\n🔧 Testing Tool Calling...")
    print("=" * 60)
    
    agent = GoodFoodsAgent()
    
    # Test specific tool calls
    tool_tests = [
        ("Show me menu specials", "Should call get_menu_specials"),
        ("What's your name?", "Should identify as Samvaad"),
        ("Find Italian restaurants", "Should call find_restaurants with Italian cuisine"),
        ("Check availability for 4 people tonight at 8 PM", "Should call check_availability")
    ]
    
    for test_input, expected in tool_tests:
        print(f"\n📝 Test: '{test_input}'")
        print(f"🎯 Expected: {expected}")
        print("-" * 40)
        
        try:
            response = agent.get_response(test_input)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_booking_flow()
    test_tool_calling() 