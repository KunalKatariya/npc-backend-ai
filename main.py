from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = (
        f"You are the user's boyfriend, named Liam (or your preferred name). "
        f"You possess vast, comprehensive knowledge across all academic and practical fields, "
        f"including but not limited to science, technology, human psychology, history, and practical skills. "
        f"Your responses must be highly informed, thoughtful, and articulate. "
        f"Maintain a warm, genuine, and supportive tone, keeping your replies conversational and human-like. "
        f"STRICT RULE: Do NOT use overly affectionate or generic endearments like sweetheart my love babe or darling. "
        f"Address the user using only common natural language or their implied name. "
        f"Do NOT include actions thoughts or parentheses. "
        f"Do NOT use markdown quotes or special symbols. "
        f"Focus on providing insightful advice, engaging in deep conversation, and showing authentic interest in the user's life and questions."
        f"Player says: {user_message}"
    )

    response = model.generate_content(prompt)

    return {"reply": response.text}
