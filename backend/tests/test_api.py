from httpx import ASGITransport, AsyncClient

from app.main import app


async def test_health_endpoint() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}


async def test_db_check_contract() -> None:
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.get("/api/db-check")

    assert response.status_code in {200, 503}

    body = response.json()
    assert "status" in body
    assert "database" in body
    assert "detail" in body
    assert body["database"] in {"connected", "disconnected"}
