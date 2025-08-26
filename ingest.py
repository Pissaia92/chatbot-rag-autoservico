import os
import re
from typing import List
from unstructured.partition.auto import partition
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(file_path):
    """Extrai texto de qualquer documento suportado."""
    try:
        elements = partition(filename=file_path)
        return "\n".join([str(el) for el in elements])
    except Exception as e:
        raise Exception(f"Erro na extração de texto: {str(e)}")

def chunk_text(text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> List[str]:
    """Divide o texto em chunks usando abordagem simples."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_size = 0
    
    for word in words:
        word_size = len(embedding_model.encode(word))
        if current_size + word_size > chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            # Mantém overlap
            overlap_words = current_chunk[-chunk_overlap//10:] if chunk_overlap > 0 else []
            current_chunk = overlap_words
            current_size = sum(len(embedding_model.encode(w)) for w in current_chunk)
        
        current_chunk.append(word)
        current_size += word_size
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks