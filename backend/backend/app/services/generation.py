"""
Builds the grounded prompt from retrieved chunks and calls Groq for the
final answer.
"""
import logging
from typing import List

from groq import Groq

from app.core.config import Settings
from app.services.retrieval import RetrievedChunk

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are an academic research assistant. Answer the user's question using "
    "ONLY the provided context excerpts. If the context does not contain the "
    "answer, say you don't have enough information rather than guessing. "
    "Cite sources inline like [source_name] when you use them."
)


class GenerationService:
    def __init__(self, settings: Settings):
        self._settings = settings
        self._client = Groq(api_key=settings.groq_api_key)

    def _build_prompt(self, question: str, chunks: List[RetrievedChunk]) -> str:
        context_blocks = "\n\n".join(
            f"[{c.source}]\n{c.text}" for c in chunks
        ) or "No relevant context was found."

        return (
            f"Context excerpts:\n{context_blocks}\n\n"
            f"Question: {question}\n\n"
            "Answer, citing sources in [brackets] where relevant:"
        )

    def generate_answer(self, question: str, chunks: List[RetrievedChunk]) -> str:
        prompt = self._build_prompt(question, chunks)

        response = self._client.chat.completions.create(
            model=self._settings.groq_model,
            temperature=self._settings.llm_temperature,
            max_tokens=self._settings.llm_max_tokens,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content
