import logging
from contextlib import asynccontextmanager
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.schemas import (
    PodcastEpisodeCreate, 
    PodcastEpisode,
    Tag,
    NoteCreate,
    Note
)
from db.crud import (
    create_podcast_episode,
    get_podcast_episode,
    get_all_podcasts,
    get_all_tags,
    add_episode_tags,
    create_note,
    get_episode_notes,
    delete_note
)
from services import utils
from db.database import get_db, engine, Base

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Checking database tables...")
        with engine.connect() as connection:
            # Check for all required tables
            required_tables = ["podcast_episodes", "tags", "notes", "episode_tag_association"]
            existing_tables = all(connection.dialect.has_table(connection, table) for table in required_tables)
            
            if not existing_tables:
                logger.info("Database tables not found. Initializing database...")
                Base.metadata.create_all(bind=engine)
                logger.info("Database initialized successfully")
            else:
                logger.info("Database already initialized. Skipping table creation.")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise HTTPException(status_code=500, detail="Database initialization failed")

    yield 

app = FastAPI(lifespan=lifespan, title="Podcast Transcriber API", version="1.0.1")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to the Podcast Transcriber API"}

@app.post("/process-podcast/", response_model=PodcastEpisode)
def process_podcast(url: str, db: Session = Depends(get_db)):
    # Process the podcast
    episode_data = utils.process_podcast(url)

    # Convert dict to Pydantic model
    episode_model = PodcastEpisodeCreate(**episode_data)

    # Save to database
    db_episode = create_podcast_episode(db, episode_model)
    return db_episode

@app.get("/episodes/", response_model=List[PodcastEpisode])
def read_episodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    episodes_query = get_all_podcasts(db)
    episodes = episodes_query[skip:skip + limit]
    return episodes

@app.get("/episodes/{episode_id}", response_model=PodcastEpisode)
def read_episode(episode_id: int, db: Session = Depends(get_db)):
    db_episode = get_podcast_episode(db, episode_id)
    if db_episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    return db_episode

@app.post("/episodes/{episode_id}/tags", response_model=PodcastEpisode)
def update_episode_tags(
    episode_id: int, 
    tags: List[str],
    db: Session = Depends(get_db)
):
    updated_episode = add_episode_tags(db, episode_id, tags)
    if not updated_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return updated_episode

@app.get("/tags/", response_model=List[Tag])
def read_tags(db: Session = Depends(get_db)):
    return get_all_tags(db)

@app.post("/episodes/{episode_id}/notes", response_model=Note)
def create_episode_note(
    episode_id: int,
    note: NoteCreate,
    db: Session = Depends(get_db)
):
    db_episode = get_podcast_episode(db, episode_id)
    if not db_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    
    return create_note(db, note, episode_id)

@app.get("/episodes/{episode_id}/notes", response_model=List[Note])
def read_episode_notes(episode_id: int, db: Session = Depends(get_db)):
    return get_episode_notes(db, episode_id)

@app.delete("/notes/{note_id}")
def remove_note(note_id: int, db: Session = Depends(get_db)):
    success = delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
