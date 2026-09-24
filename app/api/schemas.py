from pydantic import BaseModel


class IngestRequest(BaseModel):
    text: str
    source: str


class IngestResponse(BaseModel):
    chunks_stored: int


class QueryRequest(BaseModel):
    question: str
    top_k: int | None = None


class Citation(BaseModel):
    source: str
    chunk_index: int
    score: float


class QueryResponse(BaseModel):
    answer: str
    citations: list[Citation]