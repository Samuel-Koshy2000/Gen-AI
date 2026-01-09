# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from backend.council import run_council

app = FastAPI(title="LLM Council Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class ChatRequest(BaseModel):
    query: str
    history: Optional[List[dict]] = []


@app.get("/health")
async def health():
    return {
        "status": "online",
        "mode": "distributed-local",
        "llms": "ollama"
    }


@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        return await run_council(request.query, request.history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
