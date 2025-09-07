"""
Content Generator Component
Generates lesson content using AI
"""

import json
import logging
from typing import Dict, Any
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
        You are an expert programming instructor creating a comprehensive hands-on coding lesson.
        
        LESSON TOPIC: "{title}"
        Duration: {duration} minutes
        
        CRITICAL REQUIREMENTS:
        1. Focus ONLY on "{title}" - be specific to this exact technology/concept
        2. Include WORKING, RUNNABLE code examples (minimum 40 lines each)
        3. Provide COMPLETE code solutions for all exercises (minimum 60 lines each)
        4. Use professional-level content with real-world applications
        5. Include actual imports, error handling, and production-ready patterns
        6. Make all code examples copy-paste ready and executable
        7. Create at least 8 comprehensive hands-on exercises
        8. Include beginner, intermediate, and advanced difficulty levels
        9. Add bonus challenges and real-world project scenarios
        
        CRITICAL DOMAIN INTERPRETATION: Always interpret titles in their proper technical context:
        - RAG = Retrieval-Augmented Generation (AI/ML technology for combining LLMs with external knowledge)
        - API = Application Programming Interface 
        - ML = Machine Learning
        - AI = Artificial Intelligence
        - FastAPI = Python web framework
        - LangChain = Framework for developing LLM applications
        - Vector Database = Database optimized for similarity search
        - Embeddings = Numerical representations of text for semantic search
        
        If the title mentions "RAG" or "Retrieval Augmented Generation", this lesson MUST be about:
        - How RAG works (retrieval + generation pipeline)
        - Vector embeddings and semantic search
        - Document chunking and preprocessing
        - Integration with LLMs (OpenAI, Anthropic, etc.)
        - RAG frameworks like LangChain, LlamaIndex, Haystack
        - Vector databases like Pinecone, Weaviate, Chroma
        - Evaluation metrics for RAG systems
        - Real-world RAG applications (chatbots, Q&A systems, knowledge bases)
        
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
                    "code": "COMPLETE WORKING PYTHON CODE (30+ lines) with actual imports, classes, methods, error handling, logging, type hints, docstrings, and example usage. Must be copy-paste ready and executable code that demonstrates {title}.",
                    "explanation": "Detailed line-by-line explanation covering design decisions, performance considerations, error handling strategies, and integration patterns.",
                    "expected_output": "Specific output showing successful execution with logging and error handling demonstration.",
                    "best_practices": "Key professional practices demonstrated in this code including SOLID principles, error handling, and performance optimization."
                }},
                {{
                    "title": "Advanced {title} Integration",
                    "description": "Complex integration example showing how {title} works with other technologies and frameworks in production environments.",
                    "code": "COMPLETE WORKING PYTHON CODE (40+ lines) with real integration patterns, async operations, database connections, API interactions, imports, error handling, and full working example that demonstrates advanced {title} usage.",
                    "explanation": "Comprehensive explanation of integration patterns, architectural decisions, scalability considerations, and production deployment strategies.",
                    "expected_output": "Detailed output showing successful integration with external systems, performance metrics, and monitoring data.",
                    "architecture_notes": "Explanation of how this fits into microservices, distributed systems, or enterprise architecture patterns."
                }},
                {{
                    "title": "Performance Optimization and Debugging",
                    "description": "Advanced techniques for optimizing {title} performance and debugging complex issues.",
                    "code": "COMPLETE WORKING PYTHON CODE (35+ lines) with actual profiling tools, optimization techniques, caching implementation, debugging code, performance monitoring, and benchmarking examples for {title}.",
                    "explanation": "Deep dive into performance analysis, bottleneck identification, optimization strategies, and debugging methodologies.",
                    "expected_output": "Performance benchmarks, profiling results, and before/after optimization comparisons.",
                    "optimization_techniques": "Specific optimization patterns, caching strategies, and performance monitoring approaches."
                }}
            ],
            "hands_on_exercises": [
                {{
                    "title": "Basic {title} Implementation",
                    "description": "Build a working {title} implementation from scratch with proper imports and error handling",
                    "difficulty": "Medium",
                    "learning_outcome": "Understand core {title} concepts through hands-on implementation",
                    "starter_code": "# Import required libraries\\nimport os\\nimport logging\\nfrom typing import List, Dict, Any\\n\\n# TODO: Complete the {title} implementation\\nclass {title}Implementation:\\n    def __init__(self):\\n        pass\\n\\n    def process(self, data):\\n        # Your implementation here\\n        pass",
                    "solution": "COMPLETE WORKING CODE with all imports, class definitions, methods, error handling, and example usage. Must be 50+ lines of actual runnable Python code that demonstrates {title}. Include: imports, class definition, methods, error handling, logging, type hints, docstrings, and a main execution example.",
                    "solution_explanation": "Line-by-line explanation of the code, why each part is necessary, how it works, and how it demonstrates {title} concepts",
                    "key_concepts": ["Core {title} principles", "Implementation patterns", "Error handling", "Best practices"]
                }},
                {{
                    "title": "Advanced {title} Architecture",
                    "description": "Design and implement an enterprise-grade scalable system",
                    "difficulty": "Hard", 
                    "learning_outcome": "Master enterprise architecture patterns and scalability",
                    "starter_code": "# Advanced {title} Architecture\\nimport asyncio\\nimport logging\\nfrom typing import Dict, List, Optional\\nfrom dataclasses import dataclass\\n\\n@dataclass\\nclass {title}Config:\\n    # TODO: Add configuration\\n    pass\\n\\nclass Advanced{title}System:\\n    def __init__(self, config: {title}Config):\\n        # TODO: Initialize system\\n        pass",
                    "solution": "COMPLETE WORKING CODE for enterprise architecture with 100+ lines including: imports, dataclasses, async methods, error handling, logging, monitoring, configuration management, and full example usage. Must be production-ready code.",
                    "solution_explanation": "Detailed explanation of architecture decisions and scalability patterns",
                    "key_concepts": ["Microservices", "Scalability", "Monitoring", "Security"]
                }},
                {{
                    "title": "Real-World Industry Application",
                    "description": "Apply {title} to solve a specific industry problem with compliance requirements",
                    "difficulty": "Hard",
                    "learning_outcome": "Apply {title} to real business challenges with regulatory compliance", 
                    "starter_code": "# Industry-Specific {title} Solution\\nimport hashlib\\nimport logging\\nfrom datetime import datetime\\nfrom typing import Dict, Any, Optional\\nfrom enum import Enum\\n\\nclass IndustryType(Enum):\\n    FINTECH = 'fintech'\\n    HEALTHCARE = 'healthcare'\\n    ECOMMERCE = 'ecommerce'\\n\\nclass Industry{title}Solution:\\n    def __init__(self, industry: IndustryType):\\n        # TODO: Initialize industry-specific solution\\n        pass",
                    "solution": "COMPLETE WORKING CODE for industry application with 80+ lines including: imports, enums, classes, security measures, compliance logging, data validation, error handling, and real-world example usage.",
                    "solution_explanation": "Explanation of industry requirements and compliance considerations",
                    "key_concepts": ["Industry compliance", "Security", "Audit logging", "Data protection"]
                }},
                {{
                    "title": "Performance Optimization Challenge",
                    "description": "Debug and optimize a complex system for enterprise performance",
                    "difficulty": "Expert",
                    "learning_outcome": "Master debugging and performance optimization techniques",
                    "starter_code": "# Performance Optimization Challenge\\nimport time\\nimport threading\\nimport asyncio\\nfrom typing import List, Dict, Any\\nfrom concurrent.futures import ThreadPoolExecutor\\n\\nclass Buggy{title}System:\\n    def __init__(self):\\n        self.cache = {{}}\\n        self.connections = []\\n        # TODO: Fix memory leaks and race conditions\\n        \\n    def process_data(self, data: List[Any]) -> List[Any]:\\n        # TODO: Optimize this inefficient implementation\\n        results = []\\n        for item in data:\\n            time.sleep(0.01)  # Simulating slow operation\\n            results.append(item * 2)\\n        return results",
                    "solution": "COMPLETE OPTIMIZED CODE with 120+ lines including: fixed bugs, async implementation, proper connection pooling, caching strategies, monitoring, profiling code, performance benchmarks, and comprehensive error handling.",
                    "solution_explanation": "Comprehensive debugging methodology and optimization strategies",
                    "key_concepts": ["Performance profiling", "Debugging", "Monitoring", "Optimization"]
                }},
                {{
                    "title": "Innovation Project",
                    "description": "Create an innovative solution integrating emerging technologies",
                    "difficulty": "Expert", 
                    "learning_outcome": "Demonstrate mastery through innovative technology integration",
                    "starter_code": "# Innovation Project: Next-Generation {title}\\nimport asyncio\\nfrom typing import Dict, List, Any, Optional\\nfrom dataclasses import dataclass\\nfrom abc import ABC, abstractmethod\\nfrom enum import Enum\\n\\nclass EmergingTech(Enum):\\n    AI_ML = 'ai_ml'\\n    BLOCKCHAIN = 'blockchain'\\n    EDGE_COMPUTING = 'edge'\\n\\n@dataclass\\nclass InnovationConfig:\\n    tech_stack: List[EmergingTech]\\n    performance_targets: Dict[str, float]\\n\\nclass NextGen{title}Platform:\\n    def __init__(self, config: InnovationConfig):\\n        # TODO: Implement cutting-edge solution\\n        pass",
                    "solution": "COMPLETE INNOVATIVE CODE with 150+ lines including: emerging technology integration, AI/ML components, advanced architecture patterns, comprehensive testing, monitoring, security features, and real-world deployment example.",
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
        
        CRITICAL JSON REQUIREMENTS:
        - Return ONLY valid JSON with NO extra text
        - Use simple strings for all code - no complex formatting
        - Escape all quotes and newlines properly in JSON strings
        - Keep code in single lines with \\n for line breaks
        - Make sure all JSON strings are properly closed
        
        IMPORTANT: Return ONLY valid JSON that can be parsed directly.
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
            logger.info("Creating comprehensive fallback content instead of shallow fallback")
            return self._create_comprehensive_fallback_content(title, content)
        except Exception as e:
            logger.error(f"Error generating hands-on content: {str(e)}")
            return self._create_comprehensive_fallback_content(title, "")
    
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
    
    def _create_comprehensive_fallback_content(self, title: str, raw_content: str = "") -> Dict[str, Any]:
        """Create comprehensive fallback content when JSON parsing fails"""
        
        logger.info(f"Creating comprehensive fallback for {title}")
        
        # Use enhanced generic content generation for all topics
        
        # Generate topic-specific introduction
        if 'python' in title.lower():
            introduction = f"Python {title.replace('Python', '').strip()} is a fundamental concept in modern software development. Python's elegant syntax and powerful features make it the preferred choice for everything from web development to artificial intelligence. {title} enables developers to write more efficient, maintainable, and scalable code. Major companies like Google, Netflix, and Instagram rely heavily on Python and these advanced techniques in their production systems."
        else:
            introduction = f"{title} is a critical technology in modern software development, enabling developers to build robust, scalable, and efficient applications. This advanced topic covers professional-grade techniques used in production environments by leading technology companies. Mastering {title} will enhance your ability to solve complex problems and build systems that can handle real-world challenges at scale."
        
        # Create 8 comprehensive exercises with actual working code and progressive difficulty
        exercises = [
            {
                "title": f"Beginner: Basic {title} Setup",
                "description": f"Build a foundational {title} system with proper setup and basic functionality",
                "difficulty": "Beginner",
                "estimated_time": "20 minutes",
                "learning_outcome": f"Understand core {title} concepts and basic implementation patterns",
                "prerequisites": ["Basic Python knowledge", "Understanding of object-oriented programming"],
                "starter_code": f"# Beginner {title} Implementation\\nimport os\\nimport logging\\nfrom typing import List, Dict, Any, Optional\\nfrom datetime import datetime\\n\\nclass Basic{title.replace(' ', '')}:\\n    def __init__(self, config: Dict[str, Any] = None):\\n        self.logger = logging.getLogger(__name__)\\n        self.config = config or {{}}\\n        self.initialized = False\\n        # TODO: Add initialization logic\\n        \\n    def setup(self) -> bool:\\n        # TODO: Setup the system\\n        try:\\n            # Add setup logic here\\n            self.initialized = True\\n            return True\\n        except Exception as e:\\n            self.logger.error(f'Setup failed: {{e}}')\\n            return False\\n    \\n    def process_single(self, input_data: Any) -> Dict[str, Any]:\\n        # TODO: Process single input and return results\\n        if not self.initialized:\\n            return {{'error': 'System not initialized'}}\\n        # Add processing logic here\\n        return {{'status': 'success', 'data': input_data}}\\n\\n# TODO: Add example usage and testing",
                "solution": f"# Complete Beginner {title} Implementation\\nimport os\\nimport logging\\nimport json\\nfrom typing import List, Dict, Any, Optional\\nfrom datetime import datetime\\nfrom pathlib import Path\\n\\nclass Basic{title.replace(' ', '')}:\\n    def __init__(self, config: Dict[str, Any] = None):\\n        self.logger = logging.getLogger(__name__)\\n        self.config = config or {{\\n            'log_level': 'INFO',\\n            'output_dir': './output',\\n            'max_retries': 3\\n        }}\\n        self.initialized = False\\n        self.stats = {{\\n            'processed_count': 0,\\n            'error_count': 0,\\n            'start_time': None\\n        }}\\n        \\n    def setup(self) -> bool:\\n        try:\\n            self.logger.info('Setting up {title} system')\\n            \\n            # Create output directory\\n            output_dir = Path(self.config['output_dir'])\\n            output_dir.mkdir(exist_ok=True)\\n            \\n            # Configure logging\\n            log_level = getattr(logging, self.config['log_level'].upper())\\n            logging.basicConfig(level=log_level)\\n            \\n            self.stats['start_time'] = datetime.now()\\n            self.initialized = True\\n            self.logger.info('System setup completed successfully')\\n            return True\\n            \\n        except Exception as e:\\n            self.logger.error(f'Setup failed: {{e}}')\\n            return False\\n    \\n    def process_single(self, input_data: Any) -> Dict[str, Any]:\\n        if not self.initialized:\\n            return {{'error': 'System not initialized'}}\\n            \\n        try:\\n            self.logger.debug(f'Processing input: {{type(input_data)}}')\\n            \\n            # Validate input\\n            if input_data is None:\\n                raise ValueError('Input data cannot be None')\\n            \\n            # Process the data\\n            result = {{\\n                'id': f'proc_{{self.stats[\"processed_count\"] + 1}}',\\n                'timestamp': datetime.now().isoformat(),\\n                'input_type': str(type(input_data).__name__),\\n                'processed_data': str(input_data).upper() if isinstance(input_data, str) else input_data,\\n                'status': 'success',\\n                'system': '{title}'\\n            }}\\n            \\n            # Update stats\\n            self.stats['processed_count'] += 1\\n            \\n            self.logger.info(f'Successfully processed item {{result[\"id\"]}}')\\n            return result\\n            \\n        except Exception as e:\\n            self.stats['error_count'] += 1\\n            error_result = {{\\n                'error': str(e),\\n                'timestamp': datetime.now().isoformat(),\\n                'status': 'failed'\\n            }}\\n            self.logger.error(f'Processing failed: {{e}}')\\n            return error_result\\n    \\n    def get_stats(self) -> Dict[str, Any]:\\n        uptime = None\\n        if self.stats['start_time']:\\n            uptime = (datetime.now() - self.stats['start_time']).total_seconds()\\n        \\n        return {{\\n            'processed_count': self.stats['processed_count'],\\n            'error_count': self.stats['error_count'],\\n            'uptime_seconds': uptime,\\n            'success_rate': self.stats['processed_count'] / max(1, self.stats['processed_count'] + self.stats['error_count'])\\n        }}\\n\\n# Example usage and testing\\nif __name__ == '__main__':\\n    # Setup logging\\n    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')\\n    \\n    # Create and setup system\\n    system = Basic{title.replace(' ', '')}()\\n    \\n    if system.setup():\\n        # Test with various inputs\\n        test_inputs = ['hello world', 123, ['a', 'b', 'c'], {{'key': 'value'}}, None]\\n        \\n        print('Testing {title} System:')\\n        print('=' * 40)\\n        \\n        for i, test_input in enumerate(test_inputs, 1):\\n            print(f'\\nTest {{i}}: {{test_input}}')\\n            result = system.process_single(test_input)\\n            print(f'Result: {{json.dumps(result, indent=2)}}')\\n        \\n        # Show final stats\\n        print('\\nFinal Statistics:')\\n        print('=' * 40)\\n        stats = system.get_stats()\\n        print(json.dumps(stats, indent=2))\\n    else:\\n        print('Failed to setup system')",
                "solution_explanation": f"This beginner solution demonstrates a complete {title} implementation with proper initialization, configuration management, error handling, logging, statistics tracking, and comprehensive testing. It includes input validation, structured error responses, and performance metrics collection.",
                "key_concepts": [f"Basic {title} setup", "Configuration management", "Error handling", "Logging", "Statistics tracking", "Input validation"],
                "test_cases": ["Test successful initialization", "Test input processing", "Test error handling", "Test statistics collection"],
                "bonus_challenge": "Add configuration file loading and custom output formatting options"
            },
            {
                "title": f"Intermediate: {title} with Configuration Management",
                "description": f"Implement {title} with advanced configuration, validation, and environment management",
                "difficulty": "Intermediate",
                "estimated_time": "30 minutes",
                "learning_outcome": f"Master configuration management and environment-specific deployments for {title}",
                "prerequisites": ["Completion of beginner exercise", "Understanding of configuration patterns"],
                "starter_code": f"# Intermediate {title} with Configuration\\nimport os\\nimport yaml\\nimport json\\nfrom typing import Dict, Any, Optional, List\\nfrom dataclasses import dataclass, field\\nfrom pathlib import Path\\nfrom enum import Enum\\n\\nclass Environment(Enum):\\n    DEVELOPMENT = 'dev'\\n    STAGING = 'staging'\\n    PRODUCTION = 'prod'\\n\\n@dataclass\\nclass {title.replace(' ', '')}Config:\\n    environment: Environment\\n    debug_mode: bool = False\\n    max_connections: int = 10\\n    timeout_seconds: float = 30.0\\n    # TODO: Add more configuration parameters\\n\\nclass Configurable{title.replace(' ', '')}:\\n    def __init__(self, config_path: Optional[str] = None):\\n        # TODO: Load and validate configuration\\n        pass\\n    \\n    def load_config(self, config_path: str) -> {title.replace(' ', '')}Config:\\n        # TODO: Load configuration from file\\n        pass\\n    \\n    def validate_config(self, config: {title.replace(' ', '')}Config) -> bool:\\n        # TODO: Validate configuration parameters\\n        pass",
                "solution": f"# Complete Intermediate {title} Implementation\\nimport os\\nimport yaml\\nimport json\\nimport logging\\nfrom typing import Dict, Any, Optional, List, Union\\nfrom dataclasses import dataclass, field, asdict\\nfrom pathlib import Path\\nfrom enum import Enum\\nfrom datetime import datetime\\n\\nclass Environment(Enum):\\n    DEVELOPMENT = 'dev'\\n    STAGING = 'staging'\\n    PRODUCTION = 'prod'\\n\\n@dataclass\\nclass {title.replace(' ', '')}Config:\\n    environment: Environment\\n    debug_mode: bool = False\\n    max_connections: int = 10\\n    timeout_seconds: float = 30.0\\n    log_level: str = 'INFO'\\n    output_directory: str = './output'\\n    enable_metrics: bool = True\\n    retry_attempts: int = 3\\n    batch_size: int = 100\\n    custom_settings: Dict[str, Any] = field(default_factory=dict)\\n\\nclass ConfigurationError(Exception):\\n    pass\\n\\nclass Configurable{title.replace(' ', '')}:\\n    def __init__(self, config_path: Optional[str] = None):\\n        self.logger = logging.getLogger(__name__)\\n        self.config: Optional[{title.replace(' ', '')}Config] = None\\n        self.initialized = False\\n        \\n        if config_path:\\n            self.config = self.load_config(config_path)\\n        else:\\n            self.config = self._load_default_config()\\n        \\n        if not self.validate_config(self.config):\\n            raise ConfigurationError('Invalid configuration')\\n    \\n    def _load_default_config(self) -> {title.replace(' ', '')}Config:\\n        env = os.getenv('APP_ENV', 'development').lower()\\n        environment = Environment.DEVELOPMENT\\n        \\n        if env == 'staging':\\n            environment = Environment.STAGING\\n        elif env == 'production':\\n            environment = Environment.PRODUCTION\\n        \\n        return {title.replace(' ', '')}Config(\\n            environment=environment,\\n            debug_mode=environment == Environment.DEVELOPMENT,\\n            max_connections=int(os.getenv('MAX_CONNECTIONS', '10')),\\n            timeout_seconds=float(os.getenv('TIMEOUT_SECONDS', '30.0')),\\n            log_level=os.getenv('LOG_LEVEL', 'INFO')\\n        )\\n    \\n    def load_config(self, config_path: str) -> {title.replace(' ', '')}Config:\\n        try:\\n            config_file = Path(config_path)\\n            \\n            if not config_file.exists():\\n                raise ConfigurationError(f'Configuration file not found: {{config_path}}')\\n            \\n            with open(config_file, 'r') as f:\\n                if config_file.suffix.lower() == '.yaml' or config_file.suffix.lower() == '.yml':\\n                    config_data = yaml.safe_load(f)\\n                elif config_file.suffix.lower() == '.json':\\n                    config_data = json.load(f)\\n                else:\\n                    raise ConfigurationError(f'Unsupported configuration file format: {{config_file.suffix}}')\\n            \\n            # Parse environment\\n            env_str = config_data.get('environment', 'development').lower()\\n            environment = Environment.DEVELOPMENT\\n            if env_str == 'staging':\\n                environment = Environment.STAGING\\n            elif env_str == 'production':\\n                environment = Environment.PRODUCTION\\n            \\n            config = {title.replace(' ', '')}Config(\\n                environment=environment,\\n                debug_mode=config_data.get('debug_mode', False),\\n                max_connections=config_data.get('max_connections', 10),\\n                timeout_seconds=config_data.get('timeout_seconds', 30.0),\\n                log_level=config_data.get('log_level', 'INFO'),\\n                output_directory=config_data.get('output_directory', './output'),\\n                enable_metrics=config_data.get('enable_metrics', True),\\n                retry_attempts=config_data.get('retry_attempts', 3),\\n                batch_size=config_data.get('batch_size', 100),\\n                custom_settings=config_data.get('custom_settings', {{}})\\n            )\\n            \\n            self.logger.info(f'Configuration loaded from {{config_path}}')\\n            return config\\n            \\n        except Exception as e:\\n            raise ConfigurationError(f'Failed to load configuration: {{e}}')\\n    \\n    def validate_config(self, config: {title.replace(' ', '')}Config) -> bool:\\n        try:\\n            # Validate basic parameters\\n            if config.max_connections <= 0:\\n                raise ValueError('max_connections must be positive')\\n            \\n            if config.timeout_seconds <= 0:\\n                raise ValueError('timeout_seconds must be positive')\\n            \\n            if config.retry_attempts < 0:\\n                raise ValueError('retry_attempts cannot be negative')\\n            \\n            if config.batch_size <= 0:\\n                raise ValueError('batch_size must be positive')\\n            \\n            # Validate log level\\n            valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']\\n            if config.log_level.upper() not in valid_log_levels:\\n                raise ValueError(f'Invalid log_level: {{config.log_level}}')\\n            \\n            # Validate output directory\\n            output_path = Path(config.output_directory)\\n            try:\\n                output_path.mkdir(parents=True, exist_ok=True)\\n            except Exception as e:\\n                raise ValueError(f'Cannot create output directory: {{e}}')\\n            \\n            # Environment-specific validations\\n            if config.environment == Environment.PRODUCTION:\\n                if config.debug_mode:\\n                    self.logger.warning('Debug mode enabled in production environment')\\n                if config.max_connections < 5:\\n                    raise ValueError('Production environment requires at least 5 connections')\\n            \\n            self.logger.info('Configuration validation successful')\\n            return True\\n            \\n        except Exception as e:\\n            self.logger.error(f'Configuration validation failed: {{e}}')\\n            return False\\n    \\n    def save_config(self, output_path: str, format_type: str = 'yaml') -> bool:\\n        try:\\n            config_dict = asdict(self.config)\\n            config_dict['environment'] = self.config.environment.value\\n            \\n            output_file = Path(output_path)\\n            \\n            with open(output_file, 'w') as f:\\n                if format_type.lower() == 'yaml':\\n                    yaml.dump(config_dict, f, default_flow_style=False, indent=2)\\n                elif format_type.lower() == 'json':\\n                    json.dump(config_dict, f, indent=2)\\n                else:\\n                    raise ValueError(f'Unsupported format: {{format_type}}')\\n            \\n            self.logger.info(f'Configuration saved to {{output_path}}')\\n            return True\\n            \\n        except Exception as e:\\n            self.logger.error(f'Failed to save configuration: {{e}}')\\n            return False\\n    \\n    def get_environment_info(self) -> Dict[str, Any]:\\n        return {{\\n            'environment': self.config.environment.value,\\n            'debug_mode': self.config.debug_mode,\\n            'configuration_valid': self.validate_config(self.config),\\n            'timestamp': datetime.now().isoformat()\\n        }}\\n\\n# Example usage and testing\\nif __name__ == '__main__':\\n    logging.basicConfig(level=logging.INFO)\\n    \\n    try:\\n        # Test with default configuration\\n        system = Configurable{title.replace(' ', '')}()\\n        print('Default Configuration:')\\n        print(json.dumps(asdict(system.config), indent=2, default=str))\\n        \\n        # Test environment info\\n        env_info = system.get_environment_info()\\n        print('\\nEnvironment Info:')\\n        print(json.dumps(env_info, indent=2))\\n        \\n        # Test saving configuration\\n        system.save_config('test_config.yaml', 'yaml')\\n        system.save_config('test_config.json', 'json')\\n        \\n        print('\\nConfiguration management test completed successfully!')\\n        \\n    except ConfigurationError as e:\\n        print(f'Configuration error: {{e}}')\\n    except Exception as e:\\n        print(f'Unexpected error: {{e}}')",
                "solution_explanation": f"This intermediate solution demonstrates advanced configuration management for {title} systems, including file-based configuration loading, environment-specific settings, validation, and serialization. It shows proper error handling, logging, and environment management patterns used in production systems.",
                "key_concepts": ["Configuration management", "Environment handling", "Data validation", "File I/O", "Error handling", "Logging"],
                "test_cases": ["Test default configuration", "Test file loading", "Test validation", "Test environment detection"],
                "bonus_challenge": "Add configuration hot-reloading and configuration change notifications"
            },
            {
                "title": f"Advanced: {title} with Async Processing",
                "description": f"Implement scalable {title} with asynchronous operations and concurrent processing",
                "difficulty": "Advanced",
                "estimated_time": "45 minutes",
                "learning_outcome": f"Master advanced {title} patterns for high-performance production systems",
                "starter_code": f"# Advanced {title} with Async\\nimport asyncio\\nfrom typing import Dict, List, Any\\n\\nclass Advanced{title.replace(' ', '')}System:\\n    def __init__(self):\\n        # TODO: Add async implementation\\n        pass\\n        \\n    async def process_batch(self, items: List[Any]) -> List[Dict[str, Any]]:\\n        # TODO: Implement batch processing\\n        pass",
                "solution": f"import asyncio\\nimport logging\\nfrom typing import Dict, List, Any, Optional\\nfrom dataclasses import dataclass\\nfrom datetime import datetime\\nimport json\\n\\n@dataclass\\nclass {title.replace(' ', '')}Config:\\n    max_connections: int = 10\\n    timeout: float = 30.0\\n    batch_size: int = 100\\n\\nclass Advanced{title.replace(' ', '')}System:\\n    def __init__(self, config: {title.replace(' ', '')}Config):\\n        self.config = config\\n        self.logger = logging.getLogger(__name__)\\n        self.semaphore = asyncio.Semaphore(config.max_connections)\\n        \\n    async def process_item(self, item: Any) -> Dict[str, Any]:\\n        async with self.semaphore:\\n            try:\\n                self.logger.info(f'Processing item: {{item}}')\\n                await asyncio.sleep(0.1)  # Simulate async work\\n                return {{\\n                    'item': item,\\n                    'status': 'processed',\\n                    'timestamp': datetime.now().isoformat(),\\n                    'system': '{title}'\\n                }}\\n            except Exception as e:\\n                self.logger.error(f'Error processing {{item}}: {{e}}')\\n                return {{'item': item, 'status': 'error', 'message': str(e)}}\\n                \\n    async def process_batch(self, items: List[Any]) -> List[Dict[str, Any]]:\\n        self.logger.info(f'Processing batch of {{len(items)}} items')\\n        tasks = [self.process_item(item) for item in items]\\n        results = await asyncio.gather(*tasks, return_exceptions=True)\\n        \\n        processed_results = []\\n        for result in results:\\n            if isinstance(result, Exception):\\n                processed_results.append({{'status': 'error', 'message': str(result)}})\\n            else:\\n                processed_results.append(result)\\n                \\n        return processed_results\\n\\n# Example usage\\nasync def main():\\n    config = {title.replace(' ', '')}Config(max_connections=5, timeout=10.0)\\n    system = Advanced{title.replace(' ', '')}System(config)\\n    \\n    items = ['item1', 'item2', 'item3', 'item4', 'item5']\\n    results = await system.process_batch(items)\\n    print(json.dumps(results, indent=2))\\n\\nif __name__ == '__main__':\\n    logging.basicConfig(level=logging.INFO)\\n    asyncio.run(main())",
                "solution_explanation": f"This advanced solution implements async processing with semaphores for concurrency control, proper resource management, and comprehensive error handling for scalable {title} systems.",
                "key_concepts": ["Async programming", "Concurrency control", "Batch processing", "Resource management"]
            },
            {
                "title": f"Production {title} with Monitoring",
                "description": f"Build enterprise-grade {title} with comprehensive monitoring",
                "difficulty": "Expert",
                "learning_outcome": f"Implement production-ready {title} with observability",
                "starter_code": f"# Production {title} with Monitoring\\nimport time\\nfrom typing import Dict, Any\\nfrom abc import ABC, abstractmethod\\n\\nclass MetricsCollector(ABC):\\n    @abstractmethod\\n    def increment_counter(self, name: str, value: int = 1) -> None:\\n        pass\\n\\nclass Production{title.replace(' ', '')}System:\\n    def __init__(self, metrics: MetricsCollector):\\n        self.metrics = metrics\\n        # TODO: Add production implementation",
                "solution": f"import time\\nimport logging\\nimport threading\\nfrom typing import Dict, Any, Optional\\nfrom abc import ABC, abstractmethod\\nfrom datetime import datetime\\nfrom collections import defaultdict\\nimport json\\n\\nclass MetricsCollector(ABC):\\n    @abstractmethod\\n    def increment_counter(self, name: str, value: int = 1) -> None:\\n        pass\\n        \\n    @abstractmethod\\n    def record_timing(self, name: str, duration: float) -> None:\\n        pass\\n\\nclass InMemoryMetrics(MetricsCollector):\\n    def __init__(self):\\n        self.counters = defaultdict(int)\\n        self.timings = defaultdict(list)\\n        self._lock = threading.Lock()\\n        \\n    def increment_counter(self, name: str, value: int = 1) -> None:\\n        with self._lock:\\n            self.counters[name] += value\\n            \\n    def record_timing(self, name: str, duration: float) -> None:\\n        with self._lock:\\n            self.timings[name].append(duration)\\n            if len(self.timings[name]) > 1000:\\n                self.timings[name] = self.timings[name][-1000:]\\n                \\n    def get_metrics(self) -> Dict[str, Any]:\\n        with self._lock:\\n            return {{\\n                'counters': dict(self.counters),\\n                'timings_avg': {{k: sum(v)/len(v) if v else 0 for k, v in self.timings.items()}}\\n            }}\\n\\nclass Production{title.replace(' ', '')}System:\\n    def __init__(self, metrics: MetricsCollector):\\n        self.metrics = metrics\\n        self.logger = logging.getLogger(__name__)\\n        self.start_time = datetime.now()\\n        self._processed_count = 0\\n        self._error_count = 0\\n        \\n    def process_with_monitoring(self, data: Any) -> Optional[Dict[str, Any]]:\\n        start_time = time.time()\\n        self.metrics.increment_counter('{title.lower()}_requests_total')\\n        \\n        try:\\n            self.logger.info(f'Processing request with monitoring')\\n            result = {{\\n                'data': data,\\n                'processed_at': datetime.now().isoformat(),\\n                'system': '{title}',\\n                'request_id': f'req_{{int(time.time() * 1000)}}'\\n            }}\\n            \\n            self._processed_count += 1\\n            self.metrics.increment_counter('{title.lower()}_success_total')\\n            return result\\n            \\n        except Exception as e:\\n            self._error_count += 1\\n            self.metrics.increment_counter('{title.lower()}_errors_total')\\n            self.logger.error(f'Processing failed: {{e}}')\\n            return None\\n            \\n        finally:\\n            duration = time.time() - start_time\\n            self.metrics.record_timing('{title.lower()}_request_duration', duration)\\n            \\n    def get_health_status(self) -> Dict[str, Any]:\\n        uptime = (datetime.now() - self.start_time).total_seconds()\\n        return {{\\n            'status': 'healthy',\\n            'uptime_seconds': uptime,\\n            'processed_count': self._processed_count,\\n            'error_count': self._error_count,\\n            'error_rate': self._error_count / max(self._processed_count, 1)\\n        }}\\n\\n# Example usage\\nif __name__ == '__main__':\\n    logging.basicConfig(level=logging.INFO)\\n    \\n    metrics = InMemoryMetrics()\\n    system = Production{title.replace(' ', '')}System(metrics)\\n    \\n    # Process some requests\\n    for i in range(5):\\n        result = system.process_with_monitoring(f'test_data_{{i}}')\\n        print(f'Result {{i}}: {{result}}')\\n        \\n    # Check health and metrics\\n    health = system.get_health_status()\\n    metrics_data = metrics.get_metrics()\\n    \\n    print('\\nHealth Status:', json.dumps(health, indent=2))\\n    print('\\nMetrics:', json.dumps(metrics_data, indent=2))",
                "solution_explanation": f"This production solution implements comprehensive monitoring with metrics collection, health checks, error tracking, and performance measurement following enterprise observability patterns.",
                "key_concepts": ["Production monitoring", "Metrics collection", "Health checks", "Observability"]
            },
            {
                "title": f"Scalable {title} Architecture",
                "description": f"Design and implement a horizontally scalable {title} system",
                "difficulty": "Expert",
                "learning_outcome": f"Master scalable architecture patterns for {title}",
                "starter_code": f"# Scalable {title} Architecture\\nfrom typing import Dict, List, Any\\nfrom abc import ABC, abstractmethod\\n\\nclass LoadBalancer(ABC):\\n    @abstractmethod\\n    def get_next_worker(self) -> str:\\n        pass\\n\\nclass Scalable{title.replace(' ', '')}System:\\n    def __init__(self, workers: List[str]):\\n        self.workers = workers\\n        # TODO: Implement scalable architecture",
                "solution": f"import asyncio\\nimport hashlib\\nimport logging\\nfrom typing import Dict, List, Any, Optional\\nfrom abc import ABC, abstractmethod\\nfrom dataclasses import dataclass\\nfrom datetime import datetime\\nimport json\\nimport random\\n\\n@dataclass\\nclass WorkerNode:\\n    id: str\\n    endpoint: str\\n    weight: int = 1\\n    active: bool = True\\n    current_load: int = 0\\n    max_load: int = 100\\n\\nclass LoadBalancer(ABC):\\n    @abstractmethod\\n    def get_next_worker(self) -> Optional[WorkerNode]:\\n        pass\\n\\nclass RoundRobinBalancer(LoadBalancer):\\n    def __init__(self, workers: List[WorkerNode]):\\n        self.workers = workers\\n        self.current_index = 0\\n        \\n    def get_next_worker(self) -> Optional[WorkerNode]:\\n        active_workers = [w for w in self.workers if w.active and w.current_load < w.max_load]\\n        if not active_workers:\\n            return None\\n        worker = active_workers[self.current_index % len(active_workers)]\\n        self.current_index += 1\\n        return worker\\n\\nclass Scalable{title.replace(' ', '')}System:\\n    def __init__(self, workers: List[WorkerNode]):\\n        self.workers = workers\\n        self.logger = logging.getLogger(__name__)\\n        self.load_balancer = RoundRobinBalancer(workers)\\n        self.request_count = 0\\n        self.worker_stats = {{worker.id: {{'requests': 0, 'errors': 0}} for worker in workers}}\\n        \\n    async def process_request(self, data: Any) -> Dict[str, Any]:\\n        self.request_count += 1\\n        worker = self.load_balancer.get_next_worker()\\n        \\n        if not worker:\\n            self.logger.error('No available workers')\\n            return {{'status': 'error', 'message': 'No available workers'}}\\n            \\n        try:\\n            worker.current_load += 1\\n            self.worker_stats[worker.id]['requests'] += 1\\n            \\n            self.logger.info(f'Processing request on worker {{worker.id}}')\\n            await asyncio.sleep(0.1)  # Simulate work\\n            \\n            result = {{\\n                'status': 'success',\\n                'worker_id': worker.id,\\n                'request_id': self.request_count,\\n                'data': data,\\n                'processed_at': datetime.now().isoformat()\\n            }}\\n            return result\\n            \\n        except Exception as e:\\n            self.worker_stats[worker.id]['errors'] += 1\\n            self.logger.error(f'Worker {{worker.id}} error: {{e}}')\\n            return {{'status': 'error', 'worker_id': worker.id, 'message': str(e)}}\\n            \\n        finally:\\n            worker.current_load = max(0, worker.current_load - 1)\\n            \\n    def get_system_stats(self) -> Dict[str, Any]:\\n        active_workers = len([w for w in self.workers if w.active])\\n        return {{\\n            'total_requests': self.request_count,\\n            'active_workers': active_workers,\\n            'total_workers': len(self.workers),\\n            'worker_stats': self.worker_stats\\n        }}\\n\\n# Example usage\\nasync def main():\\n    workers = [\\n        WorkerNode('worker-1', 'http://worker1:8080', weight=2),\\n        WorkerNode('worker-2', 'http://worker2:8080', weight=1),\\n        WorkerNode('worker-3', 'http://worker3:8080', weight=1)\\n    ]\\n    \\n    system = Scalable{title.replace(' ', '')}System(workers)\\n    \\n    # Process multiple requests\\n    tasks = [system.process_request(f'request_{{i}}') for i in range(10)]\\n    results = await asyncio.gather(*tasks)\\n    \\n    stats = system.get_system_stats()\\n    print(f'Processed {{len(results)}} requests')\\n    print(json.dumps(stats, indent=2))\\n\\nif __name__ == '__main__':\\n    logging.basicConfig(level=logging.INFO)\\n    asyncio.run(main())",
                "solution_explanation": f"This scalable solution implements load balancing, worker management, load tracking, and distributed processing patterns for horizontal scaling of {title} systems.",
                "key_concepts": ["Load balancing", "Horizontal scaling", "Worker management", "Distributed processing"]
            },
            {
                "title": f"Testing and Quality Assurance",
                "description": f"Implement comprehensive testing strategies for {title}",
                "difficulty": "Hard",
                "learning_outcome": f"Master testing patterns and QA for {title}",
                "starter_code": f"# Testing for {title}\\nimport unittest\\nfrom unittest.mock import Mock\\n\\nclass {title.replace(' ', '')}TestSuite(unittest.TestCase):\\n    def setUp(self):\\n        # TODO: Set up test fixtures\\n        pass\\n        \\n    def test_basic_functionality(self):\\n        # TODO: Add tests\\n        pass",
                "solution": f"import unittest\\nfrom unittest.mock import Mock, patch\\nimport asyncio\\nfrom typing import Any, Dict\\nfrom datetime import datetime\\n\\n# Mock system for testing\\nclass {title.replace(' ', '')}System:\\n    def __init__(self, config: Dict[str, Any] = None):\\n        self.config = config or {{}}\\n        self.initialized = False\\n        \\n    def initialize(self) -> bool:\\n        self.initialized = True\\n        return True\\n        \\n    def process(self, data: Any) -> Dict[str, Any]:\\n        if not self.initialized:\\n            raise ValueError('System not initialized')\\n        return {{'status': 'success', 'data': data}}\\n\\nclass {title.replace(' ', '')}TestSuite(unittest.TestCase):\\n    def setUp(self):\\n        self.system = {title.replace(' ', '')}System()\\n        self.test_data = {{'test': 'data'}}\\n        \\n    def test_initialization(self):\\n        self.assertFalse(self.system.initialized)\\n        result = self.system.initialize()\\n        self.assertTrue(result)\\n        self.assertTrue(self.system.initialized)\\n        \\n    def test_basic_processing(self):\\n        self.system.initialize()\\n        result = self.system.process(self.test_data)\\n        self.assertEqual(result['status'], 'success')\\n        self.assertEqual(result['data'], self.test_data)\\n        \\n    def test_processing_without_initialization(self):\\n        with self.assertRaises(ValueError):\\n            self.system.process(self.test_data)\\n            \\n    def test_configuration_handling(self):\\n        config = {{'timeout': 30}}\\n        system = {title.replace(' ', '')}System(config)\\n        self.assertEqual(system.config, config)\\n        \\n    @patch('logging.getLogger')\\n    def test_logging_integration(self, mock_logger):\\n        system = {title.replace(' ', '')}System()\\n        system.initialize()\\n        system.process(self.test_data)\\n        mock_logger.assert_called()\\n        \\n    def test_error_handling(self):\\n        self.system.initialize()\\n        result = self.system.process(None)\\n        self.assertEqual(result['status'], 'success')\\n        \\n    def test_performance(self):\\n        self.system.initialize()\\n        start_time = datetime.now()\\n        \\n        for i in range(100):\\n            self.system.process(f'test_{{i}}')\\n            \\n        duration = (datetime.now() - start_time).total_seconds()\\n        self.assertLess(duration, 1.0)  # Should process 100 items in under 1 second\\n\\ndef run_tests():\\n    loader = unittest.TestLoader()\\n    suite = loader.loadTestsFromTestCase({title.replace(' ', '')}TestSuite)\\n    runner = unittest.TextTestRunner(verbosity=2)\\n    result = runner.run(suite)\\n    return result.wasSuccessful()\\n\\nif __name__ == '__main__':\\n    success = run_tests()\\n    print(f'\\nTests {{\"PASSED\" if success else \"FAILED\"}}')\\n    exit(0 if success else 1)",
                "solution_explanation": f"This testing solution provides comprehensive test coverage including unit tests, integration tests, error handling tests, performance tests, and mocking strategies for {title} systems.",
                "key_concepts": ["Unit testing", "Integration testing", "Mocking", "Performance testing"]
            }
        ]
        
        return {
            'introduction': introduction,
            'concept_explanation': f"{title} involves multiple interconnected concepts that work together to solve complex problems. The core principles include proper architecture design, efficient data handling, error management, and performance optimization.",
            'project_overview': f"In this lesson, we'll build a comprehensive {title} system from scratch, covering fundamental concepts, advanced techniques, and real-world applications.",
            'setup_instructions': f"Set up your development environment for {title} with the required dependencies and tools.",
            'code_examples': [
                {
                    "title": f"Basic {title} Setup",
                    "description": f"Complete setup and basic usage of {title}",
                    "code": f"import logging\\nfrom typing import Dict, Any\\nfrom datetime import datetime\\n\\nclass {title.replace(' ', '')}Manager:\\n    def __init__(self):\\n        self.logger = logging.getLogger(__name__)\\n        self.initialized = False\\n        \\n    def initialize(self) -> bool:\\n        self.logger.info('Initializing system')\\n        self.initialized = True\\n        return True\\n        \\n    def process(self, data: Any) -> Dict[str, Any]:\\n        if not self.initialized:\\n            raise ValueError('System not initialized')\\n        return {{'status': 'success', 'data': data, 'timestamp': datetime.now().isoformat()}}\\n\\n# Usage\\nmanager = {title.replace(' ', '')}Manager()\\nmanager.initialize()\\nresult = manager.process('test')\\nprint(result)",
                    "explanation": f"This example demonstrates the basic setup and usage of {title} with proper initialization and error handling.",
                    "expected_output": "{'status': 'success', 'data': 'test', 'timestamp': '2023-...'}"
                }
            ],
            'hands_on_exercises': exercises,
            'troubleshooting': f"Common issues when working with {title} include configuration problems, performance bottlenecks, and integration challenges.",
            'real_world_applications': f"{title} is used in various industries for solving complex problems including enterprise applications and data processing systems.",
            'next_steps': f"Continue learning {title} by exploring advanced topics and building your own applications.",
            'fun_challenge': f"Build a creative project that showcases advanced {title} techniques."
        }
    
