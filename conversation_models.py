from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel
from datetime import datetime
import json

class ConversationState(BaseModel):
    chat_id: str
    user_id: str
    topic_summary: str
    key_entities: List[str]
    conversation_stage: Literal["opening", "developing", "clarifying", "concluding"]
    last_updated: datetime
    importance_scores: Dict[str, float]  # message_id -> importance score

class UserProfile(BaseModel):
    user_id: str
    communication_style: Dict[str, float]  # formality, enthusiasm, technical_depth, etc.
    preferred_response_length: Literal["brief", "detailed", "adaptive"]
    topic_preferences: Dict[str, float]
    clarification_frequency: float  # How often user needs clarification
    last_updated: datetime

class IntentClarity(BaseModel):
    message: str
    clarity_score: float  # 0.0 = very ambiguous, 1.0 = crystal clear
    ambiguous_elements: List[str]
    suggested_clarifications: List[str]
    confidence: float

class EnhancedMessage(BaseModel):
    role: str
    content: Any
    timestamp: datetime
    message_id: str
    importance_score: float = 0.5
    intent_clarity: Optional[IntentClarity] = None
    tool: Optional[str] = None
