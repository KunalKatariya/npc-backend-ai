from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os

app = FastAPI()

# Allow requests from your Godot game
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_message = data.get("message", "")

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        f"You are an NPC in a fantasy 2D game. "
        f"Speak like a character in that world. "
        f"Player says: {user_message}"
    )

    return {"reply": response.text}
