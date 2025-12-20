# Smart Study Buddy - Backend Setup Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 12+
- MongoDB 4.4+
- OpenAI API Key

## Installation

### 1. Clone and Setup Python Environment
\`\`\`bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Environment Configuration
Create a `.env` file in the `backend` directory:
\`\`\`bash
cp .env.example .env
\`\`\`

Edit `.env` and set:
- `DATABASE_URL`: PostgreSQL connection string
- `MONGO_URL`: MongoDB connection string  
- `OPENAI_API_KEY`: Your OpenAI API key
- `SECRET_KEY`: A secure random string for JWT

Example `.env`:
\`\`\`
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_study_buddy
MONGO_URL=mongodb://localhost:27017
OPENAI_API_KEY=sk-...
SECRET_KEY=your-secret-key-12345
TOKEN_EXPIRE_MINUTES=60
FAISS_INDEX_PATH=./faiss_index/index.faiss
FAISS_METADATA_PATH=./faiss_index/metadata.json
UPLOAD_DIR=./uploads
\`\`\`

### 4. Initialize Database
\`\`\`bash
alembic upgrade head
\`\`\`

### 5. Start FastAPI Server
\`\`\`bash
uvicorn app.main:app --reload --port 8000
\`\`\`

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### Notes
- `POST /api/notes/upload` - Upload study material
- `GET /api/notes/list` - List user's notes
- `GET /api/notes/{note_id}` - Get note details
- `POST /api/notes/{note_id}/process` - Process note for search

### AI Generation
- `POST /api/notes/{note_id}/generate-summary` - Generate summary
- `POST /api/notes/{note_id}/generate-flashcards` - Generate flashcards
- `POST /api/notes/{note_id}/generate-quiz` - Generate quiz

### Search
- `GET /api/search?q=...` - Semantic search across notes

## Testing

Run tests:
\`\`\`bash
pytest tests/
\`\`\`

Run sample workflow:
\`\`\`bash
python scripts/sample_run.py
\`\`\`

## Database Schemas

### PostgreSQL
- `users`: User accounts
- `notes_metadata`: Notes metadata and MongoDB references

### MongoDB
- `notes`: Full note documents with extracted text, summaries, flashcards, quiz

### FAISS
- Local vector index for semantic search
- Saved to `./faiss_index/` directory

## Troubleshooting

**Connection refused**: Ensure PostgreSQL and MongoDB are running
**OpenAI errors**: Check your API key in `.env`
**FAISS issues**: Delete `./faiss_index/` to reset index

## Architecture Overview

\`\`\`
FastAPI Backend
├── Auth (JWT + bcrypt)
├── File Upload & Text Extraction
├── MongoDB (Notes Storage)
├── PostgreSQL (Users & Metadata)
├── OpenAI Integration (Embeddings & LLM)
├── FAISS (Vector Search)
└── RESTful API
