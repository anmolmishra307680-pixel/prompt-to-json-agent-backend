"""
Frontend Integration Examples
Sample code for integrating with the prompt-to-json-agent API
"""

import requests
import json
import asyncio
import aiohttp
from typing import Dict, Any, Optional

class PromptToJsonClient:
    """Python client for prompt-to-json-agent API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def generate_spec(self, prompt: str) -> Dict[str, Any]:
        """Generate specification from natural language prompt"""
        response = self.session.post(
            f"{self.base_url}/generate",
            json={"prompt": prompt}
        )
        response.raise_for_status()
        return response.json()
    
    def evaluate_spec(self, prompt: str, spec: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate specification quality and get report ID"""
        response = self.session.post(
            f"{self.base_url}/evaluate",
            json={"prompt": prompt, "spec": spec}
        )
        response.raise_for_status()
        return response.json()
    
    def iterate_spec(self, spec: Dict[str, Any], max_iters: int = 3) -> Dict[str, Any]:
        """Run RL iterations to improve specification"""
        response = self.session.post(
            f"{self.base_url}/iterate",
            json={"spec": spec, "max_iters": max_iters}
        )
        response.raise_for_status()
        return response.json()
    
    def get_report(self, report_id: str) -> Dict[str, Any]:
        """Retrieve evaluation report by ID"""
        response = self.session.get(f"{self.base_url}/reports/{report_id}")
        response.raise_for_status()
        return response.json()
    
    def log_values(self, **values) -> Dict[str, Any]:
        """Log HIDG values"""
        response = self.session.post(
            f"{self.base_url}/log-values",
            json=values
        )
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health status"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

class AsyncPromptToJsonClient:
    """Async Python client for high-performance applications"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
    
    async def generate_spec(self, prompt: str) -> Dict[str, Any]:
        """Async generate specification"""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/generate",
                json={"prompt": prompt}
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def batch_generate(self, prompts: list) -> list:
        """Generate multiple specs concurrently"""
        async with aiohttp.ClientSession() as session:
            tasks = []
            for prompt in prompts:
                task = session.post(
                    f"{self.base_url}/generate",
                    json={"prompt": prompt}
                )
                tasks.append(task)
            
            responses = await asyncio.gather(*tasks)
            results = []
            for response in responses:
                response.raise_for_status()
                results.append(await response.json())
            
            return results

# JavaScript/TypeScript Example
JAVASCRIPT_EXAMPLE = '''
// JavaScript/TypeScript Frontend Integration
class PromptToJsonAPI {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }

    async generateSpec(prompt) {
        const response = await fetch(`${this.baseURL}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    }

    async evaluateSpec(prompt, spec) {
        const response = await fetch(`${this.baseURL}/evaluate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt, spec })
        });
        
        return await response.json();
    }

    async iterateSpec(spec, maxIters = 3) {
        const response = await fetch(`${this.baseURL}/iterate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ spec, max_iters: maxIters })
        });
        
        return await response.json();
    }

    async getReport(reportId) {
        const response = await fetch(`${this.baseURL}/reports/${reportId}`);
        return await response.json();
    }

    async logValues(values) {
        const response = await fetch(`${this.baseURL}/log-values`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(values)
        });
        
        return await response.json();
    }
}

// Usage Example
const api = new PromptToJsonAPI();

async function processPrompt(userInput) {
    try {
        // Generate initial spec
        const spec = await api.generateSpec(userInput);
        console.log('Generated spec:', spec);
        
        // Evaluate quality
        const evaluation = await api.evaluateSpec(userInput, spec);
        console.log('Evaluation:', evaluation);
        
        // Improve with RL if score is low
        if (evaluation.score < 8) {
            const improved = await api.iterateSpec(spec, 3);
            console.log('Improved spec:', improved.final_spec);
            return improved.final_spec;
        }
        
        return spec;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}
'''

# React Component Example
REACT_EXAMPLE = '''
// React Component Example
import React, { useState, useCallback } from 'react';

const PromptToJsonGenerator = () => {
    const [prompt, setPrompt] = useState('');
    const [spec, setSpec] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const generateSpec = useCallback(async () => {
        if (!prompt.trim()) return;
        
        setLoading(true);
        setError(null);
        
        try {
            const response = await fetch('http://localhost:8000/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            setSpec(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }, [prompt]);

    return (
        <div className="prompt-generator">
            <h2>Prompt to JSON Generator</h2>
            
            <div className="input-section">
                <textarea
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    placeholder="Enter your design prompt..."
                    rows={4}
                    cols={50}
                />
                <br />
                <button 
                    onClick={generateSpec} 
                    disabled={loading || !prompt.trim()}
                >
                    {loading ? 'Generating...' : 'Generate Specification'}
                </button>
            </div>

            {error && (
                <div className="error">
                    Error: {error}
                </div>
            )}

            {spec && (
                <div className="result-section">
                    <h3>Generated Specification:</h3>
                    <pre>{JSON.stringify(spec, null, 2)}</pre>
                </div>
            )}
        </div>
    );
};

export default PromptToJsonGenerator;
'''

# Vue.js Example
VUE_EXAMPLE = '''
<!-- Vue.js Component Example -->
<template>
  <div class="prompt-generator">
    <h2>Prompt to JSON Generator</h2>
    
    <div class="input-section">
      <textarea
        v-model="prompt"
        placeholder="Enter your design prompt..."
        :rows="4"
        :cols="50"
      ></textarea>
      <br />
      <button 
        @click="generateSpec" 
        :disabled="loading || !prompt.trim()"
      >
        {{ loading ? 'Generating...' : 'Generate Specification' }}
      </button>
    </div>

    <div v-if="error" class="error">
      Error: {{ error }}
    </div>

    <div v-if="spec" class="result-section">
      <h3>Generated Specification:</h3>
      <pre>{{ JSON.stringify(spec, null, 2) }}</pre>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PromptToJsonGenerator',
  data() {
    return {
      prompt: '',
      spec: null,
      loading: false,
      error: null
    };
  },
  methods: {
    async generateSpec() {
      if (!this.prompt.trim()) return;
      
      this.loading = true;
      this.error = null;
      
      try {
        const response = await fetch('http://localhost:8000/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ prompt: this.prompt })
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        this.spec = await response.json();
      } catch (err) {
        this.error = err.message;
      } finally {
        this.loading = false;
      }
    }
  }
};
</script>
'''

def demo_python_client():
    """Demonstrate Python client usage"""
    client = PromptToJsonClient()
    
    try:
        # Health check
        health = client.health_check()
        print("✅ API Health:", health)
        
        # Generate spec
        prompt = "Design a lightweight carbon fiber racing drone"
        spec = client.generate_spec(prompt)
        print("📝 Generated Spec:", json.dumps(spec, indent=2))
        
        # Evaluate spec
        evaluation = client.evaluate_spec(prompt, spec)
        print("📊 Evaluation:", evaluation)
        
        # Iterate if needed
        if evaluation["score"] < 8:
            improved = client.iterate_spec(spec, max_iters=2)
            print("🔄 Improved Spec:", json.dumps(improved["final_spec"], indent=2))
        
        # Log values
        values_result = client.log_values(
            honesty="Transparent about limitations",
            integrity="Consistent quality standards",
            discipline="Systematic improvement process",
            gratitude="Appreciation for user feedback"
        )
        print("📋 Values Logged:", values_result)
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def demo_async_client():
    """Demonstrate async client usage"""
    client = AsyncPromptToJsonClient()
    
    prompts = [
        "Design a sports car",
        "Create a modern office building", 
        "Build a surveillance drone"
    ]
    
    try:
        # Batch generate specs
        specs = await client.batch_generate(prompts)
        for i, spec in enumerate(specs):
            print(f"Spec {i+1}:", json.dumps(spec, indent=2))
    except Exception as e:
        print(f"❌ Async Error: {e}")

if __name__ == "__main__":
    print("🚀 Frontend Integration Examples")
    print("=" * 50)
    
    print("\n📱 Python Client Demo:")
    demo_python_client()
    
    print("\n⚡ Async Client Demo:")
    asyncio.run(demo_async_client())
    
    print("\n💻 JavaScript Example:")
    print(JAVASCRIPT_EXAMPLE)
    
    print("\n⚛️ React Example:")
    print(REACT_EXAMPLE)
    
    print("\n🖖 Vue.js Example:")
    print(VUE_EXAMPLE)