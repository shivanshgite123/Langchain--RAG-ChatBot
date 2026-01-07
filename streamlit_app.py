import streamlit as st
import os
from dotenv import load_dotenv
from pymongo import MongoClient

from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import MongoDBAtlasVectorSearch
from langchain.chains import RetrievalQA

# LOAD ENV 
load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

DB_NAME = os.getenv("DB_NAME", "rag_db")        
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "documents")

#  VALIDATION 
if not MONGODB_URI:
    st.error(" MONGODB_URI not found in .env")
    st.stop()

if not OPENAI_API_KEY:
    st.warning(" OpenAI API key not found in .env")

#  MONGODB CONNECTION
client = MongoClient(MONGODB_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# CORE FUNCTION 
def generate_response(uploaded_file, query_text):

    documents = [uploaded_file.read().decode("utf-8")]

    # Text splitting
    text_splitter = CharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = text_splitter.create_documents(documents)

    # Embeddings
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY
    )

    # MongoDB Vector Store
    vectorstore = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=embeddings,
        collection=collection,
        index_name="vector_index"
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(openai_api_key=OPENAI_API_KEY),
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True
    )

    result = qa.invoke({"query": query_text})

    if not result["result"]:
        return " No relevant information found."

    return result["result"]

# STREAMLIT UI 
st.set_page_config(page_title="Document Q&A (MongoDB RAG)")
st.title("📄 Document Q&A Assistant (LangChain + MongoDB Atlas)")

uploaded_file = st.file_uploader(
    "Upload a TXT document",
    type=["txt"]
)

query_text = st.text_input(
    "Ask a question",
    disabled=not uploaded_file
)

if st.button("Ask") and uploaded_file and query_text:
    with st.spinner("Searching document..."):
        answer = generate_response(uploaded_file, query_text)
        st.success(answer)

# RESET KNOWLEDGE BASE
if st.button("Reset Knowledge Base"):
    collection.delete_many({})
    st.warning("Knowledge base cleared!")
