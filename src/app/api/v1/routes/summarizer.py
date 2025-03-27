from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from services.summarizer import get_podcast_summary
from db.database import get_db
from db.crud import save_podcast, get_podcast

router = APIRouter()

class TranscriptionInput(BaseModel):
    transcription: str
    podcast_id: int

@router.post("/summarize/")
async def summarize_podcast(data: TranscriptionInput, db: Session = Depends(get_db)):
    """Summarizes transcription and saves to DB."""
    summary = get_podcast_summary(data.transcription)
    
    # Update podcast record with summary
    podcast = get_podcast(db, data.podcast_id)
    if podcast:
        podcast.summary = summary
        db.commit()
    
    return {"id": data.podcast_id, "summary": summary}
