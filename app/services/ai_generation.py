import os
from groq import Groq
import json
from app.config import settings
from groq import Groq

# Initialize client with API key
client = Groq(api_key=settings.GROQ_API_KEY)


def generate_summary(text: str) -> str:
    """Generate summary using Groq"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  #  chat model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert study note summarizer. Provide clear, concise summaries."
                },
                {
                    "role": "user",
                    "content": f"Summarize the following study notes in 3-4 bullet points:\n\n{text[:2000]}"
                }
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Summary generation failed: {str(e)}")

def generate_flashcards(text: str) -> list:
    """Generate flashcards using Groq"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating study flashcards. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""Create 10 flashcard questions and answers from this text. 
Return ONLY a JSON array like this: [{{"q":"question","a":"answer"}}, ...]

Text:\n{text[:2000]}"""
                }
            ],
            temperature=0.7,
            max_tokens=800
        )

        response_text = response.choices[0].message.content
        try:
            flashcards = json.loads(response_text)
        except:
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start != -1 and end > start:
                flashcards = json.loads(response_text[start:end])
            else:
                flashcards = []

        return flashcards if isinstance(flashcards, list) else []
    except Exception as e:
        raise Exception(f"Flashcard generation failed: {str(e)}")

def generate_quiz(text: str) -> list:
    """Generate quiz questions using Groq"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating multiple choice quiz questions. Return ONLY valid JSON."
                },
                {
                    "role": "user",
                    "content": f"""Create 5 multiple choice quiz questions from this text.
Return ONLY a JSON array like this: [{{"q":"question","options":["a","b","c","d"],"answer":0}}, ...]

Text:\n{text[:2000]}"""
                }
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        response_text = response.choices[0].message.content
        try:
            quiz = json.loads(response_text)
        except:
            start = response_text.find('[')
            end = response_text.rfind(']') + 1
            if start != -1 and end > start:
                quiz = json.loads(response_text[start:end])
            else:
                quiz = []

        return quiz if isinstance(quiz, list) else []
    except Exception as e:
        raise Exception(f"Quiz generation failed: {str(e)}")
    
def generate_study_plan(text: str) -> str:
    """2. Personalized study plan"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You create structured study plans."},
                {"role": "user",
                 "content": f"Create a 3-day study plan based ONLY on these notes:\n{text[:2000]}"}
            ],
            max_tokens=700,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Study plan failed: {str(e)}")


def generate_key_terms(text: str) -> list:
    """3. Extract key terms as JSON"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Extract key terms from notes. Output JSON ONLY."},
                {"role": "user",
                 "content": f"Extract 12 key terms + definitions. JSON ONLY:"
                            f'[{{"term":"", "definition":""}}, ...]\n\n{text[:2000]}'},
            ],
            max_tokens=600,
        )
        content = response.choices[0].message.content
        return json.loads(content[content.find("["):content.rfind("]") + 1])
    except Exception as e:
        raise Exception(f"Key term extraction failed: {str(e)}")


def generate_learning_objectives(text: str) -> list:
    """4. Learning objectives"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Generate learning objectives."},
                {"role": "user", "content": f"Generate 5 learning objectives:\n{text[:2000]}"},
            ],
            max_tokens=400,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Learning objectives failed: {str(e)}")


def generate_explanation_levels(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Explain content in different difficulty levels. Return JSON."},
                {"role": "user", "content": f"""
Explain this content in 3 levels: ELI5, ELI12, and Expert.
Return JSON:
{{
  "eli5": "...",
  "eli12": "...",
  "expert": "..."
}}
Text:\n{text[:2000]}
"""}
            ],
            temperature=0.6
        )

        data = response.choices[0].message.content
        start = data.find('{')
        end = data.rfind('}') + 1
        return json.loads(data[start:end])
    except Exception as e:
        raise Exception(f"Explanation generation failed: {str(e)}")


def generate_cloze(text: str) -> list:
    """6. Cloze deletion fill-in-the-blanks"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Create fill-in-the-blanks in JSON only."},
                {"role": "user",
                 "content": f"Create 10 cloze questions from text. JSON ONLY:"
                            f'[{{"question":"sentence with ___", "answer":"actual term"}}, ...]\n\n{text[:2000]}'}
            ],
            max_tokens=700,
        )
        content = response.choices[0].message.content
        return json.loads(content[content.find("["):content.rfind("]") + 1])
    except Exception as e:
        raise Exception(f"Cloze generation failed: {str(e)}")


def generate_long_explanation(text: str) -> str:
    """7. Full tutor-mode long explanation"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Explain topics deeply like a tutor."},
                {"role": "user",
                 "content": f"Give a full long explanation of these notes:\n{text[:3000]}"}
            ],
            max_tokens=1500,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Long explanation failed: {str(e)}")


def generate_important_questions(text: str) -> list:
    """8. Important short answer questions"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Generate short-answer exam questions. JSON ONLY."},
                {"role": "user",
                 "content": f"Create 10 short-answer questions in JSON: "
                            f'[{{"q":"question"}}, ...]\n\n{text[:2000]}'}
            ],
            max_tokens=700,
        )
        content = response.choices[0].message.content
        return json.loads(content[content.find("["):content.rfind("]") + 1])
    except Exception as e:
        raise Exception(f"Important questions failed: {str(e)}")