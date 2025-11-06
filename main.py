from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
import os
from google.generativeai import types # Keep this import

# ... (App setup and genai.configure remains the same)

# --- Define the System Instruction Separately (Keep this constant at the top) ---
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


@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    
    # Receive the entire message history from Godot
    messages_history = data.get("messages", [])

    if not messages_history:
        # Prevent crash if the list is empty
        return {"reply": "Sorry, I didn't receive your message. Please try again."}

    # FIX: 1. INITIALIZE MODEL WITH SYSTEM INSTRUCTION
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_INSTRUCTION # Passed here!
    )
    
    # 2. FIX: Pass the entire conversation history to the 'contents' parameter
    # NO separate config object needed for the system instruction now.
    response = model.generate_content(
        contents=messages_history # Pass the entire array of messages
    )

    # Check for empty response text
    if not response.text:
        return {"reply": "Sorry, I missed that. Can you say it again?"}

    return {"reply": response.text}
