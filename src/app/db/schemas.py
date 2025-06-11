from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    
    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    text: str

class NoteCreate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True

# Update PodcastEpisode to include relationships
class PodcastEpisodeBase(BaseModel):
    podcast_title: str
    episode_title: str
    episode_image: str
    podcast_summary: dict
    podcast_guest: dict
    podcast_highlights: dict
    podcast_transcription: str

class PodcastEpisodeCreate(PodcastEpisodeBase):
    pass

class PodcastEpisode(PodcastEpisodeBase):
    id: int
    created_at: datetime
    tags: List[Tag] = []
    notes: List[Note] = []
    
    class Config:
        from_attributes = True
