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
