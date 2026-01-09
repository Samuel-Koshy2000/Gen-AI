import requests

async def query_model(model_name, prompt, system_prompt=None):
    from .config import COUNCIL_CONFIG
    config = COUNCIL_CONFIG.get(model_name)
    
    if not config:
        return {"content": f"Error: {model_name} not found."}

    # Ollama Chat API payload
    payload = {
        "model": config["model"],
        "messages": [
            {"role": "system", "content": system_prompt or "You are a council member."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        # We call the ngrok URL + /api/chat
        response = requests.post(f"{config['url']}/api/chat", json=payload, timeout=90)
        response.raise_for_status()
        result = response.json()
        return {"content": result['message']['content']}
    except Exception as e:
        return {"content": f"Node {model_name} unreachable: {str(e)}"}