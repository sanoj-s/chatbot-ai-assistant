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
        # Store the original input for display purposes
        original_input = input_text

        # Prepend the required prefix for processing
        if not input_text.lower().startswith("generate test cases"):
            input_text = f"Generate test cases {input_text} with steps"

        # Add the user's original input to conversation history for display
        st.session_state.conversation_history.append(("user", original_input))

        # Prepare the conversation history for the model
        chat_history = [
            ("system", "You are a testing assistant. Your job is to write manual test cases."),
        ] + [(role, msg) for role, msg in st.session_state.conversation_history if role == "user"]

        try:
            # Create a dynamic prompt from conversation history
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            modified_chain = modified_prompt | llm
        
            # Get the response
            response = modified_chain.invoke({"question": input_text})
            content = getattr(response, "content", None) or response.get("content", None)
        
            if content:
                # Add "Generated results for <input_text>" as the first line
                formatted_content = f"Generated results for **{original_input}**\n\n{content}"
                st.session_state.conversation_history.append(("assistant", formatted_content))
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
    placeholder="Describe the test scenario (e.g., 'Login functionality')",
)

# Display conversation history in reverse chronological order (latest first)
if st.session_state.conversation_history:
    for pair in reversed(st.session_state.conversation_history):
        if pair[0] == "user":
            st.markdown(
                f"""
                <div style="text-align: right; margin: 10px 0;">
                    <div style="background-color: #016580; color: white; font-weight: bold; padding: 10px; border-radius: 8px; display: inline-block; max-width: 80%;">
                        You: {pair[1]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif pair[0] == "assistant":
            st.markdown(
                f"""
                <div style="text-align: left; margin: 10px 0;">
                    <div style="color: green; font-weight: bold; margin-bottom: 5px;">Bot:</div>
                    <div style="background-color: #f4f4f4; border-radius: 8px; padding: 10px;">
                        {pair[1]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

# Add a download button for test cases only if the last bot response is not the warning message
if st.session_state.conversation_history and not st.session_state.conversation_history[-1][1].startswith("Sorry, your input must start"):
    formatted_test_cases = "\n\n".join([
        f"**You:** {pair[1]}\n**Bot:** {response[1]}"
        for pair, response in zip(st.session_state.conversation_history, st.session_state.conversation_history[1:])
        if pair[0] == "user" and response[0] == "assistant"
    ])
    st.download_button(
        label="Download Test Cases",
        data=formatted_test_cases,
        file_name="test_cases.txt",
        mime="text/plain",
    )
