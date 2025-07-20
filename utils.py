# utils.py
def format_interaction(entry):
    role = "👤 You" if entry["role"] == "user" else "🤖 AI"
    return f"**{role}:** {entry['content']}"

