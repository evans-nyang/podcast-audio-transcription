from fastapi import APIRouter, UploadFile, Depends
from sqlalchemy.orm import Session
from services.transcriber import transcribe_audio
from db.database import get_db
from db.crud import save_podcast

router = APIRouter()

@router.post("/transcribe/")
async def transcribe_podcast(file: UploadFile, db: Session = Depends(get_db)):
    """Transcribes an uploaded audio file and saves it."""
    transcription = transcribe_audio(file)
    podcast = save_podcast(db, transcription)
    return {"id": podcast.id, "transcription": transcription}
