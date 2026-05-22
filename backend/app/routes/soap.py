from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_nurse
from app.models.nurse import Nurse
from app.schemas.soap import SOAPNoteResponse, SOAPNoteEdit
from app.services import session_service, soap_service
from app.ai.soap_generator import SOAPGenerationError

router = APIRouter()


def _owned_session_or_404(db: Session, session_id: UUID, nurse: Nurse):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.nurse_id != str(nurse.id):
        raise HTTPException(status_code=403, detail="Access denied")
    return session


def _note_or_404(db: Session, session_id: UUID):
    note = soap_service.get_latest_note(db, session_id)
    if not note:
        raise HTTPException(status_code=404, detail="No SOAP note found for this session")
    return note


@router.post("/{session_id}/soap", response_model=SOAPNoteResponse, status_code=201)
def trigger_soap(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    session = _owned_session_or_404(db, session_id, current_nurse)
    if not session.raw_transcript:
        raise HTTPException(status_code=422, detail="No transcript available — add audio or text first")
    try:
        return soap_service.create_soap_note(db, session_id, session.raw_transcript)
    except SOAPGenerationError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/{session_id}/soap", response_model=SOAPNoteResponse)
def get_soap(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    _owned_session_or_404(db, session_id, current_nurse)
    return _note_or_404(db, session_id)


@router.patch("/{session_id}/soap", response_model=SOAPNoteResponse)
def edit_soap(
    session_id: UUID,
    edits: SOAPNoteEdit,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    _owned_session_or_404(db, session_id, current_nurse)
    note = _note_or_404(db, session_id)
    if note.submitted:
        raise HTTPException(status_code=409, detail="Cannot edit a submitted SOAP note")
    try:
        return soap_service.update_soap_note(db, note, edits.model_dump(exclude_none=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{session_id}/submit")
def submit_soap(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    _owned_session_or_404(db, session_id, current_nurse)
    note = _note_or_404(db, session_id)
    if note.submitted:
        raise HTTPException(status_code=409, detail="SOAP note already submitted")
    soap_service.submit_soap_note(db, note)
    return {"status": "submitted", "note_id": str(note.id)}
