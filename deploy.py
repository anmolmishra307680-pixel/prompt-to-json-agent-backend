#!/usr/bin/env python3
"""
Production deployment script for prompt-to-json-agent backend
Supports Render, Heroku, and Docker deployments
"""

import os
import subprocess
import sys
import json
from pathlib import Path

def run_command(cmd, check=True):
    """Run shell command with error handling"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    return result

def deploy_render():
    """Deploy to Render.com"""
    print("🚀 Deploying to Render...")
    
    # Check if render.yaml exists
    if not Path("render.yaml").exists():
        create_render_config()
    
    print("✅ Render deployment configured")
    print("📝 Next steps:")
    print("1. Push code to GitHub")
    print("2. Connect GitHub repo to Render")
    print("3. Deploy using render.yaml configuration")

def create_render_config():
    """Create render.yaml configuration"""
    config = {
        "services": [
            {
                "type": "web",
                "name": "prompt-to-json-agent",
                "env": "python",
                "buildCommand": "pip install -r requirements.txt",
                "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
                "envVars": [
                    {"key": "DATABASE_URL", "sync": False},
                    {"key": "PYTHON_VERSION", "value": "3.11.0"}
                ]
            },
            {
                "type": "pserv",
                "name": "postgres-db",
                "env": "postgresql",
                "plan": "starter"
            }
        ]
    }
    
    with open("render.yaml", "w") as f:
        import yaml
        yaml.dump(config, f, default_flow_style=False)

def deploy_heroku():
    """Deploy to Heroku"""
    print("🚀 Deploying to Heroku...")
    
    # Check Heroku CLI
    result = run_command("heroku --version", check=False)
    if result.returncode != 0:
        print("❌ Heroku CLI not installed. Install from: https://devcenter.heroku.com/articles/heroku-cli")
        return
    
    # Create Procfile
    with open("Procfile", "w") as f:
        f.write("web: uvicorn app.main:app --host 0.0.0.0 --port $PORT\n")
    
    # Create runtime.txt
    with open("runtime.txt", "w") as f:
        f.write("python-3.11.0\n")
    
    app_name = input("Enter Heroku app name (or press Enter for auto-generated): ").strip()
    
    if app_name:
        run_command(f"heroku create {app_name}")
    else:
        run_command("heroku create")
    
    # Add PostgreSQL addon
    run_command("heroku addons:create heroku-postgresql:mini")
    
    # Deploy
    run_command("git add .")
    run_command("git commit -m 'Deploy to Heroku'")
    run_command("git push heroku main")
    
    print("✅ Deployed to Heroku!")
    run_command("heroku open")

def deploy_docker():
    """Deploy using Docker"""
    print("🐳 Building Docker containers...")
    
    # Build and run production containers
    run_command("docker-compose -f docker-compose.prod.yml build")
    run_command("docker-compose -f docker-compose.prod.yml up -d")
    
    print("✅ Docker deployment complete!")
    print("🌐 API available at: http://localhost:8080")
    print("🔍 Health check: http://localhost:8080/health")

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    # Check if Docker files exist
    if not Path("Dockerfile").exists():
        print("❌ Dockerfile not found")
        return False
    
    print("✅ All requirements met")
    return True

def main():
    """Main deployment function"""
    print("🚀 Prompt to JSON Agent - Production Deployment")
    print("=" * 50)
    
    if not check_requirements():
        sys.exit(1)
    
    print("\nSelect deployment option:")
    print("1. Render.com (Recommended)")
    print("2. Heroku")
    print("3. Docker (Local/VPS)")
    print("4. Exit")
    
    choice = input("\nEnter choice (1-4): ").strip()
    
    if choice == "1":
        deploy_render()
    elif choice == "2":
        deploy_heroku()
    elif choice == "3":
        deploy_docker()
    elif choice == "4":
        print("👋 Goodbye!")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()