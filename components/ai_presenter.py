"""
AI Presenter Component
Generates AI presenter videos using D-ID API
"""

import os
import time
import requests
import json
import logging
from typing import Dict, List, Any, Optional
from mocks.mock_clients import MockDIDClient, create_mock_video_file

logger = logging.getLogger(__name__)

class AIPresenter:
    """
    Generates AI presenter videos using D-ID API
    """
    
    def __init__(self, did_api_key: str, test_mode: bool = False):
        """Initialize with D-ID API key and test mode flag"""
        self.test_mode = test_mode
        self.did_api_key = did_api_key
        
        if self.test_mode:
            logger.info("Using mock D-ID client for testing")
            self.client = MockDIDClient(did_api_key)
        else:
            self.client = None  # Will use requests directly for D-ID API
        
        # D-ID API configuration
        self.api_url = "https://api.d-id.com"
        self.headers = {
            "Authorization": f"Basic {did_api_key}",
            "Content-Type": "application/json"
        }
        
        # Presenter configuration
        self.presenter_id = "amy-Aq6r0S0Vg"  # Professional female presenter
        self.voice_id = "en-US-JennyNeural"  # Natural English voice
        self.video_quality = "draft"  # draft, 720p, 1080p
        
        # Output configuration
        self.base_dir = 'output_test' if self.test_mode else 'output'
    
    def create_presenter_video(self, script_text: str, lesson_title: str = "", 
                              lesson_number: int = 1) -> str:
        """
        Create AI presenter video from script
        
        Args:
            script_text: Speech script for the presenter
            lesson_title: Title of the lesson
            lesson_number: Lesson number
            
        Returns:
            Path to generated video file
        """
        try:
            logger.info(f"Creating presenter video for lesson {lesson_number}: {lesson_title}")
            
            if self.test_mode:
                # Use mock client in test mode
                video_path = self.client.create_video(script_text, lesson_title, lesson_number)
                logger.info(f"Mock video created: {video_path}")
                return video_path
            
            # Create video using D-ID API
            video_path = self._create_did_video(script_text, lesson_title, lesson_number)
            
            logger.info(f"Presenter video created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating presenter video: {str(e)}")
            # Create fallback video
            fallback_path = self._create_fallback_video(lesson_title, lesson_number)
            return fallback_path
    
    def _create_did_video(self, script_text: str, lesson_title: str, lesson_number: int) -> str:
        """Create video using D-ID API"""
        
        try:
            # Prepare request payload
            payload = {
                "script": {
                    "type": "text",
                    "input": script_text,
                    "provider": {
                        "type": "microsoft",
                        "voice_id": self.voice_id
                    }
                },
                "config": {
                    "fluent": True,
                    "pad_audio": 0.2
                },
                "source_url": f"d-id://talks/{self.presenter_id}",
                "presenter_id": self.presenter_id
            }
            
            # Create video request
            response = requests.post(
                f"{self.api_url}/talks",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 201:
                logger.error(f"D-ID API error: {response.status_code} - {response.text}")
                raise Exception(f"D-ID API error: {response.status_code}")
            
            # Get video ID from response
            video_data = response.json()
            video_id = video_data.get('id')
            
            if not video_id:
                raise Exception("No video ID received from D-ID API")
            
            logger.info(f"Video creation started with ID: {video_id}")
            
            # Wait for video to be ready
            video_path = self._wait_for_video_completion(video_id, lesson_title, lesson_number)
            
            return video_path
            
        except Exception as e:
            logger.error(f"Error in D-ID video creation: {str(e)}")
            raise
    
    def _wait_for_video_completion(self, video_id: str, lesson_title: str, lesson_number: int) -> str:
        """Wait for video to be completed and download it"""
        
        try:
            max_wait_time = 300  # 5 minutes
            check_interval = 10   # Check every 10 seconds
            elapsed_time = 0
            
            while elapsed_time < max_wait_time:
                # Check video status
                status_response = requests.get(
                    f"{self.api_url}/talks/{video_id}",
                    headers=self.headers
                )
                
                if status_response.status_code != 200:
                    logger.error(f"Error checking video status: {status_response.status_code}")
                    time.sleep(check_interval)
                    elapsed_time += check_interval
                    continue
                
                status_data = status_response.json()
                status = status_data.get('status')
                
                logger.info(f"Video status: {status}")
                
                if status == 'done':
                    # Video is ready, download it
                    video_url = status_data.get('result_url')
                    if video_url:
                        return self._download_video(video_url, lesson_title, lesson_number)
                    else:
                        raise Exception("No video URL in completed response")
                
                elif status == 'error':
                    error_msg = status_data.get('error', {}).get('message', 'Unknown error')
                    raise Exception(f"Video generation failed: {error_msg}")
                
                # Wait before next check
                time.sleep(check_interval)
                elapsed_time += check_interval
            
            # Timeout
            raise Exception("Video generation timed out")
            
        except Exception as e:
            logger.error(f"Error waiting for video completion: {str(e)}")
            raise
    
    def _download_video(self, video_url: str, lesson_title: str, lesson_number: int) -> str:
        """Download video from D-ID"""
        
        try:
            # Create output directory
            output_dir = os.path.join(self.base_dir, "videos", "presenter")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            safe_title = "".join(c for c in lesson_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"lesson_{lesson_number:02d}_{safe_title}_presenter.mp4"
            output_path = os.path.join(output_dir, filename)
            
            # Download video
            video_response = requests.get(video_url, stream=True)
            video_response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            logger.info(f"Video downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            raise
    
    def batch_create_videos(self, lesson_scripts: Dict[int, str], 
                           lesson_titles: Dict[int, str]) -> Dict[int, str]:
        """
        Create videos for multiple lessons in batch
        
        Args:
            lesson_scripts: Dictionary mapping lesson numbers to scripts
            lesson_titles: Dictionary mapping lesson numbers to titles
            
        Returns:
            Dictionary mapping lesson numbers to video paths
        """
        try:
            logger.info(f"Starting batch video creation for {len(lesson_scripts)} lessons")
            
            video_paths = {}
            
            for lesson_number, script in lesson_scripts.items():
                lesson_title = lesson_titles.get(lesson_number, f"Lesson {lesson_number}")
                
                logger.info(f"Creating video for lesson {lesson_number}")
                
                try:
                    video_path = self.create_presenter_video(script, lesson_title, lesson_number)
                    video_paths[lesson_number] = video_path
                    
                    logger.info(f"Video created for lesson {lesson_number}: {video_path}")
                    
                    # Add delay between requests to respect API limits (ONLY in production mode)
                    if not self.test_mode and len(lesson_scripts) > 1:
                        logger.info("Waiting 30 seconds before next video request...")
                        time.sleep(30)
                    
                except Exception as e:
                    logger.error(f"Error creating video for lesson {lesson_number}: {str(e)}")
                    # Continue with other lessons
                    continue
            
            logger.info(f"Batch video creation completed. {len(video_paths)} videos created.")
            return video_paths
            
        except Exception as e:
            logger.error(f"Error in batch video creation: {str(e)}")
            return {}
    
    def _create_fallback_video(self, lesson_title: str, lesson_number: int) -> str:
        """Create a simple fallback video if generation fails"""
        
        try:
            # Create output directory
            output_dir = os.path.join(self.base_dir, "videos", "fallback")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            filename = f"lesson_{lesson_number:02d}_{lesson_title.replace(' ', '_')}_fallback.mp4"
            output_path = os.path.join(output_dir, filename)
            
            # Try to create a simple colored video with text using ffmpeg
            try:
                import subprocess
                
                # Create a simple colored video with text using ffmpeg
                cmd = [
                    'ffmpeg', '-f', 'lavfi', '-i', 'color=c=0x6496FF:size=640x480:duration=10',
                    '-vf', f'drawtext=text=\'Lesson {lesson_number}\\n{lesson_title}\':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-t', '10',
                    '-y',  # Overwrite output file
                    output_path
                ]
                
                # Run ffmpeg command
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Fallback video created with ffmpeg: {output_path}")
                    return output_path
                else:
                    logger.warning(f"FFmpeg fallback failed: {result.stderr}")
                    # Continue to file creation fallback
                    
            except (ImportError, FileNotFoundError, subprocess.SubprocessError):
                logger.info("FFmpeg not available for fallback video")
                # Continue to file creation fallback
            
            # Final fallback: create an empty file
            with open(output_path, 'w') as f:
                f.write("Fallback video file")
            
            logger.info(f"Fallback video file created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating fallback video: {str(e)}")
            # Return empty string if even fallback fails
            return ""
    
    def get_video_status(self, video_id: str) -> Dict[str, Any]:
        """Get status of a video generation request"""
        
        try:
            if self.test_mode:
                return {"status": "done", "test_mode": True}
            
            response = requests.get(
                f"{self.api_url}/talks/{video_id}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status check failed: {response.status_code}"}
                
        except Exception as e:
            logger.error(f"Error checking video status: {str(e)}")
            return {"error": str(e)}
    
    def list_available_presenters(self) -> List[Dict[str, Any]]:
        """List available presenter options"""
        
        try:
            if self.test_mode:
                return [
                    {"id": "amy-Aq6r0S0Vg", "name": "Amy", "gender": "female", "style": "professional"},
                    {"id": "john-Bq7r1T1Wh", "name": "John", "gender": "male", "style": "professional"},
                    {"id": "sarah-Cq8r2U2Xi", "name": "Sarah", "gender": "female", "style": "casual"}
                ]
            
            response = requests.get(
                f"{self.api_url}/presenters",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Error fetching presenters: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error listing presenters: {str(e)}")
            return []
    
    def list_available_voices(self) -> List[Dict[str, Any]]:
        """List available voice options"""
        
        try:
            if self.test_mode:
                return [
                    {"id": "en-US-JennyNeural", "name": "Jenny", "language": "en-US", "style": "neutral"},
                    {"id": "en-US-GuyNeural", "name": "Guy", "language": "en-US", "style": "neutral"},
                    {"id": "en-GB-SoniaNeural", "name": "Sonia", "language": "en-GB", "style": "neutral"}
                ]
            
            # Note: D-ID doesn't have a direct voices endpoint, so we return common options
            return [
                {"id": "en-US-JennyNeural", "name": "Jenny", "language": "en-US", "style": "neutral"},
                {"id": "en-US-GuyNeural", "name": "Guy", "language": "en-US", "style": "neutral"},
                {"id": "en-GB-SoniaNeural", "name": "Sonia", "language": "en-GB", "style": "neutral"},
                {"id": "en-AU-NatashaNeural", "name": "Natasha", "language": "en-AU", "style": "neutral"}
            ]
                
        except Exception as e:
            logger.error(f"Error listing voices: {str(e)}")
            return []
    
    def update_presenter_config(self, presenter_id: str = None, voice_id: str = None, 
                               video_quality: str = None) -> bool:
        """Update presenter configuration"""
        
        try:
            if presenter_id:
                self.presenter_id = presenter_id
            if voice_id:
                self.voice_id = voice_id
            if video_quality:
                self.video_quality = video_quality
            
            logger.info(f"Presenter config updated: presenter={self.presenter_id}, voice={self.voice_id}, quality={self.video_quality}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating presenter config: {str(e)}")
            return False
    
    def estimate_video_duration(self, script_text: str) -> float:
        """Estimate video duration based on script length"""
        
        try:
            # Rough estimation: 150 words per minute
            word_count = len(script_text.split())
            estimated_minutes = word_count / 150
            
            # Add buffer for pauses and transitions
            estimated_minutes += (word_count / 100) * 0.1
            
            return round(estimated_minutes, 1)
            
        except Exception as e:
            logger.error(f"Error estimating video duration: {str(e)}")
            return 5.0  # Default fallback
    
    def get_video_analytics(self, video_path: str) -> Dict[str, Any]:
        """Get analytics for a generated video"""
        
        try:
            if not os.path.exists(video_path):
                return {"error": "Video file not found"}
            
            # Get file stats
            file_stats = os.stat(video_path)
            file_size_mb = file_stats.st_size / (1024 * 1024)
            
            # Try to get video duration using moviepy
            try:
                from moviepy.editor import VideoFileClip
                with VideoFileClip(video_path) as video:
                    duration = video.duration
            except:
                duration = None
            
            analytics = {
                "file_path": video_path,
                "file_size_mb": round(file_size_mb, 2),
                "duration_seconds": duration,
                "duration_minutes": round(duration / 60, 2) if duration else None,
                "created_time": file_stats.st_ctime,
                "modified_time": file_stats.st_mtime
            }
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting video analytics: {str(e)}")
            return {"error": str(e)}
