from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.soap import SOAPNoteResponse, SOAPNoteEdit
from app.services import session_service
from app.ai.soap_generator import generate_soap_note, SOAPGenerationError
from app.models.soap_note import SOAPNote

router = APIRouter()


def _get_note_or_404(db: Session, session_id: UUID) -> SOAPNote:
    note = db.query(SOAPNote).filter(SOAPNote.session_id == session_id).order_by(SOAPNote.generated_at.desc()).first()
    if not note:
        raise HTTPException(status_code=404, detail="No SOAP note found for this session")
    return note


@router.post("/{session_id}/soap", response_model=SOAPNoteResponse, status_code=201)
def trigger_soap(session_id: UUID, db: Session = Depends(get_db)):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.raw_transcript:
        raise HTTPException(status_code=422, detail="No transcript available — add audio or text first")

    try:
        result = generate_soap_note(session.raw_transcript)
    except SOAPGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))

    note = SOAPNote(
        session_id=session_id,
        subjective=result["subjective"],
        objective=result["objective"],
        assessment=result["assessment"],
        plan=result["plan"],
    )
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get("/{session_id}/soap", response_model=SOAPNoteResponse)
def get_soap(session_id: UUID, db: Session = Depends(get_db)):
    return _get_note_or_404(db, session_id)


@router.patch("/{session_id}/soap", response_model=SOAPNoteResponse)
def edit_soap(session_id: UUID, edits: SOAPNoteEdit, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, session_id)
    for field, value in edits.model_dump(exclude_none=True).items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


@router.post("/{session_id}/submit")
def submit_soap(session_id: UUID, db: Session = Depends(get_db)):
    note = _get_note_or_404(db, session_id)
    note.reviewed = True
    note.submitted = True
    db.commit()
    return {"status": "submitted", "note_id": str(note.id)}
