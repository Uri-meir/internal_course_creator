"""
Content Generator Component
Generates lesson content using AI
"""

import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from mocks.mock_clients import MockOpenAIClient

logger = logging.getLogger(__name__)

class ContentGenerator:
    """
    Generates comprehensive lesson content using AI
    """
    
    def __init__(self, api_key: str, test_mode: bool = False):
        """Initialize with OpenAI API key and test mode flag"""
        self.test_mode = test_mode
        
        if self.test_mode:
            logger.info("Using mock OpenAI client for testing")
            self.client = MockOpenAIClient(api_key)
        else:
            self.client = OpenAI(api_key=api_key)
    
    def generate_lesson_content(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive content for a lesson
        
        Args:
            lesson_data: Lesson information from curriculum
            
        Returns:
            Complete lesson content
        """
        try:
            lesson_num = lesson_data.get('lesson_number', 1)
            title = lesson_data.get('title', 'Lesson')
            lesson_type = lesson_data.get('type', 'theory')
            duration = lesson_data.get('duration_minutes', 30)
            
            logger.info(f"Generating content for lesson {lesson_num}: {title}")
            
            # Generate content based on lesson type
            if lesson_type == 'theory':
                content = self._generate_theory_content(title, duration)
            elif lesson_type == 'hands-on':
                content = self._generate_hands_on_content(title, duration)
            else:
                content = self._generate_mixed_content(title, duration)
            
            # Add lesson metadata
            content.update({
                'lesson_number': lesson_num,
                'title': title,
                'type': lesson_type,
                'duration_minutes': duration,
                'has_coding': lesson_type in ['hands-on', 'advanced', 'project']
            })
            
            return content
            
        except Exception as e:
            logger.error(f"Error generating lesson content: {str(e)}")
            return self._create_fallback_content(lesson_data)
    
    def _generate_theory_content(self, title: str, duration: int) -> Dict[str, Any]:
        """Generate theory-based lesson content"""
        
        prompt = f"""
        You are an expert teacher creating a lesson about: "{title}"
        Duration: {duration} minutes
        
        CRITICAL REQUIREMENTS:
        1. This lesson MUST be about "{title}" specifically, not generic programming concepts
        2. Explain like you're teaching a bright 12-year-old child
        3. Use vivid analogies, real-world examples, and stories
        4. Make it engaging and memorable with concrete examples
        5. Focus ONLY on the topic mentioned in the title
        
        TEACHING APPROACH:
        - Start with a relatable analogy or story
        - Use concrete examples from everyday life
        - Break complex concepts into simple, digestible pieces
        - Include "aha moments" that make concepts click
        - End with a memorable summary
        
        Create a lesson about "{title}" that includes:
        
        {{
            "introduction": "An engaging opening that hooks the student with a story, question, or surprising fact about {title}",
            "main_concept": "The core concept of {title} explained in simple terms",
            "analogy": "A vivid analogy that makes {title} easy to understand (like explaining it to a child)",
            "real_world_example": "A concrete, everyday example of how {title} works in the real world",
            "step_by_step_explanation": [
                "Step 1: [Specific step about {title}]",
                "Step 2: [Specific step about {title}]",
                "Step 3: [Specific step about {title}]"
            ],
            "common_misconceptions": "What people often get wrong about {title} and why",
            "why_it_matters": "Why understanding {title} is important in real life",
            "key_takeaways": "3-5 memorable points about {title}",
            "fun_fact": "An interesting or surprising fact about {title}",
            "summary": "A memorable summary that reinforces the main concept of {title}",
            "next_lesson_preview": "A teaser about what's coming next related to {title}"
        }}
        
        REMEMBER: This lesson is specifically about "{title}". Make it engaging, memorable, and topic-focused!
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating theory content: {str(e)}")
            return self._create_fallback_theory_content(title)
    
    def _generate_hands_on_content(self, title: str, duration: int) -> Dict[str, Any]:
        """Generate hands-on lesson content"""
        
        prompt = f"""
        You are an expert teacher creating a hands-on coding lesson about: "{title}"
        Duration: {duration} minutes
        
        CRITICAL REQUIREMENTS:
        1. This lesson MUST be about "{title}" specifically, not generic programming exercises
        2. Create a fun, engaging project that teaches "{title}" through doing
        3. Use analogies and stories to explain concepts before coding
        4. Make the code examples specific to "{title}"
        5. Include real-world scenarios where this knowledge is useful
        
        TEACHING APPROACH:
        - Start with a fun story or scenario that needs solving
        - Explain the concept using analogies
        - Show the code step-by-step with explanations
        - Include fun challenges and experiments
        - Make it feel like building something cool, not just learning syntax
        
        Create a hands-on lesson about "{title}" that includes:
        
        {{
            "introduction": "A fun story or scenario that introduces why we need to learn about {title}",
            "concept_explanation": "Explain {title} using a simple analogy that makes it click",
            "project_overview": "What we're going to build together in this lesson about {title}",
            "setup_instructions": "Step-by-step setup for our {title} project",
            "code_examples": [
                {{
                    "title": "Building our first {title} component",
                    "description": "What this code does and why it's important for {title}",
                    "code": "Complete, runnable code that demonstrates {title}",
                    "explanation": "Line-by-line explanation of how this code works with {title}",
                    "expected_output": "What students should see when they run this {title} code"
                }},
                {{
                    "title": "Adding more {title} features",
                    "description": "How to extend our {title} project with additional functionality",
                    "code": "Code that builds upon the first example for {title}",
                    "explanation": "How this code enhances our {title} project",
                    "expected_output": "What the enhanced {title} project should do"
                }}
            ],
            "hands_on_exercises": [
                {{
                    "title": "Customize your {title} project",
                    "description": "A fun challenge to make the {title} project your own",
                    "hints": ["Think about what would make your {title} project unique", "Experiment with different approaches"],
                    "solution": "One possible solution with explanations",
                    "learning_outcome": "What students will understand about {title} after this exercise"
                }}
            ],
            "troubleshooting": "Common issues students might face with {title} and how to solve them",
            "real_world_applications": "Where and how {title} is used in actual projects and companies",
            "next_steps": "How to continue learning about {title} and what to build next",
            "fun_challenge": "A bonus challenge that pushes students to think creatively about {title}"
        }}
        
        REMEMBER: This lesson is specifically about "{title}". Make it fun, engaging, and focused on building real skills!
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating hands-on content: {str(e)}")
            return self._create_fallback_hands_on_content(title)
    
    def _generate_mixed_content(self, title: str, duration: int) -> Dict[str, Any]:
        """Generate mixed theory and hands-on lesson content"""
        
        prompt = f"""
        You are an expert teacher creating a mixed theory and hands-on lesson about: "{title}"
        Duration: {duration} minutes
        
        CRITICAL REQUIREMENTS:
        1. This lesson MUST be about "{title}" specifically, not generic mixed content
        2. Combine theory and practice in a way that makes "{title}" crystal clear
        3. Use stories, analogies, and real-world examples
        4. Make the hands-on part directly demonstrate the theory
        5. Create "aha moments" where theory and practice connect
        
        TEACHING APPROACH:
        - Start with a compelling story about why "{title}" matters
        - Explain the concept using analogies and examples
        - Show how the theory works in practice
        - Let students experiment and discover
        - Connect the dots between theory and real-world application
        
        Create a mixed lesson about "{title}" that includes:
        
        {{
            "introduction": "A compelling story or scenario that shows why {title} is important and interesting",
            "theory_section": {{
                "main_concept": "The core concept of {title} explained simply",
                "analogy": "A memorable analogy that makes {title} click",
                "real_world_example": "A concrete example of {title} in action",
                "why_it_matters": "Why understanding {title} is valuable in real life"
            }},
            "practice_section": {{
                "hands_on_project": "A fun project that demonstrates {title} in action",
                "step_by_step_guide": [
                    "Step 1: [Specific step about {title}]",
                    "Step 2: [Specific step about {title}]",
                    "Step 3: [Specific step about {title}]"
                ],
                "code_examples": [
                    {{
                        "title": "Implementing {title} concepts",
                        "description": "How this code demonstrates the theory we just learned",
                        "code": "Complete, runnable code for {title}",
                        "explanation": "How the theory connects to this practical implementation"
                    }}
                ]
            }},
            "connection_moment": "A clear explanation of how the theory and practice work together for {title}",
            "real_world_applications": "Specific examples of where {title} is used in industry and real projects",
            "experiment_section": "A fun experiment students can try to explore {title} further",
            "key_insights": "The main insights students should take away about {title}",
            "summary": "How theory and practice combine to create deep understanding of {title}",
            "next_lesson_preview": "What's coming next and how it builds on {title}"
        }}
        
        REMEMBER: This lesson is specifically about "{title}". Make the connection between theory and practice crystal clear!
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            return json.loads(content)
            
        except Exception as e:
            logger.error(f"Error generating mixed content: {str(e)}")
            return self._create_fallback_mixed_content(title)
    
    def create_course_description(self, curriculum_data: Dict[str, Any]) -> str:
        """Create marketing description for the course"""
        
        try:
            logger.info("Generating course marketing description")
            
            prompt = f"""
            Create an engaging, specific course description for:
            Title: {curriculum_data.get('course_title', 'Course')}
            Difficulty: {curriculum_data.get('difficulty', 'intermediate')}
            Duration: {curriculum_data.get('total_duration_hours', 5)} hours
            Target Audience: {curriculum_data.get('target_audience', 'developers')}
            
            Make it compelling for online learning platforms like Udemy/Coursera.
            Include:
            - Specific benefits and outcomes
            - What students will actually learn (be specific, not generic)
            - Why they should take this course over others
            - Real-world applications and career benefits
            
            Focus on the specific domain/topic, not generic programming benefits.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating course description: {str(e)}")
            return f"Comprehensive course on {curriculum_data.get('course_title', 'the topic')} designed for {curriculum_data.get('difficulty', 'intermediate')} learners."
    
    def _create_fallback_content(self, lesson_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback content if generation fails"""
        
        return {
            'lesson_number': lesson_data.get('lesson_number', 1),
            'title': lesson_data.get('title', 'Lesson'),
            'type': lesson_data.get('type', 'theory'),
            'duration_minutes': lesson_data.get('duration_minutes', 30),
            'introduction': f"Welcome to {lesson_data.get('title', 'this lesson')}",
            'theory_content': {
                'main_concepts': ['Basic concept 1', 'Basic concept 2'],
                'explanations': {
                    'Basic concept 1': 'Fundamental understanding of concept 1',
                    'Basic concept 2': 'Fundamental understanding of concept 2'
                }
            },
            'examples': ['Example 1', 'Example 2'],
            'key_takeaways': ['Key point 1', 'Key point 2'],
            'summary': 'Summary of key concepts covered in this lesson',
            'has_coding': lesson_data.get('type') in ['hands-on', 'advanced', 'project']
        }
    
    def _create_fallback_theory_content(self, title: str) -> Dict[str, Any]:
        """Create fallback theory content"""
        
        return {
            'introduction': f'Introduction to {title}',
            'theory_content': {
                'main_concepts': ['Core concept 1', 'Core concept 2'],
                'explanations': {
                    'Core concept 1': 'Detailed explanation of core concept 1',
                    'Core concept 2': 'Detailed explanation of core concept 2'
                }
            },
            'examples': ['Practical example 1', 'Practical example 2'],
            'key_takeaways': ['Important takeaway 1', 'Important takeaway 2'],
            'summary': f'Summary of {title} concepts'
        }
    
    def _create_fallback_hands_on_content(self, title: str) -> Dict[str, Any]:
        """Create fallback hands-on content"""
        
        return {
            'introduction': f'Hands-on practice with {title}',
            'setup_instructions': 'Set up your development environment',
            'code_examples': [
                {
                    'title': 'Basic Example',
                    'description': 'Simple implementation example',
                    'code': '# Your code here\nprint("Hello World")',
                    'explanation': 'This example demonstrates basic functionality'
                }
            ],
            'exercises': [
                {
                    'title': 'Practice Exercise',
                    'description': 'Try implementing this feature',
                    'hints': ['Start with the basics', 'Test your code'],
                    'solution': '# Solution code\n# Implementation here'
                }
            ],
            'common_errors': ['Common error 1', 'Common error 2'],
            'troubleshooting': 'Check your syntax and logic',
            'next_steps': 'Practice with more complex examples'
        }
    
    def _create_fallback_mixed_content(self, title: str) -> Dict[str, Any]:
        """Create fallback mixed content"""
        
        return {
            'introduction': f'Combined theory and practice for {title}',
            'theory_section': {
                'main_concepts': ['Concept 1', 'Concept 2'],
                'explanations': {
                    'Concept 1': 'Explanation of concept 1',
                    'Concept 2': 'Explanation of concept 2'
                }
            },
            'practical_section': {
                'implementation_steps': ['Step 1', 'Step 2'],
                'code_examples': [
                    {
                        'title': 'Implementation Example',
                        'description': 'Practical implementation',
                        'code': '# Implementation code',
                        'explanation': 'How this works'
                    }
                ]
            },
            'summary': f'Summary of {title} concepts and practice'
        } 
