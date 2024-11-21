import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template here
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the questions."),
        ("user", "Question:{question}")
    ]
)

st.title('Your Bot is here...')
input_text = st.text_input("Ask your question!")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Create a chain that combines the prompt and the model
chain = prompt | llm

# Create a session state to store the conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Invoke the chain with the input text and display the output
if input_text:
    st.session_state.conversation_history.append(("user", input_text))
    modified_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful assistant. Please respond to the questions."),
            *st.session_state.conversation_history,
            ("user", input_text)
        ]
    )
    # Create a new chain with the modified prompt
    modified_chain = modified_prompt | llm

    # Invoke the modified chain and display the output
    response = modified_chain.invoke({"question": input_text})
    try:
        content = getattr(response, 'content', None) or response.get('content', None)
        if content:
            st.write(content)
        else:
            st.write("No valid response content received.")
    except Exception as e:
        st.write(f"Error accessing response content: {e}")
