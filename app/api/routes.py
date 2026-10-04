from fastapi import APIRouter

from app.api.schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse, Citation, DocumentListResponse, DeleteResponse
from app.ingestion.service import ingest_text
from app.retrieval.service import retrieve_chunks
from app.generation.service import build_prompt, generate_answer
from app.ingestion.documents import list_documents, delete_document

router = APIRouter()


@router.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest):
    count = ingest_text(request.text, request.source, request.tenant_id)
    return IngestResponse(chunks_stored=count)


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    results = retrieve_chunks(request.question, request.tenant_id, request.top_k)
    prompt = build_prompt(request.question, [r["text"] for r in results])
    answer = generate_answer(prompt)

    citations = [
        Citation(source=r["source"], chunk_index=r["chunk_index"], score=r["score"])
        for r in results
    ]
    return QueryResponse(answer=answer, citations=citations)

@router.get("/documents", response_model=DocumentListResponse)
def get_documents(tenant_id: str):
    documents = list_documents(tenant_id)
    return DocumentListResponse(documents=documents)

@router.delete("/documents/{source}", response_model=DeleteResponse)
def remove_document(source: str, tenant_id: str):
    delete_document(tenant_id, source)
    return DeleteResponse(deleted=True, source=source)