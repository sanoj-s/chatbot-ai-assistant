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

st.title("I'm here to help you...")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Define a callback to handle user input
def handle_input():
    input_text = st.session_state.input_text.strip()
    if input_text:
        # Append the user input to the conversation history
        st.session_state.conversation_history.append(("user", input_text))

        # Prepare the chat history for LangChain
        chat_history = base_prompt + [
            (role, f"Question:{message}" if role == "user" else message)
            for role, message in st.session_state.conversation_history
        ]

        # Generate a new prompt
        try:
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            response = modified_prompt | llm
            content = getattr(response, "content", None) or response.get("content", None)

            # Append the bot's response to the conversation history
            st.session_state.conversation_history.append(("assistant", content or "No valid response received."))
        except Exception as e:
            st.session_state.conversation_history.append(("assistant", f"Error: {e}"))

        # Clear the input field
        st.session_state.input_text = ""

# Input field with callback
st.text_input(
    "Ask your question!",
    key="input_text",
    on_change=handle_input,
)

# Display conversation history
if st.session_state.conversation_history:
    # Group user and assistant messages for display
    conversation_pairs = [
        (
            st.session_state.conversation_history[i][1],
            st.session_state.conversation_history[i + 1][1] if i + 1 < len(st.session_state.conversation_history) else "",
        )
        for i in range(0, len(st.session_state.conversation_history), 2)
    ]

    # Display the latest conversation at the top
    for user_message, bot_message in reversed(conversation_pairs):
        st.write(f"**You:** {user_message}")
        st.write(f"**Bot:** {bot_message}")
