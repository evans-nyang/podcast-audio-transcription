from fastapi import APIRouter, UploadFile, File, Depends
from services.transcriber import transcribe_audio
from services.summarizer import summarize_text
from services.downloader import download_podcast
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/upload/")
def upload_podcast(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a podcast file and process transcription & summarization."""
    transcript = transcribe_audio(file)
    summary = summarize_text(transcript)
    return {"transcript": transcript, "summary": summary}

@router.post("/download/")
def download_podcast_endpoint(url: str, db: Session = Depends(get_db)):
    """Download a podcast from a given URL, transcribe, and summarize it."""
    audio_path = download_podcast(url)
    transcript = transcribe_audio(audio_path)
    summary = summarize_text(transcript)
    return {"transcript": transcript, "summary": summary}
