import json
from app.ai.claude_client import complete
from app.ai.prompts import SOAP_SYSTEM_PROMPT, build_soap_user_prompt
from app.core.config import settings


class SOAPGenerationError(Exception):
    pass


def generate_soap_note(transcript: str) -> dict:
    if not transcript or not transcript.strip():
        raise SOAPGenerationError("Transcript is empty — cannot generate SOAP note.")

    raw = complete(
        system=SOAP_SYSTEM_PROMPT,
        user=build_soap_user_prompt(transcript),
        max_tokens=settings.soap_max_tokens,
    )

    try:
        # Strip markdown code fences if Claude wraps the JSON
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        note = json.loads(cleaned)
    except (json.JSONDecodeError, IndexError) as e:
        raise SOAPGenerationError(f"Failed to parse Claude response as JSON: {e}\nRaw: {raw}")

    required = {"subjective", "objective", "assessment", "plan"}
    missing = required - note.keys()
    if missing:
        raise SOAPGenerationError(f"SOAP response missing fields: {missing}")

    return note
