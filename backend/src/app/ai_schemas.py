from typing import Any, Literal

from pydantic import BaseModel, Field


class EmbeddingRequest(BaseModel):
    input: list[str] = Field(min_length=1)
    model: str | None = None
    encoding_format: Literal["float", "base64"] = "float"
    modality: list[Literal["text", "image"]] = Field(default_factory=lambda: ["text"])
    input_type: Literal["query", "passage", "document"] = "query"
    truncate: Literal["NONE", "START", "END"] = "NONE"


class EmbeddingResponse(BaseModel):
    status: Literal["ok"] = "ok"
    model: str
    count: int
    embeddings: list[list[float]]


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)
    system: str | None = None
    model: str | None = None
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)
    max_tokens: int = Field(default=512, ge=1, le=4096)


class ChatResponse(BaseModel):
    status: Literal["ok"] = "ok"
    model: str
    output: str


class ImageRequest(BaseModel):
    prompt: str = Field(min_length=1)
    width: int = Field(default=1024, ge=256, le=2048)
    height: int = Field(default=1024, ge=256, le=2048)
    seed: int = 0
    steps: int = Field(default=4, ge=1, le=50)


class ImageResponse(BaseModel):
    status: Literal["ok"] = "ok"
    model: str
    result: dict[str, Any]
