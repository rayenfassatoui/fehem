from typing import Any

import httpx
from openai import AsyncOpenAI

from app.ai_schemas import ChatRequest, EmbeddingRequest, ImageRequest
from app.config import settings


class NvidiaConfigError(RuntimeError):
    pass


class NvidiaProviderError(RuntimeError):
    pass


def _resolve_api_key() -> str:
    if not settings.nvidia_api_key:
        raise NvidiaConfigError(
            "NVIDIA_API_KEY is missing. Set it in backend/.env for local runs or .env.docker for Docker runs."
        )

    return settings.nvidia_api_key


def _build_openai_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=_resolve_api_key(),
        base_url=settings.nvidia_openai_base_url,
    )


async def create_embeddings(payload: EmbeddingRequest) -> dict[str, Any]:
    model = payload.model or settings.nvidia_embedding_model
    client = _build_openai_client()

    try:
        response = await client.embeddings.create(
            input=payload.input,
            model=model,
            encoding_format=payload.encoding_format,
            extra_body={
                "modality": payload.modality,
                "input_type": payload.input_type,
                "truncate": payload.truncate,
            },
        )
    except Exception as exc:
        raise NvidiaProviderError(f"NVIDIA embeddings request failed: {exc}") from exc

    embeddings = [item.embedding for item in response.data]

    return {
        "model": model,
        "count": len(embeddings),
        "embeddings": embeddings,
    }


async def create_chat_completion(payload: ChatRequest) -> dict[str, str]:
    model = payload.model or settings.nvidia_chat_model
    client = _build_openai_client()

    messages: list[dict[str, str]] = []
    if payload.system:
        messages.append({"role": "system", "content": payload.system})
    messages.append({"role": "user", "content": payload.prompt})

    try:
        response = await client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=payload.temperature,
            max_tokens=payload.max_tokens,
        )
    except Exception as exc:
        raise NvidiaProviderError(f"NVIDIA chat request failed: {exc}") from exc

    output = ""
    if response.choices:
        output = response.choices[0].message.content or ""

    return {
        "model": model,
        "output": output,
    }


async def generate_image(payload: ImageRequest) -> dict[str, Any]:
    endpoint = settings.nvidia_image_endpoint
    model = endpoint.rsplit("/", maxsplit=1)[-1]

    headers = {
        "Authorization": f"Bearer {_resolve_api_key()}",
        "Accept": "application/json",
    }
    body = {
        "prompt": payload.prompt,
        "width": payload.width,
        "height": payload.height,
        "seed": payload.seed,
        "steps": payload.steps,
    }

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(endpoint, headers=headers, json=body)
            response.raise_for_status()
            result = response.json()
    except Exception as exc:
        raise NvidiaProviderError(f"NVIDIA image request failed: {exc}") from exc

    return {
        "model": model,
        "result": result,
    }
