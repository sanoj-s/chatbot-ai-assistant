from langchain_community.document_loaders import WebBaseLoader, UnstructuredExcelLoader, UnstructuredWordDocumentLoader, DirectoryLoader
from ragas.testset import TestsetGenerator
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import streamlit as st
import os

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

generator_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o"))
generator_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())
generator = TestsetGenerator(llm=generator_llm, embedding_model=generator_embeddings)
loader = WebBaseLoader("https://www.aspiresys.com/about-us")
# loader = UnstructuredWordDocumentLoader("path_to_document.docx")
# loader = UnstructuredExcelLoader("path_to_document.xlsx")
documents = loader.load()
dataset = generator.generate_with_langchain_docs(documents, testset_size=5)

df = dataset.to_pandas()
df.to_csv(os.path.join(os.path.dirname(__file__), 'test_llm_apps_data.csv'), index=False)
