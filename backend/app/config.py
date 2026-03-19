from typing import Optional

try:
    from pydantic_settings import BaseSettings
except ImportError:  # pragma: no cover - compatibility fallback
    try:
        from pydantic.v1 import BaseSettings
    except ImportError:  # pragma: no cover
        from pydantic import BaseSettings


class Settings(BaseSettings):
    llm_api_key: str = ""
    llm_base_url: str = "https://api.openai.com/v1"
    llm_model: str = "gpt-4o"

    amap_api_key: str = ""
    amap_web_key: str = ""
    amap_security_code: Optional[str] = None

    unsplash_access_key: str = ""

    backend_cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    frontend_amap_web_key: str = ""

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.backend_cors_origins.split(",") if origin.strip()]


settings = Settings()
