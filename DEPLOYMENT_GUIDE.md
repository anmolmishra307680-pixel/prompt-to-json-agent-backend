# Production Deployment Guide

## 🚀 Quick Deployment

### Option 1: Automated Deployment Script
```bash
python deploy.py
```

### Option 2: Manual Production Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set environment variables
cp .env.example .env
# Edit .env with your production values

# 3. Start production server
python start_production.py
```

### Option 3: Docker Deployment
```bash
# Local development
docker-compose up -d

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

## 🔧 Configuration

### Environment Variables
```bash
# Required for production
DATABASE_URL=postgresql://user:pass@host:5432/db
ENVIRONMENT=production
CORS_ORIGINS=https://yourdomain.com

# Optional
API_WORKERS=4
RATE_LIMIT_REQUESTS_PER_MINUTE=60
LOG_LEVEL=INFO
```

### Database Setup
```bash
# PostgreSQL (Recommended)
DATABASE_URL=postgresql://user:password@localhost:5432/prompt_to_json

# SQLite (Development only)
DATABASE_URL=sqlite:///./app.db
```

## 🧪 Testing

### Run Test Suite
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run unit tests
python -m pytest tests/ -v

# Run API integration tests
python test_suite.py

# Run load tests
python test_suite.py load
```

### Manual API Testing
```bash
# Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/generate -H "Content-Type: application/json" -d '{"prompt":"design a car"}'
```

## 📊 Monitoring

### Health Checks
- `/health` - Basic health status
- `/metrics` - Performance metrics
- Logs in `logs/` directory

### Performance Monitoring
- Request/response tracking
- Error logging
- System resource monitoring
- Database connection health

## 🔒 Security Features

### Rate Limiting
- Configurable per-endpoint limits
- IP-based throttling
- Graceful degradation

### CORS Configuration
- Environment-specific origins
- Production security headers
- Request validation

## 🌐 Platform-Specific Deployment

### Render.com
1. Connect GitHub repository
2. Set environment variables
3. Use `render.yaml` configuration
4. Deploy automatically on push

### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku addons:create heroku-postgresql:mini
git push heroku main
```

### Docker + VPS
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Monitor logs
docker-compose logs -f
```

## 🚨 Troubleshooting

### Common Issues

**Database Connection Failed**
```bash
# Check DATABASE_URL format
# Verify PostgreSQL is running
# Check firewall/network settings
```

**Import Errors**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python version (3.11+ required)
python --version
```

**Rate Limiting Issues**
```bash
# Disable in development
RATE_LIMIT_ENABLED=false

# Adjust limits
RATE_LIMIT_REQUESTS_PER_MINUTE=120
```

### Performance Optimization

**High Memory Usage**
- Increase server resources
- Reduce API_WORKERS count
- Enable request caching

**Slow Response Times**
- Check database performance
- Monitor system resources
- Optimize database queries

## 📈 Scaling for 50+ Users

### Horizontal Scaling
```bash
# Multiple workers
API_WORKERS=4

# Load balancer configuration
# Database connection pooling
# Redis caching (optional)
```

### Database Optimization
```sql
-- Add indexes for performance
CREATE INDEX idx_specs_created_at ON specs(created_at);
CREATE INDEX idx_reports_spec_id ON reports(spec_id);
```

### Monitoring at Scale
- Set up log aggregation
- Configure alerting
- Monitor database performance
- Track API usage patterns

## ✅ Production Checklist

- [ ] Environment variables configured
- [ ] Database connection tested
- [ ] SSL/HTTPS enabled
- [ ] CORS origins restricted
- [ ] Rate limiting configured
- [ ] Monitoring enabled
- [ ] Backup strategy implemented
- [ ] Health checks working
- [ ] Error logging configured
- [ ] Performance testing completed

## 🆘 Support

### Log Locations
- API logs: `logs/api_access.log`
- Error logs: `logs/errors.log`
- Performance: `logs/performance.log`

### Debug Mode
```bash
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

### Health Check Endpoints
- `GET /health` - Basic status
- `GET /metrics` - Performance data
- Database connectivity test included