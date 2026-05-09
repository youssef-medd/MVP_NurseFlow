from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_nurse
from app.models.nurse import Nurse
from app.schemas.session import SessionCreate, SessionResponse, TranscriptUpdate
from app.services import session_service

router = APIRouter()


@router.post("", response_model=SessionResponse, status_code=201)
def create_session(
    data: SessionCreate,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    return session_service.create_session(db, data, nurse_id=str(current_nurse.id))


@router.get("/{session_id}", response_model=SessionResponse)
def get_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.nurse_id != str(current_nurse.id):
        raise HTTPException(status_code=403, detail="Access denied")
    return session


@router.delete("/{session_id}", response_model=SessionResponse)
def close_session(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.nurse_id != str(current_nurse.id):
        raise HTTPException(status_code=403, detail="Access denied")
    return session_service.close_session(db, session_id)


@router.post("/{session_id}/transcript")
def append_transcript(
    session_id: UUID,
    body: TranscriptUpdate,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.nurse_id != str(current_nurse.id):
        raise HTTPException(status_code=403, detail="Access denied")
    session_service.append_transcript(db, session_id, body.text)
    return {"status": "ok", "session_id": str(session_id)}


@router.get("/{session_id}/transcript")
def get_transcript(
    session_id: UUID,
    db: Session = Depends(get_db),
    current_nurse: Nurse = Depends(get_current_nurse),
):
    session = session_service.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.nurse_id != str(current_nurse.id):
        raise HTTPException(status_code=403, detail="Access denied")
    return {"session_id": str(session_id), "transcript": session.raw_transcript or ""}
