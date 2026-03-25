import streamlit as st
from guardrails import process_prompt

st.set_page_config(page_title="SecurePrompt")

st.title("🔐 SecurePrompt: AI Guardrail Engine")
st.write("A multi-layer guardrail system for secure and reliable AI interactions")

user_input = st.text_input("Enter your prompt:")

if user_input:
    response, status = process_prompt(user_input)

    if "blocked" in status:
        st.error(f"{response} ({status})")
    else:
        st.success(response)