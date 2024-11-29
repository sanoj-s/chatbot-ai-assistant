import streamlit as st
import os
from langchain_community.document_loaders import (
    WebBaseLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
    DirectoryLoader,
)
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import pandas as pd

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
        "Upload a file (docx, pdf, txt, xlsx):", type=["docx", "pdf", "txt", "xlsx"]
    )
    if st.button("Generate Test Data"):
        if uploaded_file:
            try:
                file_extension = uploaded_file.name.split(".")[-1].lower()
                if file_extension == "docx":
                    loader = UnstructuredWordDocumentLoader(uploaded_file)
                elif file_extension == "xlsx":
                    loader = UnstructuredExcelLoader(uploaded_file)
                elif file_extension in ["pdf", "txt"]:
                    st.error("PDF and TXT support not implemented yet.")
                    st.stop()
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
        else:
            st.error("Please upload a valid file.")
