#!/usr/bin/env python3
"""
End-to-End Test for AI Course Creator
Tests the complete workflow without external API calls
"""

import os
import sys
import logging
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from components.course_planner import CoursePlanner
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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def run_e2e_test():
    """Run complete end-to-end test"""
    
    try:
        logger.info("🧪 Starting End-to-End Test")
        logger.info("=" * 50)
        
        # Force test mode
        os.environ['TEST_MODE'] = 'true'
        
        # Get config
        config = get_config()
        logger.info(f"Test mode: {config.test_mode}")
        
        # Test data
        test_domain = "Python Programming Fundamentals"
        test_api_key = "test-key-12345"
        
        # Step 1: Test Course Planner
        logger.info("📋 Testing Course Planner...")
        planner = CoursePlanner(test_api_key)
        
        domain_analysis = planner.analyze_domain(test_domain)
        assert "domain_scope" in domain_analysis, "Domain analysis failed"
        logger.info(f"✅ Domain analysis: {domain_analysis['domain_scope']}")
        
        curriculum = planner.generate_curriculum(domain_analysis)
        assert len(curriculum.lessons) > 0, "Curriculum generation failed"
        logger.info(f"✅ Curriculum generated: {len(curriculum.lessons)} lessons")
        
        # Step 2: Test Content Generator
        logger.info("📝 Testing Content Generator...")
        content_gen = ContentGenerator(test_api_key)
        
        lesson_content = content_gen.generate_lesson_content(curriculum.lessons[0].model_dump())
        assert "introduction" in lesson_content, "Content generation failed"
        logger.info(f"✅ Lesson content generated: {lesson_content['title']}")
        
        # Step 3: Test Notebook Creator
        logger.info("📓 Testing Notebook Creator...")
        notebook_creator = NotebookCreator()
        
        notebook_content = notebook_creator.create_lesson_notebook(lesson_content)
        assert "cells" in notebook_content, "Notebook creation failed"
        logger.info("✅ Jupyter notebook created")
        
        # Step 4: Test Script Writer
        logger.info("🎭 Testing Script Writer...")
        script_writer = ScriptWriter(test_api_key)
        
        script = script_writer.convert_to_speech_script(lesson_content)
        assert len(script) > 100, "Script generation failed"
        logger.info("✅ Speech script generated")
        
        duration = script_writer.estimate_script_duration(script)
        assert duration > 0, "Script duration estimation failed"
        logger.info(f"✅ Script duration: {duration:.1f} minutes")
        
        # Step 5: Test Background Generator
        logger.info("🎨 Testing Background Generator...")
        bg_generator = BackgroundGenerator(test_api_key)
        
        background = bg_generator.generate_topic_background(test_domain, "Test Lesson")
        assert os.path.exists(background), "Background generation failed"
        logger.info(f"✅ Background generated: {background}")
        
        # Step 6: Test AI Presenter
        logger.info("🎬 Testing AI Presenter...")
        ai_presenter = AIPresenter(test_api_key)
        
        presenter_video = ai_presenter.create_presenter_video(script, "Test Lesson", 1)
        assert os.path.exists(presenter_video), "Presenter video generation failed"
        logger.info(f"✅ Presenter video generated: {presenter_video}")
        
        # Step 7: Test Video Assembler
        logger.info("🎬 Testing Video Assembler...")
        video_assembler = VideoAssembler()
        
        final_video = video_assembler.compose_final_video(
            presenter_video, background, "Test Lesson", 1
        )
        assert os.path.exists(final_video), "Video assembly failed"
        logger.info(f"✅ Final video assembled: {final_video}")
        
        # Step 8: Test Course Packager
        logger.info("📦 Testing Course Packager...")
        packager = CoursePackager()
        
        # Prepare test course data
        test_course_data = {
            'course_info': curriculum.model_dump(),
            'videos': {1: final_video},
            'notebooks': {1: notebook_content},
            'content': {1: lesson_content},
            'scripts': {1: script},
            'backgrounds': {1: background},
            'thumbnails': {'course_thumbnail': background}
        }
        
        package_path = packager.create_course_package(test_course_data)
        assert os.path.exists(package_path), "Course packaging failed"
        logger.info(f"✅ Course package created: {package_path}")
        
        # Test summary
        logger.info("=" * 50)
        logger.info("🎉 End-to-End Test Completed Successfully!")
        logger.info("=" * 50)
        
        # Print test results
        test_results = {
            "Domain Analysis": "✅ PASSED",
            "Curriculum Planning": "✅ PASSED",
            "Content Generation": "✅ PASSED",
            "Notebook Creation": "✅ PASSED",
            "Script Writing": "✅ PASSED",
            "Background Generation": "✅ PASSED",
            "AI Presenter": "✅ PASSED",
            "Video Assembly": "✅ PASSED",
            "Course Packaging": "✅ PASSED"
        }
        
        for test_name, result in test_results.items():
            logger.info(f"{test_name:<25} {result}")
        
        # Cleanup test files
        logger.info("\n🧹 Cleaning up test files...")
        cleanup_test_files()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ End-to-End Test Failed: {str(e)}")
        return False

def cleanup_test_files():
    """Clean up test-generated files"""
    
    try:
        # Remove test output directories
        test_dirs = ["output_test", "output"]
        
        for test_dir in test_dirs:
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir)
                logger.info(f"Removed test directory: {test_dir}")
        
        # Remove test log files
        test_logs = ["course_creation.log"]
        
        for log_file in test_logs:
            if os.path.exists(log_file):
                os.remove(log_file)
                logger.info(f"Removed test log: {log_file}")
        
        logger.info("✅ Test cleanup completed")
        
    except Exception as e:
        logger.warning(f"Warning: Could not complete cleanup: {str(e)}")

def main():
    """Main entry point for E2E test"""
    
    logger.info("🚀 AI Course Creator - End-to-End Test")
    logger.info("This test will verify all components work together")
    logger.info("No external API calls will be made (test mode)")
    
    # Run the test
    success = run_e2e_test()
    
    if success:
        logger.info("🎉 All tests passed! The system is working correctly.")
        return True
    else:
        logger.error("💥 Some tests failed. Please check the logs above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
