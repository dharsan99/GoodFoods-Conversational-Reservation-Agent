#!/usr/bin/env python3
"""
Create a proper validation dataset for Vertex AI fine-tuning
"""

import json

def create_validation_examples():
    """Create validation examples in input_text/output_text format"""
    
    validation_examples = [
        {
            "input_text": "User: Hello",
            "output_text": "Hello! I'm Samvaad, your AI assistant for GoodFoods restaurants. I can help you find restaurants, check availability, and make bookings. How can I assist you today?"
        },
        {
            "input_text": "User: Find restaurants in Koramangala",
            "output_text": "print(restaurant_tools.find_restaurants(location='Koramangala'))"
        },
        {
            "input_text": "User: Find restaurants in Koramangala\nUser: tool_outputs: [{'id': 1, 'name': 'GoodFoods Koramangala', 'address': 'Koramangala 4th Block, Bangalore', 'cuisine_type': 'Italian, Continental'}]\nAssistant: I found GoodFoods Koramangala in Koramangala 4th Block, Bangalore. They serve Italian and Continental cuisine. Would you like to book a table there?",
            "output_text": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"
        },
        {
            "input_text": "User: Book a table for 4 people tomorrow at 7 PM. My name is John and phone is 9876543210",
            "output_text": "print(restaurant_tools.create_booking(restaurant_id=1, party_size=4, date='tomorrow', time='7 PM', customer_name='John', phone_number='9876543210'))"
        },
        {
            "input_text": "User: Show me menu specials",
            "output_text": "print(restaurant_tools.get_menu_specials())"
        },
        {
            "input_text": "User: Show me menu specials\nUser: tool_outputs: [{'name': 'Pan-Seared Scallops', 'description': 'Fresh sea scallops with truffle risotto and seasonal vegetables', 'price': '₹1,200', 'dietary': 'non-vegetarian', 'restaurant_id': 1}, {'name': 'Mushroom Risotto', 'description': 'Creamy Arborio rice with wild mushrooms and parmesan', 'price': '₹850', 'dietary': 'vegetarian', 'restaurant_id': 2}]\nAssistant: Here are our current menu specials:\n1. Pan-Seared Scallops - Fresh sea scallops with truffle risotto and seasonal vegetables (₹1,200)\n2. Mushroom Risotto - Creamy Arborio rice with wild mushrooms and parmesan (₹850)\n\nThese are our chef's recommendations for today!",
            "output_text": "I'm glad you like our specials! Would you like me to help you find a restaurant to enjoy these dishes, or would you like to make a reservation?"
        },
        {
            "input_text": "User: Check availability for 2 people tonight at 8 PM",
            "output_text": "print(restaurant_tools.check_availability(restaurant_id=1, party_size=2, date='tonight', time='8 PM'))"
        },
        {
            "input_text": "User: Cancel my booking",
            "output_text": "I'd be happy to help you cancel your booking. Could you please provide your booking ID or the phone number you used for the reservation?"
        },
        {
            "input_text": "User: Find Italian restaurants",
            "output_text": "print(restaurant_tools.find_restaurants(cuisine='Italian'))"
        },
        {
            "input_text": "User: What's your name?",
            "output_text": "I'm Samvaad, your AI assistant for GoodFoods restaurants. I'm here to help you with restaurant reservations and dining information!"
        }
    ]
    
    return validation_examples

def main():
    """Create and save validation dataset"""
    print("🔄 Creating validation dataset...")
    
    validation_examples = create_validation_examples()
    
    # Save to file
    with open("validation_vertex_ai.jsonl", "w", encoding="utf-8") as f:
        for example in validation_examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')
    
    print(f"✅ Created validation dataset with {len(validation_examples)} examples")
    print("📁 File: validation_vertex_ai.jsonl")
    
    # Show sample
    print("\n📋 Sample validation example:")
    sample = validation_examples[0]
    print(f"Input: {sample['input_text']}")
    print(f"Output: {sample['output_text']}")
    
    print("\n📋 Next Steps:")
    print("1. Upload to GCS: gsutil cp validation_vertex_ai.jsonl gs://goodfoods-datasets-speechtotext-466820/datasets/")
    print("2. Run fine-tuning with updated validation dataset")

if __name__ == "__main__":
    main() 