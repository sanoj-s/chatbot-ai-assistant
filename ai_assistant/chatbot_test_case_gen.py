import os

import pypdf
import streamlit as st
import pandas as pd
import docx
from io import StringIO
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from openpyxl import load_workbook

# Set up OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Define the chat prompt template
# Page setup
st.logo("./bot.png")
st.title("Generate Your Manual Test Cases...")
st.caption("Bot can make mistakes. Review the response before using.")

# Initialize the model
llm = ChatOpenAI(model="gpt-4o")

# Initialize session state
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []


# Function to extract text from files
def extract_text_from_file(uploaded_file):
    file_type = uploaded_file.name.split(".")[-1].lower()

    if file_type in ["docx"]:
        doc = docx.Document(uploaded_file)
        return "\n".join([para.text for para in doc.paragraphs]).strip()

    elif file_type in ["pdf"]:
        pdf_reader = pypdf.PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()]).strip()

    elif file_type in ["txt"]:
        return StringIO(uploaded_file.getvalue().decode("utf-8")).read().strip()

    elif file_type in ["csv"]:
        csv_data = pd.read_csv(uploaded_file)
        return csv_data.to_string(index=False).strip()

    elif file_type in ["xlsx"]:
        wb = load_workbook(uploaded_file, data_only=True)
        sheet = wb.active
        return "\n".join(["\t".join([str(cell.value) for cell in row]) for row in sheet.iter_rows()]).strip()

    else:
        return "Unsupported file format!"


# Function to handle input
def handle_input(input_text, uploaded_file):
    if uploaded_file:
        input_text = extract_text_from_file(uploaded_file)
        actual_requirement = input_text

    if input_text:
        st.session_state.conversation_history.append(("user", input_text))
        actual_requirement = input_text

        test_case_format = f"""
                                Test Case ID: (Unique identifier, e.g., TC_01)
                                Test Case Title: (Briefly describe what the test case validates)
                                Pre-conditions: (Any setup or pre-requirements before executing the test case)
                                Test Data: (Data used in the test case)
                                Test Steps: (Step-by-step actions to execute the test case)
                                Expected Result: (The expected outcome after executing the steps)
                                Priority: (Low/Medium/High based on impact)
                                """
        if not input_text.lower().startswith("generate test cases"):
            input_text = (f"You are a manual software tester. Please review the given requirements carefully and write "
                          f"detailed manual test cases for {input_text} in the format {test_case_format}. Ensure "
                          f"comprehensive coverage, including positive, negative, boundary, and edge cases where "
                          f"applicable.")

        chat_history = [
                           ("system",
                            f"You are a manual software tester. Please review the given requirements carefully and "
                            f"write detailed manual test cases for {input_text} in the format {test_case_format}. "
                            f"Ensure comprehensive coverage, including positive, negative, boundary, and edge cases "
                            f"where applicable."),
                       ] + [(role, msg) for role, msg in st.session_state.conversation_history if role == "user"]

        try:
            modified_prompt = ChatPromptTemplate.from_messages(chat_history)
            modified_chain = modified_prompt | llm
            response = modified_chain.invoke({"question": input_text})
            content = getattr(response, "content", None) or response.get("content", None)

            if content:
                formatted_content = f"Generated test cases for **{actual_requirement}**\n\n{content}"
                st.session_state.conversation_history.append(("assistant", formatted_content))
            else:
                st.session_state.conversation_history.append(("assistant", "No valid response received."))
        except Exception as e:
            st.session_state.conversation_history.append(("assistant", f"Error: {e}"))


# User Input & File Upload (supports multiple formats)
user_input = st.chat_input("Describe requirement here")
uploaded_file = st.file_uploader("Upload the requirement file", type=["docx", "pdf", "txt", "csv", "xlsx"])

# Process input or file
if user_input or uploaded_file:
    handle_input(user_input, uploaded_file)

# Display the conversation
if st.session_state.conversation_history:
    for role, message in st.session_state.conversation_history:
        with st.chat_message(role):
            st.markdown(message)

# Add Download Button
if st.session_state.conversation_history:
    conversation_text = "\n".join([f"{role}: {message}" for role, message in st.session_state.conversation_history])
    st.download_button(
        label="Download Test Cases",
        data=conversation_text,
        file_name="test_cases.txt",
        mime="text/plain",
    )
