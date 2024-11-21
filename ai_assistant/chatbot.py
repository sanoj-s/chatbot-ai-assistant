import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the questions."),
        ("user", "Question:{question}"),
    ]
)

st.title("I am here to help you...")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize conversation history in session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []  # To store the question-answer pairs

if "input_text" not in st.session_state:
    st.session_state.input_text = ""  # Initialize input text

# Define a callback to process the input
def handle_input():
    input_text = st.session_state.input_text
    if input_text.strip():  # Only proceed if the input is not empty
        # Add the user's question to the conversation history
        st.session_state.conversation_history.append(("user", input_text))

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
        response = modified_chain.invoke({"question": input_text})
        try:
            content = getattr(response, "content", None) or response.get("content", None)
            if content:
                # Add the assistant's response to the history
                st.session_state.conversation_history.append(("assistant", content))
            else:
                st.session_state.conversation_history.append(("assistant", "No valid response content received."))
        except Exception as e:
            st.session_state.conversation_history.append(("assistant", f"Error accessing response content: {e}"))

        # Clear the input field
        st.session_state.input_text = ""

# Create the input field with the callback
st.text_input(
    "Ask your question!",
    key="input_text",
    on_change=handle_input,
)

# Display the conversation
for role, message in st.session_state.conversation_history:
    if role == "user":
        st.write(f"**You:** {message}")
    elif role == "assistant":
        st.write(f"**Bot:** {message}")
