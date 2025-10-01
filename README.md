# Knowledge Management Service

AI-powered document processing, RAG, and course generation service for corporate training.

## Architecture

### Core Components

1. **Document Processing Pipeline**
   - Document upload and storage
   - Text chunking using LangChain
   - AI-powered summarization
   - Vector embeddings for semantic search

2. **RAG (Retrieval-Augmented Generation)**
   - Vector-based document search
   - Context-aware responses
   - Corporate knowledge chatbot

3. **Course Generation**
   - Automated script creation from documents
   - Avatar video generation
   - Background job processing

### Technology Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL + pgvector
- **AI**: OpenAI (GPT-4, embeddings)
- **Processing**: LangChain (chunking)
- **Background Jobs**: Celery + Redis
- **Video**: HeyGen API

### API Endpoints

#### Documents
- `POST /documents/upload` - Upload and process documents
- `GET /documents/` - List all documents
- `GET /documents/{id}` - Get specific document

#### Search
- `POST /search/` - Semantic search across documents

#### Courses
- `POST /courses/generate` - Generate course from documents
- `GET /courses/{job_id}/status` - Check generation status

#### Chat
- `POST /chat/` - Chat with knowledge base

## Next Steps

1. **Set up PostgreSQL with pgvector**
   ```bash
   docker run --name postgres-pgvector -e POSTGRES_PASSWORD=password -p 5432:5432 -d pgvector/pgvector:pg16
   ```

2. **Set up Redis**
   ```bash
   docker run --name redis -p 6379:6379 -d redis:alpine
   ```

3. **Configure environment variables**
   - Copy `env_template.txt` to `.env`
   - Add your OpenAI API key
   - Add your HeyGen API key (optional for testing)
   - Update database URL

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the service**
   ```bash
   python start.py
   ```
   Or directly:
   ```bash
   python main.py
   ```

6. **Access Swagger UI**
   - Open http://localhost:8000/docs
   - Test the API endpoints

## Usage Flow

1. **Upload Documents**: Use `/documents/upload` to add corporate documents
2. **Search Knowledge**: Use `/search/` to find relevant information
3. **Generate Courses**: Use `/courses/generate` to create training videos
4. **Chat with Data**: Use `/chat/` to ask questions about your documents
