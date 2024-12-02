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

# Page setup
st.logo("./bot.png")

# Initialize the model
llm = ChatOpenAI(model="gpt-4o")

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

# Clear conversation history function
def clear_conversation():
    st.session_state.conversation_history = []

# Display the conversation using st.chat_message
st.title("I'm here to help you...")
st.caption("Bot can make mistakes. Review the response prior to use.")

# Create a new chat icon using st.button
col1, col2 = st.columns([1, 9])  # Adjust column width for alignment
with col1:
    if st.button("🗑️ New Chat"):
        clear_conversation()

# Display the chat conversation
for role, message in st.session_state.conversation_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle user input using st.chat_input
with col2:
    user_input = st.chat_input("How can I help you today?")
    if user_input:
        handle_input(user_input)

        # Automatically display the assistant's response
        for role, message in st.session_state.conversation_history[-2:]:
            with st.chat_message(role):
                st.markdown(message)
