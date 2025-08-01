import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database import DatabaseManager

# Initialize database connection
db = DatabaseManager()

def find_restaurants(location: Optional[str] = None, cuisine: Optional[str] = None) -> List[Dict]:
    """
    Search for restaurants by location and/or cuisine.
    
    Args:
        location: Optional location/area to search for
        cuisine: Optional cuisine type to filter by
    
    Returns:
        List of restaurant dictionaries matching the criteria
    """
    try:
        restaurants = db.get_restaurants(location=location, cuisine=cuisine)
        
        if not restaurants:
            return []
        
        # Format the response for better readability
        formatted_restaurants = []
        for restaurant in restaurants:
            formatted_restaurants.append({
                'restaurant_id': restaurant['restaurant_id'],
                'name': restaurant['name'],
                'address': restaurant['address'],
                'cuisine_type': restaurant['cuisine_type'],
                'opening_hours': restaurant['opening_hours']
            })
        
        return formatted_restaurants
    
    except Exception as e:
        return {"error": f"Failed to find restaurants: {str(e)}"}

def check_availability(restaurant_id: int, date: str, time: str, party_size: int) -> List[str]:
    """
    Check available time slots for a given restaurant, date, and party size.
    
    Args:
        restaurant_id: ID of the restaurant
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        party_size: Number of guests
    
    Returns:
        List of available time slots
    """
    try:
        # Validate inputs
        if party_size <= 0:
            return {"error": "Party size must be greater than 0"}
        
        # Check if the restaurant exists
        restaurants = db.get_restaurants()
        restaurant_exists = any(r['restaurant_id'] == restaurant_id for r in restaurants)
        
        if not restaurant_exists:
            return {"error": f"Restaurant with ID {restaurant_id} not found"}
        
        # Get available slots
        available_slots = db.check_availability(restaurant_id, date, time, party_size)
        
        return available_slots
    
    except Exception as e:
        return {"error": f"Failed to check availability: {str(e)}"}

def create_booking(restaurant_id: int, user_name: str, phone_number: str, 
                  date: str, time: str, party_size: int, 
                  special_requests: Optional[str] = None) -> Dict:
    """
    Create a new booking at a GoodFoods restaurant.
    
    Args:
        restaurant_id: ID of the restaurant
        user_name: Full name of the person making the booking
        phone_number: Phone number in +91-XXXXXXXXXX format
        date: Date in YYYY-MM-DD format
        time: Time in HH:MM format
        party_size: Number of guests
        special_requests: Optional special requests or dietary requirements
    
    Returns:
        Dictionary with booking confirmation details
    """
    try:
        # Validate inputs
        if not user_name or not phone_number:
            return {"error": "User name and phone number are required"}
        
        if party_size <= 0:
            return {"error": "Party size must be greater than 0"}
        
        # Validate phone number format (Indian format)
        phone_pattern = r'^\+91-\d{5}-\d{5}$'
        if not re.match(phone_pattern, phone_number):
            return {"error": "Phone number must be in format +91-XXXXX-XXXXX"}
        
        # Validate date format
        try:
            booking_date = datetime.strptime(date, '%Y-%m-%d')
            if booking_date.date() < datetime.now().date():
                return {"error": "Cannot book for past dates"}
        except ValueError:
            return {"error": "Date must be in YYYY-MM-DD format"}
        
        # Validate time format
        try:
            datetime.strptime(time, '%H:%M')
        except ValueError:
            return {"error": "Time must be in HH:MM format"}
        
        # Check if user exists, if not create them
        user_id = db.create_user_if_not_exists(user_name, phone_number)
        
        # Create the booking
        booking_time = f"{date} {time}:00"
        booking_id = db.create_booking(
            restaurant_id=restaurant_id,
            user_id=user_id,
            booking_time=booking_time,
            num_guests=party_size,
            special_requests=special_requests
        )
        
        # Generate booking reference
        booking_reference = f"GFS{booking_id:05d}"
        
        return {
            "success": True,
            "booking_id": booking_id,
            "booking_reference": booking_reference,
            "restaurant_id": restaurant_id,
            "user_name": user_name,
            "phone_number": phone_number,
            "date": date,
            "time": time,
            "party_size": party_size,
            "special_requests": special_requests,
            "message": f"Booking confirmed! Your reference number is {booking_reference}"
        }
    
    except Exception as e:
        return {"error": f"Failed to create booking: {str(e)}"}

def cancel_booking(booking_id: str) -> Dict:
    """
    Cancel an existing booking.
    
    Args:
        booking_id: Booking reference number (e.g., "GFS12345")
    
    Returns:
        Dictionary with cancellation status
    """
    try:
        # Extract numeric ID from booking reference
        if booking_id.startswith("GFS"):
            numeric_id = booking_id[3:]
        else:
            numeric_id = booking_id
        
        try:
            numeric_id = int(numeric_id)
        except ValueError:
            return {"error": "Invalid booking reference format"}
        
        # Get booking details first
        booking = db.get_booking(numeric_id)
        if not booking:
            return {"error": "Booking not found"}
        
        if booking['status'] == 'cancelled':
            return {"error": "Booking is already cancelled"}
        
        # Cancel the booking
        success = db.cancel_booking(numeric_id)
        
        if success:
            return {
                "success": True,
                "booking_id": booking_id,
                "message": f"Booking {booking_id} has been cancelled successfully"
            }
        else:
            return {"error": "Failed to cancel booking"}
    
    except Exception as e:
        return {"error": f"Failed to cancel booking: {str(e)}"}

def get_booking_details(booking_id: str) -> Dict:
    """
    Get details of an existing booking.
    
    Args:
        booking_id: Booking reference number (e.g., "GFS12345")
    
    Returns:
        Dictionary with booking details
    """
    try:
        # Extract numeric ID from booking reference
        if booking_id.startswith("GFS"):
            numeric_id = booking_id[3:]
        else:
            numeric_id = booking_id
        
        try:
            numeric_id = int(numeric_id)
        except ValueError:
            return {"error": "Invalid booking reference format"}
        
        # Get booking details
        booking = db.get_booking(numeric_id)
        
        if not booking:
            return {"error": "Booking not found"}
        
        return {
            "booking_id": f"GFS{booking['booking_id']:05d}",
            "restaurant_name": booking['restaurant_name'],
            "user_name": booking['user_name'],
            "phone_number": booking['phone_number'],
            "booking_time": booking['booking_time'],
            "num_guests": booking['num_guests'],
            "status": booking['status'],
            "special_requests": booking['special_requests']
        }
    
    except Exception as e:
        return {"error": f"Failed to get booking details: {str(e)}"} 