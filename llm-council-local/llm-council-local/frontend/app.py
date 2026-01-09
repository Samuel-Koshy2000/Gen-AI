import streamlit as st
import sys
import os
# Add backend to path so we can import our logic
sys.path.append(os.path.abspath('../backend'))
from engine import call_local_llm
from config import COUNCIL_MEMBERS

st.set_page_config(page_title="LLM Council Local", layout="wide")
st.title("🏛️ Local LLM Council")

query = st.text_input("Ask the Council a question:")

if st.button("Summon Council"):
    if query:
        # --- STAGE 1: First Opinions ---
        st.subheader("Stage 1: First Opinions")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("Member 1 (Remote)")
            ans1 = call_local_llm("Member_1", query, COUNCIL_MEMBERS)
            st.write(ans1)
            
        with col2:
            st.info("Member 2 (Remote)")
            ans2 = call_local_llm("Member_2", query, COUNCIL_MEMBERS)
            st.write(ans2)

        # --- STAGE 2: Review ---
        st.subheader("Stage 2: Peer Review")
        review_prompt = f"Rank the following response based on accuracy: {ans1}"
        review = call_local_llm("Member_2", review_prompt, COUNCIL_MEMBERS)
        st.success(f"Member 2 Review: {review}")

        # --- STAGE 3: Chairman ---
        st.subheader("Stage 3: Final Decision")
        chairman_prompt = f"Summarize these two viewpoints into one perfect answer: \n1: {ans1}\n2: {ans2}"
        final = call_local_llm("Chairman", chairman_prompt, COUNCIL_MEMBERS)
        st.header("Consensus Result:")
        st.write(final)