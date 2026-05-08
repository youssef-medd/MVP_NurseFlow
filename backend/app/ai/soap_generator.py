import json
from app.ai.claude_client import complete
from app.ai.prompts import SOAP_SYSTEM_PROMPT, SOAP_JSON_PREFILL, build_soap_user_prompt
from app.core.config import settings

SOAP_FIELDS = {"subjective", "objective", "assessment", "plan"}


class SOAPGenerationError(Exception):
    pass


def generate_soap_note(transcript: str) -> dict:
    if not transcript.strip():
        raise SOAPGenerationError("Transcript is empty — cannot generate SOAP note.")

    raw = complete(
        system=SOAP_SYSTEM_PROMPT,
        user=build_soap_user_prompt(transcript),
        prefill=SOAP_JSON_PREFILL,
        max_tokens=settings.soap_max_tokens,
    )

    try:
        note = json.loads(SOAP_JSON_PREFILL + raw)
    except json.JSONDecodeError as e:
        raise SOAPGenerationError(f"Failed to parse Claude response as JSON: {e}\nRaw: {raw}")

    missing = SOAP_FIELDS - note.keys()
    if missing:
        raise SOAPGenerationError(f"SOAP response missing fields: {missing}")

    return note
