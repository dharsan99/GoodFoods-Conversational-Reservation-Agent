#!/usr/bin/env python3
"""
Add HSR Layout restaurant to the existing database
"""

import sqlite3
import json

def add_hsr_restaurant():
    """Add HSR Layout restaurant to the database"""
    
    conn = sqlite3.connect('./goodfoods.db')
    cursor = conn.cursor()
    
    # HSR Layout restaurant data
    hsr_restaurant = {
        "name": "GoodFoods HSR Layout",
        "address": "HSR Layout 7th Sector, Bangalore",
        "latitude": 12.9141,
        "longitude": 77.6417,
        "cuisine_type": "Multi-cuisine, South Indian, North Indian, Chinese",
        "opening_hours": json.dumps({
            "monday": "11:00-23:00",
            "tuesday": "11:00-23:00",
            "wednesday": "11:00-23:00",
            "thursday": "11:00-23:00",
            "friday": "11:00-23:00",
            "saturday": "10:30-23:30",
            "sunday": "10:30-23:30"
        })
    }
    
    # Check if HSR restaurant already exists
    cursor.execute('''
        SELECT restaurant_id FROM Restaurant WHERE name = ?
    ''', (hsr_restaurant["name"],))
    
    existing = cursor.fetchone()
    if existing:
        print(f"✅ HSR Layout restaurant already exists (ID: {existing[0]})")
        return
    
    # Insert HSR restaurant
    cursor.execute('''
        INSERT INTO Restaurant (name, address, latitude, longitude, cuisine_type, opening_hours)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        hsr_restaurant["name"],
        hsr_restaurant["address"], 
        hsr_restaurant["latitude"],
        hsr_restaurant["longitude"],
        hsr_restaurant["cuisine_type"],
        hsr_restaurant["opening_hours"]
    ))
    
    restaurant_id = cursor.lastrowid
    
    # Add tables for HSR restaurant
    table_capacities = [2, 2, 4, 4, 6, 8, 10]  # Various table sizes
    
    for capacity in table_capacities:
        cursor.execute('''
            INSERT INTO RestaurantTable (restaurant_id, capacity)
            VALUES (?, ?)
        ''', (restaurant_id, capacity))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Added GoodFoods HSR Layout (ID: {restaurant_id})")
    print(f"📍 Address: {hsr_restaurant['address']}")
    print(f"🍽️  Cuisine: {hsr_restaurant['cuisine_type']}")
    print(f"🪑 Added {len(table_capacities)} tables with various capacities")

if __name__ == "__main__":
    add_hsr_restaurant() 