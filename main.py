#!/usr/bin/env python3
"""
AI Course Creator - Main Orchestrator
Automatically generates complete online courses from domain input
"""

import os
import sys
import time
import logging
import argparse
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.course_planner import CoursePlanner, Curriculum
from components.content_generator import ContentGenerator
from components.notebook_creator import NotebookCreator
from components.script_writer import ScriptWriter
from components.background_generator import BackgroundGenerator
from components.ai_presenter import AIPresenter
from components.video_assembler import VideoAssembler
from components.course_packager import CoursePackager
from config import get_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('course_creation.log')
    ]
)

logger = logging.getLogger(__name__)

class CourseCreator:
    """
    Main orchestrator for course creation
    """
    
    def __init__(self, domain: str, test_mode: bool = False):
        """Initialize course creator"""
        self.domain = domain
        self.config = get_config()
        
        # Override test mode if specified
        if test_mode:
            self.config.test_mode = True
        
        # Debug options
        self.max_lessons = None
        self.start_from_step = 1
        self.skip_steps = []
        self.retry_count = 3
        self.timeout = 300
        
        # Initialize components
        self._initialize_components()
        
        # Course data storage
        self.course_data = {}
        
        logger.info(f"Course Creator initialized for domain: {domain}")
        logger.info(f"Test mode: {self.config.test_mode}")
    
    def _initialize_components(self):
        """Initialize all system components"""
        
        try:
            # Get API keys
            openai_key = self.config.get_api_key('openai')
            did_key = self.config.get_api_key('did')
            
            if not self.config.test_mode and not openai_key:
                raise ValueError("OpenAI API key required for production mode")
            
            # Initialize components with test mode override and domain parameter
            self.course_planner = CoursePlanner(openai_key)
            self.content_generator = ContentGenerator(openai_key, test_mode=self.config.test_mode)
            self.notebook_creator = NotebookCreator()
            self.script_writer = ScriptWriter(openai_key, test_mode=self.config.test_mode)
            self.background_generator = BackgroundGenerator(openai_key, test_mode=self.config.test_mode, domain=self.domain)
            self.ai_presenter = AIPresenter(did_key, test_mode=self.config.test_mode, domain=self.domain, use_opensource=True)
            self.video_assembler = VideoAssembler(domain=self.domain)
            self.course_packager = CoursePackager(domain=self.domain)
            
            logger.info("All components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing components: {str(e)}")
            raise
    
    def generate_course(self) -> bool:
        """
        Generate complete course
        
        Returns:
            True if successful, False otherwise
        """
        try:
            start_time = time.time()
            logger.info(f"🚀 Starting course generation for: {self.domain}")
            
            # Step 1: Plan course structure
            logger.info("📋 Step 1: Planning course structure...")
            domain_analysis = self.course_planner.analyze_domain(self.domain)
            curriculum = self.course_planner.generate_curriculum(domain_analysis)
            
            # Apply lesson limit if specified
            if self.max_lessons and len(curriculum.lessons) > self.max_lessons:
                original_lessons = len(curriculum.lessons)
                curriculum.lessons = curriculum.lessons[:self.max_lessons]
                logger.info(f"🔍 Limited lessons from {original_lessons} to {self.max_lessons}")
            
            self.course_data['course_info'] = curriculum.model_dump()
            self.course_data['domain_analysis'] = domain_analysis
            
            logger.info(f"✅ Course structure planned: {curriculum.course_title}")
            logger.info(f"   Lessons: {len(curriculum.lessons)}")
            logger.info(f"   Duration: {curriculum.total_duration_hours:.1f} hours")
            
            # Step 2: Generate lesson content
            logger.info("📝 Step 2: Generating lesson content...")
            lesson_contents = {}
            for lesson in curriculum.lessons:
                lesson_data = lesson.model_dump()
                content = self.content_generator.generate_lesson_content(lesson_data)
                lesson_contents[lesson.lesson_number] = content
                
                logger.info(f"   Generated content for lesson {lesson.lesson_number}: {lesson.title}")
            
            self.course_data['content'] = lesson_contents
            
            # Step 3: Create course description
            logger.info("📖 Step 3: Creating course description...")
            course_description = self.content_generator.create_course_description(curriculum.model_dump())
            self.course_data['course_info']['description'] = course_description
            
            # Step 4: Generate speech scripts
            logger.info("🎭 Step 4: Generating speech scripts...")
            lesson_scripts = {}
            lesson_titles = {}
            
            for lesson_num, content in lesson_contents.items():
                script = self.script_writer.convert_to_speech_script(content)
                lesson_scripts[lesson_num] = script
                lesson_titles[lesson_num] = content.get('title', f'Lesson {lesson_num}')
                
                # Estimate script duration
                duration = self.script_writer.estimate_script_duration(script)
                logger.info(f"   Script for lesson {lesson_num}: {duration:.1f} minutes")
            
            self.course_data['scripts'] = lesson_scripts
            
            # Step 5: Create Jupyter notebooks
            logger.info("📓 Step 5: Creating Jupyter notebooks...")
            lesson_notebooks = {}
            
            for lesson_num, content in lesson_contents.items():
                if content.get('has_coding', False):
                    notebook = self.notebook_creator.create_lesson_notebook(content)
                    lesson_notebooks[lesson_num] = notebook
                    logger.info(f"   Notebook created for lesson {lesson_num}")
                else:
                    logger.info(f"   Skipping notebook for lesson {lesson_num} (no coding)")
            
            self.course_data['notebooks'] = lesson_notebooks
            
            # Step 6: Generate background images
            logger.info("🎨 Step 6: Generating background images...")
            lesson_backgrounds = {}
            
            for lesson_num, content in lesson_contents.items():
                background = self.background_generator.generate_topic_background(
                    self.domain, 
                    content.get('title', f'Lesson {lesson_num}')
                )
                lesson_backgrounds[lesson_num] = background
                logger.info(f"   Background generated for lesson {lesson_num}")
            
            self.course_data['backgrounds'] = lesson_backgrounds
            
            # Step 7: Create course thumbnail
            logger.info("🖼️ Step 7: Creating course thumbnail...")
            thumbnail = self.background_generator.create_course_thumbnail(
                curriculum.course_title,
                course_description
            )
            self.course_data['thumbnails'] = {'course_thumbnail': thumbnail}
            
            # Step 8: Generate AI presenter videos
            logger.info("🎬 Step 8: Generating AI presenter videos...")
            lesson_videos = {}
            
            # Create videos in batch
            video_paths = self.ai_presenter.batch_create_videos(lesson_scripts, lesson_titles)
            
            for lesson_num, video_path in video_paths.items():
                if video_path:
                    lesson_videos[lesson_num] = video_path
                    logger.info(f"   Video created for lesson {lesson_num}")
                else:
                    logger.warning(f"   Failed to create video for lesson {lesson_num}")
            
            self.course_data['videos'] = lesson_videos
            
            # Step 9: Assemble final videos
            logger.info("🎬 Step 9: Assembling final videos...")
            final_videos = {}
            
            for lesson_num, presenter_video in lesson_videos.items():
                if lesson_num in lesson_backgrounds:
                    background = lesson_backgrounds[lesson_num]
                    lesson_title = lesson_titles.get(lesson_num, f'Lesson {lesson_num}')
                    
                    final_video = self.video_assembler.compose_final_video(
                        presenter_video, background, lesson_title, lesson_num
                    )
                    final_videos[lesson_num] = final_video
                    logger.info(f"   Final video assembled for lesson {lesson_num}")
            
            self.course_data['final_videos'] = final_videos
            
            # Step 10: Create course package
            logger.info("📦 Step 10: Creating course package...")
            package_path = self.course_packager.create_course_package(self.course_data, self.domain)
            
            # Calculate total time
            total_time = time.time() - start_time
            total_time_minutes = total_time / 60
            
            logger.info(f"✅ Course generation completed successfully!")
            logger.info(f"   Total time: {total_time_minutes:.1f} minutes")
            logger.info(f"   Package location: {package_path}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Course generation failed: {str(e)}")
            return False
    
    def get_course_summary(self) -> Dict[str, Any]:
        """Get summary of generated course"""
        
        if not self.course_data:
            return {"error": "No course data available"}
        
        course_info = self.course_data.get('course_info', {})
        
        summary = {
            "domain": self.domain,
            "course_title": course_info.get('course_title', 'Unknown'),
            "total_lessons": len(course_info.get('lessons', [])),
            "duration_hours": course_info.get('total_duration_hours', 0),
            "difficulty": course_info.get('difficulty', 'Unknown'),
            "target_audience": course_info.get('target_audience', 'Unknown'),
            "generated_materials": {
                "videos": len(self.course_data.get('videos', {})),
                "notebooks": len(self.course_data.get('notebooks', {})),
                "backgrounds": len(self.course_data.get('backgrounds', {})),
                "scripts": len(self.course_data.get('scripts', {}))
            }
        }
        
        return summary
    
    def show_generation_plan(self):
        """Show what would be generated without creating files"""
        logger.info("🔍 DRY RUN - Generation Plan")
        logger.info("=" * 50)
        logger.info(f"Domain: {self.domain}")
        logger.info(f"Test Mode: {self.config.test_mode}")
        logger.info(f"Max Lessons: {self.max_lessons or 'All'}")
        logger.info(f"Start From Step: {self.start_from_step}")
        logger.info(f"Skip Steps: {self.skip_steps or 'None'}")
        logger.info(f"Retry Count: {self.retry_count}")
        logger.info(f"Timeout: {self.timeout} seconds")
        logger.info("=" * 50)
        logger.info("This would generate a complete course with all components.")
        logger.info("Use --test flag to run with mock clients.")

def main():
    """Main entry point with debug options"""
    
    parser = argparse.ArgumentParser(description='AI Course Creator with Debug Options')
    
    # Basic arguments
    parser.add_argument('--domain', required=True, help='Course domain/topic')
    parser.add_argument('--test', action='store_true', help='Run in test mode')
    parser.add_argument('--test-e2e', action='store_true', help='Run end-to-end test')
    
    # Debug arguments
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--step', type=int, help='Start from specific step (1-10)')
    parser.add_argument('--max-lessons', type=int, help='Limit number of lessons to generate')
    parser.add_argument('--skip-steps', nargs='+', help='Skip specific steps (e.g., --skip-steps 6 7 8)')
    parser.add_argument('--retry-count', type=int, default=3, help='Number of retries for content generation')
    parser.add_argument('--timeout', type=int, default=300, help='Timeout in seconds for each step')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated without creating files')
    parser.add_argument('--log-file', help='Save logs to specific file')
    
    args = parser.parse_args()
    
    # Setup logging based on debug arguments
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('components').setLevel(logging.DEBUG)
        logging.getLogger('mocks').setLevel(logging.DEBUG)
    
    if args.verbose:
        # Add console handler with more detailed formatting
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logging.getLogger().addHandler(console_handler)
    
    if args.log_file:
        # Add file handler
        file_handler = logging.FileHandler(args.log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logging.getLogger().addHandler(file_handler)
    
    # Log debug arguments
    if args.debug:
        logger.info("🔍 Debug mode enabled")
        logger.info(f"Arguments: {vars(args)}")
    
    try:
        if args.test_e2e:
            # Run end-to-end test
            logger.info("🧪 Running end-to-end test...")
            creator = CourseCreator("Test Course", test_mode=True)
            success = creator.generate_course()
            
            if success:
                logger.info("✅ End-to-end test passed!")
                summary = creator.get_course_summary()
                logger.info(f"Test summary: {summary}")
            else:
                logger.error("❌ End-to-end test failed!")
                sys.exit(1)
        else:
            # Normal course generation with debug options
            creator = CourseCreator(args.domain, test_mode=args.test)
            
            # Apply debug options
            if args.max_lessons:
                creator.max_lessons = args.max_lessons
                logger.info(f"🔍 Limiting to {args.max_lessons} lessons")
            
            if args.step:
                creator.start_from_step = args.step
                logger.info(f"🔍 Starting from step {args.step}")
            
            if args.skip_steps:
                creator.skip_steps = [int(s) for s in args.skip_steps]
                logger.info(f"🔍 Skipping steps: {args.skip_steps}")
            
            if args.retry_count:
                creator.retry_count = args.retry_count
                logger.info(f"🔍 Setting retry count to {args.retry_count}")
            
            if args.timeout:
                creator.timeout = args.timeout
                logger.info(f"🔍 Setting timeout to {args.timeout} seconds")
            
            if args.dry_run:
                logger.info("🔍 Dry run mode - showing generation plan...")
                creator.show_generation_plan()
                return
            
            success = creator.generate_course()
            
            if success:
                logger.info("🎉 Course created successfully!")
                summary = creator.get_course_summary()
                logger.info(f"Course summary: {summary}")
            else:
                logger.error("💥 Course creation failed!")
                sys.exit(1)
                
    except KeyboardInterrupt:
        logger.info("⏹️ Course generation interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 