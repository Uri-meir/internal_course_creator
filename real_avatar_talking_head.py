#!/usr/bin/env python3
"""
🎬 REAL AVATAR TALKING HEAD CREATOR
Uses a real photo to create professional talking head videos
"""

import os
import sys
import subprocess
import tempfile
import logging
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_real_avatar_video(script_text: str, avatar_image_path: str, lesson_title: str, 
                           lesson_number: int, output_path: str) -> str:
    """Create talking head video using a real avatar image with subtitles"""
    
    print(f"🎬 Creating real avatar talking head video: {lesson_title}")
    print(f"🖼️  Using avatar: {avatar_image_path}")
    
    try:
        # 1. Create high-quality audio
        audio_path = create_quality_audio(script_text)
        print(f"✅ Audio created: {audio_path}")
        
        # 2. Process the avatar image
        processed_avatar = process_avatar_image(avatar_image_path)
        print(f"✅ Avatar processed: {processed_avatar}")
        
        # 3. Generate subtitles from script
        subtitles = generate_subtitles(script_text, audio_path)
        print(f"✅ Subtitles generated: {len(subtitles)} segments")
        
        # 4. Create animated video with real avatar and subtitles
        video_path = create_animated_avatar_video(processed_avatar, audio_path, subtitles,
                                                lesson_title, lesson_number, output_path)
        print(f"✅ Video created: {video_path}")
        
        return video_path
        
    except Exception as e:
        logger.error(f"Error creating real avatar video: {e}")
        raise

def process_avatar_image(image_path: str) -> str:
    """Process and optimize the avatar image for video use"""
    
    try:
        print("🔄 Processing avatar image...")
        
        # Load the image
        img = Image.open(image_path)
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Resize to optimal video dimensions (maintain aspect ratio)
        target_size = (512, 512)
        
        # Calculate resize to fit within target while maintaining aspect ratio
        img_ratio = img.width / img.height
        target_ratio = target_size[0] / target_size[1]
        
        if img_ratio > target_ratio:
            # Image is wider - fit to width
            new_width = target_size[0]
            new_height = int(target_size[0] / img_ratio)
        else:
            # Image is taller - fit to height
            new_height = target_size[1]
            new_width = int(target_size[1] * img_ratio)
        
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Create a centered image on the target canvas
        canvas = Image.new('RGB', target_size, color=(40, 40, 50))  # Dark background
        
        # Center the image
        x_offset = (target_size[0] - new_width) // 2
        y_offset = (target_size[1] - new_height) // 2
        canvas.paste(img, (x_offset, y_offset))
        
        # Apply subtle enhancements
        # Slight sharpening
        canvas = canvas.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=3))
        
        # Save processed image
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            canvas.save(tmp.name, 'PNG', quality=95)
            processed_path = tmp.name
        
        print(f"✅ Avatar processed to {target_size[0]}x{target_size[1]}")
        return processed_path
        
    except Exception as e:
        logger.error(f"Error processing avatar image: {e}")
        raise

def create_quality_audio(text: str) -> str:
    """Create high-quality audio using modern TTS methods"""
    
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
        audio_path = tmp.name
    
    print(f"🎤 Creating professional TTS audio...")
    
    # Method 1: Try Edge TTS (Microsoft Neural Voices)
    if try_edge_tts_audio(text, audio_path):
        return audio_path
    
    # Method 2: Try macOS say with optimal settings
    if try_macos_say_audio(text, audio_path):
        return audio_path
    
    # Method 3: Try pyttsx3
    if try_pyttsx3_audio(text, audio_path):
        return audio_path
    
    # Fallback
    print("🔧 Creating synthetic speech audio...")
    return create_speech_audio(audio_path, len(text.split()) * 0.4)

def try_edge_tts_audio(text: str, output_path: str) -> bool:
    """Try Microsoft Edge TTS for neural voice"""
    try:
        print("🔄 Trying Edge TTS (Neural Voice)...")
        
        import edge_tts
        import asyncio
        
        async def create_edge_audio():
            communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
            await communicate.save(output_path)
            return True
        
        asyncio.run(create_edge_audio())
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print("✅ Edge TTS neural voice created")
            return True
            
    except Exception as e:
        print(f"⚠️ Edge TTS failed: {e}")
    
    return False

def try_macos_say_audio(text: str, output_path: str) -> bool:
    """Try macOS say with optimal settings"""
    try:
        print("🔄 Trying macOS say (High Quality)...")
        
        import platform
        if platform.system() != "Darwin":
            return False
        
        cmd = [
            'say', '-v', 'Samantha', '-r', '165', '-o', output_path,
            '--data-format=LEF32@22050', text
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0 and os.path.exists(output_path):
            size = os.path.getsize(output_path)
            if size > 1000:
                print(f"✅ macOS say created ({size:,} bytes)")
                return True
        
    except Exception as e:
        print(f"⚠️ macOS say failed: {e}")
    
    return False

def try_pyttsx3_audio(text: str, output_path: str) -> bool:
    """Try pyttsx3 TTS"""
    try:
        print("🔄 Trying pyttsx3 TTS...")
        
        import pyttsx3
        
        engine = pyttsx3.init()
        engine.setProperty('rate', 160)
        engine.setProperty('volume', 0.9)
        
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'english' in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        if os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
            print("✅ pyttsx3 TTS created")
            return True
            
    except Exception as e:
        print(f"⚠️ pyttsx3 failed: {e}")
    
    return False

def create_speech_audio(output_path: str, duration: float) -> str:
    """Create realistic speech-like audio as fallback"""
    
    try:
        import soundfile as sf
        
        sample_rate = 22050
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples)
        
        # Create speech-like waveform
        audio = np.zeros(samples)
        frequencies = [150, 300, 450, 600]
        
        for i, freq in enumerate(frequencies):
            amplitude = 1.0 / (i + 1)
            freq_mod = freq + 10 * np.sin(2 * np.pi * 0.5 * t)
            audio += amplitude * np.sin(2 * np.pi * freq_mod * t)
        
        envelope = np.exp(-0.05 * t) * (1 + 0.2 * np.sin(2 * np.pi * 0.8 * t))
        audio *= envelope
        audio = audio / np.max(np.abs(audio)) * 0.8
        
        sf.write(output_path, audio.astype(np.float32), sample_rate)
        return output_path
        
    except ImportError:
        # Basic WAV fallback
        with open(output_path, 'wb') as f:
            f.write(b'RIFF\x24\x08\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x22\x56\x00\x00\x44\xAC\x00\x00\x02\x00\x10\x00data\x00\x08\x00\x00')
            f.write(b'\x00' * 8192)
        return output_path

def generate_subtitles(script_text: str, audio_path: str) -> list:
    """Generate subtitle segments with improved timing synchronization"""
    
    try:
        print("📝 Generating subtitles with precise timing...")
        
        # Get audio duration
        try:
            import librosa
            y, sr = librosa.load(audio_path)
            duration = len(y) / sr
            print(f"   📏 Audio duration: {duration:.2f} seconds")
        except ImportError:
            # Estimate from file size
            audio_size = os.path.getsize(audio_path)
            duration = max(10, audio_size / 88000)
            print(f"   📏 Estimated duration: {duration:.2f} seconds")
        
        # Clean and split the script into sentences
        sentences = split_into_sentences(script_text)
        
        if not sentences:
            return []
        
        # Calculate more accurate timing based on speech patterns
        subtitles = []
        
        # Calculate words per minute (typical TTS is ~160-180 WPM)
        total_words = sum(len(sentence.split()) for sentence in sentences)
        estimated_wpm = 165  # Conservative estimate for neural TTS
        
        # Add small delay at start (TTS often has brief silence)
        start_delay = 0.5
        current_time = start_delay
        
        for i, sentence in enumerate(sentences):
            words = len(sentence.split())
            
            # Calculate duration based on word count and speaking rate
            sentence_duration = (words / estimated_wpm) * 60
            
            # Add natural pauses
            if sentence.endswith('.') or sentence.endswith('!'):
                sentence_duration += 0.8  # Longer pause for sentence endings
            elif sentence.endswith(',') or sentence.endswith(';'):
                sentence_duration += 0.4  # Shorter pause for commas
            
            # Minimum duration for readability
            sentence_duration = max(sentence_duration, 1.5)
            
            # Ensure we don't exceed total duration
            if current_time + sentence_duration > duration - 0.5:
                sentence_duration = duration - current_time - 0.5
            
            subtitles.append({
                'start': current_time,
                'end': current_time + sentence_duration,
                'text': sentence.strip(),
                'words': words
            })
            
            current_time += sentence_duration
        
        # Debug timing information
        print(f"   📊 Total words: {total_words}")
        print(f"   🎯 Estimated WPM: {estimated_wpm}")
        print(f"   ⏱️  Subtitle timing: {subtitles[0]['start']:.1f}s to {subtitles[-1]['end']:.1f}s")
        
        print(f"✅ Generated {len(subtitles)} subtitle segments with precise timing")
        return subtitles
        
    except Exception as e:
        print(f"⚠️ Subtitle generation failed: {e}")
        return []

def split_into_sentences(text: str) -> list:
    """Split text into natural sentences for subtitles"""
    
    import re
    
    # Clean the text
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Split by sentence endings
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter sentences
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence and len(sentence) > 3:  # Ignore very short fragments
            # Limit sentence length for readability
            if len(sentence) > 80:
                # Split long sentences at natural breaks
                parts = re.split(r'[,;:]', sentence)
                for part in parts:
                    part = part.strip()
                    if part and len(part) > 3:
                        clean_sentences.append(part)
            else:
                clean_sentences.append(sentence)
    
    return clean_sentences

def create_animated_avatar_video(avatar_path: str, audio_path: str, subtitles: list,
                               lesson_title: str, lesson_number: int, output_path: str) -> str:
    """Create animated video using the real avatar"""
    
    try:
        # Get audio duration
        try:
            import librosa
            y, sr = librosa.load(audio_path)
            duration = len(y) / sr
        except ImportError:
            # Estimate from file size
            audio_size = os.path.getsize(audio_path)
            duration = max(10, audio_size / 88000)
    
        print(f"📏 Video duration: {duration:.1f} seconds")
        
        # Video properties
        width, height = 512, 512
        fps = 24
        total_frames = int(duration * fps)
        
        # Load avatar image
        avatar_img = cv2.imread(avatar_path)
        if avatar_img is None:
            raise Exception(f"Could not load avatar image: {avatar_path}")
        
        # Create video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter('temp_avatar_video.mp4', fourcc, fps, (width, height))
        
        print(f"🎬 Creating {total_frames} frames with real avatar and subtitles...")
        
        for frame_num in range(total_frames):
            current_time = frame_num / fps
            frame = create_avatar_frame_with_subtitles(avatar_img, frame_num, total_frames, 
                                                     current_time, subtitles, lesson_title, 
                                                     lesson_number, width, height)
            video_writer.write(frame)
            
            # Progress update
            if frame_num % (fps * 2) == 0:
                progress = (frame_num / total_frames) * 100
                print(f"   Progress: {progress:.1f}%")
        
        video_writer.release()
        
        # Combine with audio using MoviePy
        print("🎵 Adding audio to avatar video...")
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
            
            video_clip = VideoFileClip('temp_avatar_video.mp4')
            audio_clip = AudioFileClip(audio_path)
            
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', 
                                     verbose=False, logger=None)
            
            video_clip.close()
            audio_clip.close()
            final_clip.close()
            
            if os.path.exists('temp_avatar_video.mp4'):
                os.remove('temp_avatar_video.mp4')
            
            print("✅ Avatar video with audio created successfully")
            return output_path
            
        except Exception as e:
            print(f"⚠️ MoviePy failed: {e}")
            if os.path.exists('temp_avatar_video.mp4'):
                os.rename('temp_avatar_video.mp4', output_path)
                print("✅ Avatar video created (without audio)")
                return output_path
            else:
                raise Exception("Failed to create video")
    
    except Exception as e:
        logger.error(f"Error creating animated avatar video: {e}")
        raise

def create_avatar_frame_with_subtitles(avatar_img: np.ndarray, frame_num: int, total_frames: int,
                                     current_time: float, subtitles: list, lesson_title: str, 
                                     lesson_number: int, width: int, height: int) -> np.ndarray:
    """Create a single frame with the real avatar, animations, and subtitles"""
    
    # Animation time
    t = frame_num / 24.0
    
    # Create base frame with avatar
    frame = avatar_img.copy()
    
    # Ensure correct size
    if frame.shape[:2] != (height, width):
        frame = cv2.resize(frame, (width, height))
    
    # Add subtle animations
    
    # 1. Breathing effect (very subtle scale change)
    breathing = 1.0 + 0.01 * np.sin(2 * np.pi * 0.3 * t)  # Slow breathing
    if breathing != 1.0:
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, 0, breathing)
        frame = cv2.warpAffine(frame, M, (width, height))
    
    # 2. Subtle head movement (very small)
    head_movement_x = int(2 * np.sin(2 * np.pi * 0.1 * t))  # Very slow, small movement
    head_movement_y = int(1 * np.sin(2 * np.pi * 0.15 * t))
    
    if head_movement_x != 0 or head_movement_y != 0:
        M = np.float32([[1, 0, head_movement_x], [0, 1, head_movement_y]])
        frame = cv2.warpAffine(frame, M, (width, height))
    
    # 3. Find current subtitle with slight timing adjustment
    current_subtitle = None
    # Adjust timing to account for any processing delay
    adjusted_time = current_time - 0.1  # Small adjustment to sync better
    
    for subtitle in subtitles:
        if subtitle['start'] <= adjusted_time <= subtitle['end']:
            current_subtitle = subtitle['text']
            break
    
    # 4. Add subtitle area (larger overlay for subtitles)
    subtitle_height = 120 if current_subtitle else 80
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, height - subtitle_height), (width, height), (0, 0, 0), -1)
    frame = cv2.addWeighted(frame, 0.7, overlay, 0.3, 0)
    
    # 5. Add subtitles if available
    if current_subtitle:
        add_subtitle_to_frame(frame, current_subtitle, width, height)
    
    # 6. Add lesson information
    info_y = height - 50 if not current_subtitle else height - 25
    cv2.putText(frame, f"LESSON {lesson_number}", (20, info_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    
    # Title (truncated and positioned)
    title_display = lesson_title[:30] + "..." if len(lesson_title) > 30 else lesson_title
    title_y = height - 25 if not current_subtitle else height - 5
    cv2.putText(frame, title_display, (20, title_y), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1)
    
    # 7. Add talking indicator (pulsing dot)
    talking_intensity = abs(np.sin(t * 8)) * 0.5 + 0.5 if current_subtitle else 0.2
    dot_color = (int(100 + 155 * talking_intensity), int(50 + 100 * talking_intensity), 50)
    cv2.circle(frame, (width - 30, 30), 8, dot_color, -1)
    cv2.putText(frame, "LIVE", (width - 70, 37), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
    
    return frame

def add_subtitle_to_frame(frame: np.ndarray, subtitle_text: str, width: int, height: int):
    """Add subtitle text to the frame with professional styling"""
    
    # Subtitle styling
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_thickness = 2
    text_color = (255, 255, 255)  # White text
    outline_color = (0, 0, 0)     # Black outline
    outline_thickness = 4
    
    # Split long subtitles into multiple lines
    words = subtitle_text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        text_size = cv2.getTextSize(test_line, font, font_scale, font_thickness)[0]
        
        if text_size[0] < width - 40:  # Leave 20px margin on each side
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)  # Single long word
    
    if current_line:
        lines.append(' '.join(current_line))
    
    # Position subtitles
    line_height = 35
    total_height = len(lines) * line_height
    start_y = height - 100 + (40 - total_height) // 2  # Center vertically in subtitle area
    
    for i, line in enumerate(lines):
        text_size = cv2.getTextSize(line, font, font_scale, font_thickness)[0]
        text_x = (width - text_size[0]) // 2  # Center horizontally
        text_y = start_y + (i + 1) * line_height
        
        # Draw text outline (for better readability)
        cv2.putText(frame, line, (text_x, text_y), font, font_scale, outline_color, outline_thickness)
        
        # Draw main text
        cv2.putText(frame, line, (text_x, text_y), font, font_scale, text_color, font_thickness)

def test_real_avatar():
    """Test with a sample avatar image"""
    
    print("🧪 TESTING REAL AVATAR TALKING HEAD CREATOR")
    print("=" * 60)
    
    # Create a sample avatar image for testing
    sample_avatar = create_sample_avatar_image()
    
    test_script = """
    Hello! I'm your AI instructor, and I'm excited to guide you through this comprehensive course.
    
    Today we'll explore advanced concepts that will enhance your understanding and skills.
    
    I'll be here to explain complex topics in a clear and engaging way.
    
    Let's embark on this learning journey together!
    """
    
    try:
        output_path = "test_real_avatar_output.mp4"
        
        video_path = create_real_avatar_video(
            script_text=test_script.strip(),
            avatar_image_path=sample_avatar,
            lesson_title="Advanced AI Course Introduction",
            lesson_number=1,
            output_path=output_path
        )
        
        if os.path.exists(video_path):
            size = os.path.getsize(video_path)
            print(f"🎉 SUCCESS! Real avatar video created:")
            print(f"   📁 Path: {video_path}")
            print(f"   📊 Size: {size:,} bytes")
            
            # Get video info
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
            
            print(f"\n🎬 REAL AVATAR VIDEO CREATED!")
            print(f"📺 This uses a real photo with subtle animations!")
            
            return True
        else:
            print("❌ Video creation failed")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_sample_avatar_image() -> str:
    """Create a sample avatar image for testing"""
    
    try:
        # Create a professional-looking avatar
        img = Image.new('RGB', (400, 500), color=(45, 55, 70))
        draw = ImageDraw.Draw(img)
        
        # Head/face area
        face_color = (220, 180, 140)  # Skin tone
        draw.ellipse([100, 80, 300, 280], fill=face_color, outline=(200, 160, 120), width=3)
        
        # Eyes
        draw.ellipse([130, 140, 150, 160], fill=(255, 255, 255), outline=(100, 100, 100), width=2)
        draw.ellipse([250, 140, 270, 160], fill=(255, 255, 255), outline=(100, 100, 100), width=2)
        draw.ellipse([135, 145, 145, 155], fill=(50, 100, 150))  # Blue eyes
        draw.ellipse([255, 145, 265, 155], fill=(50, 100, 150))
        
        # Nose
        draw.polygon([(200, 170), (195, 190), (205, 190)], fill=(200, 160, 120))
        
        # Mouth
        draw.arc([180, 200, 220, 230], 0, 180, fill=(180, 100, 100), width=3)
        
        # Hair
        draw.ellipse([90, 60, 310, 200], fill=(80, 60, 40), outline=(60, 40, 20), width=2)
        
        # Shirt/clothing
        draw.rectangle([50, 280, 350, 500], fill=(60, 80, 120), outline=(40, 60, 100), width=2)
        
        # Professional touch - add a subtle background gradient effect
        for y in range(500):
            alpha = int(255 * (1 - y / 500))
            color = (45 + alpha // 10, 55 + alpha // 10, 70 + alpha // 10)
            draw.line([(0, y), (400, y)], fill=color)
        
        # Save sample avatar
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            img.save(tmp.name, 'PNG')
            return tmp.name
            
    except Exception as e:
        logger.error(f"Error creating sample avatar: {e}")
        raise

if __name__ == "__main__":
    success = test_real_avatar()
    
    if success:
        print("\n🎉 REAL AVATAR TALKING HEAD CREATOR WORKS!")
        print("Ready to use your own avatar image!")
        print("\n📝 Usage:")
        print("   1. Provide your avatar image (JPG/PNG)")
        print("   2. System will process and optimize it")
        print("   3. Creates professional talking head video")
        print("   4. Adds subtle animations and effects")
    else:
        print("\n❌ Real avatar creation failed")
    
    sys.exit(0 if success else 1)
