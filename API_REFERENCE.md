# API Reference

Base URL: `https://prompt-to-json-agent.onrender.com` (Production)  
Local: `http://localhost:8000` (Development)

## Endpoints

### POST /generate
Generate specification from natural language prompt.

**Request:**
```json
{
  "prompt": "design a small library"
}
```

**Response:**
```json
{
  "spec": {
    "type": "building",
    "material": ["concrete", "glass"],
    "dimensions": "20x15x8m",
    "color": "gray",
    "purpose": "library",
    "extras": null
  },
  "meta": {
    "confidence": 10,
    "semantic_quality": 1.0
  }
}
```

**cURL:**
```bash
curl -X POST https://prompt-to-json-agent.onrender.com/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "design a small library"}'
```

### POST /evaluate
Evaluate specification quality and store in database.

**Request:**
```json
{
  "prompt": "Design a racing car",
  "spec": {
    "type": "car",
    "material": ["aluminum", "carbon fiber"],
    "dimensions": "4.5x1.8x1.4m",
    "color": "red",
    "purpose": "racing",
    "extras": null
  }
}
```

**Response:**
```json
{
  "report_id": "123e4567-e89b-12d3-a456-426614174000",
  "score": 9
}
```

**cURL:**
```bash
curl -X POST https://prompt-to-json-agent.onrender.com/evaluate \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Design a racing car","spec":{"type":"car","material":["aluminum"],"dimensions":"4.5x1.8x1.4m","color":"red","purpose":"racing","extras":null}}'
```

### POST /iterate
Run reinforcement learning iterations to improve specification.

**Request:**
```json
{
  "spec": {
    "type": "car",
    "material": ["unknown"],
    "dimensions": null,
    "color": null,
    "purpose": null,
    "extras": null
  },
  "max_iters": 3
}
```

**Response:**
```json
{
  "iterations": 2,
  "history": [
    {
      "iteration": 1,
      "before": {
        "type": "car",
        "material": ["unknown"],
        "dimensions": null,
        "color": null,
        "purpose": null,
        "extras": null
      },
      "after": {
        "type": "car",
        "material": ["aluminum", "steel"],
        "dimensions": "4.5x1.8x1.4m",
        "color": "gray",
        "purpose": "transportation",
        "extras": null
      },
      "feedback": {
        "fixes": ["add_dimensions", "fix_materials", "add_purpose", "improve_completeness"],
        "explanation": "Missing dimensions - add standard dimensions; Unrealistic materials - suggest alternatives; Missing purpose - add use case; Low score - improve overall completeness"
      },
      "eval_before": {"spec_score": 4, "valid": true},
      "eval_after": {"spec_score": 10, "valid": true},
      "reward": 1,
      "score_improvement": 6
    }
  ],
  "final_spec": {
    "type": "car",
    "material": ["aluminum", "steel"],
    "dimensions": "4.5x1.8x1.4m",
    "color": "gray",
    "purpose": "transportation",
    "extras": null
  }
}
```

**cURL:**
```bash
curl -X POST https://prompt-to-json-agent.onrender.com/iterate \
  -H "Content-Type: application/json" \
  -d '{"spec":{"type":"car","material":["unknown"],"dimensions":null,"color":null,"purpose":null,"extras":null},"max_iters":3}'
```

### GET /reports/{id}
Retrieve evaluation report by ID.

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "spec_id": "456e7890-e89b-12d3-a456-426614174001",
  "evaluation": {
    "spec_score": 9,
    "valid": true,
    "llm_feedback": {
      "overall_assessment": "Excellent specification",
      "quality_analysis": {
        "completeness": 100.0,
        "realism": 95.0
      }
    }
  },
  "score": 9,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**cURL:**
```bash
curl https://prompt-to-json-agent.onrender.com/reports/123e4567-e89b-12d3-a456-426614174000
```

### POST /log-values
Log HIDG (Honesty, Integrity, Discipline, Gratitude) values.

**Request:**
```json
{
  "honesty": "Completed all Day 4 requirements successfully",
  "integrity": "API documentation is comprehensive and accurate",
  "discipline": "Followed minimal code approach throughout",
  "gratitude": "Clear requirements enabled smooth implementation"
}
```

**Response:**
```json
{
  "id": "789e0123-e89b-12d3-a456-426614174002",
  "message": "Values logged successfully"
}
```

**cURL:**
```bash
curl -X POST https://prompt-to-json-agent.onrender.com/log-values \
  -H "Content-Type: application/json" \
  -d '{"honesty":"Day 4 complete","integrity":"All endpoints working","discipline":"Minimal code","gratitude":"Clear requirements"}'
```

### GET /health
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "ok",
  "service": "prompt-to-json-agent"
}
```

**cURL:**
```bash
curl https://prompt-to-json-agent.onrender.com/health
```

## Error Responses

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

**Error Format:**
```json
{
  "detail": "Error message description"
}
```

## Rate Limits

- Development: No limits
- Production: 100 requests/minute per IP

## Authentication

Currently no authentication required. API key authentication will be added in future versions.