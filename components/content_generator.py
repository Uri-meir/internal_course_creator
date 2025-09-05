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
        You are an expert programming instructor. Create comprehensive hands-on lesson content about: "{title}"
        Duration: {duration} minutes
        
        REQUIREMENTS:
        1. Make this about "{title}" specifically with real-world applications
        2. Include detailed code examples with explanations
        3. Create comprehensive exercises with full solutions
        4. Focus on professional-level content, not beginner basics
        5. Include practical applications and best practices
        
        Create detailed lesson content about "{title}" with this structure:
        
        {{
            "introduction": "A compelling introduction to {title} with real-world examples and professional use cases (minimum 200 words)",
            "concept_explanation": "Deep technical explanation of {title} concepts and principles (minimum 300 words)",
            "project_overview": "Description of a practical project we will build using {title} (minimum 150 words)",
            "setup_instructions": "Step-by-step setup instructions for the {title} development environment",
            "code_examples": [
                {{
                    "title": "Core {title} Implementation",
                    "description": "Production-ready implementation of core {title} functionality with error handling, logging, and optimization.",
                    "code": "Complete, professional-grade code (minimum 30 lines) that demonstrates advanced {title} patterns with proper error handling, logging, type hints, and documentation.",
                    "explanation": "Detailed line-by-line explanation covering design decisions, performance considerations, error handling strategies, and integration patterns.",
                    "expected_output": "Specific output showing successful execution with logging and error handling demonstration.",
                    "best_practices": "Key professional practices demonstrated in this code including SOLID principles, error handling, and performance optimization."
                }},
                {{
                    "title": "Advanced {title} Integration",
                    "description": "Complex integration example showing how {title} works with other technologies and frameworks in production environments.",
                    "code": "Advanced code (minimum 40 lines) showing integration patterns, async operations, database connections, API interactions, or similar professional scenarios.",
                    "explanation": "Comprehensive explanation of integration patterns, architectural decisions, scalability considerations, and production deployment strategies.",
                    "expected_output": "Detailed output showing successful integration with external systems, performance metrics, and monitoring data.",
                    "architecture_notes": "Explanation of how this fits into microservices, distributed systems, or enterprise architecture patterns."
                }},
                {{
                    "title": "Performance Optimization and Debugging",
                    "description": "Advanced techniques for optimizing {title} performance and debugging complex issues.",
                    "code": "Sophisticated code (minimum 35 lines) demonstrating profiling, optimization techniques, caching strategies, and debugging approaches.",
                    "explanation": "Deep dive into performance analysis, bottleneck identification, optimization strategies, and debugging methodologies.",
                    "expected_output": "Performance benchmarks, profiling results, and before/after optimization comparisons.",
                    "optimization_techniques": "Specific optimization patterns, caching strategies, and performance monitoring approaches."
                }}
            ],
            "hands_on_exercises": [
                {{
                    "title": "Professional {title} Implementation",
                    "description": "Build a production-ready implementation with error handling and best practices",
                    "difficulty": "Medium",
                    "learning_outcome": "Master professional-grade {title} development practices",
                    "starter_code": "# Professional implementation starter code here",
                    "solution": "Complete professional solution with detailed implementation (minimum 50 lines of code)",
                    "solution_explanation": "Comprehensive explanation of the solution approach and key concepts",
                    "key_concepts": ["Professional patterns", "Error handling", "Best practices", "Testing"]
                }},
                {{
                    "title": "Advanced {title} Architecture",
                    "description": "Design and implement an enterprise-grade scalable system",
                    "difficulty": "Hard", 
                    "learning_outcome": "Master enterprise architecture patterns and scalability",
                    "starter_code": "# Enterprise architecture starter code here",
                    "solution": "Complete enterprise solution with microservices and monitoring (minimum 100 lines)",
                    "solution_explanation": "Detailed explanation of architecture decisions and scalability patterns",
                    "key_concepts": ["Microservices", "Scalability", "Monitoring", "Security"]
                }},
                {{
                    "title": "Real-World Industry Application",
                    "description": "Apply {title} to solve a specific industry problem with compliance requirements",
                    "difficulty": "Hard",
                    "learning_outcome": "Apply {title} to real business challenges with regulatory compliance", 
                    "starter_code": "# Industry-specific implementation starter code here",
                    "solution": "Complete industry solution with compliance and security (minimum 80 lines)",
                    "solution_explanation": "Explanation of industry requirements and compliance considerations",
                    "key_concepts": ["Industry compliance", "Security", "Audit logging", "Data protection"]
                }},
                {{
                    "title": "Performance Optimization Challenge",
                    "description": "Debug and optimize a complex system for enterprise performance",
                    "difficulty": "Expert",
                    "learning_outcome": "Master debugging and performance optimization techniques",
                    "starter_code": "# Performance optimization challenge code here",
                    "solution": "Optimized solution with debugging and monitoring (minimum 120 lines)",
                    "solution_explanation": "Comprehensive debugging methodology and optimization strategies",
                    "key_concepts": ["Performance profiling", "Debugging", "Monitoring", "Optimization"]
                }},
                {{
                    "title": "Innovation Project",
                    "description": "Create an innovative solution integrating emerging technologies",
                    "difficulty": "Expert", 
                    "learning_outcome": "Demonstrate mastery through innovative technology integration",
                    "starter_code": "# Innovation project starter code here",
                    "solution": "Revolutionary solution with emerging tech integration (minimum 150 lines)",
                    "solution_explanation": "Innovation approach and future technology integration strategies",
                    "key_concepts": ["Emerging technologies", "Innovation", "Future-proofing", "Research"]
                }}
            ],
            "troubleshooting": "Common issues students might face with {title} and how to solve them",
            "real_world_applications": "Where and how {title} is used in actual projects and companies",
            "next_steps": "How to continue learning about {title} and what to build next",
            "fun_challenge": "A bonus challenge that pushes students to think creatively about {title}"
        }}
        
        REMEMBER: This lesson is specifically about "{title}". Make it comprehensive, professional, and focused on building real-world skills!
        
        IMPORTANT: Return ONLY valid JSON. No extra text, no markdown formatting, no code blocks. Just pure JSON that can be parsed directly.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,  # Increased for comprehensive content
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            logger.info(f"Raw OpenAI response length: {len(content)} characters")
            
            # Clean the content before parsing
            content = content.strip()
            if content.startswith('```json'):
                content = content[7:]  # Remove ```json
            if content.endswith('```'):
                content = content[:-3]  # Remove ```
            content = content.strip()
            
            # Clean and fix JSON formatting issues
            import re
            
            # Remove problematic control characters first
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
            
            # Fix unescaped quotes within JSON strings
            # This is a simple approach - replace problematic quotes
            content = content.replace('\\"', '"')  # Remove escaping first
            
            # Fix newlines and tabs within JSON strings
            lines = content.split('\n')
            fixed_lines = []
            inside_string = False
            
            for line in lines:
                if inside_string:
                    # We're inside a multi-line string, escape it properly
                    line = line.replace('"', '\\"').replace('\t', '\\t')
                    line = line.rstrip() + '\\n'
                    
                # Count quotes to determine if we're inside a string
                quote_count = line.count('"') - line.count('\\"')
                if quote_count % 2 == 1:
                    inside_string = not inside_string
                    
                fixed_lines.append(line)
            
            content = '\n'.join(fixed_lines)
            
            # Final cleanup of any remaining issues
            content = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', content)
            
            # Log first 200 chars for debugging
            logger.info(f"Cleaned content sample: {content[:200]}...")
            
            parsed_content = json.loads(content)
            logger.info("Successfully parsed OpenAI response as JSON")
            return parsed_content
            
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Raw content: {content[:500]}...")
            return self._create_fallback_hands_on_content(title)
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
