"""
Unit tests for API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db import get_db, Base
import json

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

class TestAPIEndpoints:
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "prompt-to-json-agent"
    
    def test_generate_endpoint(self):
        """Test generate endpoint"""
        payload = {"prompt": "design a red sports car"}
        response = client.post("/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "type" in data
        assert "material" in data
        assert "dimensions" in data
        assert "color" in data
        assert "purpose" in data
    
    def test_generate_empty_prompt(self):
        """Test generate with empty prompt"""
        payload = {"prompt": ""}
        response = client.post("/generate", json=payload)
        assert response.status_code == 200  # Should handle gracefully
    
    def test_evaluate_endpoint(self):
        """Test evaluate endpoint"""
        payload = {
            "prompt": "test car",
            "spec": {
                "type": "car",
                "material": ["steel", "aluminum"],
                "dimensions": "4.5x1.8x1.4m",
                "color": "red",
                "purpose": "transportation",
                "extras": None
            }
        }
        response = client.post("/evaluate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert "score" in data
        assert isinstance(data["score"], int)
        assert 0 <= data["score"] <= 10
    
    def test_iterate_endpoint(self):
        """Test iterate endpoint"""
        payload = {
            "spec": {
                "type": "car",
                "material": ["unknown"],
                "dimensions": None,
                "color": None,
                "purpose": None,
                "extras": None
            },
            "max_iters": 2
        }
        response = client.post("/iterate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "iterations" in data
        assert "history" in data
        assert "final_spec" in data
        assert isinstance(data["iterations"], int)
        assert data["iterations"] >= 0
    
    def test_log_values_endpoint(self):
        """Test HIDG values logging endpoint"""
        payload = {
            "honesty": "Always truthful",
            "integrity": "Consistent behavior",
            "discipline": "Systematic approach",
            "gratitude": "Appreciation for feedback"
        }
        response = client.post("/log-values", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "message" in data
    
    def test_reports_endpoint_not_found(self):
        """Test reports endpoint with non-existent ID"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = client.get(f"/reports/{fake_id}")
        assert response.status_code == 404
    
    def test_iterate_missing_spec(self):
        """Test iterate endpoint with missing spec"""
        payload = {"max_iters": 2}
        response = client.post("/iterate", json=payload)
        assert response.status_code == 400
    
    def test_invalid_json(self):
        """Test endpoints with invalid JSON"""
        response = client.post("/generate", data="invalid json")
        assert response.status_code == 422  # Unprocessable Entity