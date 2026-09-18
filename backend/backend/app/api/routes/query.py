import logging

from fastapi import APIRouter, HTTPException, Request

from app.schemas.query import QueryRequest, QueryResponse

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health")
async def health(request: Request):
    retrieval_service = request.app.state.retrieval_service
    ok = retrieval_service.health_check()
    return {"status": "ok" if ok else "degraded"}


@router.post("/query", response_model=QueryResponse)
async def query(payload: QueryRequest, request: Request):
    retrieval_service = request.app.state.retrieval_service
    generation_service = request.app.state.generation_service

    try:
        chunks = retrieval_service.retrieve(payload.question)
        answer = generation_service.generate_answer(question=payload.question, chunks=chunks)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("Query failed")
        raise HTTPException(status_code=500, detail="Failed to process query") from exc

    sources = sorted({c.source for c in chunks})
    return QueryResponse(answer=answer, sources=sources)
