"""
Tests use fake retrieval/generation services (via monkeypatch) so they run
fast, offline, and without needing a real Chroma index or Groq API key.
"""
import pytest
from fastapi.testclient import TestClient

from app.services.retrieval import RetrievedChunk


class FakeRetrievalService:
    def __init__(self, settings=None):
        pass

    def retrieve(self, question, top_k=None):
        return [RetrievedChunk(text="Sample chunk text.", source="paper1.pdf", score=0.1)]

    def health_check(self):
        return True


class FakeGenerationService:
    def __init__(self, settings=None):
        pass

    def generate_answer(self, question, chunks):
        return f"Fake grounded answer for: {question}"


@pytest.fixture()
def client(monkeypatch):
    import app.main as main_module

    monkeypatch.setattr(main_module, "RetrievalService", FakeRetrievalService)
    monkeypatch.setattr(main_module, "GenerationService", FakeGenerationService)

    test_app = main_module.create_app()
    with TestClient(test_app) as c:
        yield c


def test_query_happy_path(client):
    response = client.post("/query", json={"question": "What is biomedical informatics?"})
    assert response.status_code == 200
    body = response.json()
    assert "answer" in body and "sources" in body
    assert body["sources"] == ["paper1.pdf"]
    assert body["answer"]


def test_query_invalid_input_missing_question(client):
    response = client.post("/query", json={})
    assert response.status_code == 422


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
