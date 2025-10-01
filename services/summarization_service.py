"""
Text summarization service using OpenAI
"""

from openai import AsyncOpenAI
from config import settings
from typing import Optional

class SummarizationService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def summarize(self, text: str) -> str:
        """Summarize text using OpenAI - PRODUCTION VERSION"""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that creates comprehensive summaries of corporate documents. Focus on key points, procedures, and important information. Capture all essential details."},
                    {"role": "user", "content": f"Provide a comprehensive summary of this text, capturing all key points and important details:\n\n{text}"}
                ],
                max_tokens=500,  # Increased from 150 to allow full summaries
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error summarizing text: {e}")
            return text[:500] + "..." if len(text) > 500 else text