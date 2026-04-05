from fastapi import APIRouter, HTTPException, status

from app.ai_schemas import (
    ChatRequest,
    ChatResponse,
    EmbeddingRequest,
    EmbeddingResponse,
    ImageRequest,
    ImageResponse,
)
from app.nvidia_ai import (
    NvidiaConfigError,
    NvidiaProviderError,
    create_chat_completion,
    create_embeddings,
    generate_image,
)

router = APIRouter(prefix="/api/ai", tags=["ai"])


@router.post("/embeddings", response_model=EmbeddingResponse)
async def embeddings(payload: EmbeddingRequest) -> EmbeddingResponse:
    try:
        result = await create_embeddings(payload)
    except NvidiaConfigError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except NvidiaProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return EmbeddingResponse(status="ok", **result)


@router.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest) -> ChatResponse:
    try:
        result = await create_chat_completion(payload)
    except NvidiaConfigError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except NvidiaProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return ChatResponse(status="ok", **result)


@router.post("/image", response_model=ImageResponse)
async def image(payload: ImageRequest) -> ImageResponse:
    try:
        result = await generate_image(payload)
    except NvidiaConfigError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except NvidiaProviderError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc

    return ImageResponse(status="ok", **result)
