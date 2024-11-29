import streamlit as st
import os
import tempfile
from langchain_community.document_loaders import (
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
)
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

# Set OpenAI API Key
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Initialize Ragas components
generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)

# Streamlit UI
st.title("Test Data Generator")

# Option to choose input method
input_method = st.radio("Choose your input method:", ("Enter URL", "Upload a File"))

if input_method == "Enter URL":
    url = st.text_input("Enter the URL:")
    if st.button("Generate Test Data"):
        if url:
            try:
                loader = WebBaseLoader(url)
                documents = loader.load()
                dataset = generator.generate_with_langchain_docs(documents, testset_size=5)
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

elif input_method == "Upload a File":
    uploaded_file = st.file_uploader(
        "Upload a file (docx, xlsx):", type=["docx", "xlsx"]
    )
    if st.button("Generate Test Data"):
        if uploaded_file:
            try:
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
                else:
                    st.error("Unsupported file format.")
                    st.stop()

                documents = loader.load()
                dataset = generator.generate_with_langchain_docs(documents, testset_size=5)
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
            finally:
                # Clean up temporary file
                if os.path.exists(temp_file_path):
                    os.remove(temp_file_path)
        else:
            st.error("Please upload a valid file.")