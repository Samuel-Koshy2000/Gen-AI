# Configuration for the Distributed Council
COUNCIL_MEMBERS = {
    "Member_1": {
        "url": "https://your-teammate-1.ngrok-free.app", 
        "model": "smollm2:latest"
    },
    "Member_2": {
        "url": "https://your-teammate-2.ngrok-free.app",
        "model": "gemma2:2b"
    },
    "Chairman": {
        "url": "http://localhost:11434", # Running on your own PC
        "model": "smollm2:latest"
    }
}

TIMEOUT = 60 # Seconds to wait for slow local models