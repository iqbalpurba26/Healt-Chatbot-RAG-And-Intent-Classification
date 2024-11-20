"""retrieval.py for information retrieval from knowledge base chatbot"""
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores import Chroma


embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def get_chromaDB(persist_directory, embedding_function = embedding_model):
    """
    This function to get vectorstore/vectoredb from chromaDB

    Args:
    perist_directory: directory chromaDB where saved
    embedding_function: embedding model used to tokenize knowledge base

    Return:
    vectorstore: A List of knowledge base are tokenized
    """
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding_function
    )
    return vectorstore

def retrieve(intent, prompt, top_k=5, persist_directory='./vectorstore'):
    """
    This function to information retrieval in vector database or vector store

    Args:
    perist_directory: directory ChromaDB where saved
    intent: intent class from prompt
    prompt: user question
    top_k: maximal information relevant search
    """
    vectorstore = get_chromaDB(persist_directory=persist_directory)

    retriever = vectorstore.as_retriever()
    retriever.search_kwargs["filter"] = {"intent":intent}
    
    content = retriever.get_relevant_documents(prompt, top_k)
    information_relevant = [doc.page_content for doc in content]
    formatted_data = "\n".join([f"{i + 1}. {item}" for i, item in enumerate(information_relevant)])

    return formatted_data

