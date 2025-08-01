import os
from typing import Dict, List, Optional
from prisma import Prisma
from datetime import datetime
import json

class DatabaseManager:
    def __init__(self):
        self.db = Prisma()
        self._connect()
    
    def _connect(self):
        """Connect to the database"""
        try:
            self.db.connect()
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise
    
    def disconnect(self):
        """Disconnect from the database"""
        if self.db:
            self.db.disconnect()
    
    def add_restaurant(self, name: str, address: str, latitude: float, longitude: float, 
                      cuisine_type: str, opening_hours: Dict) -> int:
        """Add a new restaurant to the database."""
        try:
            restaurant = self.db.restaurant.create({
                'name': name,
                'address': address,
                'latitude': latitude,
                'longitude': longitude,
                'cuisineType': cuisine_type,
                'openingHours': opening_hours
            })
            return restaurant.id
        except Exception as e:
            print(f"Error adding restaurant: {e}")
            raise
    
    def add_tables_to_restaurant(self, restaurant_id: int, table_capacities: List[int]):
        """Add tables to a restaurant with specified capacities."""
        try:
            for capacity in table_capacities:
                self.db.table.create({
                    'restaurantId': restaurant_id,
                    'capacity': capacity
                })
        except Exception as e:
            print(f"Error adding tables: {e}")
            raise
    
    def add_user(self, name: str, phone_number: str) -> int:
        """Add a new user to the database."""
        try:
            user = self.db.user.create({
                'name': name,
                'phoneNumber': phone_number
            })
            return user.id
        except Exception as e:
            print(f"Error adding user: {e}")
            raise
    
    def create_booking(self, restaurant_id: int, user_id: int, booking_time: str, 
                      num_guests: int, special_requests: Optional[str] = None) -> int:
        """Create a new booking."""
        try:
            # Parse the booking time string to datetime
            if isinstance(booking_time, str):
                booking_datetime = datetime.fromisoformat(booking_time.replace('Z', '+00:00'))
            else:
                booking_datetime = booking_time
            
            booking = self.db.booking.create({
                'restaurantId': restaurant_id,
                'userId': user_id,
                'bookingTime': booking_datetime,
                'numGuests': num_guests,
                'specialRequests': special_requests
            })
            return booking.id
        except Exception as e:
            print(f"Error creating booking: {e}")
            raise
    
    def get_restaurants(self, location: Optional[str] = None, cuisine: Optional[str] = None) -> List[Dict]:
        """Get restaurants filtered by location and/or cuisine."""
        try:
            where_conditions = {}
            
            if location:
                where_conditions['OR'] = [
                    {'address': {'contains': location}},
                    {'name': {'contains': location}}
                ]
            
            if cuisine:
                where_conditions['cuisineType'] = {'contains': cuisine}
            
            restaurants = self.db.restaurant.find_many(
                where=where_conditions if where_conditions else None,
                include={
                    'tables': True
                }
            )
            
            result = []
            for restaurant in restaurants:
                result.append({
                    'restaurant_id': restaurant.id,
                    'name': restaurant.name,
                    'address': restaurant.address,
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude,
                    'cuisine_type': restaurant.cuisineType,
                    'opening_hours': restaurant.openingHours
                })
            
            return result
        except Exception as e:
            print(f"Error getting restaurants: {e}")
            return []
    
    def check_availability(self, restaurant_id: int, date: str, time: str, party_size: int) -> List[str]:
        """Check available time slots for a given restaurant, date, and party size."""
        try:
            # Parse the date and time
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            time_obj = datetime.strptime(time, '%H:%M').time()
            
            # Create datetime for the requested booking time
            requested_datetime = datetime.combine(date_obj.date(), time_obj)
            
            # Get existing bookings for this restaurant on this date
            existing_bookings = self.db.booking.find_many(
                where={
                    'restaurantId': restaurant_id,
                    'bookingTime': {
                        'gte': date_obj,
                        'lt': date_obj.replace(hour=23, minute=59, second=59)
                    },
                    'status': 'confirmed'
                }
            )
            
            # Mock available time slots (in a real system, this would be calculated based on table capacities)
            available_slots = [
                "12:00", "12:30", "13:00", "13:30", "14:00", "14:30",
                "19:00", "19:30", "20:00", "20:30", "21:00", "21:30"
            ]
            
            # Filter out the requested time
            filtered_slots = [slot for slot in available_slots if slot != time]
            
            return filtered_slots[:5]  # Return top 5 available slots
            
        except Exception as e:
            print(f"Error checking availability: {e}")
            return []
    
    def get_booking(self, booking_id: int) -> Optional[Dict]:
        """Get booking details by booking ID."""
        try:
            booking = self.db.booking.find_unique(
                where={'id': booking_id},
                include={
                    'restaurant': True,
                    'user': True
                }
            )
            
            if booking:
                return {
                    'booking_id': booking.id,
                    'restaurant_id': booking.restaurantId,
                    'user_id': booking.userId,
                    'booking_time': booking.bookingTime.isoformat(),
                    'num_guests': booking.numGuests,
                    'status': booking.status,
                    'special_requests': booking.specialRequests,
                    'restaurant_name': booking.restaurant.name,
                    'user_name': booking.user.name,
                    'phone_number': booking.user.phoneNumber
                }
            return None
        except Exception as e:
            print(f"Error getting booking: {e}")
            return None
    
    def cancel_booking(self, booking_id: int) -> bool:
        """Cancel a booking by setting its status to 'cancelled'."""
        try:
            booking = self.db.booking.update(
                where={'id': booking_id},
                data={'status': 'cancelled'}
            )
            return True
        except Exception as e:
            print(f"Error cancelling booking: {e}")
            return False
    
    def get_user_by_phone(self, phone_number: str) -> Optional[Dict]:
        """Get user by phone number."""
        try:
            user = self.db.user.find_unique(
                where={'phoneNumber': phone_number}
            )
            
            if user:
                return {
                    'user_id': user.id,
                    'name': user.name,
                    'phone_number': user.phoneNumber
                }
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def create_user_if_not_exists(self, name: str, phone_number: str) -> int:
        """Create a user if they don't exist, otherwise return existing user ID."""
        try:
            # Try to find existing user
            existing_user = self.get_user_by_phone(phone_number)
            if existing_user:
                return existing_user['user_id']
            
            # Create new user
            return self.add_user(name, phone_number)
        except Exception as e:
            print(f"Error creating user: {e}")
            raise 