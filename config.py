"""
Configuration settings for Knowledge Management Service
"""

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/knowledge_db")
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # File Storage
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    
    # External APIs
    HEYGEN_API_KEY: str = os.getenv("HEYGEN_API_KEY", "")
    HEYGEN_API_URL: str = os.getenv("HEYGEN_API_URL", "https://api.heygen.com")
    
    # HeyGen Video Settings (only voice and avatar from .env)
    HEYGEN_AVATAR_ID: str = os.getenv("HEYGEN_AVATAR_ID", "Lina_Dress_Sitting_Side_public")
    HEYGEN_VOICE_ID: str = os.getenv("HEYGEN_VOICE_ID", "1bd001e7e50f421d891986aad5158bc3")
    
    # Vector Settings
    EMBEDDING_MODEL: str = "text-embedding-3-small"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

settings = Settings()