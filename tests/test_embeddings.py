import pytest
from app.services.embeddings import chunk_text

def test_chunk_text():
    text = " ".join(["word"] * 500)
    chunks = chunk_text(text, chunk_size=100, overlap=10)
    assert len(chunks) > 0
    assert len(chunks[0].split()) <= 110
