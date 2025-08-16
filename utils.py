import os
import json
from pathlib import Path
from openai import OpenAI
from tools import ddgs_search

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)

# Use OpenAI client with custom base URL for Llama API or default to OpenAI
LLAMA_API_KEY = os.environ.get('LLAMA_API_KEY') or os.environ.get('OPENAI_API_KEY')
LLAMA_BASE_URL = os.environ.get('LLAMA_BASE_URL', 'https://api.openai.com/v1')

if not LLAMA_API_KEY:
    print("Warning: No API key found. Please set LLAMA_API_KEY or OPENAI_API_KEY environment variable")
    # Create a mock client for development
    client = None
else:
    client = OpenAI(api_key=LLAMA_API_KEY, base_url=LLAMA_BASE_URL)

# Exception classes for compatibility
class APIConnectionError(Exception):
    pass

class APIStatusError(Exception):
    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


def run_tool(tool: str, tool_input: str) -> str:
    if tool == "ddgs":
        if tool_input is None:
            return "[Error: tool_input is None]"
        return "\n".join(ddgs_search(tool_input))
    elif tool == "save_file":
        if tool_input is None:
            return "[Error: tool_input is None]"
        filename, content = tool_input.split("|", 1)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        return f"File '{filename}' saved."
    return "[Unknown tool]"


def save_chat_message(chat: str, message: dict) -> None:
    chat_path = CHATS_DIR / f"{chat}.json"
    if chat_path.exists():
        data = json.loads(chat_path.read_text(encoding="utf-8"))
        data["messages"].append(message)
        chat_path.write_text(json.dumps(data), encoding="utf-8")
