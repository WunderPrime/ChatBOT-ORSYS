from langchain_ollama import OllamaEmbeddings
import os

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

embeddings_model = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url=OLLAMA_BASE_URL,
)