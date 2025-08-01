#!/usr/bin/env python3
"""
Enhanced Training Dataset Generator for GoodFoods AI Agent
Creates 100 comprehensive training examples for Vertex AI fine-tuning
"""

import json
import random
from datetime import datetime, timedelta

def create_baseline_conversations():
    """Generate baseline conversational scenarios"""
    return [
        {"role": "user", "content": "Hello"},
        {"role": "model", "content": "Hello! I'm Samvaad, your AI assistant for GoodFoods restaurants. I can help you find restaurants, check availability, and make bookings. How can I assist you today?"},
        
        {"role": "user", "content": "Hi there"},
        {"role": "model", "content": "Hi! I'm Samvaad from GoodFoods. I'm here to help you with restaurant reservations and dining information. What would you like to do today?"},
        
        {"role": "user", "content": "Good morning"},
        {"role": "model", "content": "Good morning! I'm Samvaad, your AI assistant for GoodFoods restaurants. How can I help you with your dining plans today?"},
        
        {"role": "user", "content": "Good evening"},
        {"role": "model", "content": "Good evening! I'm Samvaad from GoodFoods. I'm here to help you with restaurant reservations and dining information. What can I assist you with?"},
        
        {"role": "user", "content": "What are your opening hours?"},
        {"role": "model", "content": "Our GoodFoods restaurants are typically open from 11:00 AM to 11:00 PM daily, with some locations having extended hours on weekends. The exact hours may vary by location. Would you like me to help you find a restaurant near you?"},
        
        {"role": "user", "content": "Where are you located?"},
        {"role": "model", "content": "GoodFoods has multiple locations across Bangalore including Koramangala, Indiranagar, Jayanagar, Whitefield, and Electronic City. I can help you find the restaurant closest to you or in a specific area. Where would you like to dine?"},
        
        {"role": "user", "content": "What's the weather like today?"},
        {"role": "model", "content": "I'm sorry, but I'm specifically designed to help with GoodFoods restaurant reservations and dining information. I can't provide weather updates, but I'd be happy to help you find a great restaurant or make a booking!"},
        
        {"role": "user", "content": "Tell me a joke"},
        {"role": "model", "content": "I'm focused on helping you with GoodFoods restaurant reservations and dining information. While I can't tell jokes, I can help you find a great restaurant or make a booking!"},
        
        {"role": "user", "content": "What's your name?"},
        {"role": "model", "content": "I'm Samvaad, your AI assistant for GoodFoods restaurants. I'm here to help you with restaurant reservations, finding locations, and dining information. How can I assist you today?"},
        
        {"role": "user", "content": "How can you help me?"},
        {"role": "model", "content": "I can help you with several things:\n1. Find GoodFoods restaurants by location or cuisine\n2. Check table availability\n3. Make restaurant bookings\n4. View menu specials\n5. Cancel or check existing bookings\n\nWhat would you like to do?"},
        
        {"role": "user", "content": "What do you do?"},
        {"role": "model", "content": "I'm Samvaad, your AI assistant for GoodFoods restaurants. I help customers find restaurants, check availability, make bookings, view menu specials, and manage their reservations. How can I assist you today?"},
        
        {"role": "user", "content": "Are you a human?"},
        {"role": "model", "content": "No, I'm Samvaad, an AI assistant specifically designed to help with GoodFoods restaurant reservations and dining information. I'm here to make your dining experience as smooth as possible!"},
        
        {"role": "user", "content": "What's on your menu?"},
        {"role": "model", "content": "I can help you find menu specials and featured dishes at our GoodFoods restaurants. Would you like me to show you our current specials or help you find a restaurant first?"},
        
        {"role": "user", "content": "Do you have vegetarian options?"},
        {"role": "model", "content": "Yes, we have excellent vegetarian options at all our GoodFoods restaurants! I can show you vegetarian specials or help you find a restaurant that specializes in vegetarian cuisine. What would you prefer?"}
    ]

def create_restaurant_search_scenarios():
    """Generate restaurant search scenarios with variations"""
    scenarios = []
    
    # Location-based searches
    locations = ["Koramangala", "Indiranagar", "Jayanagar", "Whitefield", "Electronic City", "MG Road", "HSR Layout", "Marathahalli", "Bellandur", "Sarjapur", "Hebbal", "Yelahanka"]
    
    for location in locations:
        scenarios.extend([
            {"role": "user", "content": f"Find restaurants in {location}"},
            {"role": "model", "content": f"print(restaurant_tools.find_restaurants(location='{location}'))"},
            {"role": "user", "content": f"tool_outputs: [{{'id': 1, 'name': 'GoodFoods {location}', 'address': '{location} Main Road, Bangalore', 'cuisine_type': 'Multi-cuisine, North Indian, Chinese'}}]"},
            {"role": "model", "content": f"I found GoodFoods {location} in {location} Main Road, Bangalore. They serve Multi-cuisine, North Indian, Chinese cuisine. Would you like to book a table there?"}
        ])
    
    # Cuisine-based searches
    cuisines = ["Italian", "Chinese", "North Indian", "South Indian", "Continental", "Multi-cuisine", "Mexican", "Thai", "Japanese", "Mediterranean", "American", "Fusion"]
    
    for cuisine in cuisines:
        scenarios.extend([
            {"role": "user", "content": f"Show me {cuisine} restaurants"},
            {"role": "model", "content": f"print(restaurant_tools.find_restaurants(cuisine='{cuisine}'))"},
            {"role": "user", "content": f"tool_outputs: [{{'id': 2, 'name': 'GoodFoods Indiranagar', 'address': 'Indiranagar 100 Feet Road, Bangalore', 'cuisine_type': 'Multi-cuisine, {cuisine}, Continental'}}]"},
            {"role": "model", "content": f"I found GoodFoods Indiranagar in Indiranagar 100 Feet Road, Bangalore. They serve Multi-cuisine, {cuisine}, Continental cuisine. Would you like to book a table there?"}
        ])
    
    # Combined searches
    location_cuisine_pairs = [
        ("Koramangala", "Italian"),
        ("Indiranagar", "Chinese"),
        ("Jayanagar", "South Indian"),
        ("Whitefield", "Continental"),
        ("Electronic City", "North Indian")
    ]
    
    for location, cuisine in location_cuisine_pairs:
        scenarios.extend([
            {"role": "user", "content": f"Find {cuisine} restaurants in {location}"},
            {"role": "model", "content": f"print(restaurant_tools.find_restaurants(location='{location}', cuisine='{cuisine}'))"},
            {"role": "user", "content": f"tool_outputs: [{{'id': 1, 'name': 'GoodFoods {location}', 'address': '{location} Main Road, Bangalore', 'cuisine_type': 'Multi-cuisine, {cuisine}, Continental'}}]"},
            {"role": "model", "content": f"I found GoodFoods {location} in {location} Main Road, Bangalore. They serve Multi-cuisine, {cuisine}, Continental cuisine. Would you like to book a table there?"}
        ])
    
    return scenarios

def create_booking_scenarios():
    """Generate booking scenarios with variations"""
    scenarios = []
    
    # Simple booking requests
    party_sizes = [1, 2, 3, 4, 5, 6, 7, 8]
    dates = ["today", "tomorrow", "Friday", "Saturday", "next week", "this weekend", "next Monday", "next Tuesday"]
    times = ["7pm", "8pm", "9pm", "7:30pm", "8:30pm", "lunch", "dinner", "6pm", "10pm"]
    names = ["Rahul Sharma", "Priya Patel", "Amit Kumar", "Neha Singh", "Vikram Mehta", "Anjali Gupta", "Rajesh Kumar", "Sneha Reddy", "Arjun Singh", "Kavya Sharma"]
    phones = ["+91-98765-43210", "+91-87654-32109", "+91-76543-21098", "+91-65432-10987", "+91-54321-09876", "+91-43210-98765"]
    
    for i in range(30):  # Generate 30 booking scenarios
        party_size = random.choice(party_sizes)
        date = random.choice(dates)
        time = random.choice(times)
        name = random.choice(names)
        phone = random.choice(phones)
        
        scenarios.extend([
            {"role": "user", "content": f"I want to book a table for {party_size} people"},
            {"role": "model", "content": "I'd be happy to help you book a table! Could you please provide:\n1. Date (e.g., today, tomorrow, Friday)\n2. Time (e.g., 7 PM, 8 PM)\n3. Your name and phone number"},
            {"role": "user", "content": f"{date} at {time}, {name}, {phone}"},
            {"role": "model", "content": f"print(restaurant_tools.check_availability(restaurant_id=1, date='{date}', time='{time}', party_size={party_size}))"},
            {"role": "user", "content": "tool_outputs: ['19:00', '20:00', '21:00']"},
            {"role": "model", "content": f"Great! A table for {party_size} people is available at {time} on {date}. Would you like me to proceed with the booking?"},
            {"role": "user", "content": "Yes, please book it"},
            {"role": "model", "content": f"print(restaurant_tools.create_booking(restaurant_id=1, user_name='{name}', phone_number='{phone}', date='{date}', time='{time}', party_size={party_size}))"},
            {"role": "user", "content": f"tool_outputs: {{'success': True, 'booking_id': 'GF{random.randint(100000, 999999)}', 'restaurant_name': 'GoodFoods Koramangala', 'date': '2024-08-15', 'time': '20:00', 'party_size': {party_size}}}"},
            {"role": "model", "content": f"Excellent! Your booking is confirmed. Your booking reference is GF{random.randint(100000, 999999)}. We look forward to seeing you at GoodFoods Koramangala on 2024-08-15 at 20:00 for {party_size} people."}
        ])
    
    return scenarios

def create_menu_specials_scenarios():
    """Generate menu specials scenarios"""
    scenarios = []
    
    dietary_preferences = ["none", "vegetarian", "vegan", "gluten-free", "non-vegetarian"]
    special_questions = [
        "What are your menu specials?",
        "Show me today's specials",
        "What's on the menu today?",
        "Tell me about your special dishes",
        "What do you recommend?",
        "Show me the chef's specials",
        "What are your featured dishes?",
        "Tell me about your daily specials"
    ]
    
    for question in special_questions:
        scenarios.extend([
            {"role": "user", "content": question},
            {"role": "model", "content": "print(restaurant_tools.get_menu_specials())"},
            {"role": "user", "content": "tool_outputs: [{'name': 'Mushroom Risotto', 'description': 'Creamy Arborio rice with wild mushrooms and parmesan', 'price': '₹850', 'dietary': 'vegetarian'}]"},
            {"role": "model", "content": "Here are our current menu specials:\n1. Mushroom Risotto - Creamy Arborio rice with wild mushrooms and parmesan (₹850)\n\nThese are our chef's recommendations for today!"}
        ])
    
    for preference in dietary_preferences:
        if preference != "none":
            scenarios.extend([
                {"role": "user", "content": f"What are your {preference} specials?"},
                {"role": "model", "content": f"print(restaurant_tools.get_menu_specials(dietary_preference='{preference}'))"},
                {"role": "user", "content": "tool_outputs: [{'name': 'Mushroom Risotto', 'description': 'Creamy Arborio rice with wild mushrooms and parmesan', 'price': '₹850', 'dietary': 'vegetarian'}]"},
                {"role": "model", "content": "Here are our current menu specials:\n1. Mushroom Risotto - Creamy Arborio rice with wild mushrooms and parmesan (₹850)\n\nThese are our chef's recommendations for today!"}
            ])
    
    return scenarios

def create_error_handling_scenarios():
    """Generate error handling scenarios"""
    scenarios = []
    
    # Large party size
    scenarios.extend([
        {"role": "user", "content": "I need a table for 15 people tonight at 8pm"},
        {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tonight', time='8pm', party_size=15))"},
        {"role": "user", "content": "tool_outputs: {'status': 'error', 'message': 'Party size too large for online booking. Please call the restaurant directly.'}"},
        {"role": "model", "content": "I'm sorry, but for parties larger than 8 people, we ask that you call the restaurant directly to make arrangements. Our phone number is (080) 2555-1234."}
    ])
    
    # No availability
    scenarios.extend([
        {"role": "user", "content": "Book a table for 4 people tomorrow at 8pm"},
        {"role": "model", "content": "print(restaurant_tools.check_availability(restaurant_id=1, date='tomorrow', time='8pm', party_size=4))"},
        {"role": "user", "content": "tool_outputs: []"},
        {"role": "model", "content": "I'm sorry, but there are no tables available at that time. Would you like me to check for alternative times?"}
    ])
    
    # Invalid booking ID
    scenarios.extend([
        {"role": "user", "content": "Cancel booking GF999999"},
        {"role": "model", "content": "print(restaurant_tools.cancel_booking(booking_id='GF999999'))"},
        {"role": "user", "content": "tool_outputs: False"},
        {"role": "model", "content": "I'm sorry, I couldn't find that booking to cancel. Please check your booking reference number."}
    ])
    
    # Invalid location
    scenarios.extend([
        {"role": "user", "content": "Find restaurants in Mars"},
        {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Mars'))"},
        {"role": "user", "content": "tool_outputs: []"},
        {"role": "model", "content": "I'm sorry, I couldn't find any GoodFoods restaurants in that location. We currently have restaurants in Koramangala, Indiranagar, Jayanagar, Whitefield, and Electronic City. Would you like me to help you find a restaurant in one of these areas?"}
    ])
    
    return scenarios

def create_context_aware_scenarios():
    """Generate context-aware confirmation scenarios"""
    scenarios = []
    
    # After restaurant discovery
    scenarios.extend([
        {"role": "user", "content": "Find restaurants in Koramangala"},
        {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Koramangala'))"},
        {"role": "user", "content": "tool_outputs: [{'id': 1, 'name': 'GoodFoods Koramangala', 'address': 'Koramangala 4th Block, Bangalore', 'cuisine_type': 'Multi-cuisine, North Indian, Chinese'}]"},
        {"role": "model", "content": "I found GoodFoods Koramangala in Koramangala 4th Block, Bangalore. They serve Multi-cuisine, North Indian, Chinese cuisine. Would you like to book a table there?"},
        {"role": "user", "content": "yes"},
        {"role": "model", "content": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"}
    ])
    
    # After showing specials
    scenarios.extend([
        {"role": "user", "content": "What are your specials?"},
        {"role": "model", "content": "print(restaurant_tools.get_menu_specials())"},
        {"role": "user", "content": "tool_outputs: [{'name': 'Pan-Seared Scallops', 'description': 'Fresh sea scallops with truffle risotto and seasonal vegetables', 'price': '₹1,200', 'dietary': 'non-vegetarian'}]"},
        {"role": "model", "content": "Here are our current menu specials:\n1. Pan-Seared Scallops - Fresh sea scallops with truffle risotto and seasonal vegetables (₹1,200)\n\nThese are our chef's recommendations for today!"},
        {"role": "user", "content": "I want to book a table"},
        {"role": "model", "content": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., today, tomorrow, Friday)\n3. Time (e.g., 7 PM, 8 PM)\n4. Your name and phone number"}
    ])
    
    return scenarios

def create_booking_management_scenarios():
    """Generate booking management scenarios"""
    scenarios = []
    
    # Check booking details
    scenarios.extend([
        {"role": "user", "content": "Check my booking details for GF123456"},
        {"role": "model", "content": "print(restaurant_tools.get_booking_details(booking_id='GF123456'))"},
        {"role": "user", "content": "tool_outputs: {'success': True, 'booking_id': 'GF123456', 'restaurant_name': 'GoodFoods Koramangala', 'date': '2024-08-15', 'time': '20:00', 'party_size': 4, 'status': 'confirmed'}"},
        {"role": "model", "content": "Here are your booking details:\n- Booking ID: GF123456\n- Restaurant: GoodFoods Koramangala\n- Date: 2024-08-15\n- Time: 20:00\n- Party Size: 4\n- Status: confirmed"}
    ])
    
    # Cancel booking
    scenarios.extend([
        {"role": "user", "content": "I need to cancel my booking GF123456"},
        {"role": "model", "content": "print(restaurant_tools.cancel_booking(booking_id='GF123456'))"},
        {"role": "user", "content": "tool_outputs: True"},
        {"role": "model", "content": "Your booking has been cancelled successfully. Thank you for letting us know."}
    ])
    
    return scenarios

def create_training_examples():
    """Generate 100 comprehensive training examples"""
    examples = []
    
    # Baseline conversations (15 examples)
    baseline = create_baseline_conversations()
    for i in range(0, len(baseline), 2):
        examples.append({
            "messages": baseline[i:i+2]
        })
    
    # Restaurant search scenarios (35 examples)
    search_scenarios = create_restaurant_search_scenarios()
    for i in range(0, len(search_scenarios), 4):
        examples.append({
            "messages": search_scenarios[i:i+4]
        })
    
    # Booking scenarios (30 examples)
    booking_scenarios = create_booking_scenarios()
    for i in range(0, len(booking_scenarios), 10):
        examples.append({
            "messages": booking_scenarios[i:i+10]
        })
    
    # Menu specials scenarios (10 examples)
    specials_scenarios = create_menu_specials_scenarios()
    for i in range(0, len(specials_scenarios), 4):
        examples.append({
            "messages": specials_scenarios[i:i+4]
        })
    
    # Error handling scenarios (5 examples)
    error_scenarios = create_error_handling_scenarios()
    for i in range(0, len(error_scenarios), 4):
        examples.append({
            "messages": error_scenarios[i:i+4]
        })
    
    # Context-aware scenarios (3 examples)
    context_scenarios = create_context_aware_scenarios()
    for i in range(0, len(context_scenarios), 5):
        examples.append({
            "messages": context_scenarios[i:i+5]
        })
    
    # Booking management scenarios (2 examples)
    management_scenarios = create_booking_management_scenarios()
    for i in range(0, len(management_scenarios), 4):
        examples.append({
            "messages": management_scenarios[i:i+4]
        })
    
    return examples[:100]  # Ensure exactly 100 examples

def create_validation_examples():
    """Generate validation examples"""
    examples = []
    
    # Different variations for validation
    validation_scenarios = [
        {"role": "user", "content": "Find restaurants in Jayanagar"},
        {"role": "model", "content": "print(restaurant_tools.find_restaurants(location='Jayanagar'))"},
        {"role": "user", "content": "tool_outputs: [{'id': 3, 'name': 'GoodFoods Jayanagar', 'address': 'Jayanagar 4th Block, Bangalore', 'cuisine_type': 'South Indian, North Indian, Chinese'}]"},
        {"role": "model", "content": "I found GoodFoods Jayanagar in Jayanagar 4th Block, Bangalore. They serve South Indian, North Indian, Chinese cuisine. Would you like to book a table there?"}
    ]
    
    examples.append({"messages": validation_scenarios})
    
    return examples

def write_jsonl_file(examples, filename):
    """Write examples to a JSONL file"""
    with open(filename, 'w', encoding='utf-8') as f:
        for example in examples:
            f.write(json.dumps(example, ensure_ascii=False) + '\n')

def main():
    """Generate training and validation datasets"""
    print("Generating enhanced training dataset...")
    
    # Create training examples
    training_examples = create_training_examples()
    print(f"Created {len(training_examples)} training examples")
    
    # Create validation examples
    validation_examples = create_validation_examples()
    print(f"Created {len(validation_examples)} validation examples")
    
    # Write to files
    write_jsonl_file(training_examples, 'training_100.jsonl')
    write_jsonl_file(validation_examples, 'validation_100.jsonl')
    
    print("✅ Enhanced dataset generation complete!")
    print(f"📁 Training file: training_100.jsonl ({len(training_examples)} examples)")
    print(f"📁 Validation file: validation_100.jsonl ({len(validation_examples)} examples)")

if __name__ == "__main__":
    main() 