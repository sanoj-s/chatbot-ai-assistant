import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Please respond to the questions.")]
)

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

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

# Add custom CSS for alignment
st.markdown(
    """
    <style>
    /* Align the user chat message to the right */
    .user-chat-message {
        text-align: right;
        background-color: #e0f7fa; /* Light blue background for user messages */
        padding: 10px;
        border-radius: 15px;
        margin: 5px;
        max-width: 70%; /* Prevents messages from stretching too far */
        margin-left: auto; /* Push message to the right */
    }
    /* Align the assistant chat message to the left */
    .assistant-chat-message {
        text-align: left;
        background-color: #f1f1f1; /* Light gray background for assistant messages */
        padding: 10px;
        border-radius: 15px;
        margin: 5px;
        max-width: 70%; /* Prevents messages from stretching too far */
        margin-right: auto; /* Push message to the left */
    }
    /* Align the user icon to the right */
    .user-chat-icon {
        text-align: right;
        display: flex;
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the conversation using st.chat_message
st.title("I'm here to help you...")
st.caption("Bot can make mistakes. Review the response prior to use.")

for role, message in st.session_state.conversation_history:
    if role == "user":
        with st.chat_message(role):
            # Use CSS classes for user messages
            st.markdown(f"<div class='user-chat-icon'>👤</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='user-chat-message'>{message}</div>", unsafe_allow_html=True)
    elif role == "assistant":
        with st.chat_message(role):
            # Use CSS classes for assistant messages
            st.markdown(f"<div class='assistant-chat-message'>{message}</div>", unsafe_allow_html=True)

# Handle user input using st.chat_input
user_input = st.chat_input("How can I help you today?")
if user_input:
    handle_input(user_input)

    # Automatically display the assistant's response
    for role, message in st.session_state.conversation_history[-2:]:
        if role == "user":
            with st.chat_message(role):
                st.markdown(f"<div class='user-chat-icon'>👤</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='user-chat-message'>{message}</div>", unsafe_allow_html=True)
        elif role == "assistant":
            with st.chat_message(role):
                st.markdown(f"<div class='assistant-chat-message'>{message}</div>", unsafe_allow_html=True)
