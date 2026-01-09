# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from backend.council import run_council_stages
import uvicorn

app = FastAPI(title="Claude Council Orchestrator")

# --- MANDATORY: CORS Middleware ---
# This allows your Streamlit frontend to talk to this FastAPI backend without browser blocks
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins for the demo
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Define the Data Model for incoming requests
class ChatRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = [] # Matches st.session_state.messages

# 2. Health Check
@app.get("/health")
async def health_check():
    # This endpoint is useful for your dashboard to check if the backend is alive
    return {
        "status": "Backend Online", 
        "architecture": "Distributed Multi-Agent",
        "protocol": "Llama 3.2"
    }

# 3. The Main Chat Endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Pass both the current query and the conversation history to the council
        result = await run_council_stages(request.query, request.history)
        return result
    except Exception as e:
        # If a node times out or the chairman fails, send the error to the dashboard
        print(f"CRITICAL ERROR: {str(e)}") # Log it in your terminal
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    # Host 0.0.0.0 is essential for your teammates to connect to your IP
    uvicorn.run(app, host="0.0.0.0", port=8000)