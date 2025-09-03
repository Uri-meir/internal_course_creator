"""
Tests for Script Writer component
"""

import pytest
from unittest.mock import Mock, patch
from components.script_writer import ScriptWriter

class TestScriptWriter:
    """Test cases for ScriptWriter"""
    
    def setup_method(self):
        """Setup test fixtures"""
        self.mock_api_key = "test-api-key"
        self.writer = ScriptWriter(self.mock_api_key)
    
    def test_init(self):
        """Test ScriptWriter initialization"""
        assert self.writer.config is not None
        assert self.writer.client is not None
        assert self.writer.pronunciation_dict is not None
        assert self.writer.pacing_rules is not None
    
    def test_convert_to_speech_script_theory(self):
        """Test theory script conversion"""
        lesson_content = {
            'lesson_number': 1,
            'title': 'Introduction to Python',
            'type': 'theory',
            'duration_minutes': 30,
            'introduction': 'Welcome to Python programming',
            'theory_content': {
                'main_concepts': ['Variables', 'Data types'],
                'explanations': {
                    'Variables': 'Variables store data',
                    'Data types': 'Different kinds of data'
                }
            },
            'key_takeaways': ['Takeaway 1', 'Takeaway 2']
        }
        
        # Mock the client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''
        Welcome to lesson 1: Introduction to Python.
        
        In this lesson, we'll learn about variables and data types.
        Variables are containers that store data.
        Data types define what kind of data we can store.
        
        Remember these key points: variables store data, and data types matter.
        '''
        
        with patch.object(self.writer.client.chat.completions, 'create', return_value=mock_response):
            script = self.writer.convert_to_speech_script(lesson_content)
            
            assert len(script) > 0
            assert 'Python' in script
            assert 'variables' in script.lower()
    
    def test_convert_to_speech_script_hands_on(self):
        """Test hands-on script conversion"""
        lesson_content = {
            'lesson_number': 2,
            'title': 'Python Practice',
            'type': 'hands-on',
            'duration_minutes': 45,
            'setup_instructions': 'Install Python and IDE',
            'code_examples': [
                {
                    'title': 'Hello World',
                    'description': 'Basic print statement',
                    'code': 'print("Hello World")',
                    'explanation': 'Simple output'
                }
            ],
            'exercises': [
                {
                    'title': 'Exercise 1',
                    'description': 'Create variables',
                    'hints': ['Use assignment operator'],
                    'solution': 'x = 5'
                }
            ]
        }
        
        # Mock the client response
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '''
        Let's practice Python programming!
        
        First, make sure you have Python installed.
        We'll start with a simple Hello World example.
        Then you'll practice creating variables.
        
        Remember to test your code as you go.
        '''
        
        with patch.object(self.writer.client.chat.completions, 'create', return_value=mock_response):
            script = self.writer.convert_to_speech_script(lesson_content)
            
            assert len(script) > 0
            assert 'Python' in script
            assert 'practice' in script.lower()
    
    def test_estimate_script_duration(self):
        """Test script duration estimation"""
        script = """
        Welcome to this lesson. We'll learn about programming.
        
        First, let's understand the basics. Programming is about giving instructions to computers.
        
        [PAUSE:2s]
        
        Now let's practice with some examples.
        
        [PAUSE:1s]
        
        Remember these key points.
        """
        
        duration = self.writer.estimate_script_duration(script)
        
        assert duration > 0
        assert isinstance(duration, float)
    
    def test_estimate_script_duration_with_pauses(self):
        """Test script duration estimation with pauses"""
        script = """
        Hello world. [PAUSE:1s]
        This is a test. [PAUSE:2s]
        With multiple pauses. [PAUSE:0.5s]
        """
        
        duration = self.writer.estimate_script_duration(script)
        
        # Should account for pauses
        assert duration > 0.1  # At least 0.1 minutes
    
    def test_estimate_script_duration_fallback(self):
        """Test script duration estimation fallback on error"""
        # Mock to raise exception
        with patch.object(self.writer, '_count_words', side_effect=Exception("Error")):
            duration = self.writer.estimate_script_duration("Test script")
            
            # Should return fallback duration
            assert duration > 0
            assert isinstance(duration, float)
    
    def test_add_timing_cues(self):
        """Test timing cues addition"""
        script = "Hello world. This is a test. With multiple sentences."
        
        enhanced_script = self.writer._add_timing_cues(script)
        
        assert '[PAUSE:' in enhanced_script
        assert len(enhanced_script) > len(script)
    
    def test_create_fallback_script(self):
        """Test fallback script creation"""
        lesson_content = {
            'title': 'Test Lesson',
            'lesson_number': 1
        }
        
        script = self.writer._create_fallback_script(lesson_content)
        
        assert len(script) > 0
        assert 'Test Lesson' in script
        assert 'lesson 1' in script.lower()
        assert '[OPENING:' in script
        assert '[CLOSING:' in script
    
    def test_pronunciation_dict(self):
        """Test pronunciation dictionary"""
        assert 'API' in self.writer.pronunciation_dict
        assert 'Python' in self.writer.pronunciation_dict
        assert self.writer.pronunciation_dict['API'] == 'A-P-I'
    
    def test_pacing_rules(self):
        """Test pacing rules"""
        assert 'sentence_pause' in self.writer.pacing_rules
        assert 'paragraph_pause' in self.writer.pacing_rules
        assert isinstance(self.writer.pacing_rules['sentence_pause'], float) 
