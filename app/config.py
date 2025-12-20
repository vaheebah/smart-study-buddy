import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/smart_study_buddy"
    MONGO_URL: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "smart_study_buddy"
    
    # AI
    GROQ_API_KEY: str
    
    # JWT
    SECRET_KEY: str = "cpORgt37bB-H1bTrhllQQ4U4EQHIPFH62y2bU80-T6E"
    TOKEN_EXPIRE_MINUTES: int = 60
    
    # FAISS
    FAISS_INDEX_PATH: str = "./faiss_index/index.faiss"
    FAISS_METADATA_PATH: str = "./faiss_index/metadata.json"
    
    # Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 50   # <-- add this line

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
