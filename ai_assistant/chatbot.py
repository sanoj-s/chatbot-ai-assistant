import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ[
    'OPENAI_API_KEY'
] = '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'

# Define the chat prompt template here
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the questions."),
        ("user", "Question:{question}")
    ]
)

st.title('Your Bot is here...')
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""  # Initialize input text
input_text = st.text_input("Ask your question!", value=st.session_state.input_text, key="input_text")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create a session state to store the conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []  # To store the question-answer pairs

# Process the input and display the output
if input_text and st.button("Submit"):
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
        content = getattr(response, 'content', None) or response.get('content', None)
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
