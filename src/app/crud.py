from sqlalchemy.orm import Session
import models, schemas

def create_podcast_episode(db: Session, episode: schemas.PodcastEpisodeCreate):
    db_episode = models.PodcastEpisode(**episode.model_dump())
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode

def get_podcast_episode(db: Session, episode_id: int):
    return db.query(models.PodcastEpisode).filter(models.PodcastEpisode.id == episode_id).first()
