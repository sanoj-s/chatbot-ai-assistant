import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import (
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredPowerPointLoader,
    UnstructuredHTMLLoader,
    UnstructuredCSVLoader,
    PyPDFLoader,
)
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import SecretStr

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

# Initialize Ragas components
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)

# Streamlit UI
st.logo("./bot.png")
st.title("Test Datasets Generator")
st.caption("To generate synthetic test datasets for evaluating your Chatbot AI applications")

# Option to choose input method
input_method = st.radio("Choose your input method:", ("Enter URL", "Upload Files"))

if input_method == "Enter URL":
    # Add a border to the URL input field using custom CSS
    st.markdown("""
        <style>
            /* Make the input field stand out with a border */
            .stTextInput div>input {
                border: 2px solid #4CAF50;  /* Green border color */
                border-radius: 5px;         /* Rounded corners */
                padding: 10px;
                font-size: 16px;
                width: 100%;
            }

            /* Add a box-shadow effect when input is focused */
            .stTextInput div>input:focus {
                box-shadow: 0 0 5px 2px rgba(76, 175, 80, 0.5);  /* Green shadow */
                border-color: #388E3C;  /* Darker green */
            }
        </style>
    """, unsafe_allow_html=True)

    # URL input field
    url = st.text_input("Enter the URL:")

    # Add the slider to select the number of test datasets
    num_test_datasets = st.slider(
        "Select the number of test datasets:", min_value=1, max_value=100, value=5, step=1
    )

    if st.button("Generate Test Data"):
        if url:
            try:
                loader = WebBaseLoader(url)
                documents = loader.load()
                dataset = generator.generate_with_langchain_docs(documents, testset_size=num_test_datasets)
                df = dataset.to_pandas()

                st.success("Test data generated successfully!")
                st.dataframe(df)

                # Download CSV
                csv_file = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Test Data as CSV",
                    data=csv_file,
                    file_name="test_llm_apps_data.csv",
                    mime="text/csv",
                )
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please enter a valid URL.")

elif input_method == "Upload Files":
    uploaded_files = st.file_uploader(
        "Upload files (docx, xlsx, pptx, pdf, csv, html):", 
        type=["docx", "xlsx", "pptx", "pdf", "csv", "html"], 
        accept_multiple_files=True
    )

    # Add the slider to select the number of test datasets
    num_test_datasets = st.slider(
        "Select the number of test datasets:", min_value=1, max_value=100, value=5, step=1
    )

    if st.button("Generate Test Data"):
        if uploaded_files:
            documents = []
            try:
                for uploaded_file in uploaded_files:
                    # Save uploaded file to a temporary location
                    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                        temp_file.write(uploaded_file.read())
                        temp_file_path = temp_file.name

                    # Determine file type and use the appropriate loader
                    file_extension = uploaded_file.name.split(".")[-1].lower()
                    if file_extension == "docx":
                        loader = UnstructuredWordDocumentLoader(temp_file_path)
                    elif file_extension == "xlsx":
                        loader = UnstructuredExcelLoader(temp_file_path)
                    elif file_extension == "pptx":
                        loader = UnstructuredPowerPointLoader(temp_file_path)
                    elif file_extension == "pdf":
                        loader = PyPDFLoader(temp_file_path)
                    elif file_extension == "csv":
                        loader = UnstructuredCSVLoader(temp_file_path)
                    elif file_extension == "html":
                        loader = UnstructuredHTMLLoader(temp_file_path)
                    else:
                        st.error("Unsupported file format.")
                        continue

                    documents.extend(loader.load())

                    # Clean up temporary file
                    if os.path.exists(temp_file_path):
                        os.remove(temp_file_path)

                if documents:
                    dataset = generator.generate_with_langchain_docs(documents, testset_size=num_test_datasets)
                    df = dataset.to_pandas()

                    st.success("Test data generated successfully!")
                    st.dataframe(df)

                    # Download CSV
                    csv_file = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        label="Download Test Data as CSV",
                        data=csv_file,
                        file_name="test_llm_apps_data.csv",
                        mime="text/csv",
                    )
                else:
                    st.error("No documents could be loaded from the uploaded files.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("Please upload valid files.")
