"""
Course Planner Component
Analyzes domains and generates course structures
"""

import json
import logging
from typing import Dict, List, Any, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from config import get_config
from mocks.mock_clients import MockOpenAIClient

logger = logging.getLogger(__name__)

class Lesson(BaseModel):
    """Individual lesson structure"""
    lesson_number: int = Field(..., description="Lesson number")
    title: str = Field(..., description="Lesson title")
    duration_minutes: int = Field(..., description="Lesson duration in minutes")
    type: str = Field(..., description="Lesson type: theory, hands-on, or mixed")
    learning_objectives: List[str] = Field(..., description="Learning objectives")
    prerequisites: List[str] = Field(..., description="Prerequisites")
    has_coding: bool = Field(..., description="Whether lesson includes coding")

class Curriculum(BaseModel):
    """Complete course curriculum"""
    course_title: str = Field(..., description="Course title")
    difficulty: str = Field(..., description="Course difficulty level")
    total_duration_hours: float = Field(..., description="Total course duration in hours")
    prerequisites: List[str] = Field(..., description="Course prerequisites")
    learning_objectives: List[str] = Field(..., description="Course learning objectives")
    target_audience: str = Field(..., description="Target audience")
    lessons: List[Lesson] = Field(..., description="List of lessons")

class CoursePlanner:
    """
    Plans course structure and generates curriculum
    """
    
    def __init__(self, api_key: str):
        """Initialize with OpenAI API key"""
        self.config = get_config()
        
        if self.config.test_mode:
            logger.info("Using mock OpenAI client for testing")
            self.client = MockOpenAIClient(api_key)
        else:
            self.client = OpenAI(api_key=api_key)
    
    def analyze_domain(self, domain: str) -> Dict[str, Any]:
        """
        Analyze domain to understand scope and requirements
        
        Args:
            domain: Course domain (e.g., "RAG", "FastAPI Development")
            
        Returns:
            Domain analysis with scope, difficulty, and structure
        """
        try:
            logger.info(f"Analyzing domain: {domain}")
            
            prompt = f"""
            Analyze the domain "{domain}" for creating an online course.
            
            Provide a JSON response with:
            {{
                "domain_scope": "Brief description of what this domain covers",
                "difficulty_level": "beginner, intermediate, or advanced",
                "estimated_hours": <number>,
                "key_topics": ["topic1", "topic2", "topic3"],
                "prerequisites": ["prereq1", "prereq2"],
                "target_audience": "Description of who this course is for",
                "learning_outcomes": ["outcome1", "outcome2", "outcome3"]
            }}
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            analysis = json.loads(content)
            
            logger.info(f"Domain analysis completed for: {domain}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing domain: {str(e)}")
            # Return fallback analysis
            return {
                "domain_scope": f"Comprehensive course on {domain}",
                "difficulty_level": "intermediate",
                "estimated_hours": 5,
                "key_topics": [f"{domain} fundamentals", f"{domain} implementation", f"{domain} best practices"],
                "prerequisites": ["Basic programming knowledge", "Familiarity with web development"],
                "target_audience": "Developers and programmers interested in learning " + domain,
                "learning_outcomes": [f"Understand {domain} concepts", f"Implement {domain} solutions", f"Apply {domain} best practices"]
            }
    
    def generate_curriculum(self, domain_analysis: Dict[str, Any]) -> Curriculum:
        """
        Generate complete curriculum structure from domain analysis
        
        Args:
            domain_analysis: Result from analyze_domain()
            
        Returns:
            Complete curriculum structure
        """
        try:
            logger.info("Generating curriculum structure")
            
            # Create lesson structure
            lessons = []
            total_duration = 0
            
            # Generate domain-specific lesson topics based on the domain
            domain = domain_analysis.get('domain_scope', 'Course Topic')
            
            # Define lesson topics based on common course progression patterns
            lesson_topics = self._generate_lesson_topics(domain)
            
            # Generate 10 lessons with appropriate distribution
            lesson_types = ["theory", "theory", "hands-on", "hands-on", "hands-on", "hands-on", "hands-on", "advanced", "case_study", "project"]
            
            for i, (lesson_type, topic) in enumerate(zip(lesson_types, lesson_topics), 1):
                lesson = Lesson(
                    lesson_number=i,
                    title=topic,
                    duration_minutes=30,
                    type=lesson_type,
                    learning_objectives=self._generate_lesson_objectives(topic, lesson_type, i),
                    prerequisites=self._generate_lesson_prerequisites(i),
                    has_coding=lesson_type in ["hands-on", "advanced", "project"]
                )
                lessons.append(lesson)
                total_duration += lesson.duration_minutes
            
            # Create curriculum
            curriculum = Curriculum(
                course_title=f"Complete {domain_analysis.get('domain_scope', 'Course')} Course",
                difficulty=domain_analysis.get('difficulty_level', 'intermediate'),
                total_duration_hours=total_duration / 60,
                prerequisites=domain_analysis.get('prerequisites', []),
                learning_objectives=domain_analysis.get('learning_outcomes', []),
                target_audience=domain_analysis.get('target_audience', ''),
                lessons=lessons
            )
            
            logger.info(f"Curriculum generated: {curriculum.course_title} with {len(lessons)} lessons")
            return curriculum
            
        except Exception as e:
            logger.error(f"Error generating curriculum: {str(e)}")
            # Return fallback curriculum
            fallback_lessons = [
                Lesson(
                    lesson_number=1,
                    title="Introduction and Overview",
                    duration_minutes=30,
                    type="theory",
                    learning_objectives=["Understand course objectives", "Set up development environment"],
                    prerequisites=[],
                    has_coding=False
                )
            ]
            
            return Curriculum(
                course_title="Complete Course",
                difficulty="intermediate",
                total_duration_hours=0.5,
                prerequisites=[],
                learning_objectives=["Learn course fundamentals"],
                target_audience="Developers and learners",
                lessons=fallback_lessons
            )
    
    def _generate_lesson_topics(self, domain: str) -> List[str]:
        """Generate domain-specific lesson topics"""
        
        # Extract the main subject from domain scope
        if "Python" in domain:
            return [
                "Introduction to Python and Setup",
                "Variables, Data Types, and Basic Operations",
                "Control Flow: Conditionals and Loops",
                "Functions and Scope",
                "Data Structures: Lists, Tuples, and Dictionaries",
                "File Handling and I/O Operations",
                "Error Handling and Debugging",
                "Object-Oriented Programming Basics",
                "Working with Libraries and APIs",
                "Final Project: Building a Complete Application"
            ]
        elif "React" in domain or "Web Development" in domain:
            return [
                "Introduction to Web Development and React",
                "React Components and JSX",
                "State Management and Hooks",
                "Props and Component Communication",
                "Event Handling and User Interactions",
                "Routing and Navigation",
                "Working with APIs and Data Fetching",
                "Advanced React Patterns",
                "Testing and Debugging React Apps",
                "Final Project: Deploying a React Application"
            ]
        elif "Machine Learning" in domain or "Data Science" in domain:
            return [
                "Introduction to Machine Learning and Data Science",
                "Data Preprocessing and Cleaning",
                "Exploratory Data Analysis (EDA)",
                "Supervised Learning: Classification",
                "Supervised Learning: Regression",
                "Unsupervised Learning: Clustering",
                "Model Evaluation and Validation",
                "Feature Engineering and Selection",
                "Deep Learning Fundamentals",
                "Final Project: End-to-End ML Pipeline"
            ]
        elif "Cybersecurity" in domain:
            return [
                "Introduction to Cybersecurity Fundamentals",
                "Network Security and Protocols",
                "Cryptography and Encryption",
                "Web Application Security",
                "Social Engineering and Human Factors",
                "Penetration Testing Basics",
                "Incident Response and Forensics",
                "Security Tools and Technologies",
                "Compliance and Risk Management",
                "Final Project: Security Assessment Report"
            ]
        elif "Mobile App" in domain:
            return [
                "Introduction to Mobile Development",
                "User Interface Design Principles",
                "Navigation and User Experience",
                "Data Storage and Management",
                "API Integration and Networking",
                "Push Notifications and Permissions",
                "Testing and Debugging Mobile Apps",
                "Performance Optimization",
                "App Store Deployment",
                "Final Project: Complete Mobile Application"
            ]
        else:
            # Generic but varied topics for any domain
            return [
                f"Introduction to {domain}",
                f"Core Concepts and Fundamentals",
                f"Practical Applications and Use Cases",
                f"Advanced Techniques and Methods",
                f"Best Practices and Standards",
                f"Tools and Technologies",
                f"Problem-Solving Approaches",
                f"Integration and Deployment",
                f"Troubleshooting and Optimization",
                f"Final Project: Comprehensive {domain} Solution"
            ]
    
    def _generate_lesson_objectives(self, topic: str, lesson_type: str, lesson_number: int) -> List[str]:
        """Generate specific learning objectives for each lesson"""
        
        if lesson_type == "theory":
            return [
                f"Understand the fundamental concepts of {topic}",
                f"Learn the theoretical foundations and principles",
                f"Identify key components and their relationships"
            ]
        elif lesson_type == "hands-on":
            return [
                f"Apply {topic} concepts in practical scenarios",
                f"Practice implementation techniques and methods",
                f"Build working examples and solutions"
            ]
        elif lesson_type == "advanced":
            return [
                f"Master advanced {topic} techniques",
                f"Explore complex scenarios and edge cases",
                f"Optimize performance and efficiency"
            ]
        elif lesson_type == "case_study":
            return [
                f"Analyze real-world {topic} applications",
                f"Learn from practical examples and experiences",
                f"Understand industry best practices"
            ]
        elif lesson_type == "project":
            return [
                f"Integrate all learned concepts into a complete project",
                f"Apply problem-solving skills to real challenges",
                f"Demonstrate mastery of {topic} through practical application"
            ]
        else:
            return [
                f"Learn key concepts about {topic}",
                f"Apply knowledge in practice",
                f"Complete relevant exercises and activities"
            ]
    
    def _generate_lesson_prerequisites(self, lesson_number: int) -> List[str]:
        """Generate prerequisites for each lesson"""
        
        if lesson_number == 1:
            return ["Basic computer literacy", "Eagerness to learn"]
        elif lesson_number <= 3:
            return [f"Completion of Lesson {lesson_number - 1}"]
        else:
            return [f"Completion of previous lessons", "Understanding of fundamental concepts"] 
