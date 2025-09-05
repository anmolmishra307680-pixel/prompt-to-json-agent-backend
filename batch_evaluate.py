import json
import requests
import pathlib

def batch_evaluate():
    """Batch evaluate all samples and store in DB"""
    samples_dir = pathlib.Path("samples")
    base_url = "http://127.0.0.1:8000"
    
    for json_file in samples_dir.glob("*.json"):
        print(f"Processing {json_file.name}...")
        
        try:
            # Load spec
            spec = json.loads(json_file.read_text())
            
            # Create payload
            payload = {
                "prompt": f"Sample from {json_file.name}",
                "spec": spec
            }
            
            # Post to evaluate endpoint
            response = requests.post(f"{base_url}/evaluate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                print(f"  Report ID: {result['report_id']}")
                print(f"  Score: {result['score']}/10")
            else:
                print(f"  Error: {response.status_code}")
                
        except Exception as e:
            print(f"  Failed: {e}")

if __name__ == "__main__":
    batch_evaluate()