"""
Video generation service using HeyGen API
"""

import requests
import asyncio
from config import settings
from typing import Optional

class VideoService:
    def __init__(self):
        self.api_key = settings.HEYGEN_API_KEY
        self.api_url = settings.HEYGEN_API_URL
    
    async def generate_video(self, script: str) -> Optional[str]:
        """Generate video using HeyGen API"""
        try:
            if not self.api_key:
                print("⚠️  HEYGEN_API_KEY not found")
                return None
            
            return await self._generate_with_heygen(script)
                
        except Exception as e:
            print(f"Video generation failed: {e}")
            return None
    
    async def _generate_with_heygen(self, script: str) -> Optional[str]:
        """Generate video using HeyGen API V2"""
        headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # HeyGen API V2 payload with hardcoded parameters
        data = {
            "caption": False,
            "dimension": {
                "width": 1280,
                "height": 720
            },
            "video_inputs": [
                {
                    "character": {
                        "type": "avatar",
                        "avatar_id": settings.HEYGEN_AVATAR_ID,
                        "scale": 1.0,
                        "avatar_style": "normal",
                        "offset": {
                            "x": 0.0,
                            "y": 0.0
                        }
                    },
                    "voice": {
                        "type": "text",
                        "voice_id": settings.HEYGEN_VOICE_ID,
                        "input_text": script,
                        "speed": 1.0,
                        "pitch": 0
                    },
                    "background": {
                        "type": "color",
                        "value": "#f6f6fc"
                    }
                }
            ]
        }
        
        print(f"🎬 Generating video with HeyGen V2 for script: {script[:100]}...")
        print(f"📏 Script length: {len(script)} characters")
        print(f"👤 Avatar ID: {settings.HEYGEN_AVATAR_ID}")
        print(f"🎤 Voice ID: {settings.HEYGEN_VOICE_ID}")
        
        # Create video using V2 endpoint
        response = requests.post(
            f"{self.api_url}/v2/video/generate", 
            headers=headers, 
            json=data
        )
        
        print(f"📡 HeyGen API Response: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔍 Full response: {result}")
            
            # Fix: Look for video_id in the correct location
            video_id = result.get("data", {}).get("video_id")
            
            if video_id:
                print(f"✅ Video creation started, ID: {video_id}")
                # Poll for completion
                return await self._wait_for_video_completion(video_id, headers)
            else:
                print(f"❌ No video_id in response: {result}")
                return None
        else:
            print(f"❌ HeyGen API error: {response.status_code} - {response.text}")
            return None
    
    async def _wait_for_video_completion(self, video_id: str, headers: dict) -> Optional[str]:
        """Poll HeyGen API until video is ready"""
        max_attempts = 180  # 30 minutes max
        attempt = 0
        
        print(f"⏳ Starting to poll for video completion: {video_id}")
        
        while attempt < max_attempts:
            try:
                print(f"🔄 Polling attempt {attempt + 1}/{max_attempts}")
                
                # Use V1 status endpoint
                response = requests.get(
                    f"{self.api_url}/v1/video_status.get?video_id={video_id}",
                    headers=headers
                )
                
                print(f"📡 Status check response: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"🔍 Status response: {result}")
                    
                    status = result.get("data", {}).get("status")
                    
                    if status == "completed":
                        video_url = result.get("data", {}).get("video_url")
                        print(f"✅ Video generation completed: {video_url}")
                        return video_url
                    elif status == "failed":
                        print(f"❌ Video generation failed: {result}")
                        return None
                    else:
                        print(f"⏳ Video status: {status}, waiting 10 seconds...")
                        await asyncio.sleep(10)  # Wait 10 seconds
                        attempt += 1
                else:
                    print(f"❌ Status check failed: {response.status_code} - {response.text}")
                    return None
                    
            except Exception as e:
                print(f"❌ Error checking video status: {e}")
                return None
        
        print("❌ Video generation timeout after 30 minutes")
        return None