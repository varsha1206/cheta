"""
YouTubeFetcher class to fetch latest videos from specified channels and get personalized recommendations using Gemini.
"""

import json
import os
import time

import requests
from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field
import logging

logging.basicConfig()
logger = logging.getLogger(__name__)

load_dotenv()  # Load environment variables from .env file


class TopVideo(BaseModel):
    title: str = Field(..., description="Title of the recommended video")
    url: str = Field(..., description="URL of the recommended video")
    reason: str = Field(..., description="Reason for recommendation")


class YouTubeFetcher(BaseModel):
    yt_api_key: str = Field(
        default_factory=lambda: os.getenv("YT_API_KEY"),
        description="YouTube Data API key",
    )
    gemini_api_key: str = Field(
        default_factory=lambda: os.getenv("GEMINI_API_KEY"),
        description="Gemini API key",
    )
    gemini_model: str = Field(
        default="gemini-2.5-flash", description="Gemini model name"
    )
    config: dict = Field(default={}, description="Configuration loaded from JSON file")

    def load_config(self, config_path="src/cheta/config.json") -> None:
        """Load configuration from a JSON file."""
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def fetch_latest_videos(self, channel_id, max_results=5) -> list | None:
        """
        Fetch latest videos from a YouTube channel.
        """
        url = (
            "https://www.googleapis.com/youtube/v3/search"
            f"?key={self.yt_api_key}"
            f"&channelId={channel_id}"
            "&part=snippet"
            "&order=date"
            f"&maxResults={max_results}"
        )
        response = requests.get(url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch videos for channel {channel_id}: {response.text}")
            return None
        
        res = response.json()
        videos = []

        for item in res.get("items", []):
            if item["id"].get("videoId"):
                videos.append(
                    {
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    }
                )
        return videos

    def create_prompt(self, videos, preferences) -> str:
        """Create a prompt for Gemini based on the videos and user preferences."""
        prompt = "You are a personal recommendation assistant.\n"
        prompt += f"My preferences: {preferences}\n\n"
        prompt += (
            "Rate these reaction videos and select the one I am most likely to enjoy.\n"
        )
        prompt += "Return your answer in valid JSON format:\n"
        prompt += """{
                    "top_video": {
                        "title": "...",
                        "url": "...",
                        "reason": "..."
                    }
                    }"""
        for idx, vid in enumerate(videos):
            prompt += f"\n{idx + 1}. Title: {vid['title']}\n"
            prompt += f"Description: {vid['description']}\n"
            prompt += f"URL: {vid['url']}\n"
        return prompt

    def recommend_video(self, videos, preferences) -> TopVideo:
        """
        Call Gemini via genai client and get top video recommendation.
        Returns a TopVideo object with title, url, and reason for recommendation.
        """
        prompt_text = self.create_prompt(videos, preferences)
        client = genai.Client()

        response = client.models.generate_content(
            model=self.gemini_model,
            contents=prompt_text,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": TopVideo.model_json_schema(),
            },
        )
        print("Gemini response:", response.text)
        top_video = TopVideo.model_validate_json(response.text)
        return top_video

    def get_recommendation(self) -> dict:
        """Main method to get top video recommendation."""
        self.load_config()
        all_videos = []
        for channel in self.config["channels"]:
            videos = self.fetch_latest_videos(channel)
            time.sleep(1)  # To avoid hitting API rate limits
            if videos:
                all_videos.extend(videos)
    
        if not all_videos:
            logger.warning("No videos fetched from any channel.")
            raise ValueError("No videos fetched from any channel.")
        
        logger.info(f"Fetched {len(all_videos)} videos from channels.")
        recommendation = self.recommend_video(all_videos, self.config["preferences"])

        if recommendation.url not in [vid["url"] for vid in all_videos]:
            logger.warning("Recommended video is not in the fetched videos list.")
            top_video = {
                "title": all_videos[0]["title"],
                "url": all_videos[0]["url"], 
                "reason": "Recommended video was not in the fetched list, so returning the most recent video.",
            }
        else:
            top_video = {
                "title": recommendation.title,
                "url": recommendation.url,
                "reason": recommendation.reason,
            }
        logger.info(f"Top recommendation: {top_video['title']} - {top_video['url']}")
        return top_video
