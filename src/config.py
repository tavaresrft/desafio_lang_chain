"""Shared provider and pgVector configuration for ingestion and search."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigurationError(ValueError):
    """Raised when required application configuration is missing or invalid."""


@dataclass(frozen=True)
class Settings:
    provider: str
    database_url: str
    collection: str
    api_key: str
    chat_model: str
    embedding_model: str


def get_settings() -> Settings:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    if provider not in {"openai", "gemini"}:
        raise ConfigurationError("LLM_PROVIDER deve ser 'openai' ou 'gemini'.")

    key_name = "OPENAI_API_KEY" if provider == "openai" else "GEMINI_API_KEY"
    api_key = os.getenv(key_name, "").strip()
    if not api_key:
        raise ConfigurationError(f"Defina {key_name} no arquivo .env.")

    chat_name = "OPENAI_CHAT_MODEL" if provider == "openai" else "GEMINI_CHAT_MODEL"
    embedding_name = "OPENAI_EMBEDDING_MODEL" if provider == "openai" else "GEMINI_EMBEDDING_MODEL"
    return Settings(
        provider=provider,
        database_url=os.getenv("DATABASE_URL", "postgresql+psycopg://langchain:langchain@localhost:5432/langchain"),
        collection=os.getenv("PGVECTOR_COLLECTION", "documents"),
        api_key=api_key,
        chat_model=os.getenv(chat_name, "gpt-4.1-mini" if provider == "openai" else "gemini-3.8-flash"),
        embedding_model=os.getenv(embedding_name, "text-embedding-3-small" if provider == "openai" else "gemini-embedding-001"),
    )


def get_embeddings(settings: Settings):
    if settings.provider == "openai":
        from langchain_openai import OpenAIEmbeddings

        return OpenAIEmbeddings(model=settings.embedding_model, api_key=settings.api_key)
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    return GoogleGenerativeAIEmbeddings(model=settings.embedding_model, google_api_key=settings.api_key)


def get_chat_model(settings: Settings):
    if settings.provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=settings.chat_model, api_key=settings.api_key, temperature=0)
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=settings.chat_model, google_api_key=settings.api_key, temperature=0)
