import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a testing assistant. Your job is to write detailed and well-structured manual test cases based on the requirements provided."),
    ]
)

# Apply custom styles for the input field
st.markdown(
    """
    <style>
    .stTextInput input {
        background-color: #e8f6fa;
        color: #000;
        border: 2px solid #007bff;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
    }
    .stTextInput input:focus {
        background-color: #e0f7ff;
        border: none;
        outline: none;
    }
    .st-dark .stTextInput input {
        background-color: #1e1e1e;
        color: #d3d3d3;
        border: 2px solid #4caf50;
        border-radius: 5px;
        padding: 10px;
        width: 100%;
    }
    .st-dark .stTextInput input:focus {
        background-color: #3a4e5c;
        border: none;
        outline: none;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Page setup
st.logo("./bot.png")
st.title("Generate your manual test cases...")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Callback function to handle input and generate responses
def handle_input():
    input_text = st.session_state.input_text.strip()
    if input_text:
        # Add the user's input to conversation history
        st.session_state.conversation_history.append(("user", input_text))

        # Prepare the conversation history for the model
        chat_history = [
            ("system", "You are a testing assistant. Your job is to write manual test cases."),
        ] + st.session_state.conversation_history

        try:
            # Create a dynamic prompt from conversation history
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            modified_chain = modified_prompt | llm

            # Get the response
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

# Create the input field with callback
st.text_input(
    "",
    key="input_text",
    on_change=handle_input,
    placeholder="Describe the test case(e.g., 'Generate your manual test cases for login functionality')",
)

# Display conversation history in reverse chronological order
if st.session_state.conversation_history:
    conversation_pairs = []
    for i in range(0, len(st.session_state.conversation_history), 2):
        user_message = st.session_state.conversation_history[i][1] if i < len(st.session_state.conversation_history) else ""
        bot_message = st.session_state.conversation_history[i + 1][1] if i + 1 < len(st.session_state.conversation_history) else ""
        conversation_pairs.append((user_message, bot_message))

    for user_message, bot_message in reversed(conversation_pairs):
        st.markdown(f"<span style='color:blue;'>**You:** {user_message}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:green;'>**Bot:**</span>", unsafe_allow_html=True)
        st.markdown(f"```markdown\n{bot_message}\n```")

# Add a download button for test cases
if st.session_state.conversation_history:
    formatted_test_cases = "\n\n".join([f"**You:** {pair[0]}\n**Bot:** {pair[1]}" for pair in conversation_pairs])
    st.download_button(
        label="Download Test Cases",
        data=formatted_test_cases,
        file_name="test_cases.txt",
        mime="text/plain",
    )
