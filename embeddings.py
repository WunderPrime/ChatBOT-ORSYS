import requests
import os

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/embeddings")
EMBED_MODEL = "nomic-embed-text"

def get_embeddings(text):
    """
    Envoie un texte à Ollama et retourne les embeddings
    """
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": EMBED_MODEL,
            "prompt": text
        }
    )
    response.raise_for_status()
    return response.json()["embedding"]