import os
import json
from pathlib import Path
from llama_api_client import LlamaAPIClient, APIConnectionError, APIStatusError
from tools import ddgs_search

CHATS_DIR = Path("chats")
CHATS_DIR.mkdir(exist_ok=True)

LLAMA_API_KEY = os.environ.get('LLAMA_API_KEY')
if not LLAMA_API_KEY:
    raise ValueError("LLAMA_API_KEY environment variable is not set")

client = LlamaAPIClient(api_key=LLAMA_API_KEY)


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
