import anthropic
from app.core.config import settings


def get_claude_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=settings.anthropic_api_key)


def complete(system: str, user: str, max_tokens: int = 1024) -> str:
    client = get_claude_client()
    message = client.messages.create(
        model=settings.claude_model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return message.content[0].text
