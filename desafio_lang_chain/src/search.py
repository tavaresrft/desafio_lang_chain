"""Semantic retrieval helpers backed by the shared pgVector collection."""

from pathlib import Path
import sys

from langchain_postgres import PGVector

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.config import get_embeddings, get_settings


def search(query: str, k: int = 10):
    """Return up to k matching (Document, score) pairs."""
    settings = get_settings()
    store = PGVector(
        embeddings=get_embeddings(settings), collection_name=settings.collection,
        connection=settings.database_url, use_jsonb=True,
    )
    return store.similarity_search_with_score(query, k=k)
