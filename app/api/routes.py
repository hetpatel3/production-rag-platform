from fastapi import APIRouter

from app.api.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse, Citation
from app.ingestion.service import ingest_text
from app.retrieval.service import retrieve_chunks
from app.generation.service import build_prompt, generate_answer

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    count = ingest_text(request.text, request.source)
    return IngestResponse(chunks_stored=count)


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    results = retrieve_chunks(request.question, request.top_k)
    prompt = build_prompt(request.question, [r["text"] for r in results])
    answer = generate_answer(prompt)

    citations = [
        Citation(source=r["source"], chunk_index=r["chunk_index"], score=r["score"])
        for r in results
    ]
    return QueryResponse(answer=answer, citations=citations)