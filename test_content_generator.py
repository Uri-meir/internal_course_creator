#!/usr/bin/env python3
"""
Test Content Generator Component
Verifies that different content is generated for each lesson
"""

import os
import sys
import json
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from components.content_generator import ContentGenerator
from mocks.mock_clients import MockOpenAIClient

def test_content_variety():
    """Test that content generator creates different content for each lesson"""
    
    print("🧪 Testing Content Generator Variety")
    print("=" * 50)
    
    mock_api_key = "mock_key_for_testing"
    content_gen = ContentGenerator(mock_api_key, test_mode=True)
    
    # Test with different lesson types and titles
    test_lessons = [
        {
            "lesson_number": 1,
            "title": "Introduction to Python and Setup",
            "type": "theory",
            "duration_minutes": 30
        },
        {
            "lesson_number": 2,
            "title": "Variables, Data Types, and Basic Operations",
            "type": "theory",
            "duration_minutes": 30
        },
        {
            "lesson_number": 3,
            "title": "Control Flow: Conditionals and Loops",
            "type": "hands-on",
            "duration_minutes": 30
        },
        {
            "lesson_number": 4,
            "title": "Functions and Scope",
            "type": "hands-on",
            "duration_minutes": 30
        }
    ]
    
    generated_contents = {}
    
    for lesson in test_lessons:
        print(f"\n📝 Generating content for: {lesson['title']}")
        print("-" * 40)
        
        try:
            content = content_gen.generate_lesson_content(lesson)
            generated_contents[lesson['lesson_number']] = content
            
            if content:
                print(f"✅ Content generated successfully")
                print(f"   Title: {content.get('title', 'N/A')}")
                print(f"   Type: {content.get('type', 'N/A')}")
                print(f"   Introduction: {content.get('introduction', 'N/A')[:100]}...")
                
                # Check theory content
                if 'theory_content' in content:
                    theory = content['theory_content']
                    if 'main_concepts' in theory:
                        print(f"   Main Concepts: {theory['main_concepts'][:2]}...")
                
                # Check code examples
                if 'code_examples' in content and content['code_examples']:
                    code_ex = content['code_examples'][0]
                    print(f"   Code Example: {code_ex.get('title', 'N/A')}")
                
                # Check exercises
                if 'exercises' in content and content['exercises']:
                    exercise = content['exercises'][0]
                    print(f"   Exercise: {exercise.get('title', 'N/A')}")
                
            else:
                print("❌ Failed to generate content")
                
        except Exception as e:
            print(f"❌ Error generating content: {str(e)}")
    
    # Analyze content variety
    print("\n🔍 Content Variety Analysis")
    print("=" * 40)
    
    if len(generated_contents) > 1:
        # Check if titles are different
        titles = [content.get('title', '') for content in generated_contents.values()]
        unique_titles = set(titles)
        print(f"   Unique titles: {len(unique_titles)} out of {len(titles)}")
        
        # Check if introductions are different
        introductions = [content.get('introduction', '') for content in generated_contents.values()]
        unique_intros = set(introductions)
        print(f"   Unique introductions: {len(unique_intros)} out of {len(introductions)}")
        
        # Check if theory content varies
        theory_concepts = []
        for content in generated_contents.values():
            if 'theory_content' in content and 'main_concepts' in content['theory_content']:
                theory_concepts.extend(content['theory_content']['main_concepts'])
        
        unique_concepts = set(theory_concepts)
        print(f"   Unique theory concepts: {len(unique_concepts)} out of {len(theory_concepts)}")
        
        # Check if code examples vary
        code_titles = []
        for content in generated_contents.values():
            if 'code_examples' in content and content['code_examples']:
                code_titles.append(content['code_examples'][0].get('title', ''))
        
        unique_code_titles = set(code_titles)
        print(f"   Unique code example titles: {len(unique_code_titles)} out of {len(code_titles)}")
        
        # Overall variety score
        variety_score = (len(unique_titles) + len(unique_intros) + len(unique_concepts) + len(unique_code_titles)) / 4
        print(f"\n📊 Overall Variety Score: {variety_score:.1f}/4.0")
        
        if variety_score >= 3.0:
            print("🎉 Excellent content variety! Each lesson has unique content.")
            return True
        elif variety_score >= 2.0:
            print("✅ Good content variety. Most lessons have different content.")
            return True
        else:
            print("⚠️  Limited content variety. Some lessons may have similar content.")
            return False
    else:
        print("❌ Not enough content generated for analysis")
        return False

if __name__ == "__main__":
    print("🚀 Starting Content Generator Variety Test")
    print("=" * 60)
    
    success = test_content_variety()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Content Generator Variety Test PASSED!")
        sys.exit(0)
    else:
        print("💥 Content Generator Variety Test FAILED!")
        sys.exit(1)
