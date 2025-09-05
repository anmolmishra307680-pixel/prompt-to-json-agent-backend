"""
Production configuration management
Environment-based settings for different deployment scenarios
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import validator

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # Database settings
    database_url: str = "postgresql://user:password@localhost:5432/prompt_to_json"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    
    # API settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 2
    api_reload: bool = False
    
    # Security settings
    cors_origins: list = ["*"]
    rate_limit_enabled: bool = True
    rate_limit_requests_per_minute: int = 60
    
    # Monitoring settings
    monitoring_enabled: bool = True
    log_level: str = "INFO"
    metrics_export_interval: int = 300  # 5 minutes
    
    # Feature flags
    multi_objective_rl_enabled: bool = True
    llm_feedback_enabled: bool = True
    batch_processing_enabled: bool = True
    
    # Performance settings
    max_prompt_length: int = 10000
    max_iterations: int = 5
    request_timeout: int = 30
    
    # External services
    openai_api_key: Optional[str] = None
    render_deploy_hook: Optional[str] = None
    
    @validator('database_url')
    def validate_database_url(cls, v):
        if not v or v == "postgresql://user:password@localhost:5432/prompt_to_json":
            # Use environment variable or default for development
            return os.getenv("DATABASE_URL", v)
        return v
    
    @validator('cors_origins', pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

class DevelopmentSettings(Settings):
    """Development environment settings"""
    api_reload: bool = True
    log_level: str = "DEBUG"
    rate_limit_requests_per_minute: int = 1000  # More lenient for development
    
class ProductionSettings(Settings):
    """Production environment settings"""
    api_reload: bool = False
    log_level: str = "INFO"
    cors_origins: list = []  # Restrict in production
    rate_limit_requests_per_minute: int = 60
    
    @validator('cors_origins', pre=True)
    def production_cors_origins(cls, v):
        # In production, get from environment variable
        origins = os.getenv("CORS_ORIGINS", "")
        if origins:
            return [origin.strip() for origin in origins.split(",")]
        return []

class TestingSettings(Settings):
    """Testing environment settings"""
    database_url: str = "sqlite:///./test.db"
    monitoring_enabled: bool = False
    rate_limit_enabled: bool = False

def get_settings() -> Settings:
    """Get settings based on environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProductionSettings()
    elif env == "testing":
        return TestingSettings()
    else:
        return DevelopmentSettings()

# Global settings instance
settings = get_settings()

# Environment validation
def validate_environment():
    """Validate required environment variables"""
    required_vars = []
    missing_vars = []
    
    if settings.__class__ == ProductionSettings:
        required_vars = ["DATABASE_URL"]
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True

# Configuration summary
def get_config_summary():
    """Get configuration summary for debugging"""
    return {
        "environment": os.getenv("ENVIRONMENT", "development"),
        "database_configured": bool(settings.database_url and settings.database_url != "postgresql://user:password@localhost:5432/prompt_to_json"),
        "monitoring_enabled": settings.monitoring_enabled,
        "rate_limiting_enabled": settings.rate_limit_enabled,
        "cors_origins_count": len(settings.cors_origins),
        "api_workers": settings.api_workers,
        "log_level": settings.log_level
    }

if __name__ == "__main__":
    # Test configuration
    print("🔧 Configuration Test")
    print("=" * 30)
    
    try:
        validate_environment()
        print("✅ Environment validation passed")
    except ValueError as e:
        print(f"❌ Environment validation failed: {e}")
    
    config_summary = get_config_summary()
    print("\n📋 Configuration Summary:")
    for key, value in config_summary.items():
        print(f"  {key}: {value}")
    
    print(f"\n🌍 Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"🗄️  Database: {settings.database_url[:50]}...")
    print(f"🚀 API: {settings.api_host}:{settings.api_port}")
    print(f"👥 Workers: {settings.api_workers}")
    print(f"📊 Monitoring: {settings.monitoring_enabled}")
    print(f"🛡️  Rate Limiting: {settings.rate_limit_enabled}")