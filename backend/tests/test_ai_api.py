from httpx import ASGITransport, AsyncClient

from app.main import app
from app.nvidia_ai import NvidiaConfigError


async def test_embeddings_endpoint_contract(monkeypatch) -> None:
    async def fake_create_embeddings(_payload):
        return {
            "model": "nvidia/llama-nemotron-embed-vl-1b-v2",
            "count": 1,
            "embeddings": [[0.11, 0.22, 0.33]],
        }

    monkeypatch.setattr("app.ai_routes.create_embeddings", fake_create_embeddings)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/embeddings",
            json={"input": ["What is Fehem?"]},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model"] == "nvidia/llama-nemotron-embed-vl-1b-v2"
    assert body["count"] == 1
    assert isinstance(body["embeddings"], list)


async def test_chat_endpoint_contract(monkeypatch) -> None:
    async def fake_create_chat_completion(_payload):
        return {
            "model": "stepfun-ai/step-3.5-flash",
            "output": "Fehem is connected.",
        }

    monkeypatch.setattr("app.ai_routes.create_chat_completion", fake_create_chat_completion)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/chat",
            json={"prompt": "Say hello"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model"] == "stepfun-ai/step-3.5-flash"
    assert body["output"] == "Fehem is connected."


async def test_image_endpoint_contract(monkeypatch) -> None:
    async def fake_generate_image(_payload):
        return {
            "model": "flux.2-klein-4b",
            "result": {"image": "base64-data"},
        }

    monkeypatch.setattr("app.ai_routes.generate_image", fake_generate_image)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/image",
            json={"prompt": "Generate logo name's fehem"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model"] == "flux.2-klein-4b"
    assert "result" in body


async def test_embeddings_returns_503_when_api_key_missing(monkeypatch) -> None:
    async def fake_create_embeddings(_payload):
        raise NvidiaConfigError("NVIDIA_API_KEY is missing. Set it in backend/.env.")

    monkeypatch.setattr("app.ai_routes.create_embeddings", fake_create_embeddings)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/embeddings",
            json={"input": ["hello"]},
        )

    assert response.status_code == 503
    assert "NVIDIA_API_KEY" in response.json()["detail"]


async def test_semantic_documents_endpoint_contract(monkeypatch) -> None:
    async def fake_upsert_semantic_chunk(_payload):
        return {
            "id": "chunk-intro",
            "model": "manual-vector",
            "dimensions": 3,
        }

    monkeypatch.setattr("app.ai_routes.upsert_semantic_chunk", fake_upsert_semantic_chunk)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/semantic-documents",
            json={
                "id": "chunk-intro",
                "content": "Fehem helps students study with AI.",
                "embedding": [0.11, 0.22, 0.33],
                "metadata": {"course": "intro"},
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["id"] == "chunk-intro"
    assert body["model"] == "manual-vector"
    assert body["dimensions"] == 3


async def test_semantic_search_endpoint_contract(monkeypatch) -> None:
    async def fake_search_semantic_chunks(_payload):
        return {
            "model": "manual-vector",
            "count": 1,
            "matches": [
                {
                    "id": "chunk-intro",
                    "content": "Fehem helps students study with AI.",
                    "metadata": {"course": "intro"},
                    "score": 0.998,
                }
            ],
        }

    monkeypatch.setattr("app.ai_routes.search_semantic_chunks", fake_search_semantic_chunks)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/semantic-search",
            json={
                "query_embedding": [0.11, 0.22, 0.33],
                "top_k": 3,
            },
        )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["model"] == "manual-vector"
    assert body["count"] == 1
    assert body["matches"][0]["id"] == "chunk-intro"


async def test_semantic_search_returns_400_on_dimension_mismatch(monkeypatch) -> None:
    async def fake_search_semantic_chunks(_payload):
        raise ValueError("Embedding dimensions mismatch.")

    monkeypatch.setattr("app.ai_routes.search_semantic_chunks", fake_search_semantic_chunks)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/semantic-search",
            json={
                "query_embedding": [0.11, 0.22, 0.33],
                "top_k": 3,
            },
        )

    assert response.status_code == 400
    assert "dimensions" in response.json()["detail"].lower()
