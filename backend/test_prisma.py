#!/usr/bin/env python3
"""
Test script to verify Prisma setup and database connectivity
"""

import sys
import os
import json

# Add the app directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from database import DatabaseManager

def test_database_connection():
    """Test database connection and basic operations"""
    print("🧪 Testing Prisma database connection...")
    
    try:
        # Initialize database with context manager
        with DatabaseManager() as db:
            print("✅ Database connection successful!")
            
            # Test restaurant retrieval (should work even if empty)
            print("🔍 Testing restaurant retrieval...")
            restaurants = db.get_restaurants()
            print(f"✅ Found {len(restaurants)} restaurants")
            
            # Test user retrieval (should work even if empty)
            print("🔍 Testing user retrieval...")
            user = db.get_user_by_phone("+91-12345-67890")
            if user:
                print(f"✅ User found: {user['name']}")
            else:
                print("✅ No user found (expected for test)")
            
            print("🧹 Test completed successfully!")
        
        print("✅ Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    sys.exit(0 if success else 1) 