import os
import streamlit as st
import base64
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import urllib.parse

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Please respond to the questions.")]
)

# Initialize the model
llm = ChatOpenAI(model="gpt-4o")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "saved_conversations" not in st.session_state:
    st.session_state.saved_conversations = []

# Function to handle input and update the conversation history
def handle_input(input_text):
    if input_text:
        if not any(msg[1] == input_text for msg in st.session_state.conversation_history if msg[0] == "user"):
            st.session_state.conversation_history.append(("user", input_text))

        chat_history = [("system", "You are a helpful assistant. Please respond to the questions.")]
        for role, message in st.session_state.conversation_history:
            if role in ["user", "assistant"]:
                escaped_message = message.replace("{", "{{").replace("}", "}}")
                chat_history.append((role, escaped_message))

        try:
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            modified_chain = modified_prompt | llm
            response = modified_chain.invoke({"question": input_text})
            content = getattr(response, "content", None) or response.get("content", None)
            if content:
                st.session_state.conversation_history.append(("assistant", content))
            else:
                st.session_state.conversation_history.append(("assistant", "No valid response received."))
        except Exception as e:
            st.session_state.conversation_history.append(("assistant", f"Error: {e}"))

# Helper function to load images as base64
def get_image_as_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Add bot, refresh, export icons
bot_icon_base64 = get_image_as_base64("./bot.png")
download_icon_base64 = get_image_as_base64("./export.png")

# Display the header with the bot icon
st.markdown(
    f"""
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="data:image/png;base64,{bot_icon_base64}" alt="Bot Icon" style="border-radius: 50%; width: 60px; height: 60px;">
        <h1 style="margin: 0;">I'm here to help you...</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Caption for the bot
st.caption("Bot can make mistakes. Review the response prior to use.")

# Display the conversation
for role, message in st.session_state.conversation_history:
    with st.chat_message(role):
        st.markdown(message)

# Add CSS for the footer
st.markdown(
    """
    <style>
    .chat-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: #f9f9f9;
        padding: 10px 20px;
        box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.1);
        z-index: 1000;
    }
    .refresh-button {
        font-size: 20px;
        cursor: pointer;
        border: none;
        background: none;
        padding: 0;
    }
    .refresh-button:hover {
        color: #007bff;
    }
    .chat-input {
        flex-grow: 1;
        margin-left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Create the refresh button and input box at the bottom
st.markdown(
    f"""
    <div class="chat-footer">
        <button class="refresh-button" onclick="window.location.reload()">🔄 Refresh</button>
        <div class="chat-input">
            {st.chat_input("How can I help you today?")}
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Handle user input using st.chat_input
user_input = st.chat_input("How can I help you today?")
if user_input:
    # Process the input to get the assistant's response
    handle_input(user_input)

    # Automatically display the user's input and the assistant's response
    with st.chat_message("user"):
        st.markdown(user_input)

    for role, message in st.session_state.conversation_history[-1:]:
        with st.chat_message(role):
            st.markdown(message)
