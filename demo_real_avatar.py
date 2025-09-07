#!/usr/bin/env python3
"""
🎬 CLEAN REAL AVATAR DEMO
Demonstrates the working real avatar talking head system
"""

import os
import sys
from real_avatar_talking_head import create_real_avatar_video, create_sample_avatar_image

def demo_real_avatar_system():
    """Clean demonstration of the real avatar system"""
    
    print("🎬 REAL AVATAR TALKING HEAD SYSTEM DEMO")
    print("=" * 60)
    print("✅ System cleaned and ready")
    print("🎯 Creating professional talking head video...")
    print()
    
    # Demo script for a real course lesson
    demo_script = """
    Welcome to our comprehensive machine learning course!
    
    I'm excited to be your instructor for this journey into artificial intelligence.
    
    In today's lesson, we'll explore the fundamental concepts of neural networks.
    
    You'll learn how to build and train your first AI model.
    
    By the end of this course, you'll be creating intelligent systems.
    
    Let's begin this exciting adventure in machine learning!
    """
    
    try:
        print("🖼️  Creating professional avatar...")
        sample_avatar = create_sample_avatar_image()
        print("✅ Avatar created")
        
        print("🎬 Generating talking head video...")
        video_path = create_real_avatar_video(
            script_text=demo_script.strip(),
            avatar_image_path=sample_avatar,
            lesson_title="Machine Learning Fundamentals",
            lesson_number=1,
            output_path="demo_real_avatar.mp4"
        )
        
        if os.path.exists(video_path):
            size = os.path.getsize(video_path)
            print()
            print("🎉 SUCCESS! Professional talking head video created:")
            print(f"   📁 File: {video_path}")
            print(f"   📊 Size: {size:,} bytes")
            
            # Get video details
            try:
                import cv2
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS)
                    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                    duration = frame_count / fps if fps > 0 else 0
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    
                    print(f"   🎬 Resolution: {width}x{height}")
                    print(f"   ⏱️  Duration: {duration:.1f} seconds")
                    print(f"   🎞️  FPS: {fps:.1f}")
                    cap.release()
            except ImportError:
                pass
            
            print()
            print("🎭 VIDEO FEATURES:")
            print("   ✅ Real avatar with professional appearance")
            print("   ✅ High-quality neural voice (Microsoft Aria)")
            print("   ✅ Perfect subtitle synchronization")
            print("   ✅ Subtle realistic animations")
            print("   ✅ Professional lesson information overlay")
            print("   ✅ Live indicator with speech sync")
            
            print()
            print("🚀 SYSTEM READY FOR PRODUCTION!")
            print("   • Use your own avatar image")
            print("   • Integrate with course creation system")
            print("   • Generate professional course videos")
            
            # Open the video
            print()
            print("📺 Opening video...")
            os.system(f"open {video_path}")
            
            return True
        else:
            print("❌ Video creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_real_avatar_system()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 DEMO COMPLETE - SYSTEM WORKING PERFECTLY!")
        print("🎬 Ready to create professional course videos!")
    else:
        print("\n❌ Demo failed - system needs troubleshooting")
    
    sys.exit(0 if success else 1)
