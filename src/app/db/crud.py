from sqlalchemy.orm import Session
from .models import PodcastEpisode
from .schemas import PodcastEpisodeCreate

def create_podcast_episode(db: Session, episode: PodcastEpisodeCreate):
    db_episode = PodcastEpisode(**episode.model_dump())
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode

def get_podcast_episode(db: Session, episode_id: int):
    return db.query(PodcastEpisode).filter(PodcastEpisode.id == episode_id).first()

def get_all_podcasts(db: Session):
    """Retrieves all podcasts."""
    return db.query(PodcastEpisode).all()
