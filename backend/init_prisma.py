#!/usr/bin/env python3
"""
Prisma initialization script for GoodFoods backend
This script sets up Prisma and generates the client
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Initializing Prisma for GoodFoods backend...")
    
    # Change to the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Generate Prisma client
    if not run_command("prisma generate", "Generating Prisma client"):
        return False
    
    # Push the schema to the database (for development)
    if not run_command("prisma db push", "Pushing schema to database"):
        return False
    
    print("🎉 Prisma initialization completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 