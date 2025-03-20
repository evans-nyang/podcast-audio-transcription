import os
import datetime
import requests
from pathlib import Path

# Read from the RSS Feed URL
import feedparser

def download_podcast_episode(rss_url, local_path="./content/audio"):
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
        requests.exceptions.RequestException: If the download request fails.
        KeyError: If the RSS feed does not contain expected fields (e.g., title, links).
    """
    
    print("Starting Podcast Transcription Function")
    print("Feed URL: ", rss_url)

    # Parse the RSS feed
    intelligence_feed = feedparser.parse(rss_url)
    podcast_title = intelligence_feed['feed']['title']
    episode_title = intelligence_feed.entries[0]['title']
    episode_image = intelligence_feed['feed']['image'].href

    # Extract the episode URL from the RSS feed
    for item in intelligence_feed.entries[0].links:
        if item['type'] == 'audio/mpeg':
            episode_url = item.href

    # Generate a unique filename for the episode
    episode_name = "podcast_episode_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp3"
    print("RSS URL read and episode URL: ", episode_url)

    # Ensure the local directory exists
    p = Path(local_path)
    p.mkdir(exist_ok=True)

    # Download the episode
    print("Downloading the podcast episode")
    with requests.get(episode_url, stream=True) as r:
        r.raise_for_status()
        episode_path = p.joinpath(episode_name)
        with open(episode_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("Podcast Episode downloaded")
    return episode_path, podcast_title, episode_title, episode_image
