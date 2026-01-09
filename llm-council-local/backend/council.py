# backend/council.py
import httpx
import asyncio
import time
from backend.config import COUNCIL_MEMBERS, COUNCIL_MODELS, CHAIRMAN_MODEL

async def call_node(name, prompt):
    node = COUNCIL_MEMBERS[name]
    start = time.time()
    # Using timeout=None to handle the 54s cold-start lag without crashing
    try:
        async with httpx.AsyncClient(timeout=None) as client:
            res = await client.post(
                f"{node['url']}/api/generate", 
                json={
                    "model": node['model'], 
                    "prompt": prompt, 
                    "stream": False,
                    "keep_alive": -1 # Instructs Ollama to keep model in VRAM
                }
            )
            
            if res.status_code == 200:
                return {
                    "response": res.json().get("response", "No response content"), 
                    "latency": round(time.time() - start, 2)
                }
            else:
                return {"response": f"Node Error {res.status_code}", "latency": 0}
    except Exception as e:
        return {"response": f"Connection Error: {str(e)}", "latency": 0}

async def run_council_stages(current_query, chat_history=[]):
    """
    Args:
        current_query (str): The latest user message.
        chat_history (list): List of dicts [{"role": "user", "content": "..."}, ...]
    """
    
    # --- MEMORY INJECTION ---
    # We summarize the history into a single block to save tokens
    context_memory = ""
    if chat_history:
        # We only take the last 3 exchanges to keep the prompt lean for Llama 3.2
        recent_history = chat_history[-6:] 
        context_memory = "PAST CONVERSATION HISTORY:\n"
        for msg in recent_history:
            role = "User" if msg["role"] == "user" else "Council"
            context_memory += f"{role}: {msg['content'][:200]}...\n"
        context_memory += "\n--- END OF HISTORY ---\n"

    # The full prompt for the nodes now includes the context memory
    full_prompt = f"{context_memory}\nNew User Query: {current_query}\n\nPlease provide your expert opinion based on the context above."

    # STAGE 1: FIRST OPINIONS
    tasks = [call_node(m, full_prompt) for m in COUNCIL_MODELS]
    stage1_results = await asyncio.gather(*tasks)
    opinions = {m: r for m, r in zip(COUNCIL_MODELS, stage1_results)}

    # STAGE 2: PEER REVIEW (Simplified for Speed)
    reviews = {}
    for reviewer in COUNCIL_MODELS:
        others = [f"Peer Ans: {opinions[m]['response'][:400]}" for m in COUNCIL_MODELS if m != reviewer]
        review_prompt = f"Topic: {current_query}\n" + "\n".join(others) + "\nRate quality 1-10."
        reviews[reviewer] = await call_node(reviewer, review_prompt)

    # STAGE 3: CHAIRMAN SYNTHESIS
    summary = "\n".join([f"Node {i}: {opinions[m]['response'][:500]}" for i, m in enumerate(COUNCIL_MODELS)])
    ranking = "\n".join([f"Review {i}: {r['response'][:200]}" for i, r in enumerate(reviews.values())])

    final_prompt = (
        f"You are the Council Chairman. {context_memory}\n"
        f"Latest Query: {current_query}\n\n"
        f"Member Perspectives:\n{summary}\n\n"
        f"Peer Evaluations:\n{ranking}\n\n"
        f"Synthesize the final authoritative answer, maintaining consistency with previous history."
    )
    
    final = await call_node(CHAIRMAN_MODEL, final_prompt)
    return {"opinions": opinions, "reviews": reviews, "final": final}