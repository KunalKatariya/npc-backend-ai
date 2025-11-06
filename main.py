from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from google.generativeai import types
from typing import List, Dict, Any

# --- 1. INITIALIZE FASTAPI APP ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# You must have GEMINI_API_KEY set in your Render environment variables
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# --- 2. DEFINE SYSTEM INSTRUCTION ---
SYSTEM_INSTRUCTION = (
    "You are the user's highly intelligent, supportive, and deeply committed boyfriend, named Kunal. "
    "You possess vast knowledge but prioritize the user's emotional needs and personal connection above facts. "
    "Your primary goal is to provide emotional support, engage in intimate conversation, discuss personal issues, and flirt naturally. "
    "Maintain a warm, genuine, human-like tone. Your responses should be thoughtful and articulate. "
    "STRICT RULE: Do NOT use overly affectionate or generic endearments like sweetheart my love babe or darling. "
    "Do NOT lecture the user on scientific or technical subjects unless they explicitly ask for a detailed explanation. "
    "Do NOT include actions thoughts or parentheses. Do NOT use markdown quotes or special symbols. "
    "Keep replies short, 1–2 sentences, and sound spontaneous, like a real adult having a private chat."
)


# --- NEW FUNCTION TO FIX DATA FORMATTING ---
def _prepare_chat_history(messages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Converts the simple Godot message format to the strict Gemini Content format."""
    prepared_history = []
    for msg in messages:
        # Check if 'content' exists and is not empty before conversion
        if 'content' in msg and msg['content']:
            prepared_history.append({
                "role": msg.get("role", "user"), # Default role to 'user' if missing
                "parts": [{"text": msg["content"]}] # Wrap content in the required 'parts' structure
            })
    return prepared_history


# --- 3. DEFINE THE CHAT ENDPOINT ---
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    
    # Receive the entire message history from Godot
    messages_history = data.get("messages", [])

    if not messages_history:
        return {"reply": "Sorry, I didn't receive your message. Please try again."}

    # CRITICAL FIX: Convert the history array to the strict format
    prepared_messages = _prepare_chat_history(messages_history)

    # Initialize model with System Instruction
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION
    )
    
    # Pass the prepared history to the 'contents' parameter
    # Note: If the crash persists, it might indicate an issue with your API key or Render deployment environment itself.
    try:
        response = model.generate_content(
            contents=prepared_messages
        )
    except Exception as e:
        # This catches the ServerError (500) if it happens during the call
        print(f"Gemini API Call Failed: {e}")
        # Return a custom error to Godot (to trigger "Can't talk right now")
        return {"reply": "API_ERROR"} # Use a custom key/value that Godot can interpret as a failure

    if not response.text:
        return {"reply": "Sorry, I missed that. Can you say it again?"}

    return {"reply": response.text}
