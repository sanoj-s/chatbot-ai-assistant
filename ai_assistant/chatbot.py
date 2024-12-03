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
        st.session_state.conversation_history.append(("user", input_text))

        chat_history = [("system", "You are a helpful assistant. Please respond to the questions.")]
        for role, message in st.session_state.conversation_history:
            chat_history.append((role, message))

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

# Add bot icon
bot_icon_base64 = get_image_as_base64("./bot.png")

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

# Save and clear the conversation on refresh button click
if st.button("🔄 Refresh", key="refresh_button", help="Refresh the conversation"):
    # Save the conversation if there's any history
    if st.session_state.conversation_history:
        # Use the first user's message as the conversation title
        first_user_message = next(
            (msg for role, msg in st.session_state.conversation_history if role == "user"),
            "Conversation",
        )
        # Avoid saving duplicates
        if not any(saved["title"] == first_user_message for saved in st.session_state.saved_conversations):
            st.session_state.saved_conversations.append(
                {"title": first_user_message, "conversation": st.session_state.conversation_history}
            )
    # Clear the current conversation history
    st.session_state.conversation_history = []

# Sidebar to show recent conversations
if st.session_state.saved_conversations:
    st.sidebar.header("Recent Conversations")
    for idx, saved in enumerate(reversed(st.session_state.saved_conversations)):
        with st.sidebar.expander(saved["title"]):
            for role, message in saved["conversation"]:
                st.markdown(f"**{role.capitalize()}**: {message}")

# Handle user input using st.chat_input
user_input = st.chat_input("How can I help you today?")
if user_input:
    handle_input(user_input)

    # Display the latest user message and assistant response
    with st.chat_message("user"):
        st.markdown(user_input)

    for role, message in st.session_state.conversation_history[-1:]:
        with st.chat_message(role):
            st.markdown(message)
