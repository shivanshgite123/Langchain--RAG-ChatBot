# Document Q&A Assistant (LangChain + MongoDB Atlas RAG)

A Streamlit-based Retrieval-Augmented Generation (RAG) application that allows users to upload text documents and ask questions about their content using OpenAI's language models and MongoDB Atlas vector search.

## Features

- 📄 Upload and process TXT documents
- 🤖 AI-powered Q&A using OpenAI's GPT models
- 🗄️ Vector embeddings stored in MongoDB Atlas
- 🔍 Semantic search with MongoDB Atlas Vector Search
- 🧹 Reset/clear knowledge base functionality
- 🔐 Secure API key management using environment variables

## Prerequisites

- Python 3.8 or higher
- OpenAI API key (https://platform.openai.com/api-keys)
- MongoDB Atlas account and cluster (https://www.mongodb.com/cloud/atlas)
- MongoDB Atlas Vector Search enabled on your cluster

## Installation

1. **Clone or download the project**
   ```bash
   cd "RAG USING LANGCHAIN"

2 .Install dependencies

pip install -r requirements.txt

3.Create a .env file in the project root directory with your credentials:

OPENAI_API_KEY=sk-your-openai-api-key-here
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
DB_NAME=rag_db
COLLECTION_NAME=documents

4.MongoDB Atlas Setup
Create a MongoDB Atlas cluster

5.Usage
1.Start the application

2.Upload a document

Click "Upload a TXT document"
Select a .txt file from your computer
3.Ask questions

Type your question in the "Ask a question" field
Click the "Ask" button
The AI will search the document and provide an answer
4.Reset knowledge base

Click "Reset Knowledge Base" to clear all stored documents and embeddings

Project Structure

RAG USING LANGCHAIN/
├── [streamlit_app.py](http://_vscodecontentref_/0)       # Main Streamlit application
├── [requirements.txt](http://_vscodecontentref_/1)       # Python dependencies
├── .env                   # Environment variables (create this)
└── README.md              # This file

Dependencies
streamlit: Web framework for the UI
langchain: Framework for building LLM applications
langchain-openai: OpenAI integration for LangChain
pymongo: MongoDB Python driver
python-dotenv: Load environment variables from .env file
openai: OpenAI Python client

How It Works
Upload: User uploads a TXT file
Split: Text is split into chunks (1000 characters with 200-character overlap)
Embed: Text chunks are converted to embeddings using OpenAI's embedding model
Store: Embeddings are stored in MongoDB Atlas with metadata
Query: User question is converted to an embedding
Search: MongoDB Vector Search finds the most relevant chunks (k=5)
Generate: OpenAI GPT generates an answer based on the relevant chunks
Return: Answer is displayed to the user