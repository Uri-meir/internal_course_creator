"""
Video Assembler Component
Assembles final videos by combining AI presenter with backgrounds
"""

import os
import logging
from typing import Dict, List, Any, Optional
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx import resize

# Apply MoviePy configuration fix
try:
    from moviepy_config_fix import fix_moviepy_config
    fix_moviepy_config()
except ImportError:
    pass

# Test TextClip availability after fix
try:
    from moviepy.editor import TextClip
    # Test if TextClip works
    test_clip = TextClip("test", fontsize=20, color='white').set_duration(1)
    test_clip.close()
    TEXTCLIP_AVAILABLE = True
except Exception as e:
    logging.warning(f"TextClip not available due to ImageMagick issue: {e}")
    TEXTCLIP_AVAILABLE = False

logger = logging.getLogger(__name__)

class VideoAssembler:
    """
    Assembles final videos by combining AI presenter videos with background images
    """
    
    def __init__(self, domain: str = None):
        """Initialize video assembler"""
        self.output_resolution = (1920, 1080)  # Full HD
        self.fps = 30
        self.domain = domain
    
    def compose_final_video(self, presenter_video: str, background_image: str, 
                           lesson_title: str, lesson_number: int) -> str:
        """
        Compose final video by combining presenter with background
        
        Args:
            presenter_video: Path to AI presenter video
            background_image: Path to background image
            lesson_title: Title of the lesson
            lesson_number: Lesson number
            
        Returns:
            Path to final composed video
        """
        try:
            logger.info(f"Composing final video for lesson {lesson_number}: {lesson_title}")
            
            # Load presenter video
            presenter_clip = self._load_presenter_clip(presenter_video)
            if not presenter_clip:
                logger.error("Failed to load presenter video")
                return presenter_video  # Return original if processing fails
            
            # Load background image
            background_clip = self._load_background_clip(background_image)
            if not background_clip:
                logger.error("Failed to load background image")
                return presenter_video  # Return original if processing fails
            
            # Create title overlay (with fallback)
            title_clip = self._create_title_overlay(lesson_title, lesson_number)
            
            # If TextClip failed, try PIL-based title image
            if title_clip is None and TEXTCLIP_AVAILABLE == False:
                logger.info("Using PIL-based title overlay as fallback")
                title_image_path = self._create_simple_title_image(lesson_title, lesson_number)
                if title_image_path:
                    try:
                        title_image_clip = ImageClip(title_image_path).set_duration(3).set_position(('center', 50))
                        title_clip = title_image_clip
                    except Exception as e:
                        logger.warning(f"PIL title image failed: {e}")
                        title_clip = None
            
            # Compose final video
            final_video = self._compose_video_layers(
                presenter_clip, background_clip, title_clip
            )
            
            # Save final video
            output_path = self._save_final_video(final_video, lesson_number, lesson_title)
            
            logger.info(f"Final video composed successfully: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error composing final video: {str(e)}")
            return presenter_video  # Return original if processing fails
    
    def _load_presenter_clip(self, video_path: str) -> Optional[VideoFileClip]:
        """Load presenter video clip"""
        
        try:
            if not os.path.exists(video_path):
                logger.error(f"Presenter video not found: {video_path}")
                return None
            
            clip = VideoFileClip(video_path)
            
            # Resize to target resolution
            clip = clip.resize(self.output_resolution)
            
            return clip
            
        except Exception as e:
            logger.error(f"Error loading presenter clip: {str(e)}")
            return None
    
    def _load_background_clip(self, image_path: str) -> Optional[ImageClip]:
        """Load background image as video clip"""
        
        try:
            if not os.path.exists(image_path):
                logger.error(f"Background image not found: {image_path}")
                return None
            
            # Load image and convert to video clip
            image_clip = ImageClip(image_path)
            
            # Resize to target resolution
            image_clip = image_clip.resize(self.output_resolution)
            
            return image_clip
            
        except Exception as e:
            logger.error(f"Error loading background clip: {str(e)}")
            return None
    
    def _create_title_overlay(self, lesson_title: str, lesson_number: int) -> Optional[CompositeVideoClip]:
        """Create title overlay for the video"""
        
        if not TEXTCLIP_AVAILABLE:
            logger.info("TextClip not available due to ImageMagick configuration - skipping title overlay")
            return None
        
        try:
            from moviepy.editor import TextClip
            
            # Create lesson number text
            lesson_num_text = f"LESSON {lesson_number}"
            lesson_num_clip = TextClip(
                lesson_num_text, 
                fontsize=48, 
                color='white',
                method='caption'  # Use caption method to avoid font issues
            ).set_position(('center', 100)).set_duration(3)
            
            # Create lesson title text
            title_clip = TextClip(
                lesson_title, 
                fontsize=36, 
                color='white',
                method='caption'  # Use caption method to avoid font issues
            ).set_position(('center', 160)).set_duration(3)
            
            # Combine title elements
            title_overlay = CompositeVideoClip([lesson_num_clip, title_clip])
            
            return title_overlay
            
        except Exception as e:
            logger.warning(f"TextClip failed, creating video without title overlay: {str(e)}")
            return None
    
    def _create_simple_title_image(self, lesson_title: str, lesson_number: int) -> Optional[str]:
        """Create a simple title image using PIL as fallback"""
        try:
            from PIL import Image, ImageDraw, ImageFont
            import tempfile
            
            # Create image
            img = Image.new('RGBA', (1920, 200), color=(0, 0, 0, 128))  # Semi-transparent black
            draw = ImageDraw.Draw(img)
            
            try:
                # Try to use a system font
                title_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 48)
                subtitle_font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 36)
            except:
                # Fallback to default font
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
            
            # Draw lesson number
            lesson_text = f"LESSON {lesson_number}"
            bbox = draw.textbbox((0, 0), lesson_text, font=title_font)
            text_width = bbox[2] - bbox[0]
            x = (1920 - text_width) // 2
            draw.text((x, 30), lesson_text, font=title_font, fill='white')
            
            # Draw lesson title
            bbox = draw.textbbox((0, 0), lesson_title, font=subtitle_font)
            text_width = bbox[2] - bbox[0]
            x = (1920 - text_width) // 2
            draw.text((x, 90), lesson_title, font=subtitle_font, fill='white')
            
            # Save temporary image
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            img.save(temp_file.name)
            temp_file.close()
            
            return temp_file.name
            
        except Exception as e:
            logger.warning(f"Could not create title image: {e}")
            return None
    
    def _compose_video_layers(self, presenter_clip: VideoFileClip, 
                             background_clip: ImageClip, 
                             title_clip) -> CompositeVideoClip:
        """Compose video layers together"""
        
        # Set background duration to match presenter
        background_clip = background_clip.set_duration(presenter_clip.duration)
        
        # Start with background
        layers = [background_clip]
        
        # Add presenter video (centered, smaller size)
        presenter_size = (640, 480)  # Smaller presenter window
        presenter_resized = presenter_clip.resize(presenter_size)
        presenter_positioned = presenter_resized.set_position('center')
        layers.append(presenter_positioned)
        
        # Add title overlay if available
        if title_clip:
            # Set title to appear at the beginning
            title_clip = title_clip.set_start(0)
            layers.append(title_clip)
        
        # Compose all layers
        final_video = CompositeVideoClip(layers, size=self.output_resolution)
        
        return final_video
    
    def _save_final_video(self, final_video: CompositeVideoClip, 
                          lesson_number: int, lesson_title: str) -> str:
        """Save the final composed video"""
        
        try:
            # Create safe filename
            safe_title = "".join(c for c in lesson_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = safe_title.replace(' ', '_')
            
            filename = f"lesson_{lesson_number:02d}_{safe_title}_final.mp4"
            
            # Create output directory
            if self.domain:
                clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_domain = clean_domain.replace(' ', '_')
                output_dir = f"output/{clean_domain}/videos/final"
            else:
                output_dir = "output/videos/final"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            # Write video file
            final_video.write_videofile(
                output_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Clean up
            final_video.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error saving final video: {str(e)}")
            raise
    
    def create_video_preview(self, video_path: str, duration: float = 10.0) -> str:
        """Create a short preview of the video"""
        
        try:
            if not os.path.exists(video_path):
                logger.error(f"Video not found: {video_path}")
                return ""
            
            # Load video
            video_clip = VideoFileClip(video_path)
            
            # Take first N seconds
            preview_clip = video_clip.subclip(0, min(duration, video_clip.duration))
            
            # Create preview filename
            base_name = os.path.splitext(video_path)[0]
            preview_path = f"{base_name}_preview.mp4"
            
            # Save preview
            preview_clip.write_videofile(
                preview_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Clean up
            preview_clip.close()
            video_clip.close()
            
            return preview_path
            
        except Exception as e:
            logger.error(f"Error creating video preview: {str(e)}")
            return ""
    
    def add_subtitles(self, video_path: str, subtitles: List[Dict[str, Any]]) -> str:
        """Add subtitles to video"""
        
        try:
            if not os.path.exists(video_path):
                logger.error(f"Video not found: {video_path}")
                return video_path
            
            # Load video
            video_clip = VideoFileClip(video_path)
            
            # Create subtitle clips
            subtitle_clips = []
            for subtitle in subtitles:
                start_time = subtitle.get('start', 0)
                end_time = subtitle.get('end', start_time + 3)
                text = subtitle.get('text', '')
                
                if text:
                    text_clip = TextClip(
                        text,
                        fontsize=24,
                        color='white',
                        font='Arial',
                        stroke_color='black',
                        stroke_width=2
                    ).set_position(('center', 'bottom')).set_start(start_time).set_end(end_time)
                    
                    subtitle_clips.append(text_clip)
            
            # Compose video with subtitles
            final_video = CompositeVideoClip([video_clip] + subtitle_clips)
            
            # Save with subtitles
            base_name = os.path.splitext(video_path)[0]
            subtitled_path = f"{base_name}_subtitled.mp4"
            
            final_video.write_videofile(
                subtitled_path,
                fps=self.fps,
                codec='libx264',
                audio_codec='aac',
                verbose=False,
                logger=None
            )
            
            # Clean up
            final_video.close()
            video_clip.close()
            
            return subtitled_path
            
        except Exception as e:
            logger.error(f"Error adding subtitles: {str(e)}")
            return video_path 
