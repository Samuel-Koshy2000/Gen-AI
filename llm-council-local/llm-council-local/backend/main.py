from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .council import run_council_stages # This exists in the repo

app = FastAPI()

# VERY IMPORTANT: This allows the frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/chat")
async def chat(payload: dict):
    user_query = payload.get("query")
    # This calls the 3-stage logic in council.py
    result = await run_council_stages(user_query)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)