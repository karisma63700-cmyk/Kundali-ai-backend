
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

app = FastAPI(title="Dipsika Kundali AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AIRequest(BaseModel):
    question: str

@app.get("/")
def home():
    return {
        "message": "Dipsika Kundali AI Backend is running"
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ai-chat")
def ai_chat(data: AIRequest):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=503,
            detail="Gemini API key is not configured"
        )

    try:
        client = genai.Client(api_key=api_key)

        prompt = f"""
        You are Dipsika Kundali AI Assistant.
        Help users understand astrology, zodiac signs,
        nakshatra and kundali concepts.

        Explain that astrology is for guidance and
        entertainment, not guaranteed predictions.

        Answer clearly in the user's language.

        User Question: {data.question}
        """

        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )

        return {
            "status": "success",
            "answer": response.text
        }

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Gemini AI request failed"
        )
