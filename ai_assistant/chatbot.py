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

# Function to reset the conversation
def reset_conversation():
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

# Custom CSS for alignment
st.markdown(
    """
    <style>
        .input-container {
            display: flex;
            align-items: center;
            gap: 10px;
            position: fixed;
            bottom: 10px;
            width: 100%;
            padding: 0 20px;
            background: white;
            z-index: 1000;
        }
        .new-chat-button {
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 15px;
            cursor: pointer;
            font-size: 14px;
        }
        .new-chat-button:hover {
            background-color: #0056b3;
        }
        .st-chat-input {
            flex-grow: 1;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add a container for the input and the new chat button
st.markdown(
    """
    <div class="input-container">
        <button class="new-chat-button" onclick="window.location.reload();">New Chat</button>
        <div class="st-chat-input">
            <!-- The chat input from Streamlit will render here -->
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Reset conversation when the user clicks "New Chat"
if st.session_state.get("reset"):
    reset_conversation()
    st.session_state["reset"] = False

# Display the conversation history
for role, message in st.session_state.conversation_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle user input
user_input = st.chat_input("How can I help you today?")
if user_input:
    # Add user input to conversation history
    st.session_state.conversation_history.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process the input and generate a response
    handle_input(user_input)

    # Display the assistant's response
    for role, message in st.session_state.conversation_history[-1:]:
        with st.chat_message(role):
            st.markdown(message)
