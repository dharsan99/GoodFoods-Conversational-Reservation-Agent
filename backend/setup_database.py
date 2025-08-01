#!/usr/bin/env python3
"""
Database setup script for GoodFoods AI Agent
Creates SQLite database with schema and sample data for development
"""

import sqlite3
import json
from datetime import datetime, timedelta

def create_database():
    """Create the SQLite database with schema"""
    conn = sqlite3.connect('./goodfoods.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurant (
            restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            cuisine_type TEXT NOT NULL,
            opening_hours TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS RestaurantTable (
            table_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            capacity INTEGER NOT NULL,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone_number TEXT NOT NULL UNIQUE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Booking (
            booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            booking_time DATETIME NOT NULL,
            num_guests INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'confirmed',
            special_requests TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurant (restaurant_id),
            FOREIGN KEY (user_id) REFERENCES User (user_id)
        )
    ''')
    
    conn.commit()
    return conn, cursor

def insert_sample_data(conn, cursor):
    """Insert sample restaurants and tables"""
    
    # Sample restaurants
    restaurants = [
        {
            "name": "GoodFoods Koramangala",
            "address": "Koramangala 4th Block, Bangalore",
            "latitude": 12.9352,
            "longitude": 77.6245,
            "cuisine_type": "Multi-cuisine, North Indian, Chinese",
            "opening_hours": json.dumps({
                "monday": "12:00-23:00",
                "tuesday": "12:00-23:00", 
                "wednesday": "12:00-23:00",
                "thursday": "12:00-23:00",
                "friday": "12:00-23:00",
                "saturday": "11:00-23:30",
                "sunday": "11:00-23:30"
            })
        },
        {
            "name": "GoodFoods Indiranagar",
            "address": "Indiranagar 100 Feet Road, Bangalore",
            "latitude": 12.9789,
            "longitude": 77.6417,
            "cuisine_type": "Multi-cuisine, Italian, Continental",
            "opening_hours": json.dumps({
                "monday": "11:30-22:30",
                "tuesday": "11:30-22:30",
                "wednesday": "11:30-22:30", 
                "thursday": "11:30-22:30",
                "friday": "11:30-22:30",
                "saturday": "11:30-22:30",
                "sunday": "11:30-22:30"
            })
        },
        {
            "name": "GoodFoods Jayanagar",
            "address": "Jayanagar 4th Block, Bangalore",
            "latitude": 12.9279,
            "longitude": 77.5871,
            "cuisine_type": "South Indian, North Indian, Chinese",
            "opening_hours": json.dumps({
                "monday": "11:00-22:00",
                "tuesday": "11:00-22:00",
                "wednesday": "11:00-22:00",
                "thursday": "11:00-22:00", 
                "friday": "11:00-22:00",
                "saturday": "10:30-23:00",
                "sunday": "10:30-23:00"
            })
        },
        {
            "name": "GoodFoods Whitefield",
            "address": "Whitefield Main Road, Bangalore",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "cuisine_type": "Multi-cuisine, Continental, Italian",
            "opening_hours": json.dumps({
                "monday": "12:00-22:00",
                "tuesday": "12:00-22:00",
                "wednesday": "12:00-22:00",
                "thursday": "12:00-22:00",
                "friday": "12:00-23:00",
                "saturday": "12:00-23:00",
                "sunday": "12:00-23:00"
            })
        },
        {
            "name": "GoodFoods Electronic City",
            "address": "Electronic City Phase 1, Bangalore",
            "latitude": 12.8458,
            "longitude": 77.6658,
            "cuisine_type": "Multi-cuisine, Chinese, North Indian",
            "opening_hours": json.dumps({
                "monday": "12:00-23:00",
                "tuesday": "12:00-23:00",
                "wednesday": "12:00-23:00",
                "thursday": "12:00-23:00",
                "friday": "12:00-23:00",
                "saturday": "12:00-23:00",
                "sunday": "12:00-23:00"
            })
        }
    ]
    
    # Insert restaurants
    for restaurant in restaurants:
        cursor.execute('''
            INSERT INTO Restaurant (name, address, latitude, longitude, cuisine_type, opening_hours)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            restaurant["name"],
            restaurant["address"], 
            restaurant["latitude"],
            restaurant["longitude"],
            restaurant["cuisine_type"],
            restaurant["opening_hours"]
        ))
    
    # Insert tables for each restaurant
    table_capacities = [2, 2, 4, 4, 6, 8, 10]  # Various table sizes
    
    for restaurant_id in range(1, len(restaurants) + 1):
        for capacity in table_capacities:
            cursor.execute('''
                INSERT INTO RestaurantTable (restaurant_id, capacity)
                VALUES (?, ?)
            ''', (restaurant_id, capacity))
    
    # Insert sample users
    users = [
        ("Rahul Sharma", "+91-98765-43210"),
        ("Priya Patel", "+91-87654-32109"),
        ("Amit Kumar", "+91-76543-21098"),
        ("Neha Singh", "+91-65432-10987"),
        ("Vikram Malhotra", "+91-54321-09876")
    ]
    
    for user in users:
        cursor.execute('''
            INSERT INTO User (name, phone_number)
            VALUES (?, ?)
        ''', user)
    
    # Insert sample bookings
    today = datetime.now()
    sample_bookings = [
        (1, 1, today + timedelta(days=1), 4, "confirmed", "Window seat preferred"),
        (2, 2, today + timedelta(days=2), 2, "confirmed", None),
        (3, 3, today + timedelta(days=3), 6, "confirmed", "Birthday celebration"),
        (1, 4, today + timedelta(days=1), 2, "confirmed", None),
        (4, 5, today + timedelta(days=4), 8, "confirmed", "Business dinner")
    ]
    
    for booking in sample_bookings:
        cursor.execute('''
            INSERT INTO Booking (restaurant_id, user_id, booking_time, num_guests, status, special_requests)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', booking)
    
    conn.commit()

def main():
    """Main function to set up the database"""
    print("Setting up GoodFoods database...")
    
    try:
        # Create database and tables
        conn, cursor = create_database()
        print("✓ Database schema created")
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM Restaurant")
        restaurant_count = cursor.fetchone()[0]
        
        if restaurant_count == 0:
            # Insert sample data
            insert_sample_data(conn, cursor)
            print("✓ Sample data inserted")
        else:
            print("✓ Database already contains data")
        
        # Verify setup
        cursor.execute("SELECT COUNT(*) FROM Restaurant")
        restaurant_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM RestaurantTable")
        table_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM User")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM Booking")
        booking_count = cursor.fetchone()[0]
        
        print(f"\nDatabase setup complete!")
        print(f"Restaurants: {restaurant_count}")
        print(f"Tables: {table_count}")
        print(f"Users: {user_count}")
        print(f"Bookings: {booking_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error setting up database: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 