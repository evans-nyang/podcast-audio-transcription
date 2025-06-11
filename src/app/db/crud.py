from sqlalchemy.orm import Session
from typing import List
from .models import PodcastEpisode, Tag, Note
from .schemas import PodcastEpisodeCreate, TagCreate, NoteCreate

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

def get_all_tags(db: Session):
    """Retrieves all tags."""
    return db.query(Tag).all()

def add_episode_tags(db: Session, episode_id: int, tags: List[str]):
    episode = db.query(PodcastEpisode).filter(PodcastEpisode.id == episode_id).first()
    if not episode:
        return None
    
    for tag_name in tags:
        # Check if tag exists
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            # Create new tag
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()
            db.refresh(tag)
        
        # Add relationship if not exists
        if tag not in episode.tags:
            episode.tags.append(tag)
    
    db.commit()
    db.refresh(episode)
    return episode

def create_note(db: Session, note: NoteCreate, episode_id: int):
    db_note = Note(
        text=note.text,
        episode_id=episode_id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

def get_episode_notes(db: Session, episode_id: int):
    return db.query(Note).filter(Note.episode_id == episode_id).all()

def delete_note(db: Session, note_id: int):
    note = db.query(Note).filter(Note.id == note_id).first()
    if note:
        db.delete(note)
        db.commit()
        return True
    return False
