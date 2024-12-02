import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import streamlit as st
import ojc

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant. Please respond to the questions.")]
)

# page setup
st.logo("./bot.png")

# Initialize the model
llm = ChatOpenAI(model="gpt-4o")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# Function to handle input and update the conversation history
def parse_java_project(project_path):
    project = ojc.Project(project_path)
    classes = project.get_classes()
    class_info = {}
    for cls in classes:
        class_info[cls.name] = {
            "methods": [method.name for method in cls.methods],
            "fields": [field.name for field in cls.fields]
        }
    return class_info


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
            # Check if the user's input is related to the Java project
            if "java" in input_text.lower():
                # Parse the Java project
                project_path = "autobots-selenium.zip"
                class_info = parse_java_project(project_path)

                # Generate a response based on the parsed information
                response = ""
                for word in input_text.split():
                    if word in class_info:
                        class_data = class_info[word]
                        response += f"The class {word} has the following methods: {', '.join(class_data['methods'])}\n"
                        response += f"The class {word} has the following fields: {', '.join(class_data['fields'])}\n"
                    else:
                        response += f"I'm sorry, I couldn't find information about {word}.\n"

                st.session_state.conversation_history.append(("assistant", response))
            else:
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
st.title("I'm here to help you...")
st.caption("Bot can make mistakes. Review the response prior to use.")
for role, message in st.session_state.conversation_history:
    with st.chat_message(role):
        st.markdown(message)

# Handle user input using st.chat_input
user_input = st.chat_input("How can I help you today?")
if user_input:
    handle_input(user_input)

    # Automatically display the assistant's response
    for role, message in st.session_state.conversation_history[-2:]:
        with st.chat_message(role):
            st.markdown(message)
