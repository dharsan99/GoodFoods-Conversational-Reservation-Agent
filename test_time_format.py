#!/usr/bin/env python3
"""
Test the improved time and date formatting
"""

import sys
import os
sys.path.append('backend')

from app.agent import GoodFoodsAgent

def test_time_and_date_formatting():
    """Test time and date formatting improvements"""
    
    print("🕐 Testing Time and Date Formatting...")
    print("=" * 60)
    
    # Initialize the agent
    agent = GoodFoodsAgent()
    
    # Test scenarios
    test_cases = [
        ("Check availability for 2 people tonight at 7 PM", "Should show 7:00 PM and today's date"),
        ("Book for 4 people tomorrow at 8 PM. My name is Sarah and phone is 9876543210", "Should show tomorrow's date and 8:00 PM"),
        ("Show me menu specials", "Should show menu specials"),
        ("What's your name?", "Should identify as Samvaad")
    ]
    
    for i, (test_input, expected) in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: '{test_input}'")
        print(f"🎯 Expected: {expected}")
        print("-" * 50)
        
        try:
            response = agent.get_response(test_input)
            print(f"🤖 Response: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Time and date formatting test completed!")

if __name__ == "__main__":
    test_time_and_date_formatting() 