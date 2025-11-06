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
        f"You are a loving boyfriend NPC in a 2D game. "
        f"Reply naturally and sweetly to the player. "
        f"Do NOT include actions, thoughts, or parentheses. "
        f"Do NOT use markdown, quotes, or special symbols. "
        f"Keep your reply short and conversational. "
        f"Player says: {user_message}"
    )

    response = model.generate_content(prompt)

    return {"reply": response.text}
