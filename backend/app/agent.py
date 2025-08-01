import json
import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv
from . import tool_functions
from .tool_definitions import tools
from openai import OpenAI
import google.auth
import google.auth.transport.requests

# Load environment variables
load_dotenv()

class GoodFoodsAgent:
    """
    The core conversational agent for GoodFoods restaurant reservations.
    Implements a from-scratch tool-calling approach without using frameworks like LangChain.
    Uses Google Cloud Vertex AI for Llama 3.1 8B.
    """
    
    def __init__(self):
        # Google Cloud configuration
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
        self.model_id = "meta/llama-3.1-8b-instruct-maas"
        
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is required")
        
        # Initialize OpenAI client for Vertex AI
        self.client = self._initialize_vertex_ai_client()
        
        # Conversation state
        self.conversation_history = []
        self.current_context = {}
    
    def _initialize_vertex_ai_client(self):
        """Initialize the OpenAI client for Google Cloud Vertex AI."""
        try:
            # Get GCP access token
            credentials, _ = google.auth.default()
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            gcp_token = credentials.token
            
            # Initialize OpenAI client pointing to Vertex AI
            return OpenAI(
                api_key=gcp_token,
                base_url=f"https://{self.location}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.location}/endpoints/openapi"
            )
        except Exception as e:
            raise ValueError(f"Failed to initialize Vertex AI client: {e}")
    
    def build_system_prompt(self) -> str:
        """Build the system prompt that instructs the LLM on its role and capabilities."""
        return """You are 'Samvaad', a helpful and friendly AI assistant for the GoodFoods restaurant chain in India. Your primary goal is to help users find restaurants and book tables.

You have access to a set of tools to perform these actions. When a user asks a question, first decide if you need to call a tool. If you need to call a tool, respond ONLY with a JSON object containing the tool call.

The JSON should be in the format: {"tool_calls": [{"name": "function_name", "arguments": {"arg1": "value1"}}]}

If you do not need to call a tool, respond with a friendly, conversational message in natural language.

Important guidelines:
1. Always use the provided tools for restaurant searches, availability checks, and bookings
2. Do not make up information about restaurants or availability
3. Be helpful and conversational in your responses
4. If a user provides incomplete information, ask clarifying questions
5. For dates, use YYYY-MM-DD format
6. For times, use HH:MM (24-hour) format
7. For phone numbers, use +91-XXXXX-XXXXX format
8. Be patient and guide users through the booking process step by step

Remember: You are representing GoodFoods, a premium restaurant chain. Always be professional, helpful, and ensure a great customer experience."""
    
    def build_messages(self, user_input: str) -> List[Dict[str, str]]:
        """Build the messages array for the LLM API call."""
        messages = [
            {"role": "system", "content": self.build_system_prompt()}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history)
        
        # Add current user input
        messages.append({"role": "user", "content": user_input})
        
        return messages
    
    def invoke_llm(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Invoke the Llama 3.1 8B API via Google Cloud Vertex AI."""
        try:
            # Use OpenAI client to call Vertex AI
            response = self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.1,  # Low temperature for deterministic tool calls
                max_tokens=512
            )
            
            # Convert OpenAI response format to our expected format
            return {
                "choices": [{
                    "message": {
                        "content": response.choices[0].message.content,
                        "tool_calls": response.choices[0].message.tool_calls
                    }
                }]
            }
        except Exception as e:
            return {"error": f"Vertex AI API call failed: {str(e)}"}
    
    def parse_llm_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse the LLM response to determine if it's a tool call or text response."""
        try:
            if "error" in response:
                return {"type": "error", "data": response["error"]}
            
            message = response['choices'][0]['message']
            
            if message.get('tool_calls'):
                return {"type": "tool_call", "data": message['tool_calls']}
            elif message.get('content'):
                return {"type": "text", "data": message['content']}
            else:
                return {"type": "error", "data": "Invalid response from LLM"}
        
        except (KeyError, IndexError) as e:
            return {"type": "error", "data": f"Failed to parse LLM response: {str(e)}"}
    
    def execute_tool(self, tool_call: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call by mapping the function name to the actual Python function."""
        try:
            function_name = tool_call['function']['name']
            arguments = json.loads(tool_call['function']['arguments'])
            
            # Map function names to actual functions
            function_mapping = {
                'find_restaurants': tool_functions.find_restaurants,
                'check_availability': tool_functions.check_availability,
                'create_booking': tool_functions.create_booking,
                'cancel_booking': tool_functions.cancel_booking,
                'get_booking_details': tool_functions.get_booking_details
            }
            
            if function_name in function_mapping:
                function_to_call = function_mapping[function_name]
                result = function_to_call(**arguments)
                return {"success": True, "result": result}
            else:
                return {"error": f"Tool '{function_name}' not found"}
        
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON in tool arguments: {str(e)}"}
        except Exception as e:
            return {"error": f"Error executing tool {function_name}: {str(e)}"}
    
    def format_tool_result_for_llm(self, tool_result: Dict[str, Any]) -> str:
        """Format tool execution result for the LLM to understand and respond to."""
        if "error" in tool_result:
            return f"Tool execution failed: {tool_result['error']}"
        
        result = tool_result.get('result', {})
        
        if isinstance(result, list):
            # Handle list results (e.g., restaurant search)
            if not result:
                return "No restaurants found matching your criteria."
            
            formatted_result = "Here are the restaurants I found:\n"
            for i, restaurant in enumerate(result[:5], 1):  # Limit to top 5
                formatted_result += f"{i}. {restaurant['name']} - {restaurant['address']} ({restaurant['cuisine_type']})\n"
            return formatted_result
        
        elif isinstance(result, dict):
            # Handle dictionary results (e.g., booking confirmation)
            if result.get('success'):
                if 'booking_reference' in result:
                    return f"Great! {result['message']}"
                elif 'message' in result:
                    return result['message']
                else:
                    return "Operation completed successfully."
            else:
                return f"Operation failed: {result.get('error', 'Unknown error')}"
        
        else:
            return str(result)
    
    def get_response(self, user_input: str) -> str:
        """
        Main method to get a response from the agent.
        Implements the complete tool-calling loop from scratch.
        """
        try:
            # Build messages for the LLM
            messages = self.build_messages(user_input)
            
            # Invoke the LLM
            llm_response = self.invoke_llm(messages)
            
            # Parse the response
            parsed_response = self.parse_llm_response(llm_response)
            
            if parsed_response["type"] == "error":
                return f"I apologize, but I encountered an error: {parsed_response['data']}"
            
            elif parsed_response["type"] == "tool_call":
                # Execute the tool call
                tool_calls = parsed_response["data"]
                tool_results = []
                
                for tool_call in tool_calls:
                    tool_result = self.execute_tool(tool_call)
                    tool_results.append(tool_result)
                
                # Format the tool results for the LLM
                formatted_results = []
                for tool_result in tool_results:
                    formatted_result = self.format_tool_result_for_llm(tool_result)
                    formatted_results.append(formatted_result)
                
                # Combine all results
                final_response = "\n".join(formatted_results)
                
                # Add to conversation history
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": final_response})
                
                return final_response
            
            elif parsed_response["type"] == "text":
                # Direct text response from LLM
                response_text = parsed_response["data"]
                
                # Add to conversation history
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": response_text})
                
                return response_text
            
            else:
                return "I apologize, but I received an unexpected response format."
        
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def get_response_with_history(self, user_input: str, conversation_history: List[Dict[str, str]]) -> str:
        """
        Get a response from the agent using provided conversation history.
        This method is used by the API to maintain conversation context.
        """
        try:
            # Temporarily set the conversation history
            original_history = self.conversation_history.copy()
            self.conversation_history = conversation_history.copy()
            
            # Get the response
            response = self.get_response(user_input)
            
            # Restore original history
            self.conversation_history = original_history
            
            return response
        
        except Exception as e:
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def clear_conversation(self):
        """Clear the conversation history."""
        self.conversation_history = []
        self.current_context = {}
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get a summary of the current conversation state."""
        return {
            "message_count": len(self.conversation_history),
            "current_context": self.current_context,
            "last_user_message": self.conversation_history[-2]["content"] if len(self.conversation_history) >= 2 else None
        } 