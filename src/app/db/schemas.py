from pydantic import BaseModel

class PodcastEpisodeBase(BaseModel):
    podcast_title: str
    episode_title: str
    episode_image: str
    podcast_summary: str
    podcast_guest: dict
    podcast_highlights: str
    podcast_transcription: str

class PodcastEpisodeCreate(PodcastEpisodeBase):
    pass

class PodcastEpisode(PodcastEpisodeBase):
    id: int

    class Config:
        orm_mode = True
