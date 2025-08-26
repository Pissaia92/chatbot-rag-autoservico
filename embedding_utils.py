from sentence_transformers import SentenceTransformer

# Modelo para gerar embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    """Gera embedding para um texto."""
    return model.encode(text).tolist()

def get_embeddings(texts):
    """Gera embeddings para uma lista de textos."""
    return model.encode(texts).tolist()