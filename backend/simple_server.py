#!/usr/bin/env python3
"""
Simple FastAPI server for local development
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Create FastAPI app
app = FastAPI(
    title="GoodFoods API",
    description="Simple development server for GoodFoods",
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

# Request/Response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    message: str

# Health check endpoint
@app.get("/")
async def root():
    return {"message": "GoodFoods API is running!", "status": "healthy"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "GoodFoods Backend"}

# Simple chat endpoint
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Simple chat endpoint for development"""
    return ChatResponse(
        response="Hello! This is a development version of GoodFoods. The full AI agent is available in production.",
        message=request.message
    )

# Restaurant endpoints (mock data)
@app.get("/restaurants")
async def get_restaurants():
    """Get mock restaurants for development"""
    return {
        "restaurants": [
            {
                "id": 1,
                "name": "GoodFoods Koramangala",
                "address": "Koramangala, Bangalore",
                "cuisine_type": "Multi-cuisine",
                "rating": 4.5
            },
            {
                "id": 2,
                "name": "GoodFoods Indiranagar",
                "address": "Indiranagar, Bangalore",
                "cuisine_type": "Multi-cuisine",
                "rating": 4.3
            }
        ]
    }

@app.get("/restaurants/{restaurant_id}")
async def get_restaurant(restaurant_id: int):
    """Get mock restaurant details"""
    if restaurant_id == 1:
        return {
            "id": 1,
            "name": "GoodFoods Koramangala",
            "address": "Koramangala, Bangalore",
            "cuisine_type": "Multi-cuisine",
            "rating": 4.5,
            "opening_hours": {
                "monday": "12:00-23:00",
                "tuesday": "12:00-23:00",
                "wednesday": "12:00-23:00",
                "thursday": "12:00-23:00",
                "friday": "12:00-23:00",
                "saturday": "11:00-23:30",
                "sunday": "11:00-23:30"
            }
        }
    else:
        raise HTTPException(status_code=404, detail="Restaurant not found")

if __name__ == "__main__":
    print("Starting GoodFoods Backend (Development Mode)...")
    print("API Documentation: http://localhost:8000/docs")
    print("Health Check: http://localhost:8000/health")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 