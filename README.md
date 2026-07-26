# 📚 Smart Study Buddy 

A scalable AI-powered backend for **Smart Study Buddy**, an intelligent learning platform that allows students to upload study materials and automatically generate summaries, flashcards, quizzes, study plans, and semantic search results using Large Language Models (LLMs) and vector embeddings.

Built with **FastAPI**, **PostgreSQL**, **MongoDB**, **OpenAI**, and **FAISS**.

---

## ✨ Features

- 🔐 JWT Authentication & Authorization
- 📄 Upload PDF, DOCX, TXT and Images
- 📝 Automatic Text Extraction
- 🤖 AI-generated Summaries
- 🎯 Flashcard Generation
- ❓ Quiz Generation
- 🔍 Semantic Search using FAISS
- 📚 MongoDB document storage
- 🗄 PostgreSQL relational database
- ⚡ FastAPI REST API
- 📖 Interactive Swagger Documentation

---

# 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend Framework | FastAPI |
| Language | Python 3.10+ |
| Relational Database | PostgreSQL |
| NoSQL Database | MongoDB |
| AI | OpenAI API |
| Vector Database | FAISS |
| Authentication | JWT |
| ORM | SQLAlchemy |
| Database Migration | Alembic |
| Password Hashing | bcrypt |
| API Documentation | Swagger / OpenAPI |

---

# 📁 Project Structure

```
backend/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── routers/
│   ├── services/
│   ├── utils/
│   ├── schemas/
│   └── main.py
│
├── uploads/
├── faiss_index/
├── scripts/
├── tests/
├── alembic/
├── requirements.txt
├── .env.example
└── README.md
```

---

# 🚀 Getting Started

## Prerequisites

Before running the project, install:

- Python 3.10+
- PostgreSQL 12+
- MongoDB 4.4+
- Git
- OpenAI API Key

---

## 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/Smart-Study-Buddy.git

cd Smart-Study-Buddy/backend
```

---

## 2. Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file inside the backend directory.

You can copy the example file:

```bash
cp .env.example .env
```

Update the following values:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/smart_study_buddy

MONGO_URL=mongodb://localhost:27017

OPENAI_API_KEY=your_openai_api_key

SECRET_KEY=your_super_secret_key

TOKEN_EXPIRE_MINUTES=60

UPLOAD_DIR=./uploads

FAISS_INDEX_PATH=./faiss_index/index.faiss

FAISS_METADATA_PATH=./faiss_index/metadata.json
```

---

## 5. Run Database Migrations

```bash
alembic upgrade head
```

---

## 6. Start the Server

```bash
uvicorn app.main:app --reload
```

The backend will be available at

```
http://localhost:8000
```

---

# 📖 API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# 🔑 Authentication

The application uses **JWT (JSON Web Tokens)**.

### Register

```
POST /api/auth/register
```

### Login

```
POST /api/auth/login
```

After login, include the access token in the Authorization header.

```
Authorization: Bearer <token>
```

---

# 📂 Notes Module

### Upload Note

```
POST /api/notes/upload
```

Supports:

- PDF
- DOCX
- TXT
- Images (OCR)

---

### List Notes

```
GET /api/notes/list
```

---

### Get Note Details

```
GET /api/notes/{note_id}
```

---

### Process Uploaded Note

Extracts text, creates embeddings and stores vectors.

```
POST /api/notes/{note_id}/process
```

---

# 🤖 AI Features

## Generate Summary

```
POST /api/notes/{note_id}/generate-summary
```

---

## Generate Flashcards

```
POST /api/notes/{note_id}/generate-flashcards
```

---

## Generate Quiz

```
POST /api/notes/{note_id}/generate-quiz
```

---

## Generate Study Plan

```
POST /api/notes/{note_id}/generate-study-plan
```

---

# 🔍 Semantic Search

Searches across all processed notes using vector similarity.

```
GET /api/search?q=<query>
```

Example

```
GET /api/search?q=Explain Operating Systems
```

---

# 🗄 Database Design

## PostgreSQL

Stores structured application data.

### Users

- User ID
- Name
- Email
- Password Hash

### Notes Metadata

- Note ID
- User ID
- File Name
- Upload Date
- MongoDB Reference
- Processing Status

---

## MongoDB

Stores unstructured learning content.

Each note contains:

- Extracted Text
- Summary
- Flashcards
- Quiz
- Study Plan
- Embeddings Metadata

---

## FAISS

Stores vector embeddings for semantic retrieval.

Files are stored locally:

```
faiss_index/

├── index.faiss
└── metadata.json
```

---

# 🧪 Running Tests

Run all tests

```bash
pytest tests/
```

Run a sample workflow

```bash
python scripts/sample_run.py
```

---

# 🏗 System Architecture

```
                   User
                     │
                     ▼
             FastAPI REST API
                     │
     ┌───────────────┼────────────────┐
     │               │                │
     ▼               ▼                ▼
 Authentication   File Upload     Search API
     │               │                │
     ▼               ▼                ▼
 PostgreSQL    Text Extraction    FAISS Index
     │               │                │
     └───────────────┼────────────────┘
                     │
                     ▼
               OpenAI Services
         (LLMs & Embedding Models)
                     │
                     ▼
                 MongoDB Storage
```

---

# ⚙️ Development Workflow

1. Upload study material.
2. Extract text from the document.
3. Store metadata in PostgreSQL.
4. Store extracted content in MongoDB.
5. Generate embeddings using OpenAI.
6. Save vectors in FAISS.
7. Generate AI-powered learning resources.
8. Perform semantic search across notes.

---

# ❗ Troubleshooting

### PostgreSQL Connection Error

- Verify PostgreSQL is running.
- Check `DATABASE_URL`.
- Ensure the database exists.

---

### MongoDB Connection Error

- Start the MongoDB server.
- Verify the `MONGO_URL`.

---

### OpenAI API Errors

- Confirm your API key is valid.
- Ensure billing/quota is available.

---

### FAISS Issues

Delete the existing FAISS index and regenerate it.

```
rm -rf faiss_index/
```

or on Windows

```
rmdir /s faiss_index
```

---

# 📌 Future Improvements

- Chat with uploaded notes (RAG)
- Multi-language support
- Collaborative study groups
- Cloud object storage (AWS S3/Azure Blob)
- Redis caching
- Docker & Kubernetes deployment
- CI/CD with GitHub Actions
- Analytics dashboard
- Admin panel

---

# 👥 Contributors

Developed as part of the **Smart Study Buddy** project.

Contributions, issues, and feature requests are welcome.

---
