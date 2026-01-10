Linux commands :

export OLLAMA_HOST=127.0.0.1:11435  
export OLLAMA_HOST=127.0.0.1:11435  
OLLAMA_HOST=0.0.0.0:11435 ollama serve

ollama run model_name 


WIndows commands : 
tailscale up
set OLLAMA_HOST=0.0.0.0:11434
ollama serve
ollama run model_name

To run the commands : 

streamlit run dashboard.py for the front end
uvicorn backend.main:app --host 0.0.0.0 --reload  for the backend
