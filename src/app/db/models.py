from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from .database import Base

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

    