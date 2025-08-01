"""
Database manager for GoodFoods AI Agent
Handles all database operations using SQLite for local development
"""

import asyncio
import os
from typing import List, Dict, Any, Optional

# Conditional import for Prisma (only for production)
try:
    from prisma import Prisma
    PRISMA_AVAILABLE = True
except ImportError:
    PRISMA_AVAILABLE = False

class DatabaseManager:
    def __init__(self):
        self._connection_string = os.getenv("DATABASE_URL", "sqlite:///./goodfoods.db")
        # Only initialize Prisma if available
        if PRISMA_AVAILABLE:
            self.prisma = Prisma()
        else:
            self.prisma = None
    
    def __enter__(self):
        """Context manager entry"""
        # For local development, we don't need Prisma connection
        if self.prisma and PRISMA_AVAILABLE:
            # Create a new event loop for this context
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(self.prisma.connect())
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.prisma and PRISMA_AVAILABLE:
            self.loop.run_until_complete(self.prisma.disconnect())
            self.loop.close()
    
    def execute_query(self, query: str, params: List[Any] = None) -> List[tuple]:
        """
        Execute a raw SQL query and return results
        For development, we'll use a simple SQLite approach
        """
        try:
            import sqlite3
            import os
            
            # Create database connection with absolute path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "..", "goodfoods.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Execute query
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Fetch results
            results = cursor.fetchall()
            
            # Commit if it's an INSERT/UPDATE/DELETE
            if query.strip().upper().startswith(('INSERT', 'UPDATE', 'DELETE')):
                conn.commit()
            
            conn.close()
            return results
            
        except Exception as e:
            print(f"Database query error: {e}")
            return []
    
    def get_last_insert_id(self) -> int:
        """Get the last inserted row ID"""
        try:
            import sqlite3
            import os
            
            # Create database connection with absolute path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(current_dir, "..", "goodfoods.db")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT last_insert_rowid()")
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            print(f"Error getting last insert ID: {e}")
            return 0

    # Prisma-based methods (for future use)
    async def get_restaurants(self, location: Optional[str] = None, cuisine: Optional[str] = None) -> List[Dict]:
        """Get restaurants with optional filtering"""
        try:
            where_conditions = {}
            
            if location:
                where_conditions["OR"] = [
                    {"address": {"contains": location}},
                    {"name": {"contains": location}}
                ]
            
            if cuisine:
                where_conditions["cuisine_type"] = {"contains": cuisine}
            
            restaurants = await self.prisma.restaurant.find_many(where=where_conditions)
            return [restaurant.dict() for restaurant in restaurants]
            
        except Exception as e:
            print(f"Error getting restaurants: {e}")
            return []

    async def create_user_if_not_exists(self, name: str, phone_number: str) -> int:
        """Create a user if they don't exist, return user ID"""
        try:
            # Check if user exists
            existing_user = await self.prisma.user.find_unique(where={"phone_number": phone_number})
            
            if existing_user:
                return existing_user.id
            
            # Create new user
            new_user = await self.prisma.user.create(data={
                "name": name,
                "phone_number": phone_number
            })
            
            return new_user.id
            
        except Exception as e:
            print(f"Error creating user: {e}")
            return 0

    async def create_booking(self, restaurant_id: int, user_id: int, booking_time: str, 
                           num_guests: int, special_requests: Optional[str] = None) -> int:
        """Create a new booking"""
        try:
            booking = await self.prisma.booking.create(data={
                "restaurant_id": restaurant_id,
                "user_id": user_id,
                "booking_time": booking_time,
                "num_guests": num_guests,
                "status": "confirmed",
                "special_requests": special_requests
            })
            
            return booking.id
            
        except Exception as e:
            print(f"Error creating booking: {e}")
            return 0

    async def get_booking(self, booking_id: int) -> Optional[Dict]:
        """Get booking details with restaurant and user info"""
        try:
            booking = await self.prisma.booking.find_unique(
                where={"booking_id": booking_id},
                include={
                    "restaurant": True,
                    "user": True
                }
            )
            
            if booking:
                return {
                    "booking_id": booking.booking_id,
                    "restaurant_name": booking.restaurant.name,
                    "user_name": booking.user.name,
                    "phone_number": booking.user.phone_number,
                    "booking_time": booking.booking_time,
                    "num_guests": booking.num_guests,
                    "status": booking.status,
                    "special_requests": booking.special_requests
                }
            
            return None
            
        except Exception as e:
            print(f"Error getting booking: {e}")
            return None

    async def cancel_booking(self, booking_id: int) -> bool:
        """Cancel a booking"""
        try:
            await self.prisma.booking.update(
                where={"booking_id": booking_id},
                data={"status": "cancelled"}
            )
            return True
            
        except Exception as e:
            print(f"Error cancelling booking: {e}")
            return False 