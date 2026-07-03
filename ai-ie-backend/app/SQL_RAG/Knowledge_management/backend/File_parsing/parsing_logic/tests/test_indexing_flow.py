"""知识索引包装层和 Qdrant 写入边界测试。"""

from __future__ import annotations

import importlib
from pathlib import Path
from unittest.mock import AsyncMock

import pytest


def test_index_item_enrichment_preserves_parsed_text(first_runtime: Path) -> None:
    indexing = importlib.import_module("app.services.ai.indexing.knowledge_index_service")
    item = indexing.to_index_item(
        {
            "file_path": "a.txt",
            "file_name": "a.txt",
            "file_type": "text",
            "engine": "text",
            "result": {"text": "正文"},
        }
    )

    enriched = indexing.enrich_index_item(
        item=item,
        kb_id="kb-test",
        file_id="file-test",
        mode="auto",
    )

    assert enriched["text"] == "正文"
    assert enriched["kb_id"] == "kb-test"
    assert enriched["file_id"] == "file-test"
    assert enriched["mode"] == "auto"


@pytest.mark.asyncio
async def test_index_file_runs_parse_transform_and_qdrant_boundary(
    first_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    indexing = importlib.import_module("app.services.ai.indexing.knowledge_index_service")
    parsed = {
        "success": True,
        "file_path": "a.txt",
        "file_name": "a.txt",
        "file_type": "text",
        "engine": "text",
        "result": {"text": "索引正文"},
    }
    monkeypatch.setattr(indexing, "process_file", AsyncMock(return_value=parsed))
    captured: dict[str, object] = {}

    def fake_upsert(*, items: list[dict[str, object]], collection_name: str) -> dict[str, object]:
        captured["items"] = items
        captured["collection_name"] = collection_name
        return {"collection_name": collection_name, "indexed_count": len(items)}

    monkeypatch.setattr(indexing, "upsert_items_to_qdrant", fake_upsert)
    result = await indexing.index_file_to_qdrant(
        file_path="a.txt",
        collection_name="unit-test",
        kb_id="kb",
        file_id="file",
    )

    assert result["success"] is True
    assert result["indexed_count"] == 1
    assert captured["items"][0]["text"] == "索引正文"


def test_build_documents_rejects_empty_items_and_preserves_metadata(
    first_runtime: Path,
) -> None:
    vector = importlib.import_module("app.ai.rag.vector_index_service")
    documents = vector.build_documents_from_items(
        [
            {"text": "", "file_name": "empty.txt"},
            {
                "text": "有效内容",
                "kb_id": "kb",
                "file_id": "file",
                "file_name": "valid.txt",
                "mode": "auto",
            },
        ]
    )

    assert len(documents) == 1
    assert documents[0].text == "有效内容"
    assert documents[0].metadata["kb_id"] == "kb"


@pytest.mark.filterwarnings(
    "ignore:Payload indexes have no effect in the local Qdrant:UserWarning"
)
def test_upsert_items_writes_to_in_memory_qdrant(
    first_runtime: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    vector = importlib.import_module("app.ai.rag.vector_index_service")
    from llama_index.core import Settings
    from llama_index.core.embeddings import MockEmbedding
    from llama_index.vector_stores.qdrant import QdrantVectorStore
    from qdrant_client import QdrantClient

    client = QdrantClient(":memory:")
    store = QdrantVectorStore(client=client, collection_name="memory-test")

    def configure_mock_embedding() -> None:
        Settings.embed_model = MockEmbedding(embed_dim=1024)

    monkeypatch.setattr(vector, "configure_embedding", configure_mock_embedding)
    monkeypatch.setattr(
        vector,
        "build_qdrant_vector_store",
        lambda collection_name: store,
    )

    result = vector.upsert_items_to_qdrant(
        items=[{"text": "内存向量测试", "file_name": "memory.txt"}],
        collection_name="memory-test",
    )

    assert result["indexed_count"] == 1
    assert client.count(collection_name="memory-test").count == 1
