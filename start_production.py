#!/usr/bin/env python3
"""
Production startup script
Handles environment validation, database setup, and server startup
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from config import get_settings, validate_environment, get_config_summary

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import psycopg2
        import slowapi
        import pydantic
        print("✅ All dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Run: pip install -r requirements.txt")
        return False

def setup_database():
    """Initialize database tables"""
    try:
        from app.db import engine
        from app.models import Base
        
        print("🗄️  Setting up database...")
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created")
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def check_environment():
    """Validate environment configuration"""
    try:
        validate_environment()
        config = get_config_summary()
        
        print("🔧 Configuration Summary:")
        for key, value in config.items():
            print(f"   {key}: {value}")
        
        return True
    except Exception as e:
        print(f"❌ Environment validation failed: {e}")
        return False

def start_server():
    """Start the production server"""
    settings = get_settings()
    
    cmd = [
        "uvicorn",
        "app.main:app",
        "--host", settings.api_host,
        "--port", str(settings.api_port),
        "--workers", str(settings.api_workers),
        "--log-level", settings.log_level.lower()
    ]
    
    if settings.api_reload:
        cmd.append("--reload")
    
    print(f"🚀 Starting server: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Server failed to start: {e}")
        sys.exit(1)

def health_check():
    """Perform startup health check"""
    import requests
    import time
    
    settings = get_settings()
    url = f"http://{settings.api_host}:{settings.api_port}/health"
    
    print("🔍 Performing health check...")
    
    for attempt in range(5):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ Health check passed")
                return True
        except requests.exceptions.RequestException:
            pass
        
        print(f"⏳ Health check attempt {attempt + 1}/5...")
        time.sleep(2)
    
    print("❌ Health check failed")
    return False

def main():
    """Main startup sequence"""
    print("🚀 Prompt to JSON Agent - Production Startup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Validate environment
    if not check_environment():
        sys.exit(1)
    
    # Setup database
    if not setup_database():
        sys.exit(1)
    
    # Start server
    print("\n🌟 Starting production server...")
    start_server()

if __name__ == "__main__":
    main()