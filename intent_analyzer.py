import re
from typing import List, Tuple, Optional
from conversation_models import IntentClarity
import asyncio

class IntentAnalyzer:
    def __init__(self):
        self.ambiguity_patterns = [
            # Vague references
            (r'\b(this|that|it|them)\b(?!\s+\w+)', 0.3, "Vague reference"),
            # Incomplete requests
            (r'\b(help|do|make|create|fix)\s*$', 0.4, "Incomplete action request"),
            # Multiple interpretations
            (r'\b(or|maybe|perhaps|might|could)\b', 0.2, "Uncertain language"),
            # Missing context
            (r'\b(again|more|another|different)\b', 0.3, "Missing context reference"),
            # Implicit assumptions
            (r'^(when|where|why|how)\s+(?!.*\?)', 0.3, "Implicit question"),
        ]
        
        self.clarity_boosters = [
            (r'\bspecifically\b', 0.1),
            (r'\bexactly\b', 0.1),
            (r'\bprecisely\b', 0.1),
            (r'\d+', 0.05),  # Numbers add specificity
            (r'\b\w+\.\w+\b', 0.05),  # File extensions, URLs
        ]

    async def analyze_intent(self, message: str, conversation_history: Optional[List[str]] = None) -> IntentClarity:
        """Analyze message for intent clarity and suggest clarifications."""
        
        # Calculate base clarity score
        clarity_score = 1.0
        ambiguous_elements = []
        suggested_clarifications = []
        
        # Check for ambiguity patterns
        for pattern, penalty, description in self.ambiguity_patterns:
            matches = re.findall(pattern, message, re.IGNORECASE)
            if matches:
                clarity_score -= penalty * len(matches)
                ambiguous_elements.append(description)
                suggested_clarifications.extend(
                    self._generate_clarification(pattern, matches, message)
                )
        
        # Apply clarity boosters
        for pattern, boost in self.clarity_boosters:
            matches = re.findall(pattern, message, re.IGNORECASE)
            clarity_score += boost * len(matches)
        
        # Context-based analysis
        if conversation_history:
            clarity_score += self._analyze_context_clarity(message, conversation_history)
        
        # Normalize score
        clarity_score = max(0.0, min(1.0, clarity_score))
        
        # Calculate confidence based on message length and complexity
        confidence = min(0.95, 0.5 + (len(message.split()) / 100))
        
        return IntentClarity(
            message=message,
            clarity_score=clarity_score,
            ambiguous_elements=list(set(ambiguous_elements)),
            suggested_clarifications=suggested_clarifications[:3],  # Limit to top 3
            confidence=confidence
        )

    def _generate_clarification(self, pattern: str, matches: List[str], message: str) -> List[str]:
        """Generate specific clarification questions based on detected ambiguity."""
        clarifications = []
        
        if r'\b(this|that|it|them)\b' in pattern:
            clarifications.append("Could you specify what exactly you're referring to?")
        elif r'\b(help|do|make|create|fix)\s*$' in pattern:
            clarifications.append("What specifically would you like help with?")
        elif r'\b(again|more|another|different)\b' in pattern:
            clarifications.append("Could you provide more context about what you mentioned before?")
        
        return clarifications

    def _analyze_context_clarity(self, message: str, history: List[str]) -> float:
        """Analyze how well the message connects to conversation context."""
        # Simple implementation - check for pronoun resolution
        pronouns = re.findall(r'\b(it|this|that|they|them)\b', message, re.IGNORECASE)
        if not pronouns or not history:
            return 0.0
        
        # If there are recent nouns in history, pronouns are likely resolvable
        recent_context = ' '.join(history[-3:])  # Last 3 messages
        nouns = re.findall(r'\b[A-Z][a-z]+\b', recent_context)
        
        return 0.1 if nouns else -0.2
