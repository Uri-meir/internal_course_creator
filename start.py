#!/usr/bin/env python3
"""
Startup script for Knowledge Management Service
"""

import os
import sys
from pathlib import Path

def check_environment():
    """Check if environment variables are set"""
    required_vars = [
        "OPENAI_API_KEY",
        "DATABASE_URL"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with the required variables.")
        print("Copy env_template.txt to .env and fill in your values.")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🚀 Starting Knowledge Management Service...")
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Create uploads directory
    upload_dir = Path("uploads")
    upload_dir.mkdir(exist_ok=True)
    print(f"📁 Created uploads directory: {upload_dir.absolute()}")
    
    # Start the service
    print("🌐 Starting FastAPI server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    
    # Import and run the main app
    from main import app
    import uvicorn
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    main()
