from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from bson.objectid import ObjectId
from app.db.postgres import get_db
from app.db.mongo import get_mongo_db
from app.models.sql_models import NotesMetadata
from app.schemas.note_schemas import ProcessNoteRequest, NoteDetailResponse
from app.services.embeddings import process_note_embeddings
from app.services.ai_generation import generate_summary, generate_flashcards, generate_quiz,generate_important_questions,generate_long_explanation,generate_cloze,generate_explanation_levels,generate_learning_objectives,generate_key_terms,generate_study_plan
from app.utils.security import verify_token
from app.services.rag import generate_rag_answer
from fastapi import Body

router = APIRouter()

@router.get("/list")
async def list_notes(
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """List all notes for user"""
    notes_metadata = db.query(NotesMetadata).filter(NotesMetadata.user_id == user_id).all()
    
    result = []
    for meta in notes_metadata:
        note = mongo_db.notes.find_one({"_id": ObjectId(meta.mongo_note_id)})
        if note:
            result.append({
                "id": meta.id,
                "mongo_id": meta.mongo_note_id,
                "file_name": meta.file_name,
                "uploaded_at": meta.uploaded_at,
                "summary_preview": note.get("summary", "Not generated")[:100] if note.get("summary") else "Not generated"
            })
    
    return result

@router.get("/{note_id}")
async def get_note(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Get full note details"""
    # Verify ownership
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note content not found")
    
    return {
        "note_id": note_id,
        "file_name": note.get("file_name"),
        "extracted_text": note.get("extracted_text"),
        "summary": note.get("summary"),
        "flashcards": note.get("flashcards"),
        "quiz": note.get("quiz"),
        "created_at": note.get("created_at")
    }

@router.post("/{note_id}/process")
async def process_note(
    note_id: str,
    req: ProcessNoteRequest,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Process note: generate embeddings and index"""
    # Verify ownership
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    result = await process_note_embeddings(
        note["extracted_text"],
        note_id,
        req.chunk_size,
        req.overlap
    )
    
    return result

@router.post("/{note_id}/generate-summary")
async def generate_note_summary(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Generate AI summary for note"""
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    summary = generate_summary(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"summary": summary}})
    
    return {"summary": summary, "saved": True}

@router.post("/{note_id}/generate-flashcards")
async def generate_note_flashcards(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Generate AI flashcards for note"""
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    flashcards = generate_flashcards(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"flashcards": flashcards}})
    
    return {"flashcards": flashcards, "saved": True}

@router.post("/{note_id}/generate-quiz")
async def generate_note_quiz(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Generate AI quiz for note"""
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    quiz = generate_quiz(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"quiz": quiz}})
    
    return {"quiz": quiz, "saved": True}

@router.post("/{note_id}/generate-study-plan")
async def generate_study_plan_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    plan = generate_study_plan(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"study_plan": plan}})

    return {"study_plan": plan, "saved": True}

@router.post("/{note_id}/generate-key-terms")
async def generate_terms_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    terms = generate_key_terms(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"key_terms": terms}})

    return {"key_terms": terms, "saved": True}

@router.post("/{note_id}/generate-objectives")
async def generate_objectives_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    objectives = generate_learning_objectives(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"objectives": objectives}})

    return {"objectives": objectives, "saved": True}

@router.post("/{note_id}/generate-explanations")
async def generate_explanations_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    explanations = generate_explanation_levels(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"explanations": explanations}})

    return {"explanations": explanations, "saved": True}

@router.post("/{note_id}/generate-cloze")
async def generate_cloze_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    cloze = generate_cloze(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"cloze": cloze}})

    return {"cloze": cloze, "saved": True}

@router.post("/{note_id}/generate-important-questions")
async def generate_short_questions_endpoint(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):

    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(404, "Note not found")

    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})

    questions = generate_important_questions(note["extracted_text"])
    mongo_db.notes.update_one({"_id": ObjectId(note_id)}, {"$set": {"important_questions": questions}})

    return {"important_questions": questions, "saved": True}

@router.post("/{note_id}/generate-long-explanation")
async def generate_note_long_explanation(
    note_id: str,
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Generate a long tutor-style explanation for the note"""
    
    # --- Verify ownership ---
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()

    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")

    # --- Fetch note from Mongo ---
    note = mongo_db.notes.find_one({"_id": ObjectId(note_id)})
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # --- Generate AI tutor explanation ---
    long_explanation = generate_long_explanation(note["extracted_text"])

    # --- Save in MongoDB ---
    mongo_db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"long_explanation": long_explanation}}
    )

    return {"long_explanation": long_explanation, "saved": True}

@router.post("/{note_id}/ask-question")
async def ask_question(
    note_id: str,
    question: str = Body(..., embed=True),  # Accept question in POST body
    user_id: int = Depends(verify_token),
    db: Session = Depends(get_db),
    mongo_db = Depends(get_mongo_db)
):
    """Answer questions about a note using RAG"""
    # Verify ownership
    metadata = db.query(NotesMetadata).filter(
        NotesMetadata.mongo_note_id == note_id,
        NotesMetadata.user_id == user_id
    ).first()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Note not found")

    # Call RAG answer generator
    answer = await generate_rag_answer(question)

    return {"question": question, "answer": answer}