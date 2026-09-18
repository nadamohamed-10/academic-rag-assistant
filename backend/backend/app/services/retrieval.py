"""
Loads the persisted Chroma vector store once and exposes retrieval helpers.

The store is expected to already exist on disk (produced by the notebook /
indexing step) under `settings.chroma_persist_directory`, using the same
embedding model and collection name recorded in config.json.
"""
import logging
from dataclasses import dataclass
from typing import List, Optional

import chromadb
from chromadb.utils import embedding_functions

from app.core.config import Settings

logger = logging.getLogger(__name__)


@dataclass
class RetrievedChunk:
    text: str
    source: str
    score: float


class RetrievalService:
    """Wraps a Chroma collection + its embedding function."""

    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = chromadb.PersistentClient(path=settings.chroma_persist_directory)
        self._embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=settings.embedding_model
        )
        self._collection = self._client.get_or_create_collection(
            name=settings.chroma_collection_name,
            embedding_function=self._embedding_fn,
        )
        logger.info(
            "Loaded Chroma collection '%s' (%d items) from %s",
            settings.chroma_collection_name,
            self._collection.count(),
            settings.chroma_persist_directory,
        )

    def retrieve(self, question: str, top_k: Optional[int] = None) -> List[RetrievedChunk]:
        k = top_k or self._settings.top_k
        results = self._collection.query(query_texts=[question], n_results=k)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        chunks: List[RetrievedChunk] = []
        for doc, meta, dist in zip(documents, metadatas, distances):
            source = (meta or {}).get("source", "unknown")
            chunks.append(RetrievedChunk(text=doc, source=source, score=dist))
        return chunks

    def health_check(self) -> bool:
        try:
            self._collection.count()
            return True
        except Exception:  # pragma: no cover - defensive
            logger.exception("Vector store health check failed")
            return False
