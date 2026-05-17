import anthropic
from app.core.config import settings

_client: anthropic.Anthropic | None = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
    return _client


def complete(system: str, user: str, prefill: str = "", max_tokens: int = 1024) -> str:
    messages: list[dict] = [{"role": "user", "content": user}]
    if prefill:
        messages.append({"role": "assistant", "content": prefill})
    message = _get_client().messages.create(
        model=settings.claude_model,
        max_tokens=max_tokens,
        system=system,
        messages=messages,
    )
    if not message.content or message.content[0].type != "text":
        raise RuntimeError("Unexpected response format from Claude API")
    return message.content[0].text
