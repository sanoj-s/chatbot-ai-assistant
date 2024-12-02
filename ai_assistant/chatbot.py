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

# page setup
# st.logo("./bot.png")

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


# Display the conversation using st.chat_message
st.markdown(
    """
    <div style="display: flex; align-items: center; gap: 10px;">
        <img src="https://via.placeholder.com/40" alt="Bot Icon" style="border-radius: 50%; width: 40px; height: 40px;">
        <h1 style="margin: 0;">I'm here to help you...</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

st.title("I'm here to help you...")
st.caption("Bot can make mistakes. Review the response prior to use.")
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
