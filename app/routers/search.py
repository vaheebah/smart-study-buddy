from fastapi import APIRouter, Depends, HTTPException
from app.services.embeddings import search_embeddings
from app.utils.security import verify_token
from app.db.mongo import get_mongo_db
from bson.objectid import ObjectId

router = APIRouter()

@router.get("")
async def search(
    q: str,
    top_k: int = 5,
    user_id: int = Depends(verify_token),
    mongo_db = Depends(get_mongo_db)
):
    """Semantic search across user's notes"""
    if not q:
        raise HTTPException(status_code=400, detail="Query required")
    
    results = await search_embeddings(q, top_k)
    
    # Enrich with file names
    enriched_results = []
    for result in results:
        note = mongo_db.notes.find_one({"_id": ObjectId(result["note_id"])})
        if note and note.get("user_id") == user_id:
            enriched_results.append({
                "note_id": result["note_id"],
                "file_name": note.get("file_name"),
                "chunk_text": result["chunk_text"],
                "similarity_score": result["similarity_score"]
            })
    
    return {"query": q, "results": enriched_results, "count": len(enriched_results)}
