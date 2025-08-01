"""
GoodFoods AI Agent - Core conversational agent with tool calling
Implements the "from scratch" tool calling system using Llama 3.1 8B
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime
from .tool_definitions import tools
from . import tool_functions

class GoodFoodsAgent:
    def __init__(self):
        """Initialize the GoodFoods AI Agent"""
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "speechtotext-466820")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        # Use the trained model instead of base model
        self.model_name = "7439580447044009984"  # Your trained Llama 3.1 8B model
        
        # Initialize conversation state
        self.conversation_history = []
        self.current_booking_context = {}
        
        # Development mode flag
        self.dev_mode = os.getenv("DEV_MODE", "true").lower() == "true"
        
        # Get Google Cloud access token
        self.api_key = self._get_gcloud_token()
        
    def _get_gcloud_token(self) -> str:
        """Get Google Cloud access token using gcloud CLI"""
        try:
            import subprocess
            result = subprocess.run(
                ["gcloud", "auth", "print-access-token"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Warning: Could not get gcloud token: {result.stderr}")
                return ""
        except Exception as e:
            print(f"Warning: Could not get gcloud token: {e}")
            return ""
    
    def build_system_prompt(self) -> str:
        """Build the system prompt for the LLM"""
        return """You are 'Samvaad', a helpful and friendly AI assistant for the GoodFoods restaurant chain.
Your primary goal is to help users find restaurants and book tables.

You have access to a set of tools to perform these actions. When a user asks a question, first decide if you need to call a tool.
If you need to call a tool, respond ONLY with a JSON object containing the tool call.
The JSON should be in the format: {"tool_calls": [{"name": "function_name", "arguments": {"arg1": "value1"}}]}

If you do not need to call a tool, respond with a friendly, conversational message.

CONVERSATION FLOW RULES:
1. When a user asks to find restaurants, use find_restaurants tool
2. After showing restaurant results, if user says "yes", "book", "book table", or similar, DO NOT call any tools - instead ask for booking details
3. Only call check_availability tool when you have specific date, time, and party size from the user
4. For booking, collect: date, time, party size, name, and phone number
5. Use check_availability tool to verify slots before creating booking
6. Use create_booking tool to finalize the reservation

IMPORTANT RULES:
1. Always use the provided tools for restaurant operations - never make up information
2. Be conversational and helpful in your responses
3. Understand context - if user confirms they want to book, proceed to booking flow
4. For booking confirmations, always ask for user name and phone number
5. Use Indian phone number format (+91-XXXXXXXXXX) when asking for phone numbers
6. Be polite and professional in all interactions
7. Remember conversation context - don't repeat the same information

Available tools:
- find_restaurants: Search for restaurants by location or cuisine
- check_availability: Check if tables are available at a specific time
- create_booking: Create a new reservation
- cancel_booking: Cancel an existing booking
- get_booking_details: Get details of an existing booking"""

    def invoke_llm(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Invoke the Llama 3.1 8B model via Google Cloud Vertex AI"""
        try:
            # Google Cloud Vertex AI endpoint (correct format)
            endpoint = f"{self.location}-aiplatform.googleapis.com"
            url = f"https://{endpoint}/v1/projects/{self.project_id}/locations/{self.location}/endpoints/openapi/chat/completions"
            
            # Prepare the request payload (OpenAI-compatible format)
            payload = {
                "model": self.model_name,  # Use the trained model ID
                "messages": [
                    {"role": "system", "content": self.build_system_prompt()}
                ] + messages[-5:],  # Last 5 messages for context
                "tools": tools,
                "tool_choice": "auto",
                "temperature": 0.1,
                "max_tokens": 512,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error invoking LLM: {e}")
            return {"error": f"Failed to get response from AI model: {str(e)}"}

    def invoke_llm_dev_mode(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Development mode LLM invocation with simple rule-based responses"""
        try:
            user_message = messages[-1]['content'].lower() if messages else ""
            
            # Handle name identification
            if any(word in user_message for word in ['your name', 'what are you', 'who are you', 'what\'s your name']):
                return {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "text": "I'm Samvaad, your AI assistant for GoodFoods restaurants. I'm here to help you with restaurant reservations and dining information!"
                            }]
                        }
                    }]
                }
            
            # Handle menu specials
            if any(word in user_message for word in ['menu', 'specials', 'dishes', 'food', 'chef', 'recommendation']):
                return {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "functionCall": {
                                    "name": "get_menu_specials",
                                    "args": json.dumps({})
                                }
                            }]
                        }
                    }]
                }
            
            # Handle availability checking
            if any(word in user_message for word in ['check', 'available', 'availability', 'slot', 'time']) and any(word in user_message for word in ['people', 'person', 'guest']):
                # Extract availability information
                party_size = None
                date = None
                time = None
                
                # Simple extraction
                if '2' in user_message or 'two' in user_message:
                    party_size = 2
                elif '4' in user_message or 'four' in user_message:
                    party_size = 4
                elif '6' in user_message or 'six' in user_message:
                    party_size = 6
                elif '8' in user_message or 'eight' in user_message:
                    party_size = 8
                
                if 'tomorrow' in user_message:
                    from datetime import datetime, timedelta
                    date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                elif 'today' in user_message or 'tonight' in user_message:
                    from datetime import datetime
                    date = datetime.now().strftime('%Y-%m-%d')
                
                if '7' in user_message or 'seven' in user_message:
                    time = '19:00'
                elif '8' in user_message or 'eight' in user_message:
                    time = '20:00'
                elif '9' in user_message or 'nine' in user_message:
                    time = '21:00'
                elif '6' in user_message or 'six' in user_message:
                    time = '18:00'
                
                if party_size and date and time:
                    return {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "functionCall": {
                                        "name": "check_availability",
                                        "args": json.dumps({
                                            "restaurant_id": 1,  # Default to first restaurant
                                            "date": date,
                                            "time": time,
                                            "party_size": party_size
                                        })
                                    }
                                }]
                            }
                        }]
                    }
            
            # Simple intent detection for development
            if any(word in user_message for word in ['find', 'search', 'restaurant', 'location', 'cuisine', 'south', 'north', 'chinese', 'italian', 'nearest']):
                # Extract location and cuisine from user message
                location = None
                cuisine = None
                
                # Location extraction logic
                if 'koramangala' in user_message:
                    location = 'Koramangala'
                elif 'indiranagar' in user_message:
                    location = 'Indiranagar'
                elif 'jayanagar' in user_message:
                    location = 'Jayanagar'
                elif 'whitefield' in user_message:
                    location = 'Whitefield'
                elif 'electronic city' in user_message or 'electronic' in user_message:
                    location = 'Electronic City'
                elif 'hsr' in user_message:
                    location = 'HSR Layout'
                
                # Cuisine extraction logic
                if 'italian' in user_message:
                    cuisine = 'Italian'
                elif 'chinese' in user_message:
                    cuisine = 'Chinese'
                elif 'north indian' in user_message or 'north' in user_message:
                    cuisine = 'North Indian'
                elif 'south indian' in user_message or 'south' in user_message:
                    cuisine = 'South Indian'
                elif 'continental' in user_message:
                    cuisine = 'Continental'
                elif 'multi-cuisine' in user_message or 'multi cuisine' in user_message:
                    cuisine = 'Multi-cuisine'
                
                # Return tool call for find_restaurants
                return {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "functionCall": {
                                    "name": "find_restaurants",
                                    "args": json.dumps({
                                        "location": location,
                                        "cuisine": cuisine
                                    })
                                }
                            }]
                        }
                    }]
                }
            
            elif any(word in user_message for word in ['book', 'reservation', 'table']) or ('yes' in user_message and len(messages) > 1):
                # Check if this is a booking confirmation after showing restaurants
                if len(messages) > 1 and any('restaurant' in msg.get('content', '').lower() for msg in messages[-3:]):
                    return {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "text": "Great! I'd be happy to help you book a table. Could you please provide:\n1. Number of people\n2. Date (e.g., tonight, tomorrow, Friday)\n3. Time (e.g., 7:00 PM, 8:00 PM)\n4. Your name and phone number"
                                }]
                            }
                        }]
                    }
                
                # Extract booking information
                party_size = None
                date = None
                time = None
                customer_name = None
                phone_number = None
                
                # Simple extraction
                if '2' in user_message or 'two' in user_message:
                    party_size = 2
                elif '4' in user_message or 'four' in user_message:
                    party_size = 4
                elif '6' in user_message or 'six' in user_message:
                    party_size = 6
                elif '8' in user_message or 'eight' in user_message:
                    party_size = 8
                
                if 'tomorrow' in user_message:
                    from datetime import datetime, timedelta
                    date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                elif 'friday' in user_message:
                    # Simple date logic for demo
                    date = '2025-08-08'  # Next Friday
                elif 'today' in user_message:
                    from datetime import datetime
                    date = datetime.now().strftime('%Y-%m-%d')
                
                if '7' in user_message or 'seven' in user_message:
                    time = '19:00'
                elif '8' in user_message or 'eight' in user_message:
                    time = '20:00'
                elif '9' in user_message or 'nine' in user_message:
                    time = '21:00'
                elif '6' in user_message or 'six' in user_message:
                    time = '18:00'
                
                # Extract name and phone (simple pattern matching)
                import re
                phone_match = re.search(r'\b\d{10}\b', user_message)
                if phone_match:
                    phone_number = phone_match.group()
                
                # Simple name extraction (look for "my name is" or "i am")
                if 'my name is' in user_message:
                    name_start = user_message.find('my name is') + 11
                    name_end = user_message.find(' ', name_start)
                    if name_end == -1:
                        name_end = len(user_message)
                    customer_name = user_message[name_start:name_end].strip()
                elif 'i am' in user_message:
                    name_start = user_message.find('i am') + 4
                    name_end = user_message.find(' ', name_start)
                    if name_end == -1:
                        name_end = len(user_message)
                    customer_name = user_message[name_start:name_end].strip()
                
                # If we have all required booking details, proceed with booking
                if party_size and date and time and customer_name and phone_number:
                    return {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "functionCall": {
                                        "name": "create_booking",
                                        "args": json.dumps({
                                            "restaurant_id": 1,  # Default to first restaurant
                                            "user_name": customer_name,
                                            "phone_number": phone_number,
                                            "date": date,
                                            "time": time,
                                            "party_size": party_size
                                        })
                                    }
                                }]
                            }
                        }]
                    }
                # If we have partial details, ask for missing information
                elif party_size and date and time:
                    missing_info = []
                    if not customer_name:
                        missing_info.append("your name")
                    if not phone_number:
                        missing_info.append("your phone number")
                    
                    return {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "text": f"Great! I have your booking details for {party_size} people on {date} at {time}. I just need: {', '.join(missing_info)}."
                                }]
                            }
                        }]
                    }
                # If we have some details but not all, ask for the rest
                else:
                    missing_info = []
                    if not party_size:
                        missing_info.append("number of people")
                    if not date:
                        missing_info.append("date")
                    if not time:
                        missing_info.append("time")
                    
                    return {
                        "candidates": [{
                            "content": {
                                "parts": [{
                                    "text": f"Could you please provide: {', '.join(missing_info)}?"
                                }]
                            }
                        }]
                    }
            
            elif 'hi' in user_message or 'hello' in user_message:
                return {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "text": "Hello! I'm Samvaad, your AI assistant for GoodFoods restaurants. I can help you find restaurants, check availability, and make bookings. How can I assist you today?"
                            }]
                        }
                    }]
                }
            
            else:
                return {
                    "candidates": [{
                        "content": {
                            "parts": [{
                                "text": "I'm here to help you with restaurant reservations at GoodFoods. You can ask me to find restaurants, check availability, or make bookings. What would you like to do?"
                            }]
                        }
                    }]
                }
                
        except Exception as e:
            print(f"Error in dev mode LLM: {e}")
            return {"error": f"Development mode error: {str(e)}"}

    def parse_llm_response(self, response: Dict) -> Dict:
        """Parse the LLM response to extract tool calls or text"""
        try:
            if "error" in response:
                return {"type": "error", "data": response["error"]}
            
            # Handle OpenAI-compatible format from Vertex AI
            if "choices" in response and response["choices"]:
                choice = response["choices"][0]
                message = choice.get("message", {})
                
                # Check if it's a tool call
                if "tool_calls" in message and message["tool_calls"]:
                    tool_calls = []
                    for tool_call in message["tool_calls"]:
                        tool_calls.append({
                            "name": tool_call["function"]["name"],
                            "arguments": json.loads(tool_call["function"]["arguments"])
                        })
                    return {"type": "tool_call", "data": tool_calls}
                
                # Check if content contains a JSON tool call (Vertex AI sometimes returns this)
                elif "content" in message and message["content"]:
                    content = message["content"]
                    # Try to parse as JSON tool call
                    try:
                        parsed_content = json.loads(content)
                        if "tool_calls" in parsed_content and parsed_content["tool_calls"]:
                            tool_calls = []
                            for tool_call in parsed_content["tool_calls"]:
                                tool_calls.append({
                                    "name": tool_call["name"],
                                    "arguments": tool_call["arguments"]
                                })
                            return {"type": "tool_call", "data": tool_calls}
                    except json.JSONDecodeError:
                        # Not JSON, treat as regular text
                        pass
                    
                    return {"type": "text", "data": content}
            
            # Fallback to old format for development mode
            if "candidates" in response and response["candidates"]:
                candidate = response["candidates"][0]
                
                if "content" in candidate and candidate["content"]["parts"]:
                    part = candidate["content"]["parts"][0]
                    
                    # Check if it's a tool call
                    if "functionCall" in part:
                        return {
                            "type": "tool_call",
                            "data": [{
                                "name": part["functionCall"]["name"],
                                "arguments": json.loads(part["functionCall"]["args"])
                            }]
                        }
                    
                    # Check if it's text content
                    elif "text" in part:
                        return {"type": "text", "data": part["text"]}
            
            return {"type": "error", "data": "Invalid response format from LLM"}
            
        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            return {"type": "error", "data": f"Failed to parse response: {str(e)}"}

    def execute_tool(self, tool_call: Dict) -> Any:
        """Execute a tool call and return the result"""
        try:
            function_name = tool_call["name"]
            arguments = tool_call["arguments"]
            
            # Map function name to actual function
            if hasattr(tool_functions, function_name):
                function_to_call = getattr(tool_functions, function_name)
                result = function_to_call(**arguments)
                return result
            else:
                return f"Error: Tool '{function_name}' not found."
        
        except Exception as e:
            print(f"Error executing tool {function_name}: {e}")
            return f"Error executing tool {function_name}: {str(e)}"

    def format_tool_result(self, tool_name: str, result: Any) -> str:
        """Format tool execution result into a user-friendly message"""
        try:
            if tool_name == "find_restaurants":
                if not result:
                    return "I couldn't find any restaurants matching your criteria. Could you try a different location or cuisine type?"
                
                restaurants = result
                if len(restaurants) == 1:
                    restaurant = restaurants[0]
                    return f"I found {restaurant['name']} in {restaurant['address']}. They serve {restaurant['cuisine_type']} cuisine. Would you like to book a table there?"
                else:
                    response = f"I found {len(restaurants)} restaurants:"
                    for i, restaurant in enumerate(restaurants[:3], 1):  # Show top 3
                        response += f"\n{i}. {restaurant['name']} - {restaurant['address']} ({restaurant['cuisine_type']})"
                    
                    if len(restaurants) > 3:
                        response += f"\n... and {len(restaurants) - 3} more"
                    
                    response += "\n\nWhich one would you like to book?"
                    return response
            
            elif tool_name == "check_availability":
                if not result:
                    return "I'm sorry, but there are no tables available at that time. Would you like me to check for alternative times?"
                
                # Convert 24-hour format to 12-hour format
                def format_time_12hr(time_24hr):
                    try:
                        from datetime import datetime
                        time_obj = datetime.strptime(time_24hr, "%H:%M")
                        return time_obj.strftime("%I:%M %p")
                    except:
                        return time_24hr
                
                if len(result) == 1:
                    formatted_time = format_time_12hr(result[0])
                    return f"Great! A table is available at {formatted_time}. Would you like me to proceed with the booking?"
                else:
                    response = f"The requested time isn't available, but I found these alternative times:"
                    for time_slot in result[:5]:  # Show top 5 alternatives
                        formatted_time = format_time_12hr(time_slot)
                        response += f"\n- {formatted_time}"
                    response += "\n\nWhich time would you prefer?"
                    return response
            
            elif tool_name == "create_booking":
                if result.get("success"):
                    # Format the date and time for better display
                    from datetime import datetime
                    
                    # Parse the date and time
                    booking_date = result.get('date', '')
                    booking_time = result.get('time', '')
                    
                    # Format date
                    try:
                        date_obj = datetime.strptime(booking_date, "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%B %d, %Y")  # e.g., "August 2, 2025"
                    except:
                        formatted_date = booking_date
                    
                    # Format time to 12-hour format
                    try:
                        time_obj = datetime.strptime(booking_time, "%H:%M")
                        formatted_time = time_obj.strftime("%I:%M %p")  # e.g., "7:00 PM"
                    except:
                        formatted_time = booking_time
                    
                    return f"Excellent! Your booking is confirmed. Your booking reference is {result['booking_id']}. We look forward to seeing you at {result['restaurant_name']} on {formatted_date} at {formatted_time} for {result['party_size']} people."
                else:
                    return f"I'm sorry, I couldn't complete the booking: {result.get('error', 'Unknown error')}"
            
            elif tool_name == "cancel_booking":
                if result:
                    return f"Your booking has been cancelled successfully. Thank you for letting us know."
                else:
                    return "I'm sorry, I couldn't find that booking to cancel. Please check your booking reference number."
            
            elif tool_name == "get_booking_details":
                if result.get("success"):
                    booking = result
                    
                    # Format date and time
                    from datetime import datetime
                    
                    try:
                        date_obj = datetime.strptime(booking['date'], "%Y-%m-%d")
                        formatted_date = date_obj.strftime("%B %d, %Y")
                    except:
                        formatted_date = booking['date']
                    
                    try:
                        time_obj = datetime.strptime(booking['time'], "%H:%M")
                        formatted_time = time_obj.strftime("%I:%M %p")
                    except:
                        formatted_time = booking['time']
                    
                    return f"Here are your booking details:\n- Booking ID: {booking['booking_id']}\n- Restaurant: {booking['restaurant_name']}\n- Date: {formatted_date}\n- Time: {formatted_time}\n- Party Size: {booking['party_size']}\n- Status: {booking['status']}"
                else:
                    return f"I'm sorry, I couldn't find that booking: {result.get('error', 'Unknown error')}"
            
            elif tool_name == "get_menu_specials":
                if not result:
                    return "I'm sorry, but I couldn't find any menu specials at the moment. Please check back later or ask about our regular menu items."
                
                specials = result
                if len(specials) == 1:
                    special = specials[0]
                    return f"Our current special is the {special['name']} - {special['description']} for {special['price']}."
                else:
                    response = f"Here are our current menu specials:"
                    for i, special in enumerate(specials, 1):
                        response += f"\n{i}. {special['name']} - {special['description']} ({special['price']})"
                    
                    response += "\n\nThese are our chef's recommendations for today!"
                    return response
            
            else:
                return f"Tool {tool_name} executed successfully."
                
        except Exception as e:
            print(f"Error formatting tool result: {e}")
            return f"I processed your request, but there was an issue formatting the response. Please try again."

    def get_response(self, user_message: str) -> str:
        """Main method to get a response from the AI agent"""
        try:
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Invoke the LLM (use dev mode if enabled)
            if self.dev_mode:
                llm_response = self.invoke_llm_dev_mode(self.conversation_history, tools)
            else:
                llm_response = self.invoke_llm(self.conversation_history, tools)
            
            # Parse the response
            parsed_response = self.parse_llm_response(llm_response)
            
            if parsed_response["type"] == "tool_call":
                # Execute the tool
                tool_calls = parsed_response["data"]
                tool_results = []
                
                for tool_call in tool_calls:
                    result = self.execute_tool(tool_call)
                    formatted_result = self.format_tool_result(tool_call["name"], result)
                    tool_results.append(formatted_result)
                
                # Combine all tool results
                final_response = "\n\n".join(tool_results)
                
            elif parsed_response["type"] == "text":
                final_response = parsed_response["data"]
                
            else:
                final_response = "I'm sorry, I'm having trouble processing your request right now. Please try again."
            
            # Add assistant response to conversation history
            self.conversation_history.append({"role": "assistant", "content": final_response})
            
            return final_response
        
        except Exception as e:
            print(f"Error in get_response: {e}")
            return "I'm sorry, I'm experiencing technical difficulties. Please try again later."
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        self.current_booking_context = {} 