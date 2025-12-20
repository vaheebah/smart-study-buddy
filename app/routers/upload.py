from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
import os
from collections import Counter
from app.db.postgres import get_db
from app.db.mongo import get_mongo_db
from app.models.sql_models import NotesMetadata
from app.models.mongo_models import MongoNote
from app.schemas.note_schemas import NoteUploadResponse
from app.services.extract_text import extract_text
from app.utils.security import verify_token
from app.config import settings

router = APIRouter()

@router.post("/upload", response_model=NoteUploadResponse, status_code=201)
async def upload_file(
    file: UploadFile = File(...),
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    try:
        # Validate file type
        if not file.filename.endswith(('.pdf', '.docx', '.doc', '.txt', '.png', '.jpg', '.jpeg')):
            raise HTTPException(status_code=400, detail="Unsupported file type. Supported: PDF, DOCX, TXT, PNG, JPG")
        
        file_content = await file.read()
        file_size = len(file_content)
        
        if file_size == 0:
            raise HTTPException(status_code=400, detail="File is empty")
        
        # Save file
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(file_content)
        
        # Extract text with advanced processing
        extraction_result = extract_text(file_path)
        extracted_text = extraction_result.get("text", "")
        page_count = extraction_result.get("pages", 0)
        language = extraction_result.get("language", "en")
        
        if not extracted_text:
            raise HTTPException(status_code=400, detail="No text could be extracted from file")
        
        words = extracted_text.lower().split()
        word_frequency = dict(Counter(words).most_common(50))
        word_count = len(words)
        
        # Create MongoDB document with advanced fields
        note_doc = MongoNote.create(
            user_id=user_id,
            file_name=file.filename,
            extracted_text=extracted_text,
            file_size=file_size,
            page_count=page_count,
            language=language
        )
        note_doc["word_frequency"] = word_frequency
        
        result = mongo_db.notes.insert_one(note_doc)
        mongo_note_id = str(result.inserted_id)
        
        # Save metadata to PostgreSQL
        metadata = NotesMetadata(
            user_id=user_id,
            file_name=file.filename,
            mongo_note_id=mongo_note_id
        )
        db.add(metadata)
        db.commit()
        db.refresh(metadata)
        
        return NoteUploadResponse(
            note_id=mongo_note_id,
            metadata_id=metadata.id,
            file_name=file.filename,
            word_count=word_count,
            page_count=page_count,
            language=language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    
@router.delete("/delete/{note_id}", status_code=200)
async def delete_note(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    try:
        # 1. Validate Mongo ID
        try:
            object_id = ObjectId(note_id)
        except:
            raise HTTPException(status_code=400, detail="Invalid note_id format")

        # 2. Get Mongo Document
        note = mongo_db.notes.find_one({"_id": object_id, "user_id": user_id})
        if not note:
            raise HTTPException(status_code=404, detail="Note not found or unauthorized")

        file_name = note.get("file_name")
        file_path = os.path.join(settings.UPLOAD_DIR, file_name)

        # -------------------
        # 3. Delete MongoDB data
        # -------------------
        mongo_db.notes.delete_one({"_id": object_id})

        # -------------------
        # 4. Delete PostgreSQL metadata
        # -------------------
        metadata = db.query(NotesMetadata).filter(
            NotesMetadata.mongo_note_id == note_id,
            NotesMetadata.user_id == user_id
        ).first()

        if metadata:
            db.delete(metadata)
            db.commit()

        # -------------------
        # 5. Delete File from Disk
        # -------------------
        if os.path.exists(file_path):
            os.remove(file_path)

        return {"message": "Note deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Delete failed: {str(e)}")
