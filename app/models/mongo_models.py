from typing import Optional, List
from datetime import datetime
from enum import Enum

class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

class MongoNote:
    """MongoDB note document schema with advanced fields"""
    
    @staticmethod
    def create(user_id: int, file_name: str, extracted_text: str, file_size: int = 0, page_count: int = 0, language: str = "en") -> dict:
        return {
            "user_id": user_id,
            "file_name": file_name,
            "file_type": file_name.split('.')[-1],
            "extracted_text": extracted_text,
            "file_size": file_size,
            "page_count": page_count,
            "language": language,
            "word_count": len(extracted_text.split()),
            "word_frequency": {},
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "summaries": {  # Store multiple summary lengths
                "short": None,
                "medium": None,
                "long": None
            },
            "flashcards": [],  # Store with difficulty levels
            "quiz": [],
            # Semantic search
            "chunks": [],  # Store text chunks
            "embedding_status": "pending"
        }

class Flashcard:
    """Enhanced flashcard with difficulty level and metadata"""
    def __init__(self, q: str, a: str, difficulty: DifficultyLevel = DifficultyLevel.MEDIUM, tags: List[str] = None):
        self.question = q
        self.answer = a
        self.difficulty = difficulty
        self.tags = tags or []
        self.created_at = datetime.utcnow()
        self.review_count = 0
    
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "answer": self.answer,
            "difficulty": self.difficulty,
            "tags": self.tags,
            "created_at": self.created_at,
            "review_count": self.review_count
        }

class QuizItem:
    """Enhanced quiz item with explanations"""
    def __init__(self, q: str, options: List[str], answer: int, explanation: str = "", difficulty: DifficultyLevel = DifficultyLevel.MEDIUM):
        self.question = q
        self.options = options
        self.correct_answer = answer
        self.explanation = explanation
        self.difficulty = difficulty
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "options": self.options,
            "correct_answer": self.correct_answer,
            "explanation": self.explanation,
            "difficulty": self.difficulty,
            "created_at": self.created_at
        }

class TextChunk:
    """Represents a chunk of text for semantic search"""
    def __init__(self, text: str, chapter: str = "", page: int = 0, heading: str = "", chunk_index: int = 0):
        self.text = text
        self.chapter = chapter
        self.page = page
        self.heading = heading
        self.chunk_index = chunk_index
        self.created_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "chapter": self.chapter,
            "page": self.page,
            "heading": self.heading,
            "chunk_index": self.chunk_index,
            "created_at": self.created_at
        }
