import os
import datetime
import requests
from pathlib import Path
import feedparser
from typing import Tuple, Optional

def download_podcast_episode(rss_url: str, local_path: str = "./content/audio") -> Tuple[Path, str, str, str]:
    """
    Downloads the latest podcast episode from an RSS feed URL and saves it locally.

    Args:
        rss_url (str): The URL of the RSS feed containing the podcast episode.
        local_path (str, optional): The local directory path where the episode will be saved. 
                                   Defaults to "./content/audio".

    Returns:
        tuple: A tuple containing:
            - episode_path (Path): The file path where the episode is saved.
            - podcast_title (str): The title of the podcast.
            - episode_title (str): The title of the downloaded episode.
            - episode_image (str): The URL of the podcast's cover image.

    Raises:
        ValueError: If the RSS feed is invalid or doesn't contain episodes.
        requests.exceptions.RequestException: If the download request fails.
    """
    print("Starting Podcast Transcription Function")
    print("Feed URL: ", rss_url)

    # Parse the RSS feed with error handling
    try:
        feed = feedparser.parse(rss_url)
        
        # Check if feed parsing was successful
        if feed.bozo:
            raise ValueError(f"Invalid RSS feed: {feed.bozo_exception}")
            
        # Check if feed contains entries
        if not feed.entries:
            raise ValueError("No podcast episodes found in the RSS feed")
            
        print(f"Found {len(feed.entries)} episodes in the feed")

        # Get feed metadata with fallbacks
        podcast_title = feed.feed.get('title', 'Unknown Podcast')
        episode_title = feed.entries[0].get('title', 'Untitled Episode')
        
        # Get image with multiple fallback options
        episode_image = "No Image"
        if hasattr(feed.feed, 'image') and hasattr(feed.feed.image, 'href'):
            episode_image = feed.feed.image.href
        elif hasattr(feed.feed, 'artwork_url'):
            episode_image = feed.feed.artwork_url
        elif hasattr(feed.entries[0], 'image'):
            episode_image = feed.entries[0].image.get('href', 'No Image')

        # Find the first audio link
        episode_url = None
        for item in feed.entries[0].links:
            if item.get('type', '').startswith('audio/'):
                episode_url = item.href
                break
                
        if not episode_url:
            raise ValueError("No audio link found in the podcast episode")

        print(f"Selected episode: {episode_title}")
        print(f"Audio URL: {episode_url}")

        # Generate a unique filename for the episode
        episode_name = f"podcast_episode_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"

        # Ensure the local directory exists
        p = Path(local_path)
        p.mkdir(parents=True, exist_ok=True)

        # Download the episode with streaming
        print("Downloading the podcast episode")
        with requests.get(episode_url, stream=True, timeout=30) as r:
            r.raise_for_status()
            episode_path = p / episode_name
            with open(episode_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:  # filter out keep-alive chunks
                        f.write(chunk)

        print("Podcast Episode downloaded successfully")
        return episode_path, podcast_title, episode_title, episode_image

    except Exception as e:
        print(f"Error downloading podcast: {str(e)}")
        raise
