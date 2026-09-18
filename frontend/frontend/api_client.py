"""
Thin wrapper around the FastAPI backend's HTTP API.

Keeping all requests logic in one place means app.py stays focused on UI,
and the base URL is never hard-coded — it always comes from the environment
(API_BASE_URL in .env).
"""
import os
from dataclasses import dataclass
from typing import List

import requests
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DEFAULT_TIMEOUT = 30  # seconds


class APIError(Exception):
    """Raised whenever the backend can't be reached or returns an error."""


@dataclass
class QueryResult:
    answer: str
    sources: List[str]


def check_health() -> bool:
    """Returns True if the backend reports itself healthy, False otherwise."""
    try:
        resp = requests.get(f"{API_BASE_URL}/health", timeout=5)
        resp.raise_for_status()
        return resp.json().get("status") == "ok"
    except requests.RequestException:
        return False


def ask_question(question: str) -> QueryResult:
    """
    Sends a question to POST /query.

    Raises APIError with a friendly message on any failure, so app.py can
    just catch one exception type and show it to the user.
    """
    payload = {"question": question}

    try:
        resp = requests.post(f"{API_BASE_URL}/query", json=payload, timeout=DEFAULT_TIMEOUT)
    except requests.ConnectionError as exc:
        raise APIError(
            f"Couldn't reach the backend at {API_BASE_URL}. "
            "Is it running (uvicorn app.main:app --reload)?"
        ) from exc
    except requests.Timeout as exc:
        raise APIError("The backend took too long to respond. Please try again.") from exc

    if resp.status_code == 422:
        raise APIError("That question wasn't valid — please enter some text and try again.")
    if not resp.ok:
        raise APIError(f"Backend returned an error ({resp.status_code}). Please try again.")

    try:
        data = resp.json()
        return QueryResult(answer=data["answer"], sources=data.get("sources", []))
    except (ValueError, KeyError) as exc:
        raise APIError("Received an unexpected response from the backend.") from exc
