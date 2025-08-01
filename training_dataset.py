#!/usr/bin/env python3
"""
Training Dataset Generator for GoodFoods AI Agent
Creates comprehensive JSONL files for Vertex AI fine-tuning
Following the guide's format for conversational agent training
"""

import json
from datetime import datetime, timedelta
import random

def create_training_examples():
    """Generate comprehensive training examples for the restaurant reservation agent"""
    
    examples = []
    
    # 1. Baseline Conversational Scenarios (No Tool-Calling)
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "Hello"},
                {"role": "model", "content": "Hello! I'm Samvaad, your AI assistant for GoodFoods restaurants. I can help you find restaurants, check availability, and make bookings. How can I assist you today?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Hi there"},
                {"role": "model", "content": "Hi! I'm Samvaad from GoodFoods. I'm here to help you with restaurant reservations and dining information. What would you like to do today?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What are your opening hours?"},
                {"role": "model", "content": "Our GoodFoods restaurants are typically open from 11:00 AM to 11:00 PM daily, with some locations having extended hours on weekends. The exact hours may vary by location. Would you like me to help you find a restaurant near you?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Where are you located?"},
                {"role": "model", "content": "GoodFoods has multiple locations across Bangalore including Koramangala, Indiranagar, Jayanagar, Whitefield, and Electronic City. I can help you find the restaurant closest to you or in a specific area. Where would you like to dine?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What's the weather like today?"},
                {"role": "model", "content": "I'm sorry, but I'm specifically designed to help with GoodFoods restaurant reservations and dining information. I can't provide weather updates, but I'd be happy to help you find a great restaurant or make a booking!"}
            ]
        }
    ])
    
    # 2. Simple Restaurant Search Scenarios
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "Find restaurants in Koramangala"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Koramangala'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 1, 'name': 'GoodFoods Koramangala', 'address': 'Koramangala 4th Block, Bangalore', 'cuisine_type': 'Multi-cuisine, North Indian, Chinese'}]"},
                {"role": "model", "content": "I found GoodFoods Koramangala in Koramangala 4th Block, Bangalore. They serve Multi-cuisine, North Indian, Chinese cuisine. Would you like to book a table there?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Show me Italian restaurants"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(cuisine='Italian'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 2, 'name': 'GoodFoods Indiranagar', 'address': 'Indiranagar 100 Feet Road, Bangalore', 'cuisine_type': 'Multi-cuisine, Italian, Continental'}, {'id': 4, 'name': 'GoodFoods Whitefield', 'address': 'Whitefield Main Road, Bangalore', 'cuisine_type': 'Multi-cuisine, Continental, Italian'}]"},
                {"role": "model", "content": "I found 2 restaurants:\n1. GoodFoods Indiranagar - Indiranagar 100 Feet Road, Bangalore (Multi-cuisine, Italian, Continental)\n2. GoodFoods Whitefield - Whitefield Main Road, Bangalore (Multi-cuisine, Continental, Italian)\n\nWhich one would you like to book?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "I want South Indian food"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(cuisine='South Indian'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 3, 'name': 'GoodFoods Jayanagar', 'address': 'Jayanagar 4th Block, Bangalore', 'cuisine_type': 'South Indian, North Indian, Chinese'}]"},
                {"role": "model", "content": "I found GoodFoods Jayanagar in Jayanagar 4th Block, Bangalore. They serve South Indian, North Indian, Chinese cuisine. Would you like to book a table there?"}
            ]
        }
    ])
    
    # 3. Multi-Turn Information Gathering Dialogues
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "I want to book a table"},
                {"role": "model", "content": "I'd be happy to help you book a table! Could you please provide:\n1. Number of people\n2. Date (e.g., tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"},
                {"role": "user", "content": "4 people, tomorrow at 8pm, my name is Rahul Sharma and phone is +91-98765-43210"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tomorrow', time='8pm', party_size=4))"},
                {"role": "user", "content": "tool_outputs: ['19:00', '20:00', '21:00']"},
                {"role": "model", "content": "Great! A table for 4 people is available at 8:00 PM tomorrow. Would you like me to proceed with the booking?"},
                {"role": "user", "content": "Yes, please book it"},
                {"role": "model", "content": "print(restaurant_tools.create_booking(restaurant_id=1, user_name='Rahul Sharma', phone_number='+91-98765-43210', date='tomorrow', time='8pm', party_size=4))"},
                {"role": "user", "content": "tool_outputs: {'success': True, 'booking_id': 'GF123456', 'restaurant_name': 'GoodFoods Koramangala', 'date': '2024-08-15', 'time': '20:00', 'party_size': 4}"},
                {"role": "model", "content": "Excellent! Your booking is confirmed. Your booking reference is GF123456. We look forward to seeing you at GoodFoods Koramangala on 2024-08-15 at 20:00 for 4 people."}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Book a table for 2 people"},
                {"role": "model", "content": "I'd be happy to help you book a table! Could you please provide:\n1. Date (e.g., today, tomorrow, Friday)\n2. Time (e.g., 7 PM, 8 PM)\n3. Your name and phone number"},
                {"role": "user", "content": "Today at 7pm, Priya Patel, +91-87654-32109"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='today', time='7pm', party_size=2))"},
                {"role": "user", "content": "tool_outputs: ['18:30', '19:00', '19:30']"},
                {"role": "model", "content": "Great! A table for 2 people is available at 7:00 PM today. Would you like me to proceed with the booking?"},
                {"role": "user", "content": "Yes"},
                {"role": "model", "content": "print(restaurant_tools.create_booking(restaurant_id=1, user_name='Priya Patel', phone_number='+91-87654-32109', date='today', time='7pm', party_size=2))"},
                {"role": "user", "content": "tool_outputs: {'success': True, 'booking_id': 'GF123457', 'restaurant_name': 'GoodFoods Koramangala', 'date': '2024-08-14', 'time': '19:00', 'party_size': 2}"},
                {"role": "model", "content": "Excellent! Your booking is confirmed. Your booking reference is GF123457. We look forward to seeing you at GoodFoods Koramangala on 2024-08-14 at 19:00 for 2 people."}
            ]
        }
    ])
    
    # 4. Menu Specials Scenarios
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "What are your menu specials?"},
                {"role": "model", "content": "print(restaurant_tools.get_menu_specials())"},
                {"role": "user", "content": "tool_outputs: [{'name': 'Pan-Seared Scallops', 'description': 'Fresh sea scallops with truffle risotto and seasonal vegetables', 'price': '₹1,200', 'dietary': 'non-vegetarian'}, {'name': 'Mushroom Risotto', 'description': 'Creamy Arborio rice with wild mushrooms and parmesan', 'price': '₹850', 'dietary': 'vegetarian'}]"},
                {"role": "model", "content": "Here are our current menu specials:\n1. Pan-Seared Scallops - Fresh sea scallops with truffle risotto and seasonal vegetables (₹1,200)\n2. Mushroom Risotto - Creamy Arborio rice with wild mushrooms and parmesan (₹850)\n\nThese are our chef's recommendations for today!"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Show me vegetarian specials"},
                {"role": "model", "content": "print(restaurant_tools.get_menu_specials(dietary_preference='vegetarian'))"},
                {"role": "user", "content": "tool_outputs: [{'name': 'Mushroom Risotto', 'description': 'Creamy Arborio rice with wild mushrooms and parmesan', 'price': '₹850', 'dietary': 'vegetarian'}, {'name': 'Truffle Pasta', 'description': 'Homemade fettuccine with black truffle and cream sauce', 'price': '₹900', 'dietary': 'vegetarian'}]"},
                {"role": "model", "content": "Here are our current menu specials:\n1. Mushroom Risotto - Creamy Arborio rice with wild mushrooms and parmesan (₹850)\n2. Truffle Pasta - Homemade fettuccine with black truffle and cream sauce (₹900)\n\nThese are our chef's recommendations for today!"}
            ]
        }
    ])
    
    # 5. Booking Management Scenarios
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "I need to cancel my booking GF123456"},
                {"role": "model", "content": "print(restaurant_tools.cancel_booking(booking_id='GF123456'))"},
                {"role": "user", "content": "tool_outputs: True"},
                {"role": "model", "content": "Your booking has been cancelled successfully. Thank you for letting us know."}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Check my booking details for GF123456"},
                {"role": "model", "content": "print(restaurant_tools.get_booking_details(booking_id='GF123456'))"},
                {"role": "user", "content": "tool_outputs: {'success': True, 'booking_id': 'GF123456', 'restaurant_name': 'GoodFoods Koramangala', 'date': '2024-08-15', 'time': '20:00', 'party_size': 4, 'status': 'confirmed'}"},
                {"role": "model", "content": "Here are your booking details:\n- Booking ID: GF123456\n- Restaurant: GoodFoods Koramangala\n- Date: 2024-08-15\n- Time: 20:00\n- Party Size: 4\n- Status: confirmed"}
            ]
        }
    ])
    
    # 6. Error Handling Scenarios
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "I need a table for 10 people tonight at 8pm"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tonight', time='8pm', party_size=10))"},
                {"role": "user", "content": "tool_outputs: {'status': 'error', 'message': 'Party size too large for online booking. Please call the restaurant directly.'}"},
                {"role": "model", "content": "I'm sorry, but for parties larger than 8 people, we ask that you call the restaurant directly to make arrangements. Our phone number is (080) 2555-1234."}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Book a table for 4 people tomorrow at 8pm"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tomorrow', time='8pm', party_size=4))"},
                {"role": "user", "content": "tool_outputs: []"},
                {"role": "model", "content": "I'm sorry, but there are no tables available at that time. Would you like me to check for alternative times?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Cancel booking GF999999"},
                {"role": "model", "content": "print(restaurant_tools.cancel_booking(booking_id='GF999999'))"},
                {"role": "user", "content": "tool_outputs: False"},
                {"role": "model", "content": "I'm sorry, I couldn't find that booking to cancel. Please check your booking reference number."}
            ]
        }
    ])
    
    # 7. Sequential Tool-Calling Scenarios
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "I want to book a table for 2 people tonight and also see the specials"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tonight', time='7pm', party_size=2))"},
                {"role": "user", "content": "tool_outputs: ['19:00', '19:30', '20:00']"},
                {"role": "model", "content": "print(restaurant_tools.get_menu_specials())"},
                {"role": "user", "content": "tool_outputs: [{'name': 'Pan-Seared Scallops', 'description': 'Fresh sea scallops with truffle risotto and seasonal vegetables', 'price': '₹1,200', 'dietary': 'non-vegetarian'}, {'name': 'Wagyu Beef Burger', 'description': 'Premium Wagyu beef patty with aged cheddar and caramelized onions', 'price': '₹950', 'dietary': 'non-vegetarian'}]"},
                {"role": "model", "content": "Yes, we do have a table for 2 available at 7:00 PM tonight! Our current specials are the Pan-Seared Scallops and our famous Wagyu Beef Burger. Would you like me to book that table for you?"}
            ]
        }
    ])
    
    # 8. Context-Aware Booking Confirmations
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "Find restaurants in Koramangala"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Koramangala'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 1, 'name': 'GoodFoods Koramangala', 'address': 'Koramangala 4th Block, Bangalore', 'cuisine_type': 'Multi-cuisine, North Indian, Chinese'}]"},
                {"role": "model", "content": "I found GoodFoods Koramangala in Koramangala 4th Block, Bangalore. They serve Multi-cuisine, North Indian, Chinese cuisine. Would you like to book a table there?"},
                {"role": "user", "content": "yes"},
                {"role": "model", "content": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Show me Italian restaurants"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(cuisine='Italian'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 2, 'name': 'GoodFoods Indiranagar', 'address': 'Indiranagar 100 Feet Road, Bangalore', 'cuisine_type': 'Multi-cuisine, Italian, Continental'}]"},
                {"role": "model", "content": "I found GoodFoods Indiranagar in Indiranagar 100 Feet Road, Bangalore. They serve Multi-cuisine, Italian, Continental cuisine. Would you like to book a table there?"},
                {"role": "user", "content": "yes book table"},
                {"role": "model", "content": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"}
            ]
        }
    ])
    
    return examples

def create_validation_examples():
    """Generate validation examples (similar but different from training)"""
    
    examples = []
    
    # Similar scenarios but with different details
    examples.extend([
        {
            "messages": [
                {"role": "user", "content": "Find restaurants in Jayanagar"},
                {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Jayanagar'))"},
                {"role": "user", "content": "tool_outputs: [{'id': 3, 'name': 'GoodFoods Jayanagar', 'address': 'Jayanagar 4th Block, Bangalore', 'cuisine_type': 'South Indian, North Indian, Chinese'}]"},
                {"role": "model", "content": "I found GoodFoods Jayanagar in Jayanagar 4th Block, Bangalore. They serve South Indian, North Indian, Chinese cuisine. Would you like to book a table there?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "Book a table for 6 people Friday at 9pm"},
                {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='Friday', time='9pm', party_size=6))"},
                {"role": "user", "content": "tool_outputs: ['20:30', '21:00', '21:30']"},
                {"role": "model", "content": "Great! A table for 6 people is available at 9:00 PM on Friday. Would you like me to proceed with the booking?"}
            ]
        },
        {
            "messages": [
                {"role": "user", "content": "What vegan options do you have?"},
                {"role": "model", "content": "print(restaurant_tools.get_menu_specials(dietary_preference='vegan'))"},
                {"role": "user", "content": "tool_outputs: [{'name': 'Impossible Burger Deluxe', 'description': 'Plant-based burger with vegan cheese and special sauce', 'price': '₹750', 'dietary': 'vegan'}]"},
                {"role": "model", "content": "Here are our current menu specials:\n1. Impossible Burger Deluxe - Plant-based burger with vegan cheese and special sauce (₹750)\n\nThese are our chef's recommendations for today!"}
            ]
        }
    ])
    
    return examples

def write_jsonl_file(examples, filename):
    """Write examples to a JSONL file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Generate training and validation datasets"""
    print("Generating training dataset...")
    
    # Create training examples
    training_examples = create_training_examples()
    print(f"Created {len(training_examples)} training examples")
    
    # Create validation examples
    validation_examples = create_validation_examples()
    print(f"Created {len(validation_examples)} validation examples")
    
    # Write to files
    write_jsonl_file(training_examples, 'training.jsonl')
    write_jsonl_file(validation_examples, 'validation.jsonl')
    
    print("✅ Dataset generation complete!")
    print(f"📁 Training file: training.jsonl ({len(training_examples)} examples)")
    print(f"📁 Validation file: validation.jsonl ({len(validation_examples)} examples)")
    print("\n📊 Dataset Statistics:")
    print(f"   Total examples: {len(training_examples) + len(validation_examples)}")
    print(f"   Training/Validation split: {len(training_examples)}/{len(validation_examples)}")
    print(f"   Split ratio: {len(training_examples)/(len(training_examples) + len(validation_examples))*100:.1f}%/{len(validation_examples)/(len(training_examples) + len(validation_examples))*100:.1f}%")
    
    print("\n🎯 Dataset Coverage:")
    print("   ✅ Baseline conversations (greetings, FAQs)")
    print("   ✅ Restaurant search scenarios")
    print("   ✅ Multi-turn booking dialogues")
    print("   ✅ Menu specials queries")
    print("   ✅ Booking management (cancel, check details)")
    print("   ✅ Error handling scenarios")
    print("   ✅ Sequential tool-calling")
    print("   ✅ Context-aware confirmations")

if __name__ == "__main__":
    main() 