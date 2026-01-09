🏛️ Project Overview: The Distributed AI Council

The goal of this project is to create a multi-agent system where a Chairman node (Windows) orchestrates two Council nodes (Windows & Kali Linux) over a Tailscale virtual private network.
The Architecture

    Infrastructure: Tailscale (VPN) allows machines on different networks to communicate as if they were in the same room.

    Inference Engine: Ollama (Local LLM runner).

    Backend: FastAPI (Python) using Asynchronous I/O for parallel processing.

    Frontend: Streamlit for a "Claude-style" chat interface.

🛠️ Phase 1: Machine Setup & Commands
Node 1: The Chairman (Windows)

    IP: 100.114.119.33

    Role: Runs the FastAPI Backend and the final Synthesis model (llama3.2:3b).

    Command: ```powershell $env:OLLAMA_HOST="0.0.0.0:11434" ollama serve


Node 2: Council Member 1 (Windows/Local)

    IP: 100.64.243.5

    Role: Runs gemma2:2b.

    Command:
    PowerShell

    $env:OLLAMA_HOST="0.0.0.0:11434"
    ollama serve

Node 3: Council Member 2 (Kali Linux)

    IP: 100.107.144.10

    Role: Runs mistral:7b on a custom port.

    Commands:
    Bash

    # Ensure port is open
    sudo ufw allow 11435/tcp
    # Start Ollama on specific IP and Port
    OLLAMA_HOST=0.0.0.0:11435 ollama serve

🧠 Phase 2: Theoretical Implementation (Bonus Points)
1. Asynchronous Parallelism (Speed)

Theory: In a standard setup (Synchronous), the system waits for Node A to finish before starting Node B. Our Solution: We used Python’s asyncio and httpx. The Chairman sends the question to all nodes simultaneously.

    Benefit: Total response time = the slowest node's time, not the sum of all nodes.

2. Multi-Agent Synthesis

Theory: Individual LLMs have biases. By "Consensus Building," we get a higher-quality answer. Our Solution:

    Stage 1: Each council member provides an independent opinion.

    Stage 2: The Chairman receives the user query + all opinions as "Context."

    Stage 3: The Chairman acts as a meta-summarizer to provide the "Final Truth."

💻 Phase 3: The Working Codebase
The Backend (backend/main.py)

This script uses Pydantic for data validation and FastAPI for the web server.
Python

# Key Logic: Parallel execution
tasks = [ask_ollama(client, info["url"], info["model"], query) 
         for name, info in COUNCIL_MEMBERS.items()]
results = await asyncio.gather(*tasks)

The Frontend (frontend/dashboard.py)

This uses Streamlit to create a UI. It monitors "True Node Status" by checking if the Ollama API is reachable before allowing a chat to start.
🚨 Troubleshooting Reference (Common Errors Solved)
Error	Meaning	Solution
404 Not Found	Model name or URL path is wrong.	Match tags exactly (e.g., mistral:7b vs mistral).
422 Unprocessable	Frontend sent wrong data format.	Ensure JSON keys match (e.g., {"message": "..."}).
Connection Refused	Ollama is only listening locally.	Set OLLAMA_HOST=0.0.0.0.
NameError: 'app'	App called before it was created.	Define app = FastAPI() at the very top of the script.
🚀 Next Steps for Your Project

To take this even further for more bonus points, would you like me to help you implement "Self-Correction"?

This is where the Chairman sends Council 1's answer to Council 2 and asks, "Do you disagree with this? If so, why?" before giving the final answer. This is called Agentic Reflection.
