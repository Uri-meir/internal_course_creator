"""
Script Writer Component
Converts lesson content into natural speech scripts
"""

import json
import logging
import re
from typing import Dict, List, Any, Optional
from openai import OpenAI
from mocks.mock_clients import MockOpenAIClient

logger = logging.getLogger(__name__)

class ScriptWriter:
    """
    Converts lesson content into natural speech scripts optimized for AI presenters
    """
    
    def __init__(self, api_key: str, test_mode: bool = False):
        """Initialize with OpenAI API key and test mode flag"""
        self.test_mode = test_mode
        
        if self.test_mode:
            logger.info("Using mock OpenAI client for testing")
            self.client = MockOpenAIClient(api_key)
        else:
            self.client = OpenAI(api_key=api_key)
            
        self.pronunciation_dict = self._load_tech_pronunciations()
        self.pacing_rules = self._load_pacing_rules()
    
    def _load_tech_pronunciations(self) -> Dict[str, str]:
        """Load dictionary of technical term pronunciations"""
        return {
            "API": "A-P-I",
            "APIs": "A-P-I-s",
            "RAG": "R-A-G",
            "SQL": "S-Q-L",
            "JSON": "J-S-O-N",
            "HTML": "H-T-M-L",
            "CSS": "C-S-S",
            "JavaScript": "Java-Script",
            "TypeScript": "Type-Script",
            "FastAPI": "Fast-A-P-I",
            "GraphQL": "Graph-Q-L",
            "OAuth": "O-Auth",
            "JWT": "J-W-T",
            "CRUD": "C-R-U-D",
            "HTTP": "H-T-T-P",
            "HTTPS": "H-T-T-P-S",
            "URL": "U-R-L",
            "URI": "U-R-I",
            "UUID": "U-U-I-D",
            "AI": "A-I",
            "ML": "M-L",
            "NLP": "N-L-P",
            "GPU": "G-P-U",
            "CPU": "C-P-U",
            "RAM": "R-A-M",
            "SSD": "S-S-D"
        }
    
    def _load_pacing_rules(self) -> Dict[str, float]:
        """Load rules for speech pacing and timing"""
        return {
            "sentence_pause": 0.8,
            "paragraph_pause": 1.5,
            "section_pause": 2.0,
            "emphasis_pause": 0.5,
            "code_explanation_pause": 1.0,
            "transition_pause": 1.2
        }
    
    def convert_to_speech_script(self, lesson_content: Dict[str, Any]) -> str:
        """
        Convert lesson content to natural speech script
        
        Args:
            lesson_content: Generated lesson content
            
        Returns:
            Natural speech script with timing cues
        """
        try:
            logger.info(f"Converting lesson {lesson_content.get('lesson_number')} to speech script")
            
            lesson_type = lesson_content.get('type', 'theory')
            
            if lesson_type == 'theory':
                return self._create_theory_script(lesson_content)
            elif lesson_type == 'hands-on':
                return self._create_hands_on_script(lesson_content)
            else:  # mixed
                return self._create_mixed_script(lesson_content)
                
        except Exception as e:
            logger.error(f"Error converting to speech script: {str(e)}")
            return self._create_fallback_script(lesson_content)
    
    def _create_theory_script(self, lesson_content: Dict[str, Any]) -> str:
        """Create script for theory-based lessons"""
        
        script_prompt = f"""
        Create a natural, conversational speech script for an AI presenter about: {lesson_content.get('title')}
        
        IMPORTANT: Respond with ONLY the speech script text, no JSON, no formatting, no metadata.
        
        The script should:
        - Be conversational and engaging
        - Include natural pauses [PAUSE:1s]
        - Emphasize key points [EMPHASIS]like this[/EMPHASIS]
        - Be about {lesson_content.get('duration_minutes', 15)} minutes long
        - Cover the topic: {lesson_content.get('title')}
        
        Use this content as inspiration:
        - Introduction: {lesson_content.get('introduction', '')}
        - Key concepts: {lesson_content.get('key_takeaways', [])}
        
        Start directly with the speech content, no quotes or formatting.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": script_prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            script = response.choices[0].message.content.strip()
            
            # Clean up any remaining formatting
            script = self._clean_script_formatting(script)
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating theory script: {str(e)}")
            return self._create_fallback_script(lesson_content)
    
    def _create_hands_on_script(self, lesson_content: Dict[str, Any]) -> str:
        """Create script for hands-on coding lessons"""
        
        script_prompt = f"""
        Create a natural speech script for an AI presenter about: {lesson_content.get('title')}
        
        IMPORTANT: Respond with ONLY the speech script text, no JSON, no formatting, no metadata.
        
        The script should:
        - Be conversational and engaging
        - Include natural pauses [PAUSE:1s]
        - Emphasize key points [EMPHASIS]like this[/EMPHASIS]
        - Be about {lesson_content.get('duration_minutes', 15)} minutes long
        - Guide students through hands-on coding activities
        
        Use this content as inspiration:
        - Setup: {lesson_content.get('setup_instructions', '')}
        - Key concepts: {lesson_content.get('key_takeaways', [])}
        
        Start directly with the speech content, no quotes or formatting.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": script_prompt}],
                max_tokens=1500,
                temperature=0.7
            )
            
            script = response.choices[0].message.content.strip()
            
            # Clean up any remaining formatting
            script = self._clean_script_formatting(script)
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating hands-on script: {str(e)}")
            return self._create_fallback_script(lesson_content)
    
    def _create_mixed_script(self, lesson_content: Dict[str, Any]) -> str:
        """Create script for mixed theory and hands-on lessons"""
        
        # Combine theory and hands-on approaches
        theory_script = self._create_theory_script(lesson_content)
        hands_on_script = self._create_hands_on_script(lesson_content)
        
        # Merge scripts with transition
        mixed_script = f"""
{theory_script}

Now let's put what we've learned into practice!

{hands_on_script}
"""
        
        return mixed_script.strip()
    
    def _clean_script_formatting(self, script: str) -> str:
        """Clean up script formatting to ensure it's plain speech text only"""
        
        # Remove JSON formatting if present
        if script.startswith('{') and script.endswith('}'):
            try:
                # Try to extract speech content from JSON
                data = json.loads(script)
                if isinstance(data, dict):
                    # Combine all text fields into a single script
                    text_parts = []
                    for key, value in data.items():
                        if isinstance(value, str):
                            text_parts.append(value)
                        elif isinstance(value, list):
                            text_parts.extend([str(item) for item in value if isinstance(item, str)])
                    
                    script = ' '.join(text_parts)
            except:
                pass
        
        # Remove all timing and pacing metadata
        script = re.sub(r'\[PAUSE[^\]]*\]', '', script)  # Remove [PAUSE:1s], [PAUSE], etc.
        script = re.sub(r'\[EMPHASIS\]', '', script)     # Remove [EMPHASIS] tags
        script = re.sub(r'\[/EMPHASIS\]', '', script)    # Remove [/EMPHASIS] tags
        script = re.sub(r'\[SLOW\]', '', script)         # Remove [SLOW] tags
        script = re.sub(r'\[/SLOW\]', '', script)        # Remove [/SLOW] tags
        script = re.sub(r'\[FAST\]', '', script)         # Remove [FAST] tags
        script = re.sub(r'\[/FAST\]', '', script)        # Remove [/FAST] tags
        script = re.sub(r'\[BREATH\]', '', script)       # Remove [BREATH] tags
        
        # Remove markdown formatting
        script = script.replace('```', '').replace('**', '').replace('*', '')
        
        # Remove any remaining JSON-like structures
        script = re.sub(r'"[^"]*":\s*', '', script)
        script = re.sub(r'\{[^}]*\}', '', script)
        script = re.sub(r'\[[^\]]*\]', '', script)       # Remove any remaining [tags]
        
        # Remove stage directions and speaker instructions
        script = re.sub(r'\([^)]*\)', '', script)        # Remove (stage directions)
        script = re.sub(r'NARRATOR:', '', script, flags=re.IGNORECASE)
        script = re.sub(r'SPEAKER:', '', script, flags=re.IGNORECASE)
        script = re.sub(r'PRESENTER:', '', script, flags=re.IGNORECASE)
        
        # Clean up extra whitespace and normalize spacing
        script = re.sub(r'\s+', ' ', script).strip()
        script = re.sub(r'\s*\.\s*', '. ', script)       # Normalize periods
        script = re.sub(r'\s*,\s*', ', ', script)        # Normalize commas
        script = re.sub(r'\s*!\s*', '! ', script)        # Normalize exclamations
        script = re.sub(r'\s*\?\s*', '? ', script)       # Normalize questions
        
        return script
    
    def _add_timing_cues(self, script: str) -> str:
        """Add timing cues and optimize pacing"""
        
        # Add natural pauses after sentences
        script = re.sub(r'([.!?])\s+', r'\1 [PAUSE:0.5s] ', script)
        
        # Add longer pauses after paragraphs
        script = re.sub(r'\n\n', '\n\n[PAUSE:1s]\n\n', script)
        
        # Add emphasis cues for key concepts
        script = re.sub(r'\b(important|key|critical|essential|remember)\b', r'[EMPHASIS]\1[/EMPHASIS]', script, flags=re.IGNORECASE)
        
        return script
    
    def estimate_script_duration(self, script: str) -> float:
        """
        Estimate the duration of a script in minutes
        
        Args:
            script: The speech script
            
        Returns:
            Estimated duration in minutes
        """
        try:
            # Count words for speech time
            words = len(re.findall(r'\b\w+\b', script))
            speech_time = words / 150  # 150 words per minute
            
            # Count pauses
            pause_matches = re.findall(r'\[PAUSE:(\d+\.?\d*)s\]', script)
            total_pause_time = sum(float(match) for match in pause_matches)
            
            # Total duration in minutes
            total_duration = speech_time + (total_pause_time / 60)
            
            return round(total_duration, 1)
            
        except Exception as e:
            logger.error(f"Error estimating script duration: {str(e)}")
            # Fallback: estimate based on word count only
            words = len(re.findall(r'\b\w+\b', script))
            return round(words / 150, 1)
    
    def _create_fallback_script(self, lesson_content: Dict[str, Any]) -> str:
        """Create basic fallback script if generation fails"""
        
        title = lesson_content.get('title', 'Lesson')
        lesson_number = lesson_content.get('lesson_number', 1)
        
        fallback_script = f"""
[OPENING: Friendly wave]
Welcome to lesson {lesson_number}: {title}.

[PAUSE:2s]

In this lesson, we're going to explore some important concepts that will help you understand this topic better.

[PAUSE:1.5s]

Let's start by understanding the fundamentals.

[EMPHASIS]This is a key concept[/EMPHASIS] that you'll need to master.

[PAUSE:1s]

Now, let's see how this works in practice.

[VISUAL_CUE: Show example]

Great! You're doing well so far.

[PAUSE:1.5s]

To wrap up, let's review what we've learned today.

[PAUSE:2s]

Thanks for joining me in this lesson. I'll see you in the next one!

[CLOSING: Thank you gesture]
"""
        
        return fallback_script.strip() 
