"""
Mock clients for testing without real API calls
"""

import os
import json
import time
import subprocess
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class MockResponse:
    """Mock response object"""
    
    def __init__(self, content: str):
        """Initialize mock response"""
        self.choices = [MockChoice(content)]
        self.usage = MockUsage()
        self.model = "gpt-4"

class MockChoice:
    """Mock choice object"""
    
    def __init__(self, content: str):
        """Initialize mock choice"""
        self.message = MockMessage(content)
        self.index = 0
        self.finish_reason = "stop"

class MockMessage:
    """Mock message object"""
    
    def __init__(self, content: str):
        """Initialize mock response"""
        self.content = content
        self.role = "assistant"

class MockUsage:
    """Mock usage object"""
    
    def __init__(self):
        """Initialize mock usage"""
        self.prompt_tokens = 100
        self.completion_tokens = 200
        self.total_tokens = 300

class MockImageResponse:
    """Mock image response object"""
    
    def __init__(self, image_path: str):
        """Initialize mock image response"""
        self.data = [MockImageData(image_path)]
        self.created = int(time.time())

class MockImageData:
    """Mock image data object"""
    
    def __init__(self, image_path: str):
        """Initialize mock image data"""
        self.url = image_path
        self.revised_prompt = "Mock generated image"

class MockOpenAIClient:
    """Mock OpenAI client for testing"""
    
    def __init__(self, api_key: str):
        """Initialize mock client"""
        self.api_key = api_key
        self.chat = MockChatCompletions()
        self.images = MockImageGenerator()
    
    def __str__(self):
        return f"MockOpenAIClient(api_key='{self.api_key[:8]}...')"

class MockChatCompletions:
    """Mock chat completions for testing"""
    
    def __init__(self):
        """Initialize mock chat completions"""
        self.completions = self
    
    def create(self, model: str, messages: List[Dict[str, str]], 
               max_tokens: int = 1000, temperature: float = 0.7) -> MockResponse:
        """Mock chat completion creation"""
        
        # Extract user message
        user_message = ""
        for msg in messages:
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        # Generate mock response based on message content
        if 'analyze' in user_message.lower() or 'domain' in user_message.lower():
            response_content = self._generate_domain_analysis(user_message)
        elif 'theory' in user_message.lower():
            response_content = self._generate_theory_content(user_message)
        elif 'hands-on' in user_message.lower() or 'coding' in user_message.lower():
            response_content = self._generate_hands_on_content(user_message)
        elif 'script' in user_message.lower():
            response_content = self._generate_script_content(user_message)
        elif 'description' in user_message.lower():
            response_content = self._generate_course_description(user_message)
        else:
            response_content = self._generate_generic_response(user_message)
        
        return MockResponse(response_content)
    
    def _generate_domain_analysis(self, message: str) -> str:
        """Generate mock domain analysis response"""
        return json.dumps({
            "domain_scope": "Comprehensive course on the topic",
            "difficulty_level": "intermediate",
            "estimated_hours": 8,
            "key_topics": ["Topic 1", "Topic 2", "Topic 3"],
            "prerequisites": ["Basic knowledge", "Familiarity with concepts"],
            "target_audience": "Developers and learners",
            "learning_outcomes": ["Understand concepts", "Apply knowledge", "Build projects"]
        })
    
    def _generate_theory_content(self, message: str) -> str:
        """Generate mock theory content response"""
        
        # Extract the lesson title from the message
        lesson_title = self._extract_lesson_title(message)
        
        return json.dumps({
            "introduction": f"Imagine you're building a magical bridge! Today we're going to learn about {lesson_title} - and trust me, it's going to be amazing!",
            "main_concept": f"The core concept of {lesson_title} is like having a superpower that lets you solve problems in a whole new way.",
            "analogy": f"Think of {lesson_title} like a recipe book. Just like how a recipe tells you exactly what ingredients to use and in what order, {lesson_title} gives you a step-by-step way to solve problems.",
            "real_world_example": f"Here's a real example: Imagine you're building a robot that needs to remember things. {lesson_title} is like giving that robot a super memory that never forgets!",
            "step_by_step_explanation": [
                f"Step 1: Understanding what {lesson_title} is and why it's important",
                f"Step 2: Learning how {lesson_title} works in practice",
                f"Step 3: Seeing {lesson_title} solve real problems"
            ],
            "common_misconceptions": f"Many people think {lesson_title} is complicated, but it's actually like learning to ride a bike - tricky at first, then suddenly it clicks!",
            "why_it_matters": f"Understanding {lesson_title} is like having a secret key that opens doors to amazing possibilities in technology and problem-solving.",
            "key_takeaways": [
                f"{lesson_title} is a powerful tool for solving complex problems",
                f"It works like a recipe - follow the steps and get amazing results",
                f"Once you understand {lesson_title}, you can use it in countless ways"
            ],
            "fun_fact": f"Did you know? {lesson_title} was inspired by how the human brain solves problems - it's like artificial intelligence that thinks like we do!",
            "summary": f"Today we learned that {lesson_title} is like having a superpower for problem-solving. It's not magic - it's science, and now you understand how it works!",
            "next_lesson_preview": f"In our next adventure, we'll see how {lesson_title} connects to even bigger and more exciting concepts!"
        })
    
    def _generate_hands_on_content(self, message: str) -> str:
        """Generate mock hands-on content response"""
        
        lesson_title = self._extract_lesson_title(message)
        
        return json.dumps({
            "introduction": f"Ready for an adventure? Today we're going to build something amazing using {lesson_title}! It's like being a wizard who creates magic with code.",
            "concept_explanation": f"Think of {lesson_title} like building with LEGO blocks. Each piece has a specific purpose, and when you put them together just right, you create something incredible!",
            "project_overview": f"We're going to build a mini-{lesson_title} project that will make you say 'Wow!' - it's going to be fun, exciting, and you'll learn tons along the way.",
            "setup_instructions": "First, let's get our magical coding environment ready. We'll need Python, some special tools, and your imagination!",
            "code_examples": [
                {
                    "title": f"Building our first {lesson_title} component",
                    "description": f"This is where the magic happens! We'll create our first piece of {lesson_title} code that actually works.",
                    "code": f"# Welcome to the world of {lesson_title}!\nimport magic\n\ndef create_{lesson_title.lower().replace(' ', '_')}_project():\n    print('Creating something amazing with {lesson_title}!')\n    return 'Success!'",
                    "explanation": f"Every line of this code is like a spell that brings our {lesson_title} project to life. Let's break it down piece by piece!",
                    "expected_output": "You'll see a magical message that says our project is working!"
                },
                {
                    "title": f"Adding more {lesson_title} features",
                    "description": f"Now let's make our {lesson_title} project even more powerful by adding cool new features!",
                    "code": f"# Making our {lesson_title} project awesome!\ndef enhance_{lesson_title.lower().replace(' ', '_')}():\n    features = ['Speed', 'Power', 'Magic']\n    for feature in features:\n        print(f'Adding {{feature}} to our {lesson_title} project!')",
                    "explanation": f"This code is like upgrading our project with superpowers! Each feature makes it more amazing.",
                    "expected_output": "You'll see each feature being added to your project!"
                }
            ],
            "hands_on_exercises": [
                {
                    "title": f"Customize your {lesson_title} project",
                    "description": f"Now it's your turn to be creative! Take what we've built and make it uniquely yours.",
                    "hints": [f"Think about what would make your {lesson_title} project special", "Don't be afraid to experiment and try new things!"],
                    "solution": f"# Your unique {lesson_title} project\n# Add your own creative touches here\nprint('This is MY amazing project!')",
                    "learning_outcome": f"After this exercise, you'll understand how to make {lesson_title} projects that are uniquely yours!"
                }
            ],
            "troubleshooting": f"Sometimes things don't work perfectly - that's normal! Here are common issues with {lesson_title} and how to fix them.",
            "real_world_applications": f"Companies like Google, Apple, and Tesla use {lesson_title} to build amazing things. You're learning the same skills they use!",
            "next_steps": f"Keep practicing with {lesson_title}! Try building bigger projects, experiment with new ideas, and never stop learning.",
            "fun_challenge": f"Here's a bonus challenge: Can you think of three completely different ways to use {lesson_title}? Be creative!"
        })
    
    def _extract_lesson_title(self, message: str) -> str:
        """Extract lesson title from the message"""
        
        # Look for lesson titles in the message
        if "lesson" in message.lower():
            # Try to find the actual lesson topic
            lines = message.split('\n')
            for line in lines:
                if "lesson" in line.lower() and ":" in line:
                    # Extract the part after the colon
                    parts = line.split(':')
                    if len(parts) > 1:
                        title = parts[1].strip()
                        # Clean up the title
                        title = title.replace('"', '').replace("'", "")
                        if title and len(title) > 5:  # Make sure it's not just "Lesson 1"
                            return title
        
        # Fallback to a generic but engaging title
        return "this amazing topic"
    
    def _generate_script_content(self, message: str) -> str:
        """Generate mock script content response"""
        return """
        Welcome to this lesson! [PAUSE:1s]
        
        Today we'll learn about important concepts. [PAUSE:1.5s]
        
        Let me explain the key points. [EMPHASIS]This is crucial[/EMPHASIS].
        
        [PAUSE:2s]
        
        Now let's practice together.
        
        [PAUSE:1s]
        
        Great job! Keep practicing.
        """
    
    def _generate_course_description(self, message: str) -> str:
        """Generate mock course description response"""
        return "Comprehensive course designed for learners who want to master the fundamentals and build real-world projects."
    
    def _generate_generic_response(self, message: str) -> str:
        """Generate generic mock response"""
        return "This is a mock response for testing purposes."

class MockImageGenerator:
    """Mock image generator for testing"""
    
    def generate(self, model: str, prompt: str, size: str = "1024x1024", 
                 quality: str = "standard", n: int = 1) -> MockImageResponse:
        """Mock image generation"""
        
        # Create mock image file
        image_path = create_mock_image_file(prompt, "Generated Image")
        
        return MockImageResponse(image_path)

class MockDIDClient:
    """Mock D-ID client for testing"""
    
    def __init__(self, api_key: str):
        """Initialize mock client"""
        self.api_key = api_key
    
    def create_video(self, script_text: str, lesson_title: str, lesson_number: int) -> str:
        """Mock video creation"""
        
        # Create mock video file
        video_path = create_mock_video_file(lesson_title, lesson_number)
        
        return video_path

def create_mock_image_file(topic: str, title: str) -> str:
    """Create a mock image file for testing"""
    
    try:
        # Create output directory
        output_dir = "output_test/backgrounds/generated"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        filename = f"mock_bg_{safe_topic}_{safe_title}.png"
        output_path = os.path.join(output_dir, filename)
        
        # Create a simple colored image using PIL
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (1024, 1024), color=(100, 150, 255))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("Arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            # Draw topic and title
            text = f"{topic}\n{title}"
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (1024 - text_width) // 2
            y = (1024 - text_height) // 2
            
            draw.text((x, y), text, font=font, fill='white')
            
            # Save image
            img.save(output_path, 'PNG')
            
        except ImportError:
            # Fallback: create empty file
            with open(output_path, 'w') as f:
                f.write("Mock image file")
        
        logger.info(f"Mock image created: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error creating mock image: {str(e)}")
        return "mock_image.png"

def create_mock_video_file(title: str, lesson_number: int) -> str:
    """Create a mock video file for testing"""
    
    try:
        # Create output directory
        output_dir = "output_test/videos/presenter"
        os.makedirs(output_dir, exist_ok=True)
        
        # Create safe filename
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')
        filename = f"lesson_{lesson_number:02d}_{safe_title}_presenter.mp4"
        output_path = os.path.join(output_dir, filename)
        
        # Create a simple mock video file using ffmpeg (more reliable than moviepy)
        try:
            # Create a simple video with ffmpeg
            cmd = [
                'ffmpeg', '-f', 'lavfi', '-i', 'color=c=0x6496FF:size=640x480:duration=15',
                '-vf', f'drawtext=text=\'Lesson {lesson_number}\\n{title}\':fontsize=40:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2',
                '-c:v', 'libx264', '-preset', 'ultrafast', '-t', '15',
                '-y',  # Overwrite output file
                output_path
            ]
            
            # Run ffmpeg command
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Mock video created with ffmpeg: {output_path}")
                return output_path
            else:
                logger.warning(f"FFmpeg failed, creating empty file: {result.stderr}")
                # Fallback: create empty file
                with open(output_path, 'w') as f:
                    f.write("Mock video file")
                return output_path
                
        except (ImportError, FileNotFoundError, subprocess.SubprocessError):
            # Fallback: create empty file
            logger.info("FFmpeg not available, creating empty mock video file")
            with open(output_path, 'w') as f:
                f.write("Mock video file")
            return output_path
        
    except Exception as e:
        logger.error(f"Error creating mock video: {str(e)}")
        # Return a default path
        return f"output_test/videos/presenter/lesson_{lesson_number:02d}_mock_presenter.mp4"

def create_mock_notebook_content(lesson_number: int, title: str) -> str:
    """Create mock notebook content for testing"""
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {title}\n\n",
                    "## Overview\n",
                    f"This is lesson {lesson_number} covering important concepts.\n\n",
                    "## Learning Objectives\n",
                    "- Understand key concepts\n",
                    "- Apply knowledge in practice\n",
                    "- Complete hands-on exercises"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Your code here\n",
                    "print('Hello from lesson {}')".format(lesson_number)
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return json.dumps(notebook_content, indent=2)

def create_mock_lesson_content(lesson_number: int, title: str) -> Dict[str, Any]:
    """Create mock lesson content for testing"""
    
    # Generate varied content based on lesson title and number
    lesson_type = "hands-on" if lesson_number % 2 == 0 else "theory"
    
    # Create domain-specific content based on the title
    if "Python" in title:
        theory_content = {
            "main_concepts": [f"Python concept {i}" for i in range(1, 4)],
            "explanations": {
                f"Python concept {i}": f"Python-specific explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "Python Example",
                "description": "Python-specific implementation",
                "code": "# Python code example\nprint('Hello from Python lesson')",
                "explanation": "This demonstrates Python syntax and concepts"
            }
        ]
    elif "React" in title or "Web" in title:
        theory_content = {
            "main_concepts": [f"Web development concept {i}" for i in range(1, 4)],
            "explanations": {
                f"Web development concept {i}": f"Web development explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "React Component Example",
                "description": "React-specific implementation",
                "code": "// React component\nexport default function MyComponent() {\n  return <div>Hello from React</div>;\n}",
                "explanation": "This demonstrates React component structure"
            }
        ]
    elif "Machine Learning" in title or "Data Science" in title:
        theory_content = {
            "main_concepts": [f"ML concept {i}" for i in range(1, 4)],
            "explanations": {
                f"ML concept {i}": f"Machine learning explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "ML Pipeline Example",
                "description": "Machine learning implementation",
                "code": "# ML pipeline\nfrom sklearn.model_selection import train_test_split\n# Your ML code here",
                "explanation": "This demonstrates machine learning workflow"
            }
        ]
    elif "Cybersecurity" in title:
        theory_content = {
            "main_concepts": [f"Security concept {i}" for i in range(1, 4)],
            "explanations": {
                f"Security concept {i}": f"Cybersecurity explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "Security Tool Example",
                "description": "Security implementation",
                "code": "# Security tool\nimport hashlib\n# Your security code here",
                "explanation": "This demonstrates security tool development"
            }
        ]
    elif "Mobile" in title:
        theory_content = {
            "main_concepts": [f"Mobile concept {i}" for i in range(1, 4)],
            "explanations": {
                f"Mobile concept {i}": f"Mobile development explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "Mobile App Example",
                "description": "Mobile app implementation",
                "code": "// Mobile app code\nclass MainActivity {\n    // Your mobile code here\n}",
                "explanation": "This demonstrates mobile app development"
            }
        ]
    else:
        # Generic content for other domains
        theory_content = {
            "main_concepts": [f"Domain concept {i}" for i in range(1, 4)],
            "explanations": {
                f"Domain concept {i}": f"General explanation of concept {i}" for i in range(1, 4)
            }
        }
        code_examples = [
            {
                "title": "General Example",
                "description": "Generic implementation example",
                "code": "# General code example\nprint('Hello from lesson')",
                "explanation": "This demonstrates general programming concepts"
            }
        ]
    
    # Generate varied exercises based on lesson type
    if lesson_type == "hands-on":
        exercises = [
            {
                "title": f"Practice Exercise {lesson_number}",
                "description": f"Hands-on practice for {title}",
                "hints": [f"Start with the basics of {title}", "Test your implementation"],
                "solution": f"# Solution for {title}\n# Implementation here"
            }
        ]
        setup_instructions = f"Set up your development environment for {title}"
    else:
        exercises = [
            {
                "title": f"Theory Exercise {lesson_number}",
                "description": f"Theoretical understanding of {title}",
                "hints": [f"Review the concepts of {title}", "Think about real-world applications"],
                "solution": f"# Theoretical solution for {title}\n# Explanation here"
            }
        ]
        setup_instructions = f"Prepare to learn about {title} concepts"
    
    # Generate varied key takeaways based on lesson content
    key_takeaways = [
        f"Key insight about {title}",
        f"Important concept from lesson {lesson_number}",
        f"Practical application of {title}"
    ]
    
    # Generate varied summary based on lesson
    summary = f"Comprehensive summary of {title} covering all key concepts, practical applications, and best practices learned in this lesson."
    
    return {
        "lesson_number": lesson_number,
        "title": title,
        "type": lesson_type,
        "duration_minutes": 30,
        "introduction": f"Welcome to lesson {lesson_number}: {title}. This lesson will cover essential concepts and provide hands-on experience.",
        "theory_content": theory_content,
        "code_examples": code_examples,
        "exercises": exercises,
        "setup_instructions": setup_instructions,
        "key_takeaways": key_takeaways,
        "summary": summary,
        "has_coding": lesson_type == "hands-on"
    } 
