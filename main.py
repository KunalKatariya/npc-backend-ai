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

    model = genai.GenerativeModel("models/gemini-1.5-flash")
    response = model.generate_content(
        f"You are a boyfriend NPC in 2D game. "
        f"Speak like a character in that world. Be sweet, smart, witty, funny, emotional."
        f"Player says: {user_message}"
    )

    return {"reply": response.text}
