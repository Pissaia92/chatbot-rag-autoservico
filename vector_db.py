import chromadb
from sentence_transformers import SentenceTransformer
import os
import tempfile

# Usar modelo mais leve e eficiente para embeddings
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embeddings(texts):
    # Retorna embeddings como lista de listas de floats
    embeddings = embedding_model.encode(texts)
    if isinstance(embeddings, list):
        return embeddings
    else:
        return embeddings.tolist() if hasattr(embeddings, 'tolist') else [embeddings]

# Usar diretório temporário para ChromaDB
chroma_path = os.path.join(tempfile.gettempdir(), "chroma_db")
client = chromadb.PersistentClient(path=chroma_path)

def get_or_create_collection(name="docs"):
    return client.get_or_create_collection(name)

def add_chunks_to_collection(chunks, collection_name="docs"):
    collection = get_or_create_collection(collection_name)
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    embeddings = get_embeddings(chunks)
    
    collection.add(
    ids=ids,
    documents=chunks,
    embeddings=embeddings
)