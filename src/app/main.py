from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, crud, utils
from dependencies import get_db, engine  # Import the engine

app = FastAPI()

# Create database tables (run once)
@app.on_event("startup")
def startup():
    # Use the engine directly to create tables
    models.Base.metadata.create_all(bind=engine)

@app.post("/process-podcast/", response_model=schemas.PodcastEpisode)
def process_podcast(url: str, db: Session = Depends(get_db)):
    # Process the podcast
    episode_data = utils.process_podcast(url)

    # Save to database
    db_episode = crud.create_podcast_episode(db, episode_data)
    return db_episode

@app.get("/episodes/{episode_id}", response_model=schemas.PodcastEpisode)
def read_episode(episode_id: int, db: Session = Depends(get_db)):
    db_episode = crud.get_podcast_episode(db, episode_id)
    if db_episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    return db_episode
