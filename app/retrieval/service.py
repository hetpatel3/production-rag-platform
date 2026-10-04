from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.core.config import get_settings
from app.core.qdrant import get_qdrant_client
from app.ingestion.embedder import embed_query


def retrieve_chunks(query: str, tenant_id: str, top_k: int | None = None) -> list[dict]:
    settings = get_settings()
    top_k = top_k or settings.top_k

    query_vector = embed_query(query)
    tenant_filter = Filter(
        must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
    )
    results = get_qdrant_client().query_points(
        collection_name=settings.collection_name,
        query=query_vector,
        query_filter=tenant_filter,
        limit=top_k,
    ).points

    return [
        {
            "text": r.payload.get("text", ""),
            "source": r.payload.get("source", ""),
            "chunk_index": r.payload.get("chunk_index"),
            "score": r.score,
        }
        for r in results
        if r.payload
    ]