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

# Page setup
st.logo("./bot.png")
st.title("Generate your manual test cases...")
st.caption("Bot can make mistakes. Review the response prior to use.")

# Initialize the model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Function to handle input and update the conversation history
def handle_input(input_text):
    if input_text:
        actual_text = input_text
        # Add the user's input to conversation history
        st.session_state.conversation_history.append(("user", input_text))

        # Prepend "Generate test cases" if not already included
        if not input_text.lower().startswith("generate test cases"):
            input_text = f"Generate test cases {input_text} with steps"

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
                formatted_content = f"Generated test cases for **{actual_text}**\n\n{content}"
                st.session_state.conversation_history.append(("assistant", formatted_content))
            else:
                st.session_state.conversation_history.append(("assistant", "No valid response received."))
        except Exception as e:
            st.session_state.conversation_history.append(("assistant", f"Error: {e}"))

# Display the conversation using st.chat_message
if st.session_state.conversation_history:
    for role, message in st.session_state.conversation_history:
        with st.chat_message(role):
            st.markdown(message)

# Use st.chat_input to handle new user input
user_input = st.chat_input("Describe requirement here")
if user_input:
    handle_input(user_input)

    # Automatically display the assistant's response after user input
    for role, message in st.session_state.conversation_history[-2:]:
        with st.chat_message(role):
            st.markdown(message)
