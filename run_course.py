#!/usr/bin/env python3
"""
🚀 SIMPLE COURSE RUNNER

Replace the complicated main.py with 2 simple commands:
1. Create a real course: python3 run_course.py "Your Course Topic"
2. Test everything: python3 simple_test.py

No confusing flags, no API complications!
"""

import sys
import os
import logging

def main():
    if len(sys.argv) != 2:
        print("🚀 SIMPLE COURSE CREATOR")
        print("=" * 50)
        print("Usage:")
        print("  python3 run_course.py \"Your Course Topic\"")
        print("")
        print("Examples:")
        print("  python3 run_course.py \"Python FastAPI Development\"")
        print("  python3 run_course.py \"Machine Learning Basics\"")
        print("  python3 run_course.py \"React Web Development\"")
        print("")
        print("🧪 To test the system:")
        print("  python3 simple_test.py")
        print("")
        sys.exit(1)
    
    course_topic = sys.argv[1]
    
    print(f"🚀 Creating course: {course_topic}")
    print("=" * 60)
    
    # Import and run
    try:
        from main import CourseCreator
        
        # Create course with production settings (no test mode)
        creator = CourseCreator(course_topic, test_mode=False)
        success = creator.generate_course()
        
        if success:
            print("🎉 COURSE CREATED SUCCESSFULLY!")
            summary = creator.get_course_summary()
            print(f"📊 Summary: {summary}")
        else:
            print("❌ COURSE CREATION FAILED!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
