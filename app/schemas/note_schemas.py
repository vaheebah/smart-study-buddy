from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class NoteUploadResponse(BaseModel):
    note_id: str
    metadata_id: int
    file_name: str
    word_count: Optional[int] = 0
    page_count: Optional[int] = 0
    language: Optional[str] = "en"

class NoteMetadataResponse(BaseModel):
    id: int
    file_name: str
    uploaded_at: datetime

class FlashcardSchema(BaseModel):
    q: str
    a: str

class QuizItemSchema(BaseModel):
    q: str
    options: List[str]
    answer: int
    explanation: Optional[str] = ""

class NoteDetailResponse(BaseModel):
    note_id: str
    file_name: str
    extracted_text: str
    summary: Optional[str]
    flashcards: Optional[List[FlashcardSchema]]
    quiz: Optional[List[QuizItemSchema]]
    created_at: datetime

class ProcessNoteRequest(BaseModel):
    chunk_size: int = 300
    overlap: int = 50

class SearchResult(BaseModel):
    note_id: str
    file_name: str
    chunk_text: str
    similarity_score: float
