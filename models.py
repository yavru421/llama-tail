from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: Any
    tool: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    image_base64: Optional[str] = None
    temperature: float = 0.7
    max_completion_tokens: int = 8024
    repetition_penalty: float = 1.0
    top_k: int = 50
    top_p: float = 1.0
    user: str = ""
    tool: Optional[str] = None
    tool_input: Optional[str] = None
    chat: Optional[str] = None
    history: List[Dict[str, Any]] = []
