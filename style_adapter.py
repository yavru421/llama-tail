import re
from typing import Dict, List, Tuple
from conversation_models import UserProfile
from datetime import datetime

class StyleAdapter:
    def __init__(self):
        self.style_indicators = {
            'formality': [
                (r'\b(please|thank you|would you|could you)\b', 0.2),
                (r'\b(gonna|wanna|gotta|yeah)\b', -0.2),
                (r'[.!?]$', 0.1),
                (r'[A-Z][a-z]', 0.05),
            ],
            'enthusiasm': [
                (r'[!]{1,}', 0.3),
                (r'\b(awesome|great|amazing|wonderful|excellent)\b', 0.2),
                (r'[A-Z]{2,}', 0.1),
                (r'[?]{2,}', 0.1),
            ],
            'technical_depth': [
                (r'\b(API|SDK|JSON|XML|HTTP|database|algorithm)\b', 0.3),
                (r'\b(function|method|class|variable|parameter)\b', 0.2),
                (r'\b\w+\(\)', 0.2),  # Function calls
                (r'```|`[^`]+`', 0.3),  # Code blocks
            ],
            'brevity': [
                (r'^.{1,50}$', 0.5),  # Short messages
                (r'^.{51,150}$', 0.0),  # Medium messages
                (r'^.{151,}$', -0.5),  # Long messages
            ]
        }

    async def analyze_user_style(self, messages: List[str]) -> Dict[str, float]:
        """Analyze user's communication style from their message history."""
        style_scores = {key: 0.0 for key in self.style_indicators.keys()}
        
        for message in messages:
            for style_type, patterns in self.style_indicators.items():
                for pattern, weight in patterns:
                    matches = len(re.findall(pattern, message, re.IGNORECASE | re.MULTILINE))
                    style_scores[style_type] += weight * matches
        
        # Normalize scores
        message_count = len(messages)
        if message_count > 0:
            for key in style_scores:
                style_scores[key] = max(-1.0, min(1.0, style_scores[key] / message_count))
        
        return style_scores

    async def adapt_response_style(
        self, 
        base_response: str, 
        user_profile: UserProfile,
        conversation_context: str = ""
    ) -> str:
        """Adapt response to match user's communication style."""
        
        adapted_response = base_response
        style = user_profile.communication_style
        
        # Adjust formality
        if style.get('formality', 0) > 0.3:
            adapted_response = self._increase_formality(adapted_response)
        elif style.get('formality', 0) < -0.3:
            adapted_response = self._decrease_formality(adapted_response)
        
        # Adjust enthusiasm
        if style.get('enthusiasm', 0) > 0.3:
            adapted_response = self._increase_enthusiasm(adapted_response)
        
        # Adjust technical depth
        if style.get('technical_depth', 0) > 0.3:
            adapted_response = self._increase_technical_detail(adapted_response)
        elif style.get('technical_depth', 0) < -0.3:
            adapted_response = self._simplify_technical_language(adapted_response)
        
        # Adjust length based on user preference
        if user_profile.preferred_response_length == "brief":
            adapted_response = self._make_concise(adapted_response)
        elif user_profile.preferred_response_length == "detailed":
            adapted_response = self._add_detail(adapted_response)
        
        return adapted_response

    def _increase_formality(self, text: str) -> str:
        """Make text more formal."""
        replacements = [
            (r'\bcan\'t\b', 'cannot'),
            (r'\bwon\'t\b', 'will not'),
            (r'\bdon\'t\b', 'do not'),
            (r'\bisn\'t\b', 'is not'),
            (r'\byeah\b', 'yes'),
            (r'\bokay\b', 'very well'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        # Add courteous phrases
        if not re.search(r'\b(please|thank you)\b', text, re.IGNORECASE):
            text = f"Please note that {text.lower()}" if text else text
        
        return text

    def _decrease_formality(self, text: str) -> str:
        """Make text more casual."""
        replacements = [
            (r'\bcannot\b', 'can\'t'),
            (r'\bwill not\b', 'won\'t'),
            (r'\bdo not\b', 'don\'t'),
            (r'\bis not\b', 'isn\'t'),
            (r'\byes\b', 'yeah'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

    def _increase_enthusiasm(self, text: str) -> str:
        """Add enthusiasm to response."""
        if not text.endswith('!'):
            text = text.rstrip('.') + '!'
        
        enthusiasm_words = {
            'good': 'great',
            'nice': 'awesome',
            'ok': 'excellent',
            'works': 'works perfectly'
        }
        
        for word, replacement in enthusiasm_words.items():
            text = re.sub(rf'\b{word}\b', replacement, text, flags=re.IGNORECASE)
        
        return text

    def _increase_technical_detail(self, text: str) -> str:
        """Add more technical detail."""
        # This is a simplified version - in production, use LLM for better enhancement
        return f"{text} For more technical details, please refer to the relevant documentation or API specifications."

    def _simplify_technical_language(self, text: str) -> str:
        """Simplify technical language."""
        simplifications = {
            'API': 'interface',
            'parameters': 'settings',
            'function': 'feature',
            'execute': 'run',
            'implement': 'create'
        }
        
        for technical, simple in simplifications.items():
            text = re.sub(rf'\b{technical}\b', simple, text, flags=re.IGNORECASE)
        
        return text

    def _make_concise(self, text: str) -> str:
        """Make response more concise."""
        # Remove unnecessary phrases
        text = re.sub(r'\b(in order to|for the purpose of)\b', 'to', text, flags=re.IGNORECASE)
        text = re.sub(r'\b(at this point in time|at the present time)\b', 'now', text, flags=re.IGNORECASE)
        
        # If still too long, truncate to first sentence
        sentences = text.split('. ')
        if len(sentences) > 1 and len(text) > 200:
            return sentences[0] + '.'
        
        return text

    def _add_detail(self, text: str) -> str:
        """Add more detail to response."""
        # This is simplified - in production, use LLM for better expansion
        return f"{text} Additionally, you might want to consider the various options and alternatives available for this approach."
