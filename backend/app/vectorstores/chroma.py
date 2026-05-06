import chromadb

from backend.app.core.config import get_settings

settings = get_settings()

chroma_client = chromadb.HttpClient(
    host=settings.chroma_host,
    port=settings.chroma_port,
)

def get_chroma_client():
    return chroma_client