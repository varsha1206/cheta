"""
GUI module for Cheta, providing a simple interface to access features like YouTube recommendations.
"""

import webbrowser

from .youtube.youtube_fetcher import YouTubeFetcher

import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

def get_reactions() -> None:
    """
    Fetch personalized YouTube video recommendations and open the top recommendation in the web browser.
    """
    yt_fetcher = YouTubeFetcher()
    top_video = yt_fetcher.get_recommendation()

    if not top_video:
        logger.warning("No recommendations available.")
        return
    
    url = top_video["url"]
    logger.info(f"Opening URL: {url}")
    webbrowser.open(url)