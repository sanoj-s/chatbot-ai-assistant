import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the questions."),
    ]
)

# Define the background color for the edit field
st.markdown(
    """
    <style>
    .stTextInput input {
        background-color: #f0f8ff;  /* Light blue background */
        border: none;  /* Remove the border */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px;
        color: #000;  /* Black text for light themes */
    }
    .st-dark .stTextInput input {
        background-color: #1e1e1e;  /* Dark background for dark theme */
        color: #fff;  /* White text for contrast */
        border: none;  /* Remove the border */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.logo("./bot.png")
st.title("I'm here to help you...")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Define a callback to handle input
def handle_input():
    input_text = st.session_state.input_text.strip()
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

        # Clear the input field
        st.session_state.input_text = ""

# Create the input field with the callback
st.text_input(
    "Ask your question!",
    key="input_text",
    on_change=handle_input,
)

# Group conversation pairs and display latest first
if st.session_state.conversation_history:
    conversation_pairs = []
    for i in range(0, len(st.session_state.conversation_history), 2):
        user_message = st.session_state.conversation_history[i][1] if i < len(st.session_state.conversation_history) else ""
        bot_message = st.session_state.conversation_history[i + 1][1] if i + 1 < len(st.session_state.conversation_history) else ""
        conversation_pairs.append((user_message, bot_message))

    for user_message, bot_message in reversed(conversation_pairs):
        # Display "You" with color
        st.markdown(f"<span style='color:blue;'>**You:** {user_message}</span>", unsafe_allow_html=True)
        # Display "Bot" with color
        st.markdown(f"<span style='color:green;'>**Bot:** {bot_message}</span>", unsafe_allow_html=True)
