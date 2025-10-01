"""
Script generation service using OpenAI
"""

from openai import AsyncOpenAI
from config import settings
from typing import List

class ScriptService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_script(self, summaries: List[str], topic: str) -> str:
        """Generate video script from document summaries"""
        combined_content = "\n\n".join(summaries)
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert corporate trainer. Create engaging, professional video scripts for employee training. Focus on clear explanations, practical examples, and actionable insights."},
                    {"role": "user", "content": f"Create a comprehensive video script for a corporate training video on '{topic}'. Use the following document summaries as source material:\n\n{combined_content}\n\nMake the script engaging, professional, and suitable for corporate training. Include an introduction, main content sections, and a conclusion. Aim for 5-10 minutes of content."}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating script: {e}")
            return f"Training Script for {topic}\n\n{combined_content}"
