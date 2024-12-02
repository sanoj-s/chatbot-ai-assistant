import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
import base64

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

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
        # Add the user's input to conversation history
        st.session_state.conversation_history.append(("user", input_text))

        # Build the conversation history for the model
        chat_history = [("system", "You are a helpful assistant. Please respond to the questions.")]
        for role, message in st.session_state.conversation_history:
            if role in ["user", "assistant"]:  # Ensure only valid roles
                # Escape curly braces in the message to prevent them from being interpreted as placeholders
                escaped_message = message.replace("{", "{{").replace("}", "}}")
                chat_history.append((role, escaped_message))

        try:
            # Create a prompt from the history
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            modified_chain = modified_prompt | llm

            # Get the model response
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

# Add bot and refresh icons
bot_icon_base64 = get_image_as_base64("./bot.png")
refresh_icon_base64 = get_image_as_base64("./refresh.png")

# Display the header with the refresh icon
col1, col2 = st.columns([0.9, 0.1])
with col1:
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="data:image/png;base64,{bot_icon_base64}" alt="Bot Icon" style="border-radius: 50%; width: 60px; height: 60px;">
            <h1 style="margin: 0;">I'm here to help you...</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    if st.button("🔄", key="refresh_button", help="Refresh"):
        # Save the current conversation and reset
        if st.session_state.conversation_history:
            first_user_message = next(
                (msg for role, msg in st.session_state.conversation_history if role == "user"),
                "Conversation",
            )
            st.session_state.saved_conversations.append(
                {"title": first_user_message, "conversation": st.session_state.conversation_history}
            )
        st.session_state.conversation_history = []

# Display saved conversations in the sidebar
st.sidebar.header("Recent Conversations")
for idx, saved_conversation in enumerate(reversed(st.session_state.saved_conversations)):
    title = saved_conversation["title"]
    with st.sidebar.expander(f"{title}"):
        for role, message in saved_conversation["conversation"]:
            st.markdown(f"**{role.capitalize()}**: {message}")

# Caption for the bot
st.caption("Bot can make mistakes. Review the response prior to use.")

# Display the conversation
for role, message in st.session_state.conversation_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle user input using st.chat_input
user_input = st.chat_input("How can I help you today?")
if user_input:
    # Display the user's input immediately
    st.session_state.conversation_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the input to get the assistant's response
    handle_input(user_input)

    # Automatically display the assistant's response
    for role, message in st.session_state.conversation_history[-1:]:
        with st.chat_message(role):
            st.markdown(message)
