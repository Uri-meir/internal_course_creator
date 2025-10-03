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
        # Truncate summaries to ensure we don't exceed limits
        combined_content = "\n\n".join(summaries)
        
        # Limit input content to prevent long outputs
        if len(combined_content) > 2000:
            combined_content = combined_content[:2000] + "..."
        
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert corporate trainer. Create a SHORT, engaging video script for employee training. Keep it under 4000 characters total. Focus on key points only. Be concise and direct."},
                    {"role": "user", "content": f"Create a SHORT video script (under 4000 characters) for training on '{topic}'. Use this source material:\n\n{combined_content}\n\nMake it concise, professional, and under 4000 characters total."}
                ],
                max_tokens=1000,  # Very conservative limit
                temperature=0.7
            )
            
            script = response.choices[0].message.content
            
            # Aggressively ensure script is under 5000 characters
            if len(script) > 5000:
                script = script[:4997] + "..."
                print(f"⚠️  Script truncated to 5000 characters (was {len(script)})")
            
            # Double-check and truncate if needed
            if len(script) > 5000:
                script = script[:5000]
            
            print(f"📝 Generated script length: {len(script)} characters")
            return script
            
        except Exception as e:
            print(f"Error generating script: {e}")
            # Fallback: create a very short script
            fallback_script = f"Training on {topic}:\n\nKey points from the documents:\n{combined_content[:3000]}"
            if len(fallback_script) > 5000:
                fallback_script = fallback_script[:5000]
            return fallback_script