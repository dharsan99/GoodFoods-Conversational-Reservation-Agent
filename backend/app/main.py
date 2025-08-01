from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv

# Import the existing agent logic
from .agent import GoodFoodsAgent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="GoodFoods Reservation Agent API",
    description="AI-powered restaurant reservation system for GoodFoods chain",
    version="1.0.0"
)

# Initialize the agent
try:
    agent = GoodFoodsAgent()
except ValueError as e:
    print(f"Warning: Agent initialization failed: {e}")
    agent = None

# CORS Configuration
# Allow requests from the Streamlit frontend and other origins
origins = [
    "http://localhost:8501",  # Local Streamlit
    "http://localhost:3000",  # Alternative local port
    "https://goodfoods-agent-ui.onrender.com",  # Render frontend
    "https://goodfoods-agent-frontend.onrender.com",  # Alternative Render URL
    "*"  # Allow all origins for development (remove in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models for Request/Response
class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, str]]] = []

class ChatResponse(BaseModel):
    reply: str
    success: bool = True
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    agent_ready: bool
    message: str

# API Endpoints
@app.get("/", response_model=HealthResponse)
async def read_root():
    """Health check endpoint"""
    return HealthResponse(
        status="running",
        agent_ready=agent is not None,
        message="GoodFoods Agent API is running"
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check endpoint"""
    if agent is None:
        return HealthResponse(
            status="error",
            agent_ready=False,
            message="Agent not initialized - check API key configuration"
        )
    
    return HealthResponse(
        status="healthy",
        agent_ready=True,
        message="Agent is ready to handle requests"
    )

@app.post("/chat", response_model=ChatResponse)
async def handle_chat(request: ChatRequest):
    """Handle chat requests from the frontend"""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="Agent not available - please check configuration"
        )
    
    try:
        # Get response from the agent
        response_text = agent.get_response_with_history(request.message, request.history)
        
        return ChatResponse(
            reply=response_text,
            success=True
        )
    
    except Exception as e:
        return ChatResponse(
            reply="I apologize, but I encountered an error processing your request.",
            success=False,
            error=str(e)
        )

@app.post("/chat/simple", response_model=ChatResponse)
async def handle_simple_chat(request: ChatRequest):
    """Simplified chat endpoint that doesn't require history management"""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="Agent not available - please check configuration"
        )
    
    try:
        # Use the original get_response method
        response_text = agent.get_response(request.message)
        
        return ChatResponse(
            reply=response_text,
            success=True
        )
    
    except Exception as e:
        return ChatResponse(
            reply="I apologize, but I encountered an error processing your request.",
            success=False,
            error=str(e)
        )

@app.get("/restaurants")
async def get_restaurants(location: Optional[str] = None, cuisine: Optional[str] = None):
    """Get restaurants by location or cuisine"""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="Agent not available - please check configuration"
        )
    
    try:
        from .tool_functions import find_restaurants
        restaurants = find_restaurants(location=location, cuisine=cuisine)
        return {"restaurants": restaurants}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch restaurants: {str(e)}"
        )

@app.get("/availability/{restaurant_id}")
async def check_availability(
    restaurant_id: int,
    date: str,
    time: str,
    party_size: int
):
    """Check table availability for a specific restaurant"""
    if agent is None:
        raise HTTPException(
            status_code=503,
            detail="Agent not available - please check configuration"
        )
    
    try:
        from .tool_functions import check_availability
        slots = check_availability(restaurant_id, date, time, party_size)
        return {"available_slots": slots}
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check availability: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 