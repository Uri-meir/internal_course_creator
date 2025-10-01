#!/usr/bin/env python3
"""
Knowledge Management Service
AI-powered document processing, RAG, and course generation service
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import routers
from routers import documents, search, courses, chat
from services.database import init_db
from services.background_worker import init_workers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        await init_db()
        await init_workers()
        print("✅ Knowledge Management Service started successfully")
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        raise
    yield
    # Shutdown
    print("🔄 Shutting down Knowledge Management Service")

app = FastAPI(
    title="Knowledge Management Service",
    description="AI-powered document processing, RAG, and course generation service",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents.router, prefix="/documents", tags=["documents"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Knowledge Management Service", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "knowledge-management"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)