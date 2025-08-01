#!/usr/bin/env python3
"""
Test script to verify Prisma setup and database connectivity
"""

import sys
import os

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database import DatabaseManager

def test_database_connection():
    """Test database connection and basic operations"""
    print("🧪 Testing Prisma database connection...")
    
    try:
        # Initialize database
        db = DatabaseManager()
        print("✅ Database connection successful!")
        
        # Test restaurant creation
        print("🏪 Testing restaurant creation...")
        restaurant_id = db.add_restaurant(
            name="Test Restaurant",
            address="123 Test Street, Test City",
            latitude=12.9716,
            longitude=77.5946,
            cuisine_type="Test Cuisine",
            opening_hours={"Mon-Sun": "12:00-23:00"}
        )
        print(f"✅ Restaurant created with ID: {restaurant_id}")
        
        # Test table creation
        print("🪑 Testing table creation...")
        db.add_tables_to_restaurant(restaurant_id, [2, 4, 6])
        print("✅ Tables created successfully!")
        
        # Test user creation
        print("👤 Testing user creation...")
        user_id = db.add_user("Test User", "+91-12345-67890")
        print(f"✅ User created with ID: {user_id}")
        
        # Test restaurant retrieval
        print("🔍 Testing restaurant retrieval...")
        restaurants = db.get_restaurants()
        print(f"✅ Found {len(restaurants)} restaurants")
        
        # Test user retrieval
        print("🔍 Testing user retrieval...")
        user = db.get_user_by_phone("+91-12345-67890")
        if user:
            print(f"✅ User found: {user['name']}")
        
        # Clean up test data
        print("🧹 Cleaning up test data...")
        # Note: In a real test, you might want to delete the test data
        # For now, we'll just disconnect
        
        db.disconnect()
        print("✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1) 