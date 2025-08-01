"""
Tool definitions for the GoodFoods AI Agent
Defines the JSON schema for all available tools following OpenAPI specification
"""

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_restaurants",
            "description": "Searches for GoodFoods restaurants based on location or cuisine preferences. Use this when users ask to find restaurants, search by location, or ask about available dining options. This is typically the first step in the reservation process.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string", 
                        "description": "The specific location or area to search for restaurants. Examples: 'Koramangala', 'Indiranagar', 'Jayanagar', 'Whitefield', 'Electronic City', 'near MG Road'. If not provided, will return all available locations."
                    },
                    "cuisine": {
                        "type": "string", 
                        "description": "The type of cuisine to filter restaurants by. Examples: 'Italian', 'Chinese', 'North Indian', 'South Indian', 'Continental', 'Multi-cuisine'. If not provided, will return restaurants of all cuisines."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Checks for table availability for a specified number of guests on a given date and time. Use this before attempting to make a reservation to ensure the requested slot is available. This is the second step in the booking process after finding a restaurant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "integer", 
                        "description": "The unique identifier of the restaurant to check availability for. This should be obtained from the find_restaurants tool results."
                    },
                    "date": {
                        "type": "string", 
                        "description": "The desired date for the reservation. Accepts formats: 'YYYY-MM-DD' (e.g., '2024-08-15'), 'today', 'tomorrow', or specific days like 'Friday', 'Saturday'."
                    },
                    "time": {
                        "type": "string", 
                        "description": "The desired time for the reservation. Accepts formats: 'HH:MM' (24-hour, e.g., '19:00'), 'H:MM AM/PM' (12-hour, e.g., '7:00 PM'), or relative times like '7pm', '8pm'."
                    },
                    "party_size": {
                        "type": "integer", 
                        "description": "The number of people in the dinner party. Must be between 1 and 10 guests."
                    }
                },
                "required": ["restaurant_id", "date", "time", "party_size"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Creates a new dinner reservation for a customer. This action is final and should only be used when all details are confirmed and availability has been verified. This is the final step in the booking process.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "integer", 
                        "description": "The unique identifier of the restaurant where the booking should be made. This should be obtained from the find_restaurants tool results."
                    },
                    "user_name": {
                        "type": "string", 
                        "description": "The full name of the person under whom the reservation should be made. This is required for the booking confirmation."
                    },
                    "phone_number": {
                        "type": "string", 
                        "description": "The contact phone number for the customer to send confirmations and updates. Should be in Indian format: +91-XXXXXXXXXX or 10-digit number."
                    },
                    "date": {
                        "type": "string", 
                        "description": "The calendar date for the reservation. Accepts formats: 'YYYY-MM-DD' (e.g., '2024-08-15'), 'today', 'tomorrow', or specific days like 'Friday'."
                    },
                    "time": {
                        "type": "string", 
                        "description": "The specific time for the reservation. Accepts formats: 'HH:MM' (24-hour, e.g., '19:00'), 'H:MM AM/PM' (12-hour, e.g., '7:00 PM'), or relative times like '7pm', '8pm'."
                    },
                    "party_size": {
                        "type": "integer", 
                        "description": "The total number of guests for the reservation. Must be between 1 and 10 guests."
                    },
                    "special_requests": {
                        "type": "string", 
                        "description": "Any special requests, dietary requirements, or notes for the reservation. Examples: 'Window seat preferred', 'Birthday celebration', 'Vegetarian options needed'."
                    }
                },
                "required": ["restaurant_id", "user_name", "phone_number", "date", "time", "party_size"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_booking",
            "description": "Cancels an existing dinner reservation. Use this when customers want to cancel their booking or need to modify their reservation. The booking will be marked as cancelled and the table will be made available for other customers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string", 
                        "description": "The unique booking reference number to cancel. Format: 'GF' followed by 6 digits (e.g., 'GF123456'). This is provided to customers when their booking is confirmed."
                    }
                },
                "required": ["booking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_booking_details",
            "description": "Retrieves detailed information about an existing dinner reservation. Use this when customers want to check their booking details, confirm their reservation, or need to verify booking information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string", 
                        "description": "The unique booking reference number to look up. Format: 'GF' followed by 6 digits (e.g., 'GF123456'). This is provided to customers when their booking is confirmed."
                    },
                    "phone_number": {
                        "type": "string", 
                        "description": "The phone number associated with the booking for verification purposes. Should be in Indian format: +91-XXXXXXXXXX or 10-digit number."
                    }
                },
                "required": ["booking_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_menu_specials",
            "description": "Retrieves the list of current menu specials and featured dishes. Use this when customers ask about daily specials, chef's recommendations, or want to know what's unique on the menu. Can be filtered by dietary preference.",
            "parameters": {
                "type": "object",
                "properties": {
                    "dietary_preference": {
                        "type": "string", 
                        "description": "An optional dietary filter for the specials. If not provided, returns all specials.",
                        "enum": ["none", "vegetarian", "vegan", "gluten-free", "non-vegetarian"]
                    },
                    "restaurant_id": {
                        "type": "integer", 
                        "description": "The unique identifier of the restaurant to get specials for. If not provided, returns specials for all restaurants."
                    }
                },
                "required": []
            }
        }
    }
]