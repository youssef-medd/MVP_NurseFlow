from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/nurseflow"
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    jwt_secret: str = "change-this"
    environment: str = "development"

    # Claude model to use for SOAP generation
    claude_model: str = "claude-sonnet-4-6"

    # Max tokens for SOAP note output
    soap_max_tokens: int = 2048

    class Config:
        env_file = ".env"


settings = Settings()
