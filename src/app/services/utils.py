from .downloader import download_podcast_episode
from .transcriber import transcribe_podcast_episode
from .summarizer import get_podcast_summary, get_podcast_highlights, get_podcast_guest


def process_podcast(url: str) -> dict:
    """
    Processes a podcast episode by downloading, transcribing, and analyzing it.

    Args:
        url (str): The RSS feed URL of the podcast.

    Returns:
        dict: A dictionary containing the podcast title, episode title, episode image,
              summary, guest information, highlights, and full transcript.
    """
    output = {}
    podcast_episode_path, podcast_title, episode_title, episode_image = download_podcast_episode(url)
    podcast_transcription = transcribe_podcast_episode(podcast_episode_path)
    podcast_summary = get_podcast_summary(podcast_transcription)
    podcast_guest = get_podcast_guest(podcast_transcription)
    podcast_highlights = get_podcast_highlights(podcast_transcription)

    output['podcast_title'] = podcast_title
    output['episode_title'] = episode_title
    output['episode_image'] = episode_image
    output['podcast_summary'] = podcast_summary
    output['podcast_guest'] = podcast_guest
    output['podcast_highlights'] = podcast_highlights
    output['podcast_transcription'] = podcast_transcription
    
    return output
