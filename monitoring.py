"""
Production monitoring and logging system
Tracks API performance, errors, and usage metrics
"""

import logging
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any
from functools import wraps
import psutil
import os

class ProductionMonitor:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup loggers
        self.setup_loggers()
        
        # Metrics storage
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "response_times": [],
            "error_counts": {},
            "endpoint_usage": {}
        }
    
    def setup_loggers(self):
        """Setup structured logging"""
        # API access logger
        self.api_logger = logging.getLogger("api_access")
        api_handler = logging.FileHandler(self.log_dir / "api_access.log")
        api_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        api_handler.setFormatter(api_formatter)
        self.api_logger.addHandler(api_handler)
        self.api_logger.setLevel(logging.INFO)
        
        # Error logger
        self.error_logger = logging.getLogger("api_errors")
        error_handler = logging.FileHandler(self.log_dir / "errors.log")
        error_formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(pathname)s:%(lineno)d - %(message)s'
        )
        error_handler.setFormatter(error_formatter)
        self.error_logger.addHandler(error_handler)
        self.error_logger.setLevel(logging.ERROR)
        
        # Performance logger
        self.perf_logger = logging.getLogger("performance")
        perf_handler = logging.FileHandler(self.log_dir / "performance.log")
        perf_formatter = logging.Formatter(
            '%(asctime)s - %(message)s'
        )
        perf_handler.setFormatter(perf_formatter)
        self.perf_logger.addHandler(perf_handler)
        self.perf_logger.setLevel(logging.INFO)
    
    def log_request(self, endpoint: str, method: str, status_code: int, 
                   response_time: float, user_ip: str = None):
        """Log API request details"""
        self.metrics["requests_total"] += 1
        
        if 200 <= status_code < 400:
            self.metrics["requests_success"] += 1
        else:
            self.metrics["requests_error"] += 1
            self.metrics["error_counts"][status_code] = self.metrics["error_counts"].get(status_code, 0) + 1
        
        self.metrics["response_times"].append(response_time)
        self.metrics["endpoint_usage"][endpoint] = self.metrics["endpoint_usage"].get(endpoint, 0) + 1
        
        # Log to file
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "response_time_ms": round(response_time * 1000, 2),
            "user_ip": user_ip
        }
        
        self.api_logger.info(json.dumps(log_data))
    
    def log_error(self, error: Exception, context: Dict[str, Any] = None):
        """Log error with context"""
        error_data = {
            "timestamp": datetime.now().isoformat(),
            "error_type": type(error).__name__,
            "error_message": str(error),
            "context": context or {}
        }
        
        self.error_logger.error(json.dumps(error_data))
    
    def log_performance_metrics(self):
        """Log system performance metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "cpu_percent": cpu_percent,
            "memory_percent": memory.percent,
            "memory_available_gb": round(memory.available / (1024**3), 2),
            "disk_percent": disk.percent,
            "disk_free_gb": round(disk.free / (1024**3), 2)
        }
        
        self.perf_logger.info(json.dumps(metrics))
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get current metrics summary"""
        avg_response_time = 0
        if self.metrics["response_times"]:
            avg_response_time = sum(self.metrics["response_times"]) / len(self.metrics["response_times"])
        
        return {
            "total_requests": self.metrics["requests_total"],
            "success_requests": self.metrics["requests_success"],
            "error_requests": self.metrics["requests_error"],
            "success_rate": (self.metrics["requests_success"] / max(1, self.metrics["requests_total"])) * 100,
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "error_breakdown": self.metrics["error_counts"],
            "endpoint_usage": self.metrics["endpoint_usage"]
        }
    
    def export_metrics(self, filename: str = None):
        """Export metrics to JSON file"""
        if not filename:
            filename = f"metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        filepath = self.log_dir / filename
        with open(filepath, 'w') as f:
            json.dump(self.get_metrics_summary(), f, indent=2)
        
        return str(filepath)

# Global monitor instance
monitor = ProductionMonitor()

def track_endpoint(endpoint_name: str):
    """Decorator to track endpoint performance"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            status_code = 200
            error = None
            
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                error = e
                status_code = 500
                monitor.log_error(e, {"endpoint": endpoint_name, "args": str(args)})
                raise
            finally:
                response_time = time.time() - start_time
                monitor.log_request(endpoint_name, "POST", status_code, response_time)
        
        return wrapper
    return decorator

class HealthChecker:
    """System health monitoring"""
    
    @staticmethod
    def check_database_connection():
        """Check database connectivity"""
        try:
            from app.db import engine
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            return {"status": "healthy", "message": "Database connection OK"}
        except Exception as e:
            return {"status": "unhealthy", "message": f"Database error: {str(e)}"}
    
    @staticmethod
    def check_disk_space():
        """Check available disk space"""
        try:
            disk = psutil.disk_usage('/')
            free_gb = disk.free / (1024**3)
            
            if free_gb < 1:  # Less than 1GB free
                return {"status": "warning", "message": f"Low disk space: {free_gb:.2f}GB free"}
            else:
                return {"status": "healthy", "message": f"Disk space OK: {free_gb:.2f}GB free"}
        except Exception as e:
            return {"status": "error", "message": f"Disk check error: {str(e)}"}
    
    @staticmethod
    def check_memory_usage():
        """Check memory usage"""
        try:
            memory = psutil.virtual_memory()
            
            if memory.percent > 90:
                return {"status": "warning", "message": f"High memory usage: {memory.percent}%"}
            else:
                return {"status": "healthy", "message": f"Memory usage OK: {memory.percent}%"}
        except Exception as e:
            return {"status": "error", "message": f"Memory check error: {str(e)}"}
    
    @classmethod
    def get_health_status(cls):
        """Get comprehensive health status"""
        checks = {
            "database": cls.check_database_connection(),
            "disk_space": cls.check_disk_space(),
            "memory": cls.check_memory_usage()
        }
        
        overall_status = "healthy"
        if any(check["status"] == "unhealthy" for check in checks.values()):
            overall_status = "unhealthy"
        elif any(check["status"] == "warning" for check in checks.values()):
            overall_status = "warning"
        
        return {
            "overall_status": overall_status,
            "timestamp": datetime.now().isoformat(),
            "checks": checks,
            "metrics": monitor.get_metrics_summary()
        }

def setup_monitoring():
    """Initialize monitoring system"""
    # Start performance logging
    import threading
    import time
    
    def performance_monitor():
        while True:
            monitor.log_performance_metrics()
            time.sleep(60)  # Log every minute
    
    # Start background performance monitoring
    perf_thread = threading.Thread(target=performance_monitor, daemon=True)
    perf_thread.start()
    
    print("Monitoring system initialized")

if __name__ == "__main__":
    # Test monitoring system
    print("🔍 Testing monitoring system...")
    
    # Test logging
    monitor.log_request("/test", "GET", 200, 0.1, "127.0.0.1")
    monitor.log_error(Exception("Test error"), {"test": True})
    
    # Test health checks
    health = HealthChecker.get_health_status()
    print("Health Status:", json.dumps(health, indent=2))
    
    # Export metrics
    metrics_file = monitor.export_metrics()
    print(f"Metrics exported to: {metrics_file}")
    
    print("✅ Monitoring system test complete")