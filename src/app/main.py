import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db.schemas import PodcastEpisodeCreate, PodcastEpisode
from db.crud import create_podcast_episode, get_podcast_episode
# from services.utils import process_podcast
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
            existing_tables = connection.dialect.has_table(connection, "podcast_episodes") 
            
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


@app.get("/episodes/{episode_id}", response_model=PodcastEpisode)
def read_episode(episode_id: int, db: Session = Depends(get_db)):
    db_episode = get_podcast_episode(db, episode_id)

    if db_episode is None:
        raise HTTPException(status_code=404, detail="Episode not found")
    return db_episode
