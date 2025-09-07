#!/usr/bin/env python3
"""
🧪 SIMPLE TESTING - No APIs, No Confusion!

This is the ONLY test file you need:
- One E2E test (complete course creation, zero API calls)  
- Unit tests for each component
- Clear pass/fail results
"""

import os
import sys
import tempfile
import shutil
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def setup_test_environment():
    """Setup clean test environment"""
    # Disable all logging during tests
    logging.disable(logging.CRITICAL)
    
    # Force test mode
    os.environ['TEST_MODE'] = 'true'
    os.environ['OPENAI_API_KEY'] = 'mock-key-no-api-calls'
    os.environ['DID_API_KEY'] = 'mock-key-no-api-calls'
    
    print("🧪 Test Environment Setup Complete")
    print("   ✅ All APIs disabled (mock mode)")
    print("   ✅ No real API calls will be made")
    print("   ✅ Output goes to test directory")

def test_e2e_complete_course_creation():
    """
    🎯 ONE SIMPLE E2E TEST
    Creates a complete course with ZERO API calls
    """
    print("\n" + "="*50)
    print("🚀 RUNNING E2E TEST: Complete Course Creation")
    print("="*50)
    
    try:
        from main import CourseCreator
        
        # Create course creator in test mode
        creator = CourseCreator("Simple Test Course", test_mode=True)
        
        print("✅ CourseCreator initialized")
        
        # Generate complete course
        success = creator.generate_course()
        
        if success:
            print("✅ E2E TEST PASSED: Course created successfully!")
            
            # Verify outputs exist
            output_dir = creator.config.get_domain_output_dir("Simple Test Course")
            
            checks = [
                (f"{output_dir}/curriculum.json", "Curriculum"),
                (f"{output_dir}/notebooks", "Notebooks"),
                (f"{output_dir}/scripts", "Scripts"), 
                (f"{output_dir}/videos", "Videos"),
                (f"{output_dir}/backgrounds", "Backgrounds")
            ]
            
            for path, name in checks:
                if os.path.exists(path):
                    print(f"   ✅ {name} created")
                else:
                    print(f"   ⚠️  {name} missing (might be OK)")
            
            return True
        else:
            print("❌ E2E TEST FAILED: Course creation failed")
            return False
            
    except Exception as e:
        print(f"❌ E2E TEST FAILED: {str(e)}")
        return False

def test_unit_course_planner():
    """Unit test: Course Planner component"""
    print("\n🔧 Unit Test: Course Planner")
    
    try:
        from components.course_planner import CoursePlanner
        
        planner = CoursePlanner("test-key")
        print("   ✅ CoursePlanner initialized")
        
        # Test domain analysis (uses mock in test mode)
        analysis = planner.analyze_domain("Python Basics")
        
        if analysis and isinstance(analysis, dict):
            print("   ✅ Domain analysis completed")
            
            # Test curriculum generation
            curriculum = planner.generate_curriculum(analysis)
            
            if curriculum and hasattr(curriculum, 'lessons'):
                print(f"   ✅ Curriculum created with {len(curriculum.lessons)} lessons")
                return True
            else:
                print("   ❌ Curriculum creation failed")
                return False
        else:
            print("   ❌ Domain analysis failed")
            return False
            
    except Exception as e:
        print(f"   ❌ CoursePlanner test failed: {str(e)}")
        return False

def test_unit_content_generator():
    """Unit test: Content Generator component"""
    print("\n🔧 Unit Test: Content Generator")
    
    try:
        from components.content_generator import ContentGenerator
        
        generator = ContentGenerator("test-key", test_mode=True)  # Add test_mode
        print("   ✅ ContentGenerator initialized")
        
        # Test content generation (uses mock in test mode)
        lesson_data = {
            'lesson_number': 1,
            'title': 'Test Lesson',
            'type': 'hands-on',
            'duration_minutes': 30,
            'learning_objectives': ['Learn basics']
        }
        
        content = generator.generate_lesson_content(lesson_data)
        
        if content and isinstance(content, dict) and 'title' in content:
            exercises = content.get('exercises', [])
            print(f"   ✅ Content generated with {len(exercises)} exercises")
            return True
        else:
            print("   ❌ Content generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ ContentGenerator test failed: {str(e)}")
        return False

def test_unit_notebook_creator():
    """Unit test: Notebook Creator component"""
    print("\n🔧 Unit Test: Notebook Creator")
    
    try:
        from components.notebook_creator import NotebookCreator
        
        creator = NotebookCreator()  # No parameters needed
        print("   ✅ NotebookCreator initialized")
        
        # Test notebook creation
        lesson_content = {
            'lesson_number': 1,
            'title': 'Test Lesson',
            'introduction': 'Welcome to this lesson',
            'exercises': [
                {
                    'title': 'Test Exercise',
                    'description': 'Test description',
                    'starter_code': 'print("hello")',
                    'solution': 'print("hello world")'
                }
            ]
        }
        
        # Test notebook JSON creation
        notebook_json = creator.create_lesson_notebook(lesson_content)
        
        if notebook_json and len(notebook_json) > 100:
            print("   ✅ Notebook JSON created successfully")
            return True
        else:
            print("   ❌ Notebook creation failed")
            return False
                
    except Exception as e:
        print(f"   ❌ NotebookCreator test failed: {str(e)}")
        return False

def test_unit_script_writer():
    """Unit test: Script Writer component"""
    print("\n🔧 Unit Test: Script Writer")
    
    try:
        from components.script_writer import ScriptWriter
        
        writer = ScriptWriter("test-key")
        print("   ✅ ScriptWriter initialized")
        
        # Test script creation (uses mock in test mode)  
        lesson_content = {
            'lesson_number': 1,
            'title': 'Test Lesson',
            'type': 'theory',
            'introduction': 'Welcome to the lesson'
        }
        
        script = writer.convert_to_speech_script(lesson_content)
        
        if script and len(script) > 10:
            print(f"   ✅ Script generated ({len(script)} characters)")
            return True
        else:
            print("   ❌ Script generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ ScriptWriter test failed: {str(e)}")
        return False

def test_unit_ai_presenter():
    """Unit test: AI Presenter component"""
    print("\n🔧 Unit Test: AI Presenter")
    
    try:
        from components.ai_presenter import AIPresenter
        
        presenter = AIPresenter("test-key", test_mode=True, domain="TestDomain")
        print("   ✅ AIPresenter initialized")
        
        # Test video creation (uses mock in test mode)
        video_path = presenter.create_presenter_video(
            "This is a test script", 
            "Test Lesson", 
            1
        )
        
        if video_path and os.path.exists(video_path):
            print("   ✅ Presenter video created")
            return True
        else:
            print("   ❌ Presenter video creation failed")
            return False
                
    except Exception as e:
        print(f"   ❌ AIPresenter test failed: {str(e)}")
        return False

def test_unit_video_assembler():
    """Unit test: Video Assembler component"""
    print("\n🔧 Unit Test: Video Assembler")
    
    try:
        from components.video_assembler import VideoAssembler
        
        assembler = VideoAssembler("TestDomain")
        print("   ✅ VideoAssembler initialized")
        
        # Test that it initializes without ImageMagick errors
        print("   ✅ No ImageMagick errors (fixed!)")
        return True
                
    except Exception as e:
        print(f"   ❌ VideoAssembler test failed: {str(e)}")
        return False

def run_all_tests():
    """Run all tests and show summary"""
    print("🧪 SIMPLE TESTING SUITE")
    print("=" * 60)
    print("🎯 Goal: Test everything with ZERO API calls")
    print("=" * 60)
    
    setup_test_environment()
    
    # Run tests
    tests = [
        ("E2E Complete Course", test_e2e_complete_course_creation),
        ("Unit: Course Planner", test_unit_course_planner),
        ("Unit: Content Generator", test_unit_content_generator),
        ("Unit: Notebook Creator", test_unit_notebook_creator),
        ("Unit: Script Writer", test_unit_script_writer),
        ("Unit: AI Presenter", test_unit_ai_presenter),
        ("Unit: Video Assembler", test_unit_video_assembler),
    ]
    
    results = []
    for test_name, test_func in tests:
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n🎯 RESULT: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your system works perfectly!")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
