#!/usr/bin/env python3
"""
Add more examples to reach exactly 100 training examples
"""

import json

def add_more_examples():
    """Add 6 more examples to reach 100"""
    
    # Read existing examples
    with open('training_100.jsonl', 'r', encoding='utf-8') as f:
        existing_examples = [json.loads(line) for line in f]
    
    # Additional examples to reach 100
    additional_examples = [
        {
            "messages": [
                {"role": "user", "content": "What's the best restaurant for a date?"},
                {"role": "model", "content": "I'd recommend GoodFoods Indiranagar for a romantic date! They have excellent Italian and Continental cuisine with a great ambiance. Would you like me to help you book a table there?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "I'm looking for a family restaurant"},
                {"role": "model", "content": "GoodFoods Koramangala is perfect for families! They have a wide variety of cuisines including North Indian, Chinese, and Multi-cuisine options that everyone will enjoy. Would you like me to help you book a table?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Do you have outdoor seating?"},
                {"role": "model", "content": "Yes, several of our GoodFoods locations offer outdoor seating! GoodFoods Indiranagar and GoodFoods Koramangala both have beautiful outdoor dining areas. Would you like me to help you find a restaurant with outdoor seating?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What's your most popular dish?"},
                {"role": "model", "content": "Our most popular dishes include the Butter Chicken, Paneer Tikka, and our signature Biryani. Would you like me to show you our current menu specials or help you book a table to try these dishes?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Can I bring my own wine?"},
                {"role": "model", "content": "I'm sorry, but I don't have information about BYOB policies. I'd recommend calling the specific restaurant directly to ask about their wine policy. Would you like me to help you find a restaurant or make a booking?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What's the dress code?"},
                {"role": "model", "content": "Our GoodFoods restaurants have a smart casual dress code. While formal attire isn't required, we recommend dressing comfortably but appropriately for a nice dining experience. Would you like me to help you book a table?"}
            ]
        }
    ]
    
    # Combine existing and additional examples
    all_examples = existing_examples + additional_examples
    
    # Write back to file
    with open('training_100.jsonl', 'w', encoding='utf-8') as f:
        for example in all_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    print(f"✅ Added {len(additional_examples)} more examples")
    print(f"📁 Total training examples: {len(all_examples)}")

if __name__ == "__main__":
    add_more_examples() 