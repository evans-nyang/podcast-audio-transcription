import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models, schemas, crud, utils
from dependencies import get_db, engine


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Checking database tables...")
        with engine.connect() as connection:
            existing_tables = connection.dialect.has_table(connection, "podcast_episodes") 
            
            if not existing_tables:
                logger.info("Database tables not found. Initializing database...")
                models.Base.metadata.create_all(bind=engine)
                logger.info("Database initialized successfully")
            else:
                logger.info("Database already initialized. Skipping table creation.")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise HTTPException(status_code=500, detail="Database initialization failed")

    yield 

app = FastAPI(lifespan=lifespan)

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
