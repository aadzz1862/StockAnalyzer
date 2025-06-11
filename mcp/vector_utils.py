# mcp/vector_utils.py

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Initialize the Chroma client
chroma_client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./data/embeddings"))

# Define collection (like a table for vectors)
collection_name = "news_articles"

# Load or create collection
collection = chroma_client.get_or_create_collection(name=collection_name)

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and fast model

def embed_text(text):
    """
    Embeds a given text using SentenceTransformer.
    """
    return embedding_model.encode(text).tolist()  # Chroma expects list of floats

def add_article_to_vectorstore(article_id, text, metadata):
    """
    Adds the article text + metadata into the vector DB.
    """
    embedding = embed_text(text)
    collection.add(
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata],
        ids=[str(article_id)]
    )

def query_similar_articles(query_text, top_k=5):
    """
    Semantic search for similar articles.
    """
    query_embedding = embed_text(query_text)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )
    return results

def persist_vectorstore():
    """
    Save current state of the vector DB.
    """
    chroma_client.persist()

