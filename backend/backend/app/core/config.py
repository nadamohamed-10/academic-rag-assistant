"""
Central application settings, loaded from environment variables / .env.

Using pydantic-settings means every value below can be overridden by an
env var of the same (uppercased) name without touching this file, e.g.
GROQ_API_KEY, TOP_K, CORS_ORIGINS, ...
"""

from functools import lru_cache
from pathlib import Path
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root:
# rag-assistant-project/
# ├── .env
# └── backend/
#     └── backend/
#         └── app/
#             └── core/
#                 └── config.py
PROJECT_ROOT = Path(__file__).resolve().parents[4]

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- App metadata ---
    app_name: str = "Academic RAG API"
    app_version: str = "1.0.0"

    # --- CORS ---
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    # --- Vector store (Chroma) ---
    chroma_persist_directory: str = str(PROJECT_ROOT / "models" / "vectorstore")
    chroma_collection_name: str = "academic_rag"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    top_k: int = 5

    # --- Groq LLM ---
    groq_api_key: str = Field(
        default="",
        description="Set via GROQ_API_KEY env var",
    )
    groq_model: str = "openai/gpt-oss-120b"
    llm_temperature: float = 0.0
    llm_max_tokens: int = 1024

    @property
    def cors_origins_list(self) -> List[str]:
        return [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]


@lru_cache
def get_settings() -> Settings:
    """Cached so we parse the environment once per process."""
    return Settings()