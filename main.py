import streamlit as st
import os
import json
from groq import Groq

# Initialize Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Memory store file
HISTORY_FILE = "memory_store.json"

# Valid message roles for Groq API
VALID_ROLES = {"user", "assistant", "system"}

# Load messages into session state from disk
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return [{"role": "system", "content": "You are a helpful assistant. Try to improve your last answer each time by reflecting on it briefly before responding."}]

# Save messages to disk
def save_history(messages):
    with open(HISTORY_FILE, "w") as f:
        json.dump(messages, f, indent=2)

# Get model response
def get_gpt_response(messages):
    # Filter only valid roles for safety
    filtered = [msg for msg in messages if msg["role"] in VALID_ROLES]
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=filtered
    )
    return response.choices[0].message.content

# Setup session state
if "messages" not in st.session_state:
    st.session_state.messages = load_history()

# Display messages in UI
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
prompt = st.chat_input("Say something...")

# Handle user input
if prompt:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Add reflection prompt if assistant just replied before
    if len(st.session_state.messages) >= 2 and st.session_state.messages[-2]["role"] == "assistant":
        prev = st.session_state.messages[-2]["content"]
        reflection = {
            "role": "user",
            "content": f"Earlier you said:\n\"{prev}\"\nCan you improve or clarify that before continuing?"
        }
        st.session_state.messages.append(reflection)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = get_gpt_response(st.session_state.messages)
            st.markdown(reply)

    # Add assistant reply
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Save updated history
    save_history(st.session_state.messages)

