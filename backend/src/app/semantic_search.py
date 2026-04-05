import json
from asyncio import Lock
from typing import Any

import asyncpg

from app.ai_schemas import (
    EmbeddingRequest,
    SemanticDocumentUpsertRequest,
    SemanticSearchRequest,
)
from app.db import get_database_pool
from app.nvidia_ai import create_embeddings


class SemanticSearchStoreError(RuntimeError):
    pass


_schema_ready = False
_schema_lock = Lock()


def _to_vector_literal(values: list[float]) -> str:
    if not values:
        raise ValueError("Embedding cannot be empty.")

    return "[" + ",".join(str(float(value)) for value in values) + "]"


def _normalize_metadata(raw_metadata: Any) -> dict[str, Any]:
    if raw_metadata is None:
        return {}

    if isinstance(raw_metadata, dict):
        return raw_metadata

    if isinstance(raw_metadata, str):
        try:
            parsed = json.loads(raw_metadata)
        except json.JSONDecodeError:
            return {}

        if isinstance(parsed, dict):
            return parsed

    return {}


async def _ensure_schema(connection: asyncpg.Connection) -> None:
    global _schema_ready

    if _schema_ready:
        return

    async with _schema_lock:
        if _schema_ready:
            return

        try:
            await connection.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            await connection.execute(
                """
                CREATE TABLE IF NOT EXISTS semantic_chunks (
                    chunk_id TEXT PRIMARY KEY,
                    content TEXT NOT NULL,
                    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
                    embedding vector NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
                );
                """
            )
        except Exception as exc:
            raise SemanticSearchStoreError(f"Failed to initialize pgvector schema: {exc}") from exc

        _schema_ready = True


async def _current_dimensions(connection: asyncpg.Connection) -> int | None:
    value = await connection.fetchval("SELECT vector_dims(embedding) FROM semantic_chunks LIMIT 1;")

    if value is None:
        return None

    return int(value)


async def upsert_semantic_chunk(payload: SemanticDocumentUpsertRequest) -> dict[str, Any]:
    if payload.embedding is not None:
        embedding = payload.embedding
        model = "manual-vector"
    else:
        embedding_result = await create_embeddings(
            EmbeddingRequest(
                input=[payload.content],
                input_type="document",
                truncate="END",
            )
        )
        embedding = embedding_result["embeddings"][0]
        model = embedding_result["model"]

    vector_literal = _to_vector_literal(embedding)
    dimensions = len(embedding)

    pool = await get_database_pool()

    async with pool.acquire() as connection:
        await _ensure_schema(connection)

        existing_dimensions = await _current_dimensions(connection)
        if existing_dimensions is not None and existing_dimensions != dimensions:
            raise ValueError(
                "Embedding dimensions mismatch. Existing rows use "
                f"{existing_dimensions}, but received {dimensions}."
            )

        try:
            await connection.execute(
                """
                INSERT INTO semantic_chunks (chunk_id, content, metadata, embedding, updated_at)
                VALUES ($1, $2, $3::jsonb, $4::vector, NOW())
                ON CONFLICT (chunk_id) DO UPDATE
                SET content = EXCLUDED.content,
                    metadata = EXCLUDED.metadata,
                    embedding = EXCLUDED.embedding,
                    updated_at = NOW();
                """,
                payload.id,
                payload.content,
                json.dumps(payload.metadata),
                vector_literal,
            )
        except Exception as exc:
            raise SemanticSearchStoreError(f"Failed to upsert semantic chunk: {exc}") from exc

    return {
        "id": payload.id,
        "model": model,
        "dimensions": dimensions,
    }


async def search_semantic_chunks(payload: SemanticSearchRequest) -> dict[str, Any]:
    if payload.query_embedding is not None:
        query_embedding = payload.query_embedding
        model = "manual-vector"
    else:
        query_text = payload.query or ""
        embedding_result = await create_embeddings(
            EmbeddingRequest(
                input=[query_text],
                input_type="query",
                truncate="END",
            )
        )
        query_embedding = embedding_result["embeddings"][0]
        model = embedding_result["model"]

    vector_literal = _to_vector_literal(query_embedding)
    query_dimensions = len(query_embedding)

    pool = await get_database_pool()
    async with pool.acquire() as connection:
        await _ensure_schema(connection)

        existing_dimensions = await _current_dimensions(connection)
        if existing_dimensions is not None and existing_dimensions != query_dimensions:
            raise ValueError(
                "Query embedding dimensions mismatch. Existing rows use "
                f"{existing_dimensions}, but received {query_dimensions}."
            )

        try:
            rows = await connection.fetch(
                """
                SELECT
                    chunk_id,
                    content,
                    metadata,
                    1 - (embedding <=> $1::vector) AS score
                FROM semantic_chunks
                ORDER BY embedding <=> $1::vector
                LIMIT $2;
                """,
                vector_literal,
                payload.top_k,
            )
        except Exception as exc:
            raise SemanticSearchStoreError(f"Failed to run semantic search: {exc}") from exc

    matches: list[dict[str, Any]] = []
    for row in rows:
        score_value = row["score"]
        score = float(score_value) if score_value is not None else 0.0
        matches.append(
            {
                "id": row["chunk_id"],
                "content": row["content"],
                "metadata": _normalize_metadata(row["metadata"]),
                "score": score,
            }
        )

    return {
        "model": model,
        "count": len(matches),
        "matches": matches,
    }
