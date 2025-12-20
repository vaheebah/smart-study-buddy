from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    
    # Profile fields
    full_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    institution = Column(String, nullable=True)
    preferred_subject = Column(String, nullable=True)
    profile_picture_url = Column(String, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Account metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

class NotesMetadata(Base):
    __tablename__ = "notes_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_name = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    mongo_note_id = Column(String, nullable=False)
