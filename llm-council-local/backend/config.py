# backend/config.py
COUNCIL_MEMBERS = {
    "Member_1": {"url": "https://5b828916775c.ngrok-free.app", "model": "gemma2:2b"},
    "Member_2": {"url": "https://wrongfully-gonidioid-alexzander.ngrok-free.dev", "model": "codegemma:2b"},
    "Chairman": {"url": "http://localhost:11434", "model": "llama3.2:1b"}
}

COUNCIL_MODELS = ["Member_1", "Member_2"]
CHAIRMAN_MODEL = "Chairman"