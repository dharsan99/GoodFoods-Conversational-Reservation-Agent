"""
Tool functions for the GoodFoods AI Agent
Implements the actual Python functions that correspond to the tool definitions
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from .database import DatabaseManager

def find_restaurants(location: str = None, cuisine: str = None) -> List[Dict]:
    """
    Search for restaurants based on location and/or cuisine type.
    
    Args:
        location: Location or area to search for
        cuisine: Type of cuisine to search for
    
    Returns:
        List of matching restaurants
    """
    try:
        with DatabaseManager() as db:
            # Build query based on provided parameters
            query = "SELECT * FROM Restaurant WHERE 1=1"
            params = []
            
            if location:
                query += " AND (address LIKE ? OR name LIKE ?)"
                location_pattern = f"%{location}%"
                params.extend([location_pattern, location_pattern])
            
            if cuisine:
                query += " AND cuisine_type LIKE ?"
                cuisine_pattern = f"%{cuisine}%"
                params.append(cuisine_pattern)
            
            # Execute query
            restaurants = db.execute_query(query, params)
            
            # Format results
            result = []
            for restaurant in restaurants:
                result.append({
                    "id": restaurant[0],
                    "name": restaurant[1],
                    "address": restaurant[2],
                    "cuisine_type": restaurant[5],  # cuisine_type is at index 5
                    "rating": 4.5  # Mock rating for now
                })
            
            return result
            
    except Exception as e:
        print(f"Error in find_restaurants: {e}")
        return []

def check_availability(restaurant_id: int, date: str, time: str, party_size: int) -> List[str]:
    """
    Check for available tables at a specific restaurant.
    
    Args:
        restaurant_id: ID of the restaurant
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        party_size: Number of guests
    
    Returns:
        List of available time slots
    """
    try:
        with DatabaseManager() as db:
            # Check if restaurant exists
            restaurant = db.execute_query(
                "SELECT * FROM Restaurant WHERE restaurant_id = ?", 
                [restaurant_id]
            )
            
            if not restaurant:
                return []
            
            # Get all tables for this restaurant
            tables = db.execute_query(
                "SELECT * FROM RestaurantTable WHERE restaurant_id = ?", 
                [restaurant_id]
            )
            
            # Check existing bookings for the given date and time
            booking_time = f"{date} {time}:00"
            existing_bookings = db.execute_query(
                """
                SELECT SUM(num_guests) FROM Booking 
                WHERE restaurant_id = ? AND booking_time = ? AND status = 'confirmed'
                """,
                [restaurant_id, booking_time]
            )
            
            total_booked = existing_bookings[0][0] if existing_bookings[0][0] else 0
            total_capacity = sum(table[2] for table in tables)  # table[2] is capacity
            
            # Check if we have enough capacity
            if total_capacity - total_booked >= party_size:
                return [time]  # Return the requested time if available
            
            # If exact time not available, suggest alternatives
            alternative_times = []
            base_time = datetime.strptime(time, "%H:%M")
            
            for i in range(-2, 3):  # Check 2 hours before and after
                if i == 0:
                    continue
                check_time = base_time + timedelta(hours=i)
                check_time_str = check_time.strftime("%H:%M")
                
                # Check availability for this alternative time
                alt_booking_time = f"{date} {check_time_str}:00"
                alt_bookings = db.execute_query(
                    """
                    SELECT SUM(num_guests) FROM Booking 
                    WHERE restaurant_id = ? AND booking_time = ? AND status = 'confirmed'
                    """,
                    [restaurant_id, alt_booking_time]
                )
                
                alt_total_booked = alt_bookings[0][0] if alt_bookings[0][0] else 0
                if total_capacity - alt_total_booked >= party_size:
                    alternative_times.append(check_time_str)
            
            return alternative_times
            
    except Exception as e:
        print(f"Error in check_availability: {e}")
        return []

def create_booking(restaurant_id: int, user_name: str, phone_number: str, 
                  date: str, time: str, party_size: int, 
                  special_requests: str = None) -> Dict:
    """
    Create a new reservation.
    
    Args:
        restaurant_id: ID of the restaurant
        user_name: Name of the person making the booking
        phone_number: Contact phone number
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        party_size: Number of guests
        special_requests: Any special requests
    
    Returns:
        Dictionary with booking details
    """
    try:
        with DatabaseManager() as db:
            # Check if restaurant exists
            restaurant = db.execute_query(
                "SELECT * FROM Restaurant WHERE restaurant_id = ?", 
                [restaurant_id]
            )
            
            if not restaurant:
                return {"success": False, "error": "Restaurant not found"}
            
            # Check availability
            available_times = check_availability(restaurant_id, date, time, party_size)
            if not available_times or time not in available_times:
                return {"success": False, "error": "Requested time not available"}
            
            # Create or get user
            user = db.execute_query(
                "SELECT * FROM User WHERE phone_number = ?", 
                [phone_number]
            )
            
            if user:
                user_id = user[0][0]
            else:
                # Create new user
                db.execute_query(
                    "INSERT INTO User (name, phone_number) VALUES (?, ?)",
                    [user_name, phone_number]
                )
                user_id = db.get_last_insert_id()
            
            # Create booking
            booking_time = f"{date} {time}:00"
            db.execute_query(
                """
                INSERT INTO Booking (restaurant_id, user_id, booking_time, num_guests, status, special_requests)
                VALUES (?, ?, ?, ?, 'confirmed', ?)
                """,
                [restaurant_id, user_id, booking_time, party_size, special_requests]
            )
            
            booking_id = db.get_last_insert_id()
            
            return {
                "success": True,
                "booking_id": f"GF{booking_id:06d}",
                "restaurant_name": restaurant[0][1],
                "date": date,
                "time": time,
                "party_size": party_size,
                "user_name": user_name,
                "phone_number": phone_number
            }
            
    except Exception as e:
        print(f"Error in create_booking: {e}")
        return {"success": False, "error": str(e)}

def cancel_booking(booking_id: str) -> bool:
    """
    Cancel an existing booking.
    
    Args:
        booking_id: Booking reference number (format: GF123456)
    
    Returns:
        True if cancellation successful, False otherwise
    """
    try:
        with DatabaseManager() as db:
            # Extract numeric ID from booking reference
            if not booking_id.startswith("GF"):
                return False
            
            numeric_id = int(booking_id[2:])
            
            # Check if booking exists and is confirmed
            booking = db.execute_query(
                "SELECT * FROM Booking WHERE booking_id = ? AND status = 'confirmed'",
                [numeric_id]
            )
            
            if not booking:
                return False
            
            # Cancel the booking
            db.execute_query(
                "UPDATE Booking SET status = 'cancelled' WHERE booking_id = ?",
                [numeric_id]
            )
            
            return True
            
    except Exception as e:
        print(f"Error in cancel_booking: {e}")
        return False

def get_booking_details(booking_id: str, phone_number: str = None) -> Dict:
    """
    Get details of an existing booking.
    
    Args:
        booking_id: Booking reference number (format: GF123456)
        phone_number: Phone number associated with the booking
    
    Returns:
        Dictionary with booking details
    """
    try:
        with DatabaseManager() as db:
            # Extract numeric ID from booking reference
            if not booking_id.startswith("GF"):
                return {"success": False, "error": "Invalid booking ID format"}
            
            numeric_id = int(booking_id[2:])
            
            # Build query
            query = """
                SELECT b.*, r.name as restaurant_name, u.name as user_name, u.phone_number
                FROM Booking b
                JOIN Restaurant r ON b.restaurant_id = r.restaurant_id
                JOIN User u ON b.user_id = u.user_id
                WHERE b.booking_id = ?
            """
            params = [numeric_id]
            
            if phone_number:
                query += " AND u.phone_number = ?"
                params.append(phone_number)
            
            booking = db.execute_query(query, params)
            
            if not booking:
                return {"success": False, "error": "Booking not found"}
            
            booking_data = booking[0]
            
            return {
                "success": True,
                "booking_id": f"GF{booking_data[0]:06d}",
                "restaurant_name": booking_data[8],  # restaurant_name
                "user_name": booking_data[9],        # user_name
                "phone_number": booking_data[10],    # phone_number
                "date": booking_data[3].split()[0],  # booking_time date part
                "time": booking_data[3].split()[1][:5],  # booking_time time part
                "party_size": booking_data[4],
                "status": booking_data[5],
                "special_requests": booking_data[6]
            }
            
    except Exception as e:
        print(f"Error in get_booking_details: {e}")
        return {"success": False, "error": str(e)}

def get_menu_specials(dietary_preference: str = None, restaurant_id: int = None) -> List[Dict]:
    """
    Get menu specials and featured dishes.
    
    Args:
        dietary_preference: Optional dietary filter
        restaurant_id: Optional restaurant ID to filter by
    
    Returns:
        List of menu specials
    """
    try:
        # Mock menu specials data (in a real system, this would come from a database)
        all_specials = [
            {
                "name": "Pan-Seared Scallops",
                "description": "Fresh sea scallops with truffle risotto and seasonal vegetables",
                "price": "₹1,200",
                "dietary": "non-vegetarian",
                "restaurant_id": 1
            },
            {
                "name": "Wagyu Beef Burger",
                "description": "Premium Wagyu beef patty with aged cheddar and caramelized onions",
                "price": "₹950",
                "dietary": "non-vegetarian",
                "restaurant_id": 1
            },
            {
                "name": "Mushroom Risotto",
                "description": "Creamy Arborio rice with wild mushrooms and parmesan",
                "price": "₹850",
                "dietary": "vegetarian",
                "restaurant_id": 2
            },
            {
                "name": "Impossible Burger Deluxe",
                "description": "Plant-based burger with vegan cheese and special sauce",
                "price": "₹750",
                "dietary": "vegan",
                "restaurant_id": 2
            },
            {
                "name": "Truffle Pasta",
                "description": "Homemade fettuccine with black truffle and cream sauce",
                "price": "₹900",
                "dietary": "vegetarian",
                "restaurant_id": 3
            },
            {
                "name": "Gluten-Free Chocolate Cake",
                "description": "Rich chocolate cake made with almond flour",
                "price": "₹350",
                "dietary": "gluten-free",
                "restaurant_id": 4
            }
        ]
        
        # Filter by restaurant if specified
        if restaurant_id:
            all_specials = [s for s in all_specials if s["restaurant_id"] == restaurant_id]
        
        # Filter by dietary preference if specified
        if dietary_preference and dietary_preference != "none":
            all_specials = [s for s in all_specials if s["dietary"] == dietary_preference]
        
        return all_specials
        
    except Exception as e:
        print(f"Error in get_menu_specials: {e}")
        return [] 