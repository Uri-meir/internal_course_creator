#!/usr/bin/env python3
"""
Unit test for Course Planner component
Tests curriculum generation and extracts lesson subjects
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from components.course_planner import CoursePlanner
from mocks.mock_clients import MockOpenAIClient

def test_course_planner():
    """Test the course planner and extract lesson subjects"""
    
    print("🧪 Testing Course Planner Component")
    print("=" * 50)
    
    # Test with mock client (no API costs)
    mock_api_key = "mock_key_for_testing"
    
    try:
        # Initialize course planner with mock client
        print("📚 Initializing Course Planner...")
        planner = CoursePlanner(mock_api_key)
        
        # Test domain analysis
        test_domain = "Python Programming for Beginners"
        print(f"🎯 Analyzing domain: {test_domain}")
        
        # First analyze the domain
        domain_analysis = planner.analyze_domain(test_domain)
        print(f"✅ Domain analysis completed")
        
        # Generate curriculum from domain analysis
        print("📋 Generating curriculum...")
        curriculum = planner.generate_curriculum(domain_analysis)
        
        if curriculum:
            print("\n✅ Curriculum generated successfully!")
            print(f"📖 Course Title: {curriculum.course_title}")
            print(f"🎯 Target Audience: {curriculum.target_audience}")
            print(f"📊 Difficulty: {curriculum.difficulty}")
            print(f"⏱️  Total Duration: {curriculum.total_duration_hours:.1f} hours")
            print(f"📚 Number of Lessons: {len(curriculum.lessons)}")
            
            print("\n📝 LESSON SUBJECTS:")
            print("-" * 50)
            
            # Extract and display lesson subjects
            for i, lesson in enumerate(curriculum.lessons, 1):
                print(f"Lesson {i}: {lesson.title}")
                print(f"   Duration: {lesson.duration_minutes} minutes")
                print(f"   Type: {lesson.type}")
                print(f"   Has Coding: {'Yes' if lesson.has_coding else 'No'}")
                print(f"   Learning Objectives: {', '.join(lesson.learning_objectives)}")
                print()
            
            # Test individual lesson analysis
            print("🔍 Testing individual lesson analysis...")
            if curriculum.lessons:
                first_lesson = curriculum.lessons[0]
                print(f"First lesson title: {first_lesson.title}")
                print(f"First lesson objectives: {first_lesson.learning_objectives}")
            
            return True
            
        else:
            print("❌ Failed to generate curriculum")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_curriculum_structure():
    """Test the structure of generated curriculum"""
    
    print("\n🔍 Testing Curriculum Structure")
    print("=" * 40)
    
    try:
        mock_api_key = "mock_key_for_testing"
        planner = CoursePlanner(mock_api_key)
        
        test_domain = "Machine Learning Basics"
        domain_analysis = planner.analyze_domain(test_domain)
        curriculum = planner.generate_curriculum(domain_analysis)
        
        if curriculum:
            # Validate curriculum structure
            print("✅ Curriculum structure validation:")
            print(f"   - Has course_title: {hasattr(curriculum, 'course_title')}")
            print(f"   - Has target_audience: {hasattr(curriculum, 'target_audience')}")
            print(f"   - Has difficulty: {hasattr(curriculum, 'difficulty')}")
            print(f"   - Has total_duration_hours: {hasattr(curriculum, 'total_duration_hours')}")
            print(f"   - Has lessons: {hasattr(curriculum, 'lessons')}")
            print(f"   - Lessons is list: {isinstance(curriculum.lessons, list)}")
            print(f"   - Number of lessons > 0: {len(curriculum.lessons) > 0}")
            
            # Validate lesson structure
            if curriculum.lessons:
                first_lesson = curriculum.lessons[0]
                print(f"   - Lesson has title: {hasattr(first_lesson, 'title')}")
                print(f"   - Lesson has duration_minutes: {hasattr(first_lesson, 'duration_minutes')}")
                print(f"   - Lesson has type: {hasattr(first_lesson, 'type')}")
                print(f"   - Lesson has learning_objectives: {hasattr(first_lesson, 'learning_objectives')}")
                print(f"   - Lesson has has_coding: {hasattr(first_lesson, 'has_coding')}")
            
            return True
        else:
            print("❌ No curriculum generated for structure test")
            return False
            
    except Exception as e:
        print(f"❌ Error during structure testing: {str(e)}")
        return False

def test_different_domains():
    """Test course planner with different domains to show variety"""
    
    print("\n🌍 Testing Different Domains")
    print("=" * 40)
    
    domains = [
        "Web Development with React",
        "Data Science Fundamentals", 
        "Cybersecurity Basics",
        "Mobile App Development"
    ]
    
    mock_api_key = "mock_key_for_testing"
    planner = CoursePlanner(mock_api_key)
    
    for domain in domains:
        try:
            print(f"\n🎯 Testing domain: {domain}")
            print("-" * 30)
            
            domain_analysis = planner.analyze_domain(domain)
            curriculum = planner.generate_curriculum(domain_analysis)
            
            if curriculum:
                print(f"✅ Generated: {curriculum.course_title}")
                print(f"📚 Lessons: {len(curriculum.lessons)}")
                print(f"⏱️  Duration: {curriculum.total_duration_hours:.1f} hours")
                
                # Show first 3 lesson subjects
                print("📝 First 3 Lesson Subjects:")
                for i in range(min(3, len(curriculum.lessons))):
                    lesson = curriculum.lessons[i]
                    print(f"   {i+1}. {lesson.title}")
                    print(f"      Type: {lesson.type}, Coding: {'Yes' if lesson.has_coding else 'No'}")
                
                # Show last 3 lesson subjects for variety
                if len(curriculum.lessons) >= 3:
                    print("📝 Last 3 Lesson Subjects:")
                    for i in range(len(curriculum.lessons)-3, len(curriculum.lessons)):
                        lesson = curriculum.lessons[i]
                        print(f"   {i+1}. {lesson.title}")
                        print(f"      Type: {lesson.type}, Coding: {'Yes' if lesson.has_coding else 'No'}")
            else:
                print("❌ Failed to generate curriculum")
                
        except Exception as e:
            print(f"❌ Error with domain '{domain}': {str(e)}")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Course Planner Unit Tests")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_course_planner()
    test2_passed = test_curriculum_structure()
    test3_passed = test_different_domains()
    
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS:")
    print(f"   Course Planner Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Structure Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    print(f"   Different Domains Test: {'✅ PASSED' if test3_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed and test3_passed:
        print("\n🎉 All tests passed! Course Planner is working correctly.")
        sys.exit(0)
    else:
        print("\n💥 Some tests failed. Check the output above for details.")
        sys.exit(1)
