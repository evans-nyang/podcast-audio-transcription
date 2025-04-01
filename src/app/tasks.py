import os
from celery import Celery

# Get Redis URL from environment variables
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/0")

celery = Celery(
    "tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

celery.conf.update(
    task_routes={
        "tasks.process_podcast_task": {"queue": "podcast_queue"},
    }
)

@celery.task(name="tasks.process_podcast_task")
def process_podcast_task(url):
    """Background task for processing a podcast"""
    from services.utils import process_podcast
    from db.database import SessionLocal
    from db.crud import create_podcast_episode
    from db.schemas import PodcastEpisodeCreate

    try:
        session = SessionLocal()
        
        # Process the podcast
        episode_data = process_podcast(url)

        # Convert to Pydantic model
        episode_model = PodcastEpisodeCreate(**episode_data)

        # Save to database
        create_podcast_episode(session, episode_model)

        session.close()

        return {"message": f"Podcast {url} processed successfully!"}

    except Exception as e:
        return {"error": str(e)}
