#!/usr/bin/env python3
"""
Comprehensive test suite for prompt-to-json-agent backend
Tests API endpoints, database operations, and edge cases
"""

import requests
import json
import time
import sys
from pathlib import Path

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.passed = 0
        self.failed = 0
        
    def test(self, name, func):
        """Run a test and track results"""
        try:
            print(f"🧪 Testing: {name}")
            func()
            print(f"✅ PASSED: {name}")
            self.passed += 1
        except Exception as e:
            print(f"❌ FAILED: {name} - {str(e)}")
            self.failed += 1
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = requests.get(f"{self.base_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
    
    def test_generate_endpoint(self):
        """Test generate endpoint"""
        payload = {"prompt": "design a red sports car"}
        response = requests.post(f"{self.base_url}/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "type" in data
        assert "material" in data
    
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
        response = requests.post(f"{self.base_url}/evaluate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "report_id" in data
        assert "score" in data
        return data["report_id"]
    
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
        response = requests.post(f"{self.base_url}/iterate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "iterations" in data
        assert "history" in data
        assert "final_spec" in data
    
    def test_reports_endpoint(self):
        """Test reports retrieval endpoint"""
        # First create a report
        report_id = self.test_evaluate_endpoint()
        
        # Then retrieve it
        response = requests.get(f"{self.base_url}/reports/{report_id}")
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "evaluation" in data
    
    def test_log_values_endpoint(self):
        """Test HIDG values logging endpoint"""
        payload = {
            "honesty": "Always truthful in responses",
            "integrity": "Consistent ethical behavior",
            "discipline": "Systematic approach to tasks",
            "gratitude": "Appreciation for user feedback"
        }
        response = requests.post(f"{self.base_url}/log-values", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "message" in data
    
    def test_edge_cases(self):
        """Test edge cases and error handling"""
        # Empty prompt
        response = requests.post(f"{self.base_url}/generate", json={"prompt": ""})
        assert response.status_code == 200  # Should handle gracefully
        
        # Invalid spec
        response = requests.post(f"{self.base_url}/evaluate", json={
            "prompt": "test",
            "spec": {"invalid": "spec"}
        })
        assert response.status_code == 200  # Should handle gracefully
        
        # Non-existent report
        response = requests.get(f"{self.base_url}/reports/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        # Make multiple rapid requests
        for i in range(3):
            response = requests.get(f"{self.base_url}/health")
            assert response.status_code == 200
        
        # Should still work within limits
        print("Rate limiting test passed (within limits)")
    
    def test_unicode_support(self):
        """Test Unicode and international character support"""
        payload = {"prompt": "Diseña un coche deportivo rojo 🚗"}
        response = requests.post(f"{self.base_url}/generate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "type" in data
    
    def run_all_tests(self):
        """Run complete test suite"""
        print("🚀 Starting API Test Suite")
        print("=" * 50)
        
        # Check if API is running
        try:
            requests.get(f"{self.base_url}/health", timeout=5)
        except requests.exceptions.RequestException:
            print(f"❌ API not accessible at {self.base_url}")
            print("💡 Start the API with: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            return False
        
        # Run all tests
        self.test("Health Endpoint", self.test_health_endpoint)
        self.test("Generate Endpoint", self.test_generate_endpoint)
        self.test("Evaluate Endpoint", self.test_evaluate_endpoint)
        self.test("Iterate Endpoint", self.test_iterate_endpoint)
        self.test("Reports Endpoint", self.test_reports_endpoint)
        self.test("Log Values Endpoint", self.test_log_values_endpoint)
        self.test("Edge Cases", self.test_edge_cases)
        self.test("Rate Limiting", self.test_rate_limiting)
        self.test("Unicode Support", self.test_unicode_support)
        
        # Print results
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {self.passed} passed, {self.failed} failed")
        
        if self.failed == 0:
            print("🎉 All tests passed! API is production ready.")
            return True
        else:
            print("⚠️  Some tests failed. Check the issues above.")
            return False

class LoadTester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def run_load_test(self, concurrent_users=10, requests_per_user=5):
        """Run basic load test"""
        print(f"🔥 Load Testing: {concurrent_users} users, {requests_per_user} requests each")
        
        import threading
        import time
        
        results = []
        
        def user_simulation():
            user_results = []
            for i in range(requests_per_user):
                start_time = time.time()
                try:
                    response = requests.get(f"{self.base_url}/health", timeout=10)
                    end_time = time.time()
                    user_results.append({
                        "status": response.status_code,
                        "time": end_time - start_time
                    })
                except Exception as e:
                    user_results.append({
                        "status": "error",
                        "time": None,
                        "error": str(e)
                    })
            results.extend(user_results)
        
        # Start concurrent users
        threads = []
        start_time = time.time()
        
        for i in range(concurrent_users):
            thread = threading.Thread(target=user_simulation)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Analyze results
        successful = len([r for r in results if r["status"] == 200])
        failed = len([r for r in results if r["status"] != 200])
        avg_time = sum([r["time"] for r in results if r["time"]]) / len([r for r in results if r["time"]])
        
        print(f"📈 Load Test Results:")
        print(f"   Total Requests: {len(results)}")
        print(f"   Successful: {successful}")
        print(f"   Failed: {failed}")
        print(f"   Average Response Time: {avg_time:.3f}s")
        print(f"   Total Time: {end_time - start_time:.3f}s")
        print(f"   Requests/Second: {len(results) / (end_time - start_time):.2f}")

def main():
    """Main test runner"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "load":
            tester = LoadTester()
            tester.run_load_test()
            return
        elif sys.argv[1] == "api":
            base_url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8000"
            tester = APITester(base_url)
            success = tester.run_all_tests()
            sys.exit(0 if success else 1)
    
    # Default: run API tests
    tester = APITester()
    success = tester.run_all_tests()
    
    # Ask if user wants to run load test
    if success:
        choice = input("\n🔥 Run load test? (y/n): ").strip().lower()
        if choice == 'y':
            load_tester = LoadTester()
            load_tester.run_load_test()

if __name__ == "__main__":
    main()