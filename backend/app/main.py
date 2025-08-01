"""
Main FastAPI application for GoodFoods AI Agent
Provides the API endpoints for the conversational agent
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from .agent import GoodFoodsAgent

# Create FastAPI app
app = FastAPI(
    title="GoodFoods AI Agent API",
    description="Conversational AI agent for restaurant reservations",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the AI agent
agent = GoodFoodsAgent()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    response: str
    message: str
    conversation_history: List[Dict[str, str]]

class RestaurantResponse(BaseModel):
    id: int
    name: str
    address: str
    cuisine_type: str
    rating: float

class BookingRequest(BaseModel):
    restaurant_id: int
    user_name: str
    phone_number: str
    date: str
    time: str
    party_size: int
    special_requests: Optional[str] = None

class BookingResponse(BaseModel):
    success: bool
    booking_id: Optional[str] = None
    restaurant_name: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    party_size: Optional[int] = None
    user_name: Optional[str] = None
    phone_number: Optional[str] = None
    error: Optional[str] = None

# Health check endpoints
@app.get("/")
async def root():
    """Root endpoint with basic info"""
    return {
        "message": "GoodFoods AI Agent API is running!",
        "status": "healthy",
        "version": "1.0.0",
        "agent": "Samvaad - AI Reservation Assistant"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "GoodFoods AI Agent",
        "model": "Llama 3.1 8B",
        "features": ["restaurant_search", "availability_check", "booking_management"]
    }

# Main chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main conversational endpoint for the AI agent.
    Handles natural language queries and tool calling.
    """
    try:
        # Set conversation history if provided
        if request.conversation_history:
            agent.conversation_history = request.conversation_history
        
        # Get response from AI agent
        response = agent.get_response(request.message)
        
        return ChatResponse(
            response=response,
            message=request.message,
            conversation_history=agent.conversation_history
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

# Restaurant endpoints
@app.get("/restaurants", response_model=List[RestaurantResponse])
async def get_restaurants(location: Optional[str] = None, cuisine: Optional[str] = None):
    """
    Get restaurants with optional filtering by location and cuisine.
    This endpoint can be used directly or through the AI agent.
    """
    try:
        from . import tool_functions
        restaurants = tool_functions.find_restaurants(location=location, cuisine=cuisine)
        
        # Convert to response model format
        response_restaurants = []
        for restaurant in restaurants:
            response_restaurants.append(RestaurantResponse(
                id=restaurant["id"],
                name=restaurant["name"],
                address=restaurant["address"],
                cuisine_type=restaurant["cuisine_type"],
                rating=restaurant.get("rating", 4.5)
            ))
        
        return response_restaurants
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching restaurants: {str(e)}")

@app.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: int):
    """Get details of a specific restaurant"""
    try:
        from . import tool_functions
        
        # Get all restaurants and find the specific one
        restaurants = tool_functions.find_restaurants()
        restaurant = next((r for r in restaurants if r["id"] == restaurant_id), None)
        
        if not restaurant:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        
        return restaurant
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching restaurant: {str(e)}")

# Availability endpoint
@app.get("/availability/{restaurant_id}")
async def check_availability(restaurant_id: int, date: str, time: str, party_size: int):
    """
    Check table availability for a specific restaurant, date, time, and party size.
    This endpoint can be used directly or through the AI agent.
    """
    try:
        from . import tool_functions
        available_times = tool_functions.check_availability(
            restaurant_id=restaurant_id,
            date=date,
            time=time,
            party_size=party_size
        )
        
        return {
            "restaurant_id": restaurant_id,
            "date": date,
            "requested_time": time,
            "party_size": party_size,
            "available_times": available_times,
            "is_requested_time_available": time in available_times
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking availability: {str(e)}")

# Booking endpoints
@app.post("/bookings", response_model=BookingResponse)
async def create_booking(request: BookingRequest):
    """
    Create a new booking.
    This endpoint can be used directly or through the AI agent.
    """
    try:
        from . import tool_functions
        result = tool_functions.create_booking(
            restaurant_id=request.restaurant_id,
            user_name=request.user_name,
            phone_number=request.phone_number,
            date=request.date,
            time=request.time,
            party_size=request.party_size,
            special_requests=request.special_requests
        )
        
        return BookingResponse(**result)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating booking: {str(e)}")

@app.delete("/bookings/{booking_id}")
async def cancel_booking(booking_id: str):
    """Cancel an existing booking"""
    try:
        from . import tool_functions
        success = tool_functions.cancel_booking(booking_id=booking_id)
        
        if success:
            return {"success": True, "message": f"Booking {booking_id} cancelled successfully"}
        else:
            raise HTTPException(status_code=404, detail="Booking not found or already cancelled")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling booking: {str(e)}")

@app.get("/bookings/{booking_id}")
async def get_booking_details(booking_id: str, phone_number: Optional[str] = None):
    """Get details of an existing booking"""
    try:
        from . import tool_functions
        result = tool_functions.get_booking_details(
            booking_id=booking_id,
            phone_number=phone_number
        )
        
        if result.get("success"):
            return result
        else:
            raise HTTPException(status_code=404, detail=result.get("error", "Booking not found"))
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching booking: {str(e)}")

# Agent management endpoints
@app.post("/agent/reset")
async def reset_agent():
    """Reset the AI agent's conversation history"""
    try:
        agent.reset_conversation()
        return {"message": "Agent conversation history reset successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting agent: {str(e)}")

@app.get("/agent/status")
async def get_agent_status():
    """Get the current status of the AI agent"""
    try:
        return {
            "status": "active",
            "model": "Llama 3.1 8B",
            "conversation_length": len(agent.conversation_history),
            "available_tools": [tool["function"]["name"] for tool in agent.tools],
            "project_id": agent.project_id,
            "location": agent.location
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting agent status: {str(e)}")

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Resource not found", "detail": str(exc)}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "detail": str(exc)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 