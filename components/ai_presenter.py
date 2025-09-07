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
from mocks.mock_clients import MockDIDClient
from components.opensource_presenter import OpenSourcePresenter

logger = logging.getLogger(__name__)

class AIPresenter:
    """
    Generates AI presenter videos using D-ID API
    """
    
    def __init__(self, did_api_key: str, test_mode: bool = False, domain: str = None, use_opensource: bool = True):
        """Initialize with D-ID API key and test mode flag"""
        self.test_mode = test_mode
        self.did_api_key = did_api_key
        self.domain = domain
        self.use_opensource = use_opensource
        
        # Initialize open-source presenter
        if self.use_opensource:
            logger.info("🚀 Using open-source AI presenter (no API costs!)")
            self.opensource_presenter = OpenSourcePresenter(domain)
        else:
            self.opensource_presenter = None
        
        if self.test_mode:
            logger.info("Using mock D-ID client for testing")
            # We'll set the base_dir after it's calculated below
            self.client = None
        else:
            self.client = None  # Will use requests directly for D-ID API
        
        # Validate API key format
        if not self.test_mode and did_api_key:
            if ':' in did_api_key:
                logger.info("D-ID API key contains ':' - this is correct for Basic auth (username:password format)")
            if len(did_api_key) < 20:
                logger.warning("D-ID API key seems too short - expected format is username:password or base64 encoded key")
        
        # D-ID API configuration - use the official studio API
        self.api_url = "https://api.d-id.com"
        self.api_endpoints = [
            "https://api.d-id.com/talks",  # Main endpoint
        ]
        self.headers = {
            "Authorization": f"Basic {did_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Presenter configuration
        self.presenter_id = "amy-Aq6r0S0Vg"  # Professional female presenter
        self.voice_id = "en-US-JennyNeural"  # Natural English voice
        self.video_quality = "draft"  # draft, 720p, 1080p
        
        # Presenter image URL (use D-ID public image that works reliably)
        self.presenter_image_url = "https://d-id-public-bucket.s3.amazonaws.com/alice.jpg"
        
        # Output configuration
        base_dir = 'output_test' if self.test_mode else 'output'
        if self.domain:
            # Clean domain name for filesystem
            clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
            clean_domain = clean_domain.replace(' ', '_')
            self.base_dir = f'{base_dir}/{clean_domain}'
        else:
            self.base_dir = base_dir
        
        # Initialize mock client with base_dir if in test mode
        if self.test_mode:
            self.client = MockDIDClient(did_api_key, self.base_dir)
    
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
            
            # Priority 1: Use open-source presenter (best option)
            if self.use_opensource and self.opensource_presenter:
                try:
                    video_path = self.opensource_presenter.create_presenter_video(script_text, lesson_title, lesson_number)
                    logger.info(f"✅ Open-source presenter video created: {video_path}")
                    return video_path
                except Exception as e:
                    logger.warning(f"Open-source presenter failed, falling back to D-ID: {e}")
            
            # Priority 2: Use test mode mock
            if self.test_mode:
                video_path = self.client.create_video(script_text, lesson_title, lesson_number)
                logger.info(f"Mock video created: {video_path}")
                return video_path
            
            # Priority 3: Use D-ID API (last resort)
            video_path = self._create_did_video(script_text, lesson_title, lesson_number)
            
            logger.info(f"Presenter video created successfully: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating presenter video: {str(e)}")
            # Check if it's a credits issue
            if "402" in str(e) or "payment" in str(e).lower() or "credit" in str(e).lower():
                logger.error("🚨 D-ID API credits exhausted! Please add credits to your account.")
                logger.error("Visit: https://studio.d-id.com/account-settings to add credits")
            
            # Create enhanced fallback video with TTS voice
            fallback_path = self._create_enhanced_fallback_video(script_text, lesson_title, lesson_number)
            return fallback_path
    
    def _create_did_video(self, script_text: str, lesson_title: str, lesson_number: int) -> str:
        """Create video using D-ID API"""
        
        try:
            # Check if we have a valid API key
            if not self.did_api_key or self.did_api_key == 'your_did_api_key_here':
                logger.error("D-ID API key not configured. Please set DID_API_KEY in your .env file")
                logger.error("Get your API key from: https://studio.d-id.com/account-settings")
                raise Exception("D-ID API key not configured")
            
            # Prepare request payload - use format that works with D-ID API
            payload = {
                "source_url": self.presenter_image_url,
                "script": {
                    "type": "text",
                    "input": script_text,
                    "subtitles": True  # Enable subtitle generation (must be in script object)
                }
            }
            
            # Try multiple endpoints and authentication methods
            response = None
            last_error = None
            
            for endpoint in self.api_endpoints:
                logger.info(f"Trying D-ID API endpoint: {endpoint}")
                logger.info(f"Headers: {self.headers}")
                logger.info(f"Payload: {payload}")
                
                try:
                    # Create video request
                    response = requests.post(
                        endpoint,
                        headers=self.headers,
                        json=payload,
                        timeout=30
                    )
                    
                    logger.info(f"D-ID API response status: {response.status_code}")
                    logger.info(f"D-ID API response headers: {dict(response.headers)}")
                    logger.info(f"D-ID API response body: {response.text}")
                    
                    # If successful, break out of loop
                    if response.status_code == 201:
                        logger.info(f"✅ Success with endpoint: {endpoint}")
                        break
                    elif response.status_code == 500 and "circular structure" in response.text:
                        logger.warning(f"⚠️  Endpoint {endpoint} has server-side bug, trying next...")
                        last_error = f"Server bug at {endpoint}"
                        continue
                    elif response.status_code in [401, 403]:
                        logger.warning(f"🔒 Authentication failed at {endpoint}, trying next...")
                        last_error = f"Auth failed at {endpoint}"
                        continue
                    else:
                        # Other error, but still try next endpoint
                        logger.warning(f"⚠️  Unexpected error {response.status_code} at {endpoint}, trying next...")
                        last_error = f"Error {response.status_code} at {endpoint}"
                        continue
                        
                except requests.exceptions.RequestException as e:
                    logger.warning(f"🔌 Request failed for {endpoint}: {str(e)}")
                    last_error = f"Request failed for {endpoint}: {str(e)}"
                    continue
            
            # If we get here, check if we have a valid response
            if not response or response.status_code != 201:
                if last_error:
                    logger.error(f"All D-ID endpoints failed. Last error: {last_error}")
                else:
                    logger.error("All D-ID endpoints failed with unknown errors")
            
            if response.status_code == 401:
                logger.error("D-ID API authentication failed. Please check your API key.")
                logger.error("Get your API key from: https://studio.d-id.com/account-settings")
                logger.error("The API key should be in username:password format for Basic auth")
                raise Exception("D-ID API authentication failed - check your API key")
            elif response.status_code != 201:
                logger.error(f"D-ID API error: {response.status_code} - {response.text}")
                raise Exception(f"D-ID API error: {response.status_code} - {response.text}")
            
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
                    # Video is ready, download it and embed subtitles if available
                    video_url = status_data.get('result_url')
                    subtitles_url = status_data.get('subtitles_url')
                    subtitles_enabled = status_data.get('subtitles', False)
                    
                    if video_url:
                        # Download the base video
                        video_path = self._download_video(video_url, lesson_title, lesson_number)
                        
                        # If subtitles are available, embed them into the video
                        if subtitles_enabled and subtitles_url:
                            logger.info("✅ Embedding subtitles into video...")
                            final_video_path = self._embed_subtitles(video_path, subtitles_url, lesson_title, lesson_number)
                            return final_video_path
                        else:
                            logger.info("Video generated without subtitles")
                            return video_path
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
    
    def _embed_subtitles(self, video_path: str, subtitles_url: str, lesson_title: str, lesson_number: int) -> str:
        """Embed subtitles into video using OpenCV (no ImageMagick dependency)"""
        
        try:
            import cv2
            import numpy as np
            
            # Download SRT file
            logger.info(f"Downloading subtitles from: {subtitles_url}")
            srt_response = requests.get(subtitles_url)
            srt_response.raise_for_status()
            
            srt_content = srt_response.text
            logger.info(f"SRT content received ({len(srt_content)} characters)")
            
            # Parse SRT content
            subtitle_segments = self._parse_srt_content(srt_content)
            logger.info(f"Parsed {len(subtitle_segments)} subtitle segments")
            
            if not subtitle_segments:
                logger.warning("No subtitle segments found, returning original video")
                return video_path
            
            # Create output path for video with embedded subtitles
            output_path = video_path.replace('.mp4', '_with_subtitles.mp4')
            
            # Process video with OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                logger.error(f"Could not open video file: {video_path}")
                return video_path
            
            # Get video properties
            fps = int(cap.get(cv2.CAP_PROP_FPS))
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            logger.info(f"Video properties: {width}x{height}, {fps} FPS, {total_frames} frames")
            
            # Create video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Calculate current time in seconds
                current_time = frame_count / fps
                
                # Find active subtitle for current time
                active_subtitle = None
                for segment in subtitle_segments:
                    if segment['start'] <= current_time <= segment['end']:
                        active_subtitle = segment['text']
                        break
                
                # Add subtitle text to frame if available
                if active_subtitle:
                    frame = self._add_subtitle_to_frame(frame, active_subtitle, width, height)
                
                out.write(frame)
                frame_count += 1
                
                # Progress logging every 5 seconds
                if frame_count % (fps * 5) == 0:
                    progress = (frame_count / total_frames) * 100
                    logger.info(f"Processing subtitles: {progress:.1f}% complete")
            
            # Clean up
            cap.release()
            out.release()
            cv2.destroyAllWindows()
            
            # Remove original video without subtitles
            if os.path.exists(video_path):
                os.remove(video_path)
            
            logger.info(f"✅ Video with embedded subtitles created: {output_path}")
            return output_path
            
        except ImportError:
            logger.error("OpenCV not available, cannot embed subtitles")
            logger.info("Install with: pip install opencv-python")
            return video_path
        except Exception as e:
            logger.error(f"Error embedding subtitles: {str(e)}")
            logger.warning("Falling back to video without embedded subtitles")
            return video_path
    
    def _parse_srt_content(self, srt_content: str) -> list:
        """Parse SRT content into subtitle segments"""
        
        segments = []
        blocks = srt_content.strip().split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 3:
                try:
                    # Parse timestamp (format: 00:00:00,000 --> 00:00:03,000)
                    timestamp_line = lines[1]
                    if ' --> ' in timestamp_line:
                        start_time, end_time = timestamp_line.split(' --> ')
                        
                        # Convert timestamp to seconds
                        start_seconds = self._timestamp_to_seconds(start_time.strip())
                        end_seconds = self._timestamp_to_seconds(end_time.strip())
                        
                        # Get subtitle text (join all lines after timestamp)
                        text = ' '.join(lines[2:]).strip()
                        
                        if text and start_seconds is not None and end_seconds is not None:
                            segments.append({
                                'start': start_seconds,
                                'end': end_seconds,
                                'text': text
                            })
                except Exception as e:
                    logger.warning(f"Error parsing SRT block: {e}")
                    continue
        
        return segments
    
    def _timestamp_to_seconds(self, timestamp: str) -> float:
        """Convert SRT timestamp to seconds"""
        try:
            # Format: 00:00:03,000
            time_part, ms_part = timestamp.split(',')
            hours, minutes, seconds = map(int, time_part.split(':'))
            milliseconds = int(ms_part)
            
            total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0
            return total_seconds
            
        except Exception as e:
            logger.error(f"Error parsing timestamp {timestamp}: {str(e)}")
            return None
    
    def _add_subtitle_to_frame(self, frame, text: str, width: int, height: int):
        """Add subtitle text to video frame using OpenCV"""
        
        try:
            import cv2
            
            # Text properties
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = min(width, height) / 800  # Scale font based on video size
            font_thickness = max(1, int(font_scale * 2))
            
            # Calculate text size and position
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
            text_x = (width - text_size[0]) // 2
            text_y = height - 60  # Position near bottom
            
            # Add black outline for better visibility
            outline_thickness = font_thickness + 1
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 0, 0), outline_thickness, cv2.LINE_AA)
            
            # Add white text on top
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness, cv2.LINE_AA)
            
            return frame
            
        except Exception as e:
            logger.error(f"Error adding subtitle to frame: {e}")
            return frame
    
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
    
    def _create_enhanced_fallback_video(self, script_text: str, lesson_title: str, lesson_number: int) -> str:
        """Create enhanced fallback video with TTS voice when D-ID API fails"""
        
        try:
            # Create output directory
            output_dir = os.path.join(self.base_dir, "videos", "fallback")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            safe_title = "".join(c for c in lesson_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"lesson_{lesson_number:02d}_{safe_title}_enhanced_fallback.mp4"
            output_path = os.path.join(output_dir, filename)
            
            logger.info(f"Creating enhanced fallback video with TTS: {output_path}")
            
            # Use the same TTS logic as the mock video system
            from mocks.mock_clients import create_mock_video_with_audio
            
            # Create video with TTS audio
            video_path = create_mock_video_with_audio(
                lesson_title=lesson_title,
                lesson_number=lesson_number, 
                script_text=script_text,
                base_dir=self.base_dir,
                is_fallback=True
            )
            
            logger.info(f"Enhanced fallback video created: {video_path}")
            return video_path
            
        except Exception as e:
            logger.error(f"Error creating enhanced fallback video: {str(e)}")
            # Fall back to basic fallback
            return self._create_fallback_video(lesson_title, lesson_number)
    
    def _create_fallback_video(self, lesson_title: str, lesson_number: int) -> str:
        """Create a simple fallback video if generation fails"""
        
        try:
            # Create output directory
            output_dir = os.path.join(self.base_dir, "videos", "fallback")
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            safe_title = "".join(c for c in lesson_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            filename = f"lesson_{lesson_number:02d}_{safe_title}_fallback.mp4"
            output_path = os.path.join(output_dir, filename)
            
            logger.info(f"Creating fallback video: {output_path}")
            
            # Method 1: Try using ffmpeg if available (most reliable)
            try:
                import subprocess
                
                # Create a simple colored video with text
                cmd = [
                    'ffmpeg', '-f', 'lavfi', '-i', 'color=c=0x6496FF:size=640x480:duration=5',
                    '-vf', f'drawtext=text=\'Lesson {lesson_number}\\n{lesson_title[:30]}\':fontsize=32:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-t', '5',
                    '-y', output_path
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"Fallback video created with ffmpeg: {output_path}")
                    return output_path
                else:
                    logger.warning(f"FFmpeg fallback failed: {result.stderr}")
                    
            except (FileNotFoundError, subprocess.SubprocessError):
                logger.info("FFmpeg not available for fallback video")
            
            # Method 2: Try using PIL + moviepy
            try:
                from PIL import Image, ImageDraw, ImageFont
                import numpy as np
                
                # Create a simple image frame
                width, height = 640, 480
                img = Image.new('RGB', (width, height), color=(100, 150, 255))
                draw = ImageDraw.Draw(img)
                
                # Try to use a font, fallback to default if not available
                try:
                    font = ImageFont.truetype("Arial.ttf", 32)
                except:
                    font = ImageFont.load_default()
                
                # Add text to the image
                text = f"Lesson {lesson_number}\n{lesson_title[:30]}..."
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                draw.text((x, y), text, fill=(255, 255, 255), font=font)
                
                # Convert to numpy array
                frame = np.array(img)
                
                # Create a simple video using moviepy
                try:
                    from moviepy.editor import ImageClip
                    
                    # Create a clip from the image
                    clip = ImageClip(frame, duration=5)
                    
                    # Write the video
                    clip.write_videofile(
                        output_path,
                        fps=24,
                        codec='libx264',
                        audio=False,
                        verbose=False,
                        logger=None
                    )
                    
                    logger.info(f"Fallback video created with moviepy: {output_path}")
                    return output_path
                    
                except Exception as moviepy_error:
                    logger.warning(f"MoviePy fallback failed: {moviepy_error}")
                    
            except ImportError:
                logger.info("PIL/moviepy not available for fallback video")
            
            # Method 3: Create a simple image file as fallback
            try:
                from PIL import Image, ImageDraw, ImageFont
                
                # Create a simple image
                width, height = 640, 480
                img = Image.new('RGB', (width, height), color=(100, 150, 255))
                draw = ImageDraw.Draw(img)
                
                # Try to use a font, fallback to default if not available
                try:
                    font = ImageFont.truetype("Arial.ttf", 32)
                except:
                    font = ImageFont.load_default()
                
                # Add text to the image
                text = f"Lesson {lesson_number}\n{lesson_title[:30]}..."
                bbox = draw.textbbox((0, 0), text, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                x = (width - text_width) // 2
                y = (height - text_height) // 2
                
                draw.text((x, y), text, fill=(255, 255, 255), font=font)
                
                # Save as PNG
                png_path = output_path.replace('.mp4', '.png')
                img.save(png_path, 'PNG')
                
                logger.info(f"Fallback image created: {png_path}")
                return png_path
                
            except ImportError:
                logger.info("PIL not available for fallback image")
            
            # Ultimate fallback: create a text file
            logger.warning("All fallback methods failed, creating text file")
            txt_path = output_path.replace('.mp4', '.txt')
            with open(txt_path, 'w') as f:
                f.write(f"Fallback file for lesson {lesson_number}: {lesson_title}\n")
                f.write("D-ID API is not working. Please check your API key.\n")
                f.write("Get your API key from: https://studio.d-id.com/account-settings\n")
            
            logger.info(f"Fallback text file created: {txt_path}")
            return txt_path
            
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
