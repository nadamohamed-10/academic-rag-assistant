from typing import List

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User's natural-language question")


class QueryResponse(BaseModel):
    answer: str
    sources: List[str] = Field(default_factory=list)
