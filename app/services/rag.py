from app.services.embeddings import search_embeddings
from app.config import settings
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

async def generate_rag_answer(question: str, top_k: int = 5) -> str:
    # Step 1 & 2: Retrieve relevant chunks
    retrieved_chunks = await search_embeddings(question, top_k)

    # Step 3: Build context from retrieved chunks
    context_text = "\n\n".join([chunk['chunk_text'] for chunk in retrieved_chunks])

    # Step 4: Call LLM with question + context for answer generation
    prompt = (
        "You are a helpful assistant answering student questions based on their uploaded study notes.\n\n"
        f"Context:\n{context_text}\n\n"
        f"Question: {question}\n\nAnswer:"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are an expert tutor."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise Exception(f"RAG answer generation failed: {str(e)}")
