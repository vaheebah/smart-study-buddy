
import os
import json
import numpy as np
import faiss
from typing import List
from sentence_transformers import SentenceTransformer
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Load a free embedding model from Hugging‑Face
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"  # small, fast, free
embed_model = SentenceTransformer(EMBEDDING_MODEL_NAME)

# embedding dimension
EMBEDDING_DIM = embed_model.get_sentence_embedding_dimension()
logger.info("Using embedding model %s with dim %d", EMBEDDING_MODEL_NAME, EMBEDDING_DIM)

class FAISSIndex:
    def __init__(self):
        self.index = None
        self.metadata = []
        self.load_or_create()
    
    def load_or_create(self):
        if os.path.exists(settings.FAISS_INDEX_PATH):
            self.index = faiss.read_index(settings.FAISS_INDEX_PATH)
            with open(settings.FAISS_METADATA_PATH, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
            self.metadata = []
    
    def add_embeddings(self, chunk_ids: List[str], vectors: np.ndarray, chunk_texts: List[str], note_id: str):
        faiss.normalize_L2(vectors)
        self.index.add(vectors.astype('float32'))
        for chunk_id, chunk_text in zip(chunk_ids, chunk_texts):
            self.metadata.append({
                "chunk_id": chunk_id,
                "note_mongo_id": note_id,
                "chunk_text": chunk_text,
            })
        self.save()
    
    def save(self):
        faiss.write_index(self.index, settings.FAISS_INDEX_PATH)
        with open(settings.FAISS_METADATA_PATH, 'w') as f:
            json.dump(self.metadata, f)
        logger.info("FAISS index saved")

    def search(self, query_vector: np.ndarray, top_k: int = 5):
        query_vector = query_vector.astype('float32')
        faiss.normalize_L2(query_vector)
        distances, indices = self.index.search(query_vector.reshape(1, -1), top_k)
        results = []
        for distance, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results.append((idx, float(distance), self.metadata[idx]))
        return results

faiss_index = FAISSIndex()

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = ' '.join(words[i : i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def get_embeddings(texts: List[str]) -> np.ndarray:
    """Generate embeddings locally using SentenceTransformers."""
    vectors = embed_model.encode(texts, show_progress_bar=False)
    return np.array(vectors).astype('float32')

async def process_note_embeddings(extracted_text: str, note_mongo_id: str, chunk_size: int = 300, overlap: int = 50):
    chunks = chunk_text(extracted_text, chunk_size, overlap)
    embeddings = get_embeddings(chunks)
    chunk_ids = [f"{note_mongo_id}_chunk_{i}" for i in range(len(chunks))]
    faiss_index.add_embeddings(chunk_ids, embeddings, chunks, note_mongo_id)
    return {
        "chunks_count": len(chunks),
        "indexed_count": embeddings.shape[0]
    }

async def search_embeddings(query: str, top_k: int = 5):
    query_embedding = get_embeddings([query])[0]
    results = faiss_index.search(query_embedding.reshape(1, -1), top_k)
    return [
        {
            "note_id": metadata["note_mongo_id"],
            "chunk_text": metadata["chunk_text"],
            "similarity_score": distance
        }
        for _, distance, metadata in results
    ]
