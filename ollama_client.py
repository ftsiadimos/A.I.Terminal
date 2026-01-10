"""
Ollama Client for AI Terminal Desktop
"""

import requests


class OllamaClient:
    def __init__(self, host='http://localhost:11434', model='llama2'):
        self.host = host.rstrip('/')
        self.model = model
    
    def generate(self, prompt, stream=False):
        """Generate a response from Ollama"""
        try:
            url = f"{self.host}/api/generate"
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": stream
            }
            
            response = requests.post(url, json=payload, timeout=300)
            response.raise_for_status()
            
            if stream:
                return True, response
            else:
                data = response.json()
                return True, data.get('response', '')
        except Exception as e:
            return False, str(e)
    
    def list_models(self):
        """List available models"""
        try:
            url = f"{self.host}/api/tags"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            return True, data.get('models', [])
        except Exception as e:
            return False, str(e)
    
    def test_connection(self):
        """Test connection to Ollama"""
        try:
            url = f"{self.host}/api/tags"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return True, "Connected"
        except Exception as e:
            return False, str(e)
