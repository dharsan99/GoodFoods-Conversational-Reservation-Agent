"""
Database manager for GoodFoods AI Agent
Handles all database operations using SQLite for local development
"""

import asyncio
import os
from typing import List, Dict, Any, Optional

# Conditional import for Prisma (only for production)
PRISMA_AVAILABLE = False  # Disabled for deployment
# Note: Prisma import removed for deployment - using SQLite only

class DatabaseManager:
    def __init__(self):
        self._connection_string = os.getenv("DATABASE_URL", "sqlite:///./goodfoods.db")
        # Using SQLite for deployment - no Prisma needed
    
    def __enter__(self):
        """Context manager entry"""
        # No connection needed for SQLite
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        # No cleanup needed for SQLite
        pass
    
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

    # Prisma-based methods (commented out for deployment - using SQLite only)
    # These methods are not used in the current deployment
    # They can be uncommented when switching to PostgreSQL with Prisma
    
    # async def get_restaurants(self, location: Optional[str] = None, cuisine: Optional[str] = None) -> List[Dict]:
    #     """Get restaurants with optional filtering"""
    #     pass
    
    # async def create_user_if_not_exists(self, name: str, phone_number: str) -> int:
    #     """Create a user if they don't exist, return user ID"""
    #     pass
    
    # async def create_booking(self, restaurant_id: int, user_id: int, booking_time: str, 
    #                        num_guests: int, special_requests: Optional[str] = None) -> int:
    #     """Create a new booking"""
    #     pass
    
    # async def get_booking(self, booking_id: int) -> Optional[Dict]:
    #     """Get booking details with restaurant and user info"""
    #     pass
    
    # async def cancel_booking(self, booking_id: int) -> bool:
    #     """Cancel a booking"""
    #     pass 