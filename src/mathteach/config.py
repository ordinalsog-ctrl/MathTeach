from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MathTeach API"
    environment: str = "development"
    session_store_dir: str | None = None
    calibration_store_path: str | None = None
    calibration_autosave_threshold: int = 10
    primary_reasoner_model: str = "gpt-5.4"
    fast_path_model: str = "gpt-5.4-mini"
    ingestion_model: str = "gemini-2.5-pro"
    verifier_model: str = "claude-opus-4-6"
    embeddings_model: str = "text-embedding-3-large"

    model_config = SettingsConfigDict(
        env_prefix="MATHTEACH_",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
