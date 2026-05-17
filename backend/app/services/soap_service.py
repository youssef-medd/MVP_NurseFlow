from uuid import UUID
from sqlalchemy.orm import Session
from app.models.soap_note import SOAPNote
from app.ai.soap_generator import generate_soap_note, SOAPGenerationError


def get_latest_note(db: Session, session_id: UUID) -> SOAPNote | None:
    return (
        db.query(SOAPNote)
        .filter(SOAPNote.session_id == session_id)
        .order_by(SOAPNote.generated_at.desc())
        .first()
    )


def create_soap_note(db: Session, session_id: UUID, transcript: str) -> SOAPNote:
    result = generate_soap_note(transcript)
    note = SOAPNote(session_id=session_id, **result)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


_EDITABLE_FIELDS = {"subjective", "objective", "assessment", "plan"}


def update_soap_note(db: Session, note: SOAPNote, fields: dict) -> SOAPNote:
    unknown = set(fields) - _EDITABLE_FIELDS
    if unknown:
        raise ValueError(f"Cannot modify fields: {unknown}")
    for key, value in fields.items():
        setattr(note, key, value)
    db.commit()
    db.refresh(note)
    return note


def submit_soap_note(db: Session, note: SOAPNote) -> SOAPNote:
    note.reviewed = True
    note.submitted = True
    db.commit()
    db.refresh(note)
    return note
