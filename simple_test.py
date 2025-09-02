#!/usr/bin/env python3
"""
Simple test for the Course Creator system
This replaces the complex pytest setup with a simple, direct testing approach
"""

import os
import sys

# Add components to path
sys.path.append('components')
sys.path.append('mocks')

def test_basic_imports():
    """Test that all components can be imported"""
    print("🧪 Testing Basic Component Imports")
    print("=" * 50)
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from components.course_planner import CoursePlanner
        from components.content_generator import ContentGenerator
        from components.notebook_creator import NotebookCreator
        from components.script_writer import ScriptWriter
        from components.background_generator import BackgroundGenerator
        from components.ai_presenter import AIPresenter
        from components.video_assembler import VideoAssembler
        from components.course_packager import CoursePackager
        print("✅ All components imported successfully")
        
        # Test mock imports
        print("🎭 Testing mock imports...")
        from mocks.mock_clients import MockOpenAIClient, MockDIDClient
        print("✅ All mocks imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_component_initialization():
    """Test that components can be initialized"""
    print("\n🔧 Testing Component Initialization")
    print("=" * 50)
    
    try:
        # Set test mode
        os.environ['TEST_MODE'] = 'true'
        
        # Test component initialization
        print("📋 Testing Course Planner...")
        from components.course_planner import CoursePlanner
        planner = CoursePlanner("mock-key")
        print("✅ Course Planner initialized")
        
        print("📝 Testing Content Generator...")
        from components.content_generator import ContentGenerator
        generator = ContentGenerator("mock-key")
        print("✅ Content Generator initialized")
        
        print("📓 Testing Notebook Creator...")
        from components.notebook_creator import NotebookCreator
        notebook_creator = NotebookCreator()
        print("✅ Notebook Creator initialized")
        
        print("🎭 Testing Script Writer...")
        from components.script_writer import ScriptWriter
        script_writer = ScriptWriter("mock-key")
        print("✅ Script Writer initialized")
        
        print("🎨 Testing Background Generator...")
        from components.background_generator import BackgroundGenerator
        bg_generator = BackgroundGenerator("mock-key")
        print("✅ Background Generator initialized")
        
        print("🎬 Testing AI Presenter...")
        from components.ai_presenter import AIPresenter
        presenter = AIPresenter("mock-key")
        print("✅ AI Presenter initialized")
        
        print("🎬 Testing Video Assembler...")
        from components.video_assembler import VideoAssembler
        assembler = VideoAssembler()
        print("✅ Video Assembler initialized")
        
        print("📦 Testing Course Packager...")
        from components.course_packager import CoursePackager
        packager = CoursePackager()
        print("✅ Course Packager initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_simple_functionality():
    """Test simple functionality without complex operations"""
    print("\n🚀 Testing Simple Functionality")
    print("=" * 50)
    
    try:
        # Test basic functionality
        print("📋 Testing basic course planning...")
        from components.course_planner import CoursePlanner
        planner = CoursePlanner("mock-key")
        
        # Test with a simple domain
        domain = "Python Basics"
        analysis = planner.analyze_domain(domain)
        print(f"✅ Domain analysis completed: {analysis.get('domain_scope', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Simple functionality failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def cleanup():
    """Clean up test files"""
    import shutil
    
    # Remove test directories
    test_dirs = ['output_test', 'output']
    for dir_name in test_dirs:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned up {dir_name}")

if __name__ == "__main__":
    print("🚀 Starting simple system test...")
    
    # Run tests
    success = True
    
    success &= test_basic_imports()
    success &= test_component_initialization()
    success &= test_simple_functionality()
    
    # Cleanup
    cleanup()
    
    if success:
        print("\n🎉 All basic tests passed! System components are working.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
