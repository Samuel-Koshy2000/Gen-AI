# backend/memory_manager.py
import json
import os

MEMORY_FILE = "council_memory.json"

def save_to_memory(query, final_answer):
    memory = load_memory()
    memory.append({"query": query, "answer": final_answer})
    # Keep only the last 5 interactions to save space/tokens
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory[-5:], f)

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)

def get_context_string():
    history = load_memory()
    if not history:
        return ""
    context = "\n--- Past Discussions ---\n"
    for item in history:
        context += f"Previous Query: {item['query']}\nPrevious Decision: {item['answer']}\n"
    return context