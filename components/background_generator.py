"""
Background Generator Component
Creates visual backgrounds and course graphics using AI image generation
"""

import os
import time
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
from PIL import Image, ImageDraw, ImageFont
from openai import OpenAI
import logging
from mocks.mock_clients import MockOpenAIClient, create_mock_image_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackgroundGenerator:
    """
    Generates visual backgrounds and course graphics using DALL-E and PIL
    """
    
    def __init__(self, openai_api_key: str, test_mode: bool = False, domain: str = None):
        """Initialize with OpenAI API key for DALL-E and test mode flag"""
        self.test_mode = test_mode
        self.domain = domain
        
        if self.test_mode:
            logger.info("Using mock OpenAI client for testing")
            self.client = MockOpenAIClient(openai_api_key)
        else:
            self.client = OpenAI(api_key=openai_api_key)
            
        self.brand_colors = self._get_brand_colors()
        self.topic_prompts = self._load_topic_prompts()
        self.output_resolution = (1920, 1080)  # Full HD
        self.thumbnail_resolution = (1280, 720)  # HD thumbnail
    
    def _get_brand_colors(self) -> List[str]:
        """Get brand color palette"""
        return [
            "#667eea",  # Primary blue-purple
            "#764ba2",  # Secondary purple
            "#4facfe",  # Light blue
            "#00f2fe",  # Cyan
            "#f093fb",  # Pink
            "#f5576c",  # Red-pink
            "#4facfe",  # Blue
            "#43e97b"   # Green
        ]
    
    def _load_topic_prompts(self) -> Dict[str, str]:
        """Load topic-specific background prompts"""
        return {
            "rag": "Professional tech background with abstract data flow, neural network patterns, retrieval and generation concepts, modern gradient colors, clean minimal design for educational video, high-tech atmosphere",
            "machine_learning": "Clean data visualization background, flowing data points, neural networks, gradient blue to purple, professional educational setting, ML algorithms visualization",
            "web_development": "Modern code editor interface background, subtle syntax highlighting, professional development environment, web technologies, clean design",
            "python": "Python programming background, code snippets, snake-inspired gradients, professional coding environment, clean syntax highlighting",
            "api": "API connection visualization, data flow between services, modern tech background, network connections, professional blue tones",
            "database": "Database schema visualization, data tables, connections, professional data management background, structured data flow",
            "cloud": "Cloud computing visualization, servers, data centers, modern infrastructure, professional cloud services background",
            "ai": "Artificial intelligence background, neural networks, brain-inspired patterns, futuristic tech design, AI visualization",
            "data_science": "Data analysis visualization, charts, graphs, statistics, professional analytics background, data insights",
            "cybersecurity": "Security-focused background, shield patterns, lock symbols, secure connections, professional security design",
            "default": "Professional educational background, clean modern design, subtle tech patterns, gradient colors, minimalist style"
        }
    
    def generate_topic_background(self, topic: str, lesson_title: str, style: str = "professional") -> str:
        """
        Generate topic-relevant background using AI image generation
        
        Args:
            topic: Course topic (e.g., "RAG", "Machine Learning")
            lesson_title: Specific lesson title
            style: Style preference (professional, casual, modern)
            
        Returns:
            Path to generated background image
        """
        try:
            logger.info(f"Generating background for topic: {topic}, lesson: {lesson_title}")
            
            # Get appropriate prompt
            topic_key = topic.lower().replace(" ", "_")
            base_prompt = self.topic_prompts.get(topic_key, self.topic_prompts["default"])
            
            # Enhance prompt with lesson-specific context
            enhanced_prompt = self._enhance_prompt_for_lesson(base_prompt, lesson_title, style)
            
            # Generate image using DALL-E
            image_path = self._generate_dalle_image(enhanced_prompt, topic, lesson_title)
            
            # Post-process for video use
            processed_path = self._post_process_background(image_path)
            
            logger.info(f"Background generated successfully: {processed_path}")
            return processed_path
            
        except Exception as e:
            logger.error(f"Error generating background: {str(e)}")
            # Create fallback background
            fallback_path = self._create_fallback_background(topic, lesson_title)
            return fallback_path
    
    def _enhance_prompt_for_lesson(self, base_prompt: str, lesson_title: str, style: str) -> str:
        """Enhance base prompt with lesson-specific details"""
        
        enhanced = f"{base_prompt}, lesson: {lesson_title}, style: {style}"
        
        # Add style-specific enhancements
        if style == "modern":
            enhanced += ", contemporary design, sleek lines, minimalist approach"
        elif style == "casual":
            enhanced += ", friendly atmosphere, warm colors, approachable design"
        else:  # professional
            enhanced += ", corporate aesthetic, clean lines, business-appropriate"
        
        return enhanced
    
    def _generate_dalle_image(self, prompt: str, topic: str, lesson_title: str) -> str:
        """Generate image using DALL-E API"""
        
        try:
            if self.test_mode:
                logger.info("Generating mock image...")
                return create_mock_image_file(topic, lesson_title)
            
            # Create safe filename
            safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_title = "".join(c for c in lesson_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
            
            filename = f"bg_{safe_topic}_{safe_title}.png"
            
            # Create output directory
            base_dir = "output/backgrounds/generated"
            if self.domain:
                clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_domain = clean_domain.replace(' ', '_')
                output_dir = f"output/{clean_domain}/backgrounds/generated"
            else:
                output_dir = base_dir
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            # Generate image with DALL-E
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            
            # Download image
            response = requests.get(image_url)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.info(f"Image downloaded: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error downloading image: {str(e)}")
            raise
    
    def _post_process_background(self, image_path: str) -> str:
        """Post-process background for video use"""
        
        try:
            # Open and resize image
            with Image.open(image_path) as img:
                # Convert to RGB if necessary
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Resize to exact video resolution
                img_resized = img.resize(self.output_resolution, Image.Resampling.LANCZOS)
                
                # Apply subtle overlay to reduce distraction
                overlay = Image.new('RGBA', self.output_resolution, (255, 255, 255, 30))
                img_with_overlay = Image.alpha_composite(img_resized.convert('RGBA'), overlay)
                
                # Save processed version
                processed_path = image_path.replace('.png', '_processed.png')
                img_with_overlay.convert('RGB').save(processed_path, 'PNG', quality=95)
                
                return processed_path
                
        except Exception as e:
            logger.error(f"Error post-processing background: {str(e)}")
            return image_path  # Return original if processing fails
    
    def create_course_thumbnail(self, course_title: str, course_description: str = "") -> str:
        """
        Create main course thumbnail for platform upload
        
        Args:
            course_title: Title of the course
            course_description: Brief description
            
        Returns:
            Path to course thumbnail
        """
        try:
            logger.info(f"Creating course thumbnail for: {course_title}")
            
            # Create thumbnail image
            img = Image.new('RGB', self.thumbnail_resolution, color='#667eea')
            draw = ImageDraw.Draw(img)
            
            # Apply gradient background
            self._apply_gradient_background(img, ['#4facfe', '#00f2fe'])
            
            # Load fonts
            title_font = self._load_font('title', 64)
            subtitle_font = self._load_font('subtitle', 32)
            
            # Calculate positioning
            img_width, img_height = self.thumbnail_resolution
            center_x = img_width // 2
            center_y = img_height // 2
            
            # Wrap and draw title
            wrapped_title = self._wrap_text(course_title, title_font, img_width - 100)
            title_y = center_y - 60
            
            for line in wrapped_title:
                line_bbox = draw.textbbox((0, 0), line, font=title_font)
                line_width = line_bbox[2] - line_bbox[0]
                
                # Add text shadow
                draw.text((center_x - line_width // 2 + 2, title_y + 2), 
                         line, font=title_font, fill='#333333', anchor='mm')
                # Main text
                draw.text((center_x - line_width // 2, title_y), 
                         line, font=title_font, fill='white', anchor='mm')
                title_y += 70
            
            # Add "COMPLETE COURSE" badge
            badge_text = "COMPLETE COURSE"
            badge_bbox = draw.textbbox((0, 0), badge_text, font=subtitle_font)
            badge_width = badge_bbox[2] - badge_bbox[0]
            badge_height = badge_bbox[3] - badge_bbox[1]
            
            # Badge background
            badge_x = center_x - badge_width // 2 - 20
            badge_y = title_y + 40
            draw.rounded_rectangle(
                [badge_x, badge_y, badge_x + badge_width + 40, badge_y + badge_height + 20],
                radius=10, fill='#f5576c'
            )
            
            # Badge text
            draw.text((center_x, badge_y + badge_height // 2 + 10), 
                     badge_text, font=subtitle_font, fill='white', anchor='mm')
            
            # Save thumbnail
            filename = "course_thumbnail.png"
            if self.domain:
                clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_domain = clean_domain.replace(' ', '_')
                output_dir = f"output/{clean_domain}/marketing"
            else:
                output_dir = "output/marketing"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            img.save(output_path, 'PNG', quality=95)
            
            logger.info(f"Course thumbnail created: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating course thumbnail: {str(e)}")
            return self._create_simple_thumbnail(course_title)
    
    def _create_fallback_background(self, topic: str, lesson_title: str) -> str:
        """Create simple fallback background if generation fails"""
        
        try:
            # Create simple colored background
            img = Image.new('RGB', self.output_resolution, color='#667eea')
            draw = ImageDraw.Draw(img)
            
            # Add simple text
            try:
                font = ImageFont.truetype("Arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Draw topic and lesson
            text = f"{topic}\n{lesson_title}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (self.output_resolution[0] - text_width) // 2
            y = (self.output_resolution[1] - text_height) // 2
            
            draw.text((x, y), text, font=font, fill='white')
            
            # Save fallback
            filename = f"fallback_{topic}_{lesson_title}.png"
            if self.domain:
                clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_domain = clean_domain.replace(' ', '_')
                output_dir = f"output/{clean_domain}/backgrounds/fallback"
            else:
                output_dir = "output/backgrounds/fallback"
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)
            
            img.save(output_path, 'PNG')
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating fallback background: {str(e)}")
            # Return a simple path
            if self.domain:
                clean_domain = "".join(c for c in self.domain if c.isalnum() or c in (' ', '-', '_')).strip()
                clean_domain = clean_domain.replace(' ', '_')
                return f"output/{clean_domain}/backgrounds/fallback/simple_background.png"
            else:
                return "output/backgrounds/fallback/simple_background.png"
    
    def _create_simple_thumbnail(self, course_title: str) -> str:
        """Create simple thumbnail if main creation fails"""
        
        try:
            img = Image.new('RGB', self.thumbnail_resolution, color='#667eea')
            draw = ImageDraw.Draw(img)
            
            # Simple text
            try:
                font = ImageFont.truetype("Arial.ttf", 36)
            except:
                font = ImageFont.load_default()
            
            text = course_title[:30] + "..." if len(course_title) > 30 else course_title
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            
            x = (self.thumbnail_resolution[0] - text_width) // 2
            y = self.thumbnail_resolution[1] // 2
            
            draw.text((x, y), text, font=font, fill='white')
            
            # Save
            output_path = "output/marketing/simple_thumbnail.png"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            img.save(output_path, 'PNG')
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating simple thumbnail: {str(e)}")
            return ""
    
    def _apply_gradient_background(self, img: Image.Image, colors: List[str]) -> None:
        """Apply gradient background to image"""
        
        try:
            width, height = img.size
            
            # Convert hex colors to RGB
            start_color = tuple(int(colors[0][1:][i:i+2], 16) for i in (0, 2, 4))
            end_color = tuple(int(colors[1][1:][i:i+2], 16) for i in (0, 2, 4))
            
            # Create gradient
            for y in range(height):
                ratio = y / height
                r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
                g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
                b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
                
                for x in range(width):
                    img.putpixel((x, y), (r, g, b))
                    
        except Exception as e:
            logger.error(f"Error applying gradient: {str(e)}")
    
    def _load_font(self, font_type: str, size: int) -> ImageFont.ImageFont:
        """Load font with fallbacks"""
        
        try:
            if font_type == 'title':
                return ImageFont.truetype("Arial-Bold.ttf", size)
            elif font_type == 'subtitle':
                return ImageFont.truetype("Arial.ttf", size)
            else:
                return ImageFont.truetype("Arial.ttf", size)
        except:
            try:
                return ImageFont.truetype("Arial.ttf", size)
            except:
                return ImageFont.load_default()
    
    def _wrap_text(self, text: str, font: ImageFont.ImageFont, max_width: int) -> List[str]:
        """Wrap text to fit within max_width"""
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = font.getbbox(test_line)
            line_width = bbox[2] - bbox[0]
            
            if line_width > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
                    current_line = []
        
        if current_line:
            lines.append(' '.join(current_line))
        
        return lines 
