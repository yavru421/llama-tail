from typing import List, Dict, Any, Optional, Literal
from conversation_models import ConversationState, EnhancedMessage
import json
import asyncio
from datetime import datetime, timedelta
import re

class ContextManager:
    def __init__(self, max_context_messages: int = 20):
        self.max_context_messages = max_context_messages
        self.entity_patterns = [
            r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',  # Proper nouns
            r'\b\w+\.\w+\b',  # File names, URLs
            r'\b\d+(?:\.\d+)?\b',  # Numbers
        ]

    async def update_conversation_state(
        self, 
        chat_id: str, 
        user_id: str, 
        new_message: EnhancedMessage,
        existing_state: Optional[ConversationState] = None
    ) -> ConversationState:
        """Update conversation state with new message."""
        
        if existing_state is None:
            existing_state = ConversationState(
                chat_id=chat_id,
                user_id=user_id,
                topic_summary="",
                key_entities=[],
                conversation_stage="opening",
                last_updated=datetime.now(),
                importance_scores={}
            )

        # Extract entities from new message
        new_entities = self._extract_entities(str(new_message.content))
        
        # Update key entities (keep most recent and important)
        all_entities = existing_state.key_entities + new_entities
        existing_state.key_entities = list(set(all_entities))[-10:]  # Keep last 10 unique

        # Update importance scores
        existing_state.importance_scores[new_message.message_id] = new_message.importance_score

        # Update conversation stage
        existing_state.conversation_stage = self._determine_stage(new_message, existing_state)

        # Update topic summary (simplified - in production, use LLM)
        existing_state.topic_summary = self._update_topic_summary(
            existing_state.topic_summary, 
            str(new_message.content)
        )

        existing_state.last_updated = datetime.now()
        
        return existing_state

    async def get_relevant_context(
        self, 
        conversation_state: ConversationState, 
        current_message: str,
        full_history: List[EnhancedMessage]
    ) -> List[EnhancedMessage]:
        """Get most relevant context for current message."""
        
        # Sort messages by importance and recency
        scored_messages = []
        current_time = datetime.now()
        
        for msg in full_history[-self.max_context_messages:]:
            # Recency score (more recent = higher score)
            time_diff = (current_time - msg.timestamp).total_seconds() / 3600  # hours
            recency_score = max(0, 1 - (time_diff / 24))  # Decay over 24 hours
            
            # Importance score
            importance_score = conversation_state.importance_scores.get(msg.message_id, 0.5)
            
            # Relevance score (check for entity/topic overlap)
            relevance_score = self._calculate_relevance(current_message, str(msg.content))
            
            # Combined score
            final_score = (recency_score * 0.3 + importance_score * 0.4 + relevance_score * 0.3)
            scored_messages.append((msg, final_score))
        
        # Sort by score and return top messages
        scored_messages.sort(key=lambda x: x[1], reverse=True)
        return [msg for msg, score in scored_messages[:10]]

    def _extract_entities(self, text: str) -> List[str]:
        """Extract key entities from text."""
        entities = []
        for pattern in self.entity_patterns:
            matches = re.findall(pattern, text)
            entities.extend(matches)
        return list(set(entities))

    def _determine_stage(self, message: EnhancedMessage, state: ConversationState) -> Literal["opening", "developing", "clarifying", "concluding"]:
        """Determine conversation stage based on message content."""
        content = str(message.content).lower()
        
        if any(word in content for word in ['hello', 'hi', 'start', 'begin']):
            return "opening"
        elif any(word in content for word in ['clarify', 'explain', 'what', 'how', 'why']):
            return "clarifying"
        elif any(word in content for word in ['thanks', 'bye', 'done', 'finish']):
            return "concluding"
        else:
            return "developing"

    def _calculate_relevance(self, current_message: str, historical_message: str) -> float:
        """Calculate relevance between current and historical message."""
        current_entities = set(self._extract_entities(current_message))
        historical_entities = set(self._extract_entities(historical_message))
        
        if not current_entities and not historical_entities:
            return 0.1
        
        overlap = len(current_entities.intersection(historical_entities))
        total = len(current_entities.union(historical_entities))
        
        return overlap / total if total > 0 else 0.0

    def _update_topic_summary(self, existing_summary: str, new_content: str) -> str:
        """Update topic summary with new content (simplified version)."""
        # In production, use LLM for better summarization
        key_words = self._extract_entities(new_content)
        
        if not existing_summary:
            return f"Discussion about: {', '.join(key_words[:5])}"
        
        return f"{existing_summary}; {', '.join(key_words[:3])}"
