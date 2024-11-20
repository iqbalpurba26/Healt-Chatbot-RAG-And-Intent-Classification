"""this file to load knowledge base (.json) to vector database (chromaDB)"""
import json
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma

def chunk_texts(dataset, chunk_size=5000, chunk_overlap=100):
    """
    This function to chunking text

    Args:
    dataset: knowledge base chatbot,
    chunk_size: maximal total chunk
    chunk_overlap: number of overlapping tokens

    Return:
    all_splits : A List
    """
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    documents = [Document(page_content=data["answer"], metadata={'intent': data['intent']}) for data in dataset]
    all_splits = text_splitter.split_documents(documents)

    return all_splits

def add_to_chromadb(text_chunk, embedding_model, persist_directory):
    """
    This function to add the text chunk to chromaDB

    Args:
    text_chunk: A list of chunking texts
    embedding_model: model embedding used to tokenize text
    persist_directory: directory of chromaDB saved

    Return:
    vectordb: A vector database
    """
    vectordb = Chroma.from_documents(
        documents=text_chunk,
        embedding=embedding_model,
        persist_directory=persist_directory
    )

    return vectordb

with open("knowledge_base.json", "r") as file:
    dataset = json.load(file)

embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

text_chunk = chunk_texts(dataset)

path_db = './vectorstore'
vectordb = add_to_chromadb(text_chunk, embedding_model, path_db)
