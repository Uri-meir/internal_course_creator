"""
Video generation service using external APIs
"""

import requests
import json
from config import settings
from typing import Optional

class VideoService:
    def __init__(self):
        self.api_key = settings.HEYGEN_API_KEY
        self.api_url = settings.HEYGEN_API_URL
    
    async def generate_video(self, script: str) -> str:
        """Generate video using HeyGen API"""
        try:
            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "script": script,
                "voice": "en-US-female",
                "avatar": "professional",
                "background": "office"
            }
            
            # Make API call
            response = requests.post(
                f"{self.api_url}/v1/video/generate",
                headers=headers,
                json=payload,
                timeout=300
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("video_url", "")
            else:
                print(f"Video generation failed: {response.status_code} - {response.text}")
                return ""
                
        except Exception as e:
            print(f"Error generating video: {e}")
            return ""
