from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_INSECURE_JWT_DEFAULTS = {"change-this", "secret", ""}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://postgres:password@localhost:5432/nurseflow"
    anthropic_api_key: str = ""
    jwt_secret: str = "change-this"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    claude_model: str = "claude-sonnet-4-6"
    soap_max_tokens: int = 2048

    @model_validator(mode="after")
    def _require_strong_jwt_secret(self) -> "Settings":
        if self.jwt_secret in _INSECURE_JWT_DEFAULTS or len(self.jwt_secret) < 32:
            raise ValueError(
                "JWT_SECRET must be set to a random string of at least 32 characters. "
                "Set it in your .env file."
            )
        return self


settings = Settings()
