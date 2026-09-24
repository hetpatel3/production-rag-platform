from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    groq_api_key: str  # it is compulsory to set this environment variable in your .env file else the application will not run.

    # below are the default values for the settings, you can override them in your .env file if needed.
    llm_model: str = "openai/gpt-oss-120b"
    embedding_model: str = "all-MiniLM-L6-v2"
    qdrant_url: str = "http://localhost:6333"
    collection_name: str = "rag_starter"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5


# Reading files from a hard drive is slow. The @lru_cache decorator ensures that Python reads the .env file exactly once. Every time your API asks for settings after that, it instantly hands over the copy stored in your system's RAM, keeping your RAG application running fast.
@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore
