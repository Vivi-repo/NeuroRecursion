# gpt_decision.py

import os
from dotenv import load_dotenv
from groq import Groq  # <--- YES, this is needed and included

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Raise error if key not found
if not api_key:
    raise ValueError("API key not found. Make sure you have a .env file with GROQ_API_KEY set.")

# Initialize Groq client
client = Groq(api_key=api_key)

def get_gpt_response(messages):
    # Filter out any invalid messages
    valid_roles = {"user", "assistant", "system"}
    cleaned_messages = [
        m for m in messages if isinstance(m, dict)
        and m.get("role") in valid_roles
        and isinstance(m.get("content"), str)
    ]

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=cleaned_messages,
        temperature=0.7,
    )
    return response.choices[0].message.content






