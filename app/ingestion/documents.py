from qdrant_client.models import Filter, FieldCondition, MatchValue

from app.core.config import get_settings
from app.core.qdrant import get_qdrant_client


def list_documents(tenant_id: str) -> list[str]:
    """Return the distinct source names ingested by this tenant."""
    client = get_qdrant_client()
    settings = get_settings()

    tenant_filter = Filter(
        must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id))]
    )

    sources = set()
    next_offset = None
    while True:
        points, next_offset = client.scroll(
            collection_name=settings.collection_name,
            scroll_filter=tenant_filter,
            with_payload=True,
            with_vectors=False,
            limit=100,
            offset=next_offset,
        )
        for point in points:
            if point.payload and "source" in point.payload:
                sources.add(point.payload["source"])
        if next_offset is None:
            break

    return sorted(sources)


def delete_document(tenant_id: str, source: str) -> None:
    """Delete all chunks belonging to this tenant's document."""
    client = get_qdrant_client()
    settings = get_settings()

    doc_filter = Filter(
        must=[
            FieldCondition(key="tenant_id", match=MatchValue(value=tenant_id)),
            FieldCondition(key="source", match=MatchValue(value=source)),
        ]
    )

    client.delete(
        collection_name=settings.collection_name,
        points_selector=doc_filter,
    )