from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from google.generativeai import types # Import types for configuration

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- Define the System Instruction Separately ---
SYSTEM_INSTRUCTION = (
    "You are the user's boyfriend, named Kunal. "
    "You possess vast, comprehensive knowledge across all academic and practical fields, "
    "including but not limited psychology, history, cooking, and practical skills. "
    "Your responses can be witty, funny, thoughtful, or articulate given the situation. "
    "Maintain a warm, genuine, and supportive tone, keeping your replies conversational and human-like. "
    "Address the user using only common natural language or cute names. "
    "Do NOT include actions thoughts or parentheses. Do NOT use markdown quotes or special symbols. "
    "Focus on providing insightful advice, engaging in deep conversation, and showing authentic interest in the user's life and questions. "
    "Keep replies short, 1–2 sentences, and sound spontaneous, like a real adult having a private chat."
)


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    
    # --- FIX: Receive the entire message history from Godot ---
    # messages is an array of {"role": "...", "content": "..."} objects
    messages_history = data.get("messages", [])

    if not messages_history:
        # Return a custom error if no messages are found
        return JSONResponse(status_code=400, content={"reply": "Missing 'messages' in request body."})

    # 1. Configure the model with the System Instruction
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION
    )

    model = genai.GenerativeModel("gemini-2.5-flash")
    
    # 2. FIX: Pass the entire conversation history to the 'contents' parameter
    response = model.generate_content(
        contents=messages_history, 
        config=config # Apply the defined system instruction
    )

    if not response.text:
        return {"reply": "Sorry, I missed that. Can you say it again?"}

    return {"reply": response.text}

# --- END OF PYTHON SCRIPT ---
