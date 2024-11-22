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
    .stTextInput textarea {
        background-color: #7cbaf2; 
        color: #000;  /* Black text for light themes */
        border: 2px solid #007acc;  /* Add a border with color */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px;
        font-size: 16px;  /* Slightly larger font for better readability */
    }
    .stTextInput textarea:focus {
        background-color: #e0f7ff;  /* Light blue background when focused */
        border-color: #005f99;  /* Darker border color on focus */
        outline: none;  /* Remove focus outline */
    }
    .st-dark .stTextInput textarea {
        background-color: #333333;  /* Dark background for dark theme */
        color: #d3d3d3;  /* Light gray text for better contrast */
        border: 2px solid #4caf50;  /* Green border for dark mode */
        border-radius: 5px;  /* Rounded corners */
        padding: 10px;
        font-size: 16px;  /* Slightly larger font for better readability */
    }
    .st-dark .stTextInput textarea:focus {
        background-color: #3a4e5c;  /* Slightly lighter dark background when focused */
        border-color: #45a049;  /* Darker green border on focus */
        outline: none;  /* Remove focus outline */
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
st.text_area(
    label="", 
    placeholder="How can I help you today?", 
    key="input_text",
    on_change=handle_input,
    height=100, 
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
