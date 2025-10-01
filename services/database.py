"""
Database connection and session management
"""

from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import settings

# Create database engine
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    # Create pgvector extension
    try:
        with engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
        print("✅ pgvector extension enabled")
    except Exception as e:
        print(f"⚠️  pgvector extension: {e}")
    
    # Create tables
    from models.document import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")
    
    # Create pgvector index for fast similarity search
    try:
        with engine.connect() as conn:
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS embeddings_vector_idx 
                ON embeddings 
                USING ivfflat (embedding vector_cosine_ops) 
                WITH (lists = 100)
            """))
            conn.commit()
        print("✅ pgvector index created for fast similarity search")
    except Exception as e:
        print(f"⚠️  pgvector index: {e}")