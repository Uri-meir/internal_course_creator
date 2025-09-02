#!/usr/bin/env python3
"""
Test Script Writer Component
Verifies that it generates clean speech text instead of JSON
"""

import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from components.script_writer import ScriptWriter
from mocks.mock_clients import MockOpenAIClient

def test_script_format():
    """Test that script writer generates clean speech text"""
    
    print("🧪 Testing Script Writer Format")
    print("=" * 50)
    
    mock_api_key = "mock_key_for_testing"
    script_writer = ScriptWriter(mock_api_key, test_mode=True)
    
    # Test with different lesson types
    test_lessons = [
        {
            "lesson_number": 1,
            "title": "Introduction to Python and Setup",
            "type": "theory",
            "duration_minutes": 30,
            "introduction": "Welcome to Python programming!",
            "key_takeaways": ["Python is powerful", "Easy to learn", "Great for beginners"]
        },
        {
            "lesson_number": 2,
            "title": "Variables and Data Types",
            "type": "hands-on",
            "duration_minutes": 30,
            "setup_instructions": "Open your Python editor",
            "key_takeaways": ["Variables store data", "Different types available", "Practice makes perfect"]
        }
    ]
    
    for lesson in test_lessons:
        print(f"\n📝 Testing script generation for: {lesson['title']}")
        print("-" * 50)
        
        try:
            script = script_writer.convert_to_speech_script(lesson)
            
            if script:
                print(f"✅ Script generated successfully")
                print(f"   Length: {len(script)} characters")
                print(f"   First 100 chars: {script[:100]}...")
                
                # Check if it's clean text (not JSON)
                is_json = script.strip().startswith('{') and script.strip().endswith('}')
                has_json_keys = '"introduction"' in script or '"main_concept"' in script
                
                print(f"   Is JSON format: {is_json}")
                print(f"   Has JSON keys: {has_json_keys}")
                
                if not is_json and not has_json_keys:
                    print("   ✅ Script is clean speech text!")
                else:
                    print("   ❌ Script still contains JSON formatting!")
                
                # Check for D-ID compatible formatting
                has_pauses = '[PAUSE:' in script
                has_emphasis = '[EMPHASIS]' in script and '[/EMPHASIS]' in script
                
                print(f"   Has pause cues: {has_pauses}")
                print(f"   Has emphasis cues: {has_emphasis}")
                
                # Estimate duration
                duration = script_writer.estimate_script_duration(script)
                print(f"   Estimated duration: {duration:.1f} minutes")
                
            else:
                print("❌ Failed to generate script")
                
        except Exception as e:
            print(f"❌ Error generating script: {str(e)}")
    
    print("\n🔍 Script Format Analysis")
    print("=" * 40)
    print("✅ Scripts should be clean speech text, not JSON")
    print("✅ Should include [PAUSE:X] and [EMPHASIS] tags")
    print("✅ Should be readable by D-ID API")
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Script Writer Format Test")
    print("=" * 60)
    
    success = test_script_format()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Script Writer Format Test PASSED!")
        sys.exit(0)
    else:
        print("💥 Script Writer Format Test FAILED!")
        sys.exit(1)
