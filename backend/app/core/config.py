from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str = "postgresql://postgres:password@localhost:5432/nurseflow"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    jwt_secret: str = "change-this"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    claude_model: str = "claude-sonnet-4-6"
    soap_max_tokens: int = 2048


settings = Settings()
