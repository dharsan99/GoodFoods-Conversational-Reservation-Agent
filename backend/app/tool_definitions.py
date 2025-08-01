# Tool definitions for the GoodFoods conversational agent
# These define the JSON schema that the LLM uses to understand available functions

tools = [
    {
        "type": "function",
        "function": {
            "name": "find_restaurants",
            "description": "Search for GoodFoods restaurants by location or cuisine type. Use this when users want to find restaurants in a specific area or serving specific cuisine.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string", 
                        "description": "The location or area to search for (e.g., 'Koramangala', 'Indiranagar', 'Mumbai')"
                    },
                    "cuisine": {
                        "type": "string", 
                        "description": "The type of cuisine to search for (e.g., 'North Indian', 'Italian', 'Chinese')"
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
            "description": "Check for available tables at a specific restaurant for a given date, time, and party size. Use this when users want to know if tables are available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "integer", 
                        "description": "The ID of the restaurant to check availability for"
                    },
                    "date": {
                        "type": "string", 
                        "description": "The desired date in YYYY-MM-DD format (e.g., '2025-01-15')"
                    },
                    "time": {
                        "type": "string", 
                        "description": "The desired time in HH:MM (24-hour) format (e.g., '19:00' for 7 PM)"
                    },
                    "party_size": {
                        "type": "integer", 
                        "description": "The number of guests for the booking"
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
            "description": "Create a new reservation at a GoodFoods restaurant. Use this when users want to confirm a booking after availability has been checked.",
            "parameters": {
                "type": "object",
                "properties": {
                    "restaurant_id": {
                        "type": "integer", 
                        "description": "The ID of the restaurant for the booking"
                    },
                    "user_name": {
                        "type": "string", 
                        "description": "The full name of the person making the booking"
                    },
                    "phone_number": {
                        "type": "string", 
                        "description": "The phone number for the booking (should be in format +91-XXXXXXXXXX)"
                    },
                    "date": {
                        "type": "string", 
                        "description": "The date of the reservation in YYYY-MM-DD format"
                    },
                    "time": {
                        "type": "string", 
                        "description": "The time of the reservation in HH:MM (24-hour) format"
                    },
                    "party_size": {
                        "type": "integer", 
                        "description": "The number of guests for the booking"
                    },
                    "special_requests": {
                        "type": "string", 
                        "description": "Any special requests or dietary requirements (optional)"
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
            "description": "Cancel an existing booking. Use this when users want to cancel their reservation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string", 
                        "description": "The booking reference number to cancel"
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
            "description": "Get details of an existing booking. Use this when users want to check their booking information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_id": {
                        "type": "string", 
                        "description": "The booking reference number to look up"
                    }
                },
                "required": ["booking_id"]
            }
        }
    }
] 