from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.ai_routes import router as ai_router
from app.config import settings
from app.db import connect_database, disconnect_database, ping_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    await connect_database()
    yield
    await disconnect_database()


app = FastAPI(
    title="Fehem Backend",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai_router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "backend"}


@app.get("/api/db-check", response_model=None)
async def db_check():
    connected, detail = await ping_database()

    if connected:
        return {
            "status": "ok",
            "database": "connected",
            "detail": detail,
        }

    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "status": "error",
            "database": "disconnected",
            "detail": detail,
        },
    )
