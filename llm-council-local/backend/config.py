# backend/config.py

# Mapping of council roles to physical machines (via Tailscale)
COUNCIL_MEMBERS = {
    "Council_1": {
        "url": "http://100.64.243.5:11434",   # laptop-ra4u7g00
        "model": "gemma2:2b"
    }
}

CHAIRMAN = {
    "url": "http://100.120.97.23:11434",      # samuel-pc
    "model": "llama3.2:3b"
}

# Timeout kept high to tolerate cold starts
REQUEST_TIMEOUT = None

# Maximum history entries injected into prompts
MAX_HISTORY_MESSAGES = 6
