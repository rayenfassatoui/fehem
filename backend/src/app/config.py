from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    frontend_origin: str = "http://localhost:3000"
    nvidia_api_key: str | None = None
    nvidia_openai_base_url: str = "https://integrate.api.nvidia.com/v1"
    nvidia_embedding_model: str = "nvidia/llama-nemotron-embed-vl-1b-v2"
    nvidia_chat_model: str = "stepfun-ai/step-3.5-flash"
    nvidia_image_endpoint: str = (
        "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.2-klein-4b"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
