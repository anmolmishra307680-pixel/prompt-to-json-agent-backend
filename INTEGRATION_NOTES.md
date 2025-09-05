# Integration Notes

## For Rishabh (Frontend)

### Backend REST Endpoints Ready
- **Base URL**: `https://prompt-to-json-agent.onrender.com`
- **Endpoints**: POST /generate, POST /evaluate, POST /iterate, GET /reports/{id}, POST /log-values
- **Documentation**: See `API_REFERENCE.md` for complete examples
- **CORS**: Enabled for frontend integration

### UI Requirements
- **Prompt Input**: Text area for natural language prompts
- **JSON Viewer**: Display generated specifications with syntax highlighting
- **Evaluate Button**: Run evaluation and show scores
- **Iterate Button**: Run RL improvements and show before/after
- **Reports View**: Display evaluation reports with LLM feedback
- **Values Form**: Submit HIDG values (honesty, integrity, discipline, gratitude)

### Sample Integration Code
```javascript
// Generate spec from prompt
const response = await fetch('https://prompt-to-json-agent.onrender.com/generate', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ prompt: userInput })
});
const result = await response.json();
```

## For Nipun (BHIV Bucket/DB)

### Database Schema
```sql
-- Specifications table
CREATE TABLE specs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  prompt TEXT NOT NULL,
  spec JSONB NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Evaluation reports table  
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  spec_id UUID REFERENCES specs(id),
  evaluation JSONB,
  score INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- RL iteration history
CREATE TABLE feedback_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  spec_id UUID,
  iteration INTEGER,
  before JSONB,
  after JSONB,
  feedback JSONB,
  reward INTEGER,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- HIDG values logging
CREATE TABLE values_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  honesty TEXT,
  integrity TEXT,
  discipline TEXT,
  gratitude TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

### Recommended Indexes
```sql
CREATE INDEX idx_specs_created_at ON specs(created_at);
CREATE INDEX idx_reports_spec_id ON reports(spec_id);
CREATE INDEX idx_feedback_logs_spec_id ON feedback_logs(spec_id);
CREATE INDEX idx_values_logs_created_at ON values_logs(created_at);
```

### Supabase Migration
- Current: PostgreSQL via Docker
- Migration: Update `DATABASE_URL` environment variable
- RLS Policies: Add row-level security as needed
- API Keys: Use service role key for backend access

## For Nisarg (BHIV Core)

### Agent Architecture
All agents implement the same interface:
```python
from core.agent_base import AgentBase

class YourAgent(AgentBase):
    def run(self, input: dict) -> dict:
        # Your implementation
        return {"result": "..."}
```

### Available Agents
```python
# Generate specs from prompts
from agents.prompt_agent import PromptAgent
agent = PromptAgent()
result = agent.run({"prompt": "design a car"})

# Evaluate spec quality
from agents.evaluator import Evaluator
evaluator = Evaluator()
result = evaluator.run({"spec": {...}})

# Generate improvement feedback
from agents.feedback import FeedbackAgent
feedback = FeedbackAgent()
result = feedback.run({"spec": {...}, "score": 6})

# Run RL iterations
from agents.rl_agent import RLAgent
rl_agent = RLAgent(evaluator, feedback)
result = rl_agent.iterate(spec, max_iters=3)
```

### Direct Agent Usage (Bypass REST)
```python
# Import agents directly
from agents.evaluator import Evaluator
from agents.feedback import FeedbackAgent

# Use without FastAPI
evaluator = Evaluator()
feedback_agent = FeedbackAgent()

# Process spec
spec = {"type": "car", "material": ["steel"]}
evaluation = evaluator.run({"spec": spec})
improvements = feedback_agent.run({"spec": spec, "score": evaluation["spec_score"]})
```

### Extension Points
- Add new agents in `agents/` directory
- Implement `AgentBase.run(input) -> output`
- Register in FastAPI for REST access
- Use existing evaluation and feedback systems

## Database Access

### Local Development
```bash
# PostgreSQL connection
DATABASE_URL="postgresql://devuser:devpass@localhost:5432/bhiv"

# Connect via psql
psql postgresql://devuser:devpass@localhost:5432/bhiv
```

### Production Access
- **Read-only user**: Will be provided separately
- **Full access**: Available via environment variables
- **Supabase**: Migration instructions in deployment docs

## Sample Data

### Test Specifications
Located in `samples/` directory:
- `car.json` - Complete car specification
- `building.json` - Office building example
- `drone.json` - Racing drone specification
- `table.json` - Dining table example

### Sample API Calls
See `API_REFERENCE.md` for complete cURL examples and expected responses.

## Deployment Info

- **Production URL**: `https://prompt-to-json-agent.onrender.com`
- **Health Check**: `GET /health`
- **Docker Images**: Available via `docker-compose.prod.yml`
- **Environment Variables**: `DATABASE_URL` for database connection