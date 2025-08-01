#!/usr/bin/env python3
"""
Seed script for GoodFoods database
Populates the database with sample restaurants, tables, and users
"""

import random
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database import DatabaseManager
from faker import Faker

def seed_database():
    """Seed the database with initial data"""
    print("🌱 Seeding GoodFoods database...")
    
    # Initialize Faker with Indian locale
    fake = Faker(['en_IN'])
    
    # Initialize database with context manager
    with DatabaseManager() as db:
        try:
            # Indian cities and areas for restaurant locations
            cities = [
                "Bangalore", "Mumbai", "Delhi", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"
            ]
            
            areas = {
                "Bangalore": ["Koramangala", "Indiranagar", "Jayanagar", "Whitefield", "Marathahalli", "Electronic City"],
                "Mumbai": ["Bandra", "Andheri", "Juhu", "Worli", "Colaba", "Powai"],
                "Delhi": ["Connaught Place", "Hauz Khas", "Dwarka", "Gurgaon", "Noida", "Greater Noida"],
                "Chennai": ["T Nagar", "Anna Nagar", "Adyar", "OMR", "Porur", "Velachery"],
                "Hyderabad": ["Banjara Hills", "Jubilee Hills", "Gachibowli", "Hitech City", "Secunderabad"],
                "Pune": ["Koregaon Park", "Viman Nagar", "Kharadi", "Hinjewadi", "Wakad"],
                "Kolkata": ["Park Street", "Salt Lake", "New Town", "Howrah", "Dum Dum"],
                "Ahmedabad": ["Satellite", "Vastrapur", "Navrangpura", "Paldi", "Bodakdev"]
            }
            
            # Cuisine types for Indian restaurants
            cuisines = [
                "North Indian", "South Indian", "Chinese", "Italian", "Continental", 
                "Mexican", "Thai", "Japanese", "Mediterranean", "Fusion", "Street Food",
                "Biryani", "Kebabs", "Seafood", "Vegetarian", "Multi-cuisine"
            ]
            
            # Opening hours templates (simplified JSON structure)
            opening_hours_templates = [
                {"monday": "12:00-23:00", "tuesday": "12:00-23:00", "wednesday": "12:00-23:00", "thursday": "12:00-23:00", "friday": "12:00-23:00", "saturday": "11:00-23:30", "sunday": "11:00-23:30"},
                {"monday": "11:30-22:30", "tuesday": "11:30-22:30", "wednesday": "11:30-22:30", "thursday": "11:30-22:30", "friday": "11:30-22:30", "saturday": "11:30-22:30", "sunday": "11:30-22:30"},
                {"monday": "11:00-22:00", "tuesday": "11:00-22:00", "wednesday": "11:00-22:00", "thursday": "11:00-22:00", "friday": "11:00-22:00", "saturday": "10:30-23:00", "sunday": "10:30-23:00"},
                {"monday": "12:00-22:00", "tuesday": "12:00-22:00", "wednesday": "12:00-22:00", "thursday": "12:00-22:00", "friday": "12:00-23:00", "saturday": "12:00-23:00", "sunday": "12:00-23:00"},
                {"monday": "12:00-23:00", "tuesday": "12:00-23:00", "wednesday": "12:00-23:00", "thursday": "12:00-23:00", "friday": "12:00-23:00", "saturday": "12:00-23:00", "sunday": "12:00-23:00"}
            ]
            
            print("🏪 Creating restaurants...")
            
            # Generate 50-100 restaurants
            num_restaurants = random.randint(50, 100)
            
            for i in range(num_restaurants):
                # Select random city and area
                city = random.choice(cities)
                area = random.choice(areas[city])
                
                # Generate restaurant name
                restaurant_name = f"GoodFoods {area}"
                
                # Generate address
                street_address = fake.street_address()
                address = f"{street_address}, {area}, {city}"
                
                # Generate coordinates (simplified - in real app would use geocoding)
                latitude = 12.9716 + random.uniform(-0.1, 0.1)  # Bangalore center + variation
                longitude = 77.5946 + random.uniform(-0.1, 0.1)
                
                # Select cuisine
                cuisine = random.choice(cuisines)
                
                # Select opening hours
                opening_hours = random.choice(opening_hours_templates)
                
                # Add restaurant to database
                restaurant_id = db.add_restaurant(
                    name=restaurant_name,
                    address=address,
                    latitude=latitude,
                    longitude=longitude,
                    cuisine_type=cuisine,
                    opening_hours=opening_hours
                )
                
                # Add tables to restaurant
                # Generate random number of tables with varying capacities
                num_tables = random.randint(8, 25)
                table_capacities = []
                
                for _ in range(num_tables):
                    # 60% 2-4 seaters, 30% 6-8 seaters, 10% large tables
                    capacity_choice = random.random()
                    if capacity_choice < 0.6:
                        capacity = random.choice([2, 3, 4])
                    elif capacity_choice < 0.9:
                        capacity = random.choice([6, 8])
                    else:
                        capacity = random.choice([10, 12, 15])
                    table_capacities.append(capacity)
                
                db.add_tables_to_restaurant(restaurant_id, table_capacities)
                
                if (i + 1) % 10 == 0:
                    print(f"   Created {i + 1} restaurants...")
            
            print(f"✅ Successfully created {num_restaurants} restaurants with tables!")
            
            # Generate some sample users
            print("👥 Creating sample users...")
            sample_users = [
                ("Rahul Sharma", "+91-98765-43210"),
                ("Priya Patel", "+91-87654-32109"),
                ("Amit Kumar", "+91-76543-21098"),
                ("Sneha Reddy", "+91-65432-10987"),
                ("Vikram Singh", "+91-54321-09876"),
                ("Anjali Desai", "+91-43210-98765"),
                ("Rajesh Khanna", "+91-32109-87654"),
                ("Meera Iyer", "+91-21098-76543"),
                ("Suresh Menon", "+91-10987-65432"),
                ("Kavita Gupta", "+91-09876-54321")
            ]
            
            for name, phone in sample_users:
                try:
                    db.add_user(name, phone)
                except Exception as e:
                    # Skip if user already exists (due to unique constraint)
                    print(f"   User {name} already exists, skipping...")
            
            print("✅ Sample users created!")
            print("🎉 Database seeding completed successfully!")
            
        except Exception as e:
            print(f"❌ Error seeding database: {e}")
            raise

if __name__ == "__main__":
    seed_database() 