import requests
import json

def call_local_llm(member_key, prompt, config):
    member = config[member_key]
    endpoint = f"{member['url']}/api/generate"
    
    payload = {
        "model": member['model'],
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(endpoint, json=payload, timeout=60)
        return response.json().get("response", "Error: No response")
    except Exception as e:
        return f"Connection Error: {str(e)}"