# models.py - Updated version
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func, Table, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

# Association table for many-to-many relationship between episodes and tags
episode_tag_association = Table(
    'episode_tag_association',
    Base.metadata,
    Column('episode_id', Integer, ForeignKey('podcast_episodes.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Tag(Base):
    __tablename__ = 'tags'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    episodes = relationship("PodcastEpisode", secondary=episode_tag_association, back_populates="tags")

class Note(Base):
    __tablename__ = 'notes'
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())
    episode_id = Column(Integer, ForeignKey('podcast_episodes.id'))
    episode = relationship("PodcastEpisode", back_populates="notes")

class PodcastEpisode(Base):
    __tablename__ = "podcast_episodes"

    id = Column(Integer, primary_key=True, index=True)
    podcast_title = Column(String, nullable=False)
    episode_title = Column(String, nullable=False)
    episode_image = Column(String, nullable=False)
    podcast_summary = Column(JSON, nullable=False)
    podcast_guest = Column(JSON, nullable=False)
    podcast_highlights = Column(JSON, nullable=False)
    podcast_transcription = Column(Text, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    tags = relationship("Tag", secondary=episode_tag_association, back_populates="episodes")
    notes = relationship("Note", back_populates="episode")
