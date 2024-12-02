import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
import base64

# Existing code remains the same...

# Add a new function to reset the conversation
def start_new_chat():
    st.session_state.conversation_history = []
    st.experimental_rerun()

# Modify the Streamlit UI to include New Chat icon
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="data:image/png;base64,{bot_icon_base64}" alt="Bot Icon" style="border-radius: 50%; width: 60px; height: 60px;">
        <h1 style="margin: 0;">I'm here to help you...</h1>
    </div>
    """,
    unsafe_allow_html=True,
)
st.caption("Bot can make mistakes. Review the response prior to use.")

# Create a container for chat input and new chat button
col1, col2 = st.columns([0.9, 0.1])

with col1:
    user_input = st.chat_input("How can I help you today?")

with col2:
    # Add New Chat button
    new_chat_button = st.button("🆕", help="Start a new chat")
    if new_chat_button:
        start_new_chat()

# Existing conversation display and input handling code remains the same...
if user_input:
    # Process input as before
    st.session_state.conversation_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    
    handle_input(user_input)
    
    for role, message in st.session_state.conversation_history[-1:]:
        with st.chat_message(role):
            st.markdown(message)
