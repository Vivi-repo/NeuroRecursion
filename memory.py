# memory.py
class Memory:
    def __init__(self):
        self.context = []

    def store(self, role, content):
        if role not in ["system", "user", "assistant"]:
            raise ValueError(f"Invalid role: {role}. Must be 'system', 'user', or 'assistant'.")
        self.context.append({"role": role, "content": content})

    def get_context(self):
        return self.context[-10:]  # optional: limit to last 10 messages


