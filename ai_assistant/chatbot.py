import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ[
    'OPENAI_API_KEY'] = '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'

# Define the chat prompt template here
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the questions."),
        ("user", "Question:{question}")
    ]
)

st.title("Your Bot is here...")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create a session state to store the conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []  # To store the question-answer pairs

# Create the input field
input_text = st.text_input(
    "Ask your question!",
    value="",
    key="input_text",
    on_change=lambda: st.session_state.conversation_history.append(("user", st.session_state.input_text)),
)

# Process the input and generate the output
if "input_text" in st.session_state and st.session_state.input_text.strip():
    # Create a modified prompt using the history
    modified_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please respond to the questions."),
            *st.session_state.conversation_history,
        ]
    )
    # Create a new chain with the modified prompt
    modified_chain = modified_prompt | llm

    # Invoke the chain and get the response
    response = modified_chain.invoke({"question": st.session_state.input_text})
    try:
        content = getattr(response, "content", None) or response.get("content", None)
        if content:
            # Add the assistant's response to the history
            st.session_state.conversation_history.append(("assistant", content))
        else:
            content = "No valid response content received."
    except Exception as e:
        content = f"Error accessing response content: {e}"

    # Clear the input field after processing
    st.session_state.input_text = ""

# Display the conversation
for role, message in st.session_state.conversation_history:
    if role == "user":
        st.write(f"**You:** {message}")
    elif role == "assistant":
        st.write(f"**Bot:** {message}")
