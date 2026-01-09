# frontend/dashboard.py
import streamlit as st
import requests
import pandas as pd
import asyncio
from backend.config import COUNCIL_MEMBERS

# 1. Anthropic/Claude Aesthetic Configuration
st.set_page_config(page_title="Claude Council", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: var(--background-color); font-family: 'Inter', sans-serif; }
    section[data-testid="stSidebar"] { background-color: #E8E6DC; border-right: 1px solid #B1ADA1; }
    .main .block-container { max-width: 900px; padding-top: 2rem; }
    .stChatMessage { background-color: transparent !important; border-bottom: 1px solid #E8E6DC; padding: 1.5rem 0px !important; }
    [data-testid="stMetricValue"] { font-size: 1.2rem; color: #D97757; }
    </style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. SIDEBAR: The Fixed "Truth" Monitor
with st.sidebar:
    st.title("🏛️ Council Control")
    
    if st.button("➕ New Discussion", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("📡 True Node Status")
    
    for name, info in COUNCIL_MEMBERS.items():
        try:
            # We add a 2.0s timeout and check for the Ollama header
            # This bypasses the 'fake' 200 OK that ngrok sends when the PC is off
            r = requests.get(f"{info['url']}/api/tags", timeout=2.0)
            
            # If Ngrok is active but Ollama is CLOSED, Ngrok usually returns a 
            # 502/504 error or a specific HTML page. 
            # Real Ollama returns JSON with 'models' or 'tags'.
            if r.status_code == 200 and ("models" in r.text or "tags" in r.text):
                st.write(f"🟢 **{name}**: AI ACTIVE")
            else:
                st.write(f"⚠️ **{name}**: TUNNEL UP / AI DOWN")
        except:
            # This triggers if Ngrok is closed OR PC is shut down
            st.write(f"🔴 **{name}**: OFFLINE")

# 4. MAIN CHAT INTERFACE
st.title("Council of Agents")
st.caption("Distributed Consensus Network | Llama 3.2 Protocol")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "data" in message:
            with st.expander("View Deliberation Details"):
                st.json(message["data"])

# 5. CHAT INPUT & WORKFLOW
if prompt := st.chat_input("Ask the council..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.status("🔗 Deliberating...", expanded=True) as status:
            try:
                payload = {"query": prompt, "history": st.session_state.messages[:-1]}
                res = requests.post("http://localhost:8000/api/chat", json=payload, timeout=300)
                
                if res.status_code != 200:
                    status.update(label="❌ Council Error", state="error")
                    st.error(f"Backend reported error {res.status_code}")
                else:
                    data = res.json()
                    status.update(label="✅ Consensus Reached", state="complete", expanded=False)
                    
                    st.markdown("### 📍 Stage 1: Opinions")
                    tabs = st.tabs(list(data['opinions'].keys()))
                    for i, (name, content) in enumerate(data['opinions'].items()):
                        with tabs[i]:
                            st.metric("Inference Time", f"{content.get('latency', 0)}s")
                            st.write(content.get('response', 'No response'))

                    st.markdown("---")
                    st.markdown("### ⚖️ Stage 2: Peer Review")
                    review_df = pd.DataFrame([
                        {"Node": m, "Ranking Logic": r.get('response', '')[:250] + "..."} 
                        for m, r in data['reviews'].items()
                    ])
                    st.table(review_df)

                    st.markdown("---")
                    st.markdown("### 👑 Final Synthesis")
                    final_answer = data['final']['response']
                    st.info(final_answer)

                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": final_answer,
                        "data": data 
                    })

            except Exception as e:
                status.update(label="❌ Connection Failed", state="error")
                st.error(f"Could not reach backend: {str(e)}")