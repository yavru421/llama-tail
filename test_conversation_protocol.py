import pytest
import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from intent_analyzer import IntentAnalyzer
from context_manager import ContextManager
from style_adapter import StyleAdapter
from conversation_models import ConversationState, UserProfile, EnhancedMessage
from datetime import datetime

class TestIntentAnalyzer:
    @pytest.fixture
    def analyzer(self):
        return IntentAnalyzer()
    
    @pytest.mark.asyncio
    async def test_clear_intent(self, analyzer):
        message = "Please create a Python function that calculates the factorial of a number"
        result = await analyzer.analyze_intent(message)
        assert result.clarity_score > 0.7
        assert len(result.suggested_clarifications) == 0
    
    @pytest.mark.asyncio
    async def test_ambiguous_intent(self, analyzer):
        message = "Can you help me with this?"
        result = await analyzer.analyze_intent(message)
        assert result.clarity_score < 0.6
        assert len(result.suggested_clarifications) > 0
    
    @pytest.mark.asyncio
    async def test_pronoun_resolution(self, analyzer):
        history = ["I'm working on a Python project", "It has a web interface"]
        message = "Can you improve it?"
        result = await analyzer.analyze_intent(message, history)
        # Should have better clarity with context
        assert result.clarity_score > 0.3

class TestContextManager:
    @pytest.fixture
    def manager(self):
        return ContextManager()
    
    @pytest.mark.asyncio
    async def test_conversation_state_update(self, manager):
        message = EnhancedMessage(
            role="user",
            content="I need help with Python programming",
            timestamp=datetime.now(),
            message_id="test123",
            importance_score=0.8
        )
        
        state = await manager.update_conversation_state(
            "chat1", "user1", message
        )
        
        assert state.chat_id == "chat1"
        assert state.user_id == "user1"
        assert "Python" in state.key_entities
    
    @pytest.mark.asyncio
    async def test_relevance_calculation(self, manager):
        current = "I need help with database design"
        historical = "Let's work on the database schema together"
        
        relevance = manager._calculate_relevance(current, historical)
        assert relevance > 0.0  # Should have some overlap

class TestStyleAdapter:
    @pytest.fixture
    def adapter(self):
        return StyleAdapter()
    
    @pytest.mark.asyncio
    async def test_formal_style_detection(self, adapter):
        messages = [
            "Could you please help me with this issue?",
            "Thank you for your assistance.",
            "I would appreciate your guidance."
        ]
        
        style = await adapter.analyze_user_style(messages)
        assert style['formality'] > 0.2
    
    @pytest.mark.asyncio
    async def test_casual_style_detection(self, adapter):
        messages = [
            "hey can u help me?",
            "yeah that works",
            "gonna try this now"
        ]
        
        style = await adapter.analyze_user_style(messages)
        assert style['formality'] < 0.0
    
    @pytest.mark.asyncio
    async def test_technical_style_detection(self, adapter):
        messages = [
            "I need to implement an API endpoint",
            "The database query is returning null",
            "Can you help with this function()?",
            "Here's the code: ```python\nprint('test')\n```"
        ]
        
        style = await adapter.analyze_user_style(messages)
        assert style['technical_depth'] > 0.3
    
    @pytest.mark.asyncio
    async def test_response_adaptation(self, adapter):
        profile = UserProfile(
            user_id="test",
            communication_style={
                'formality': 0.8,
                'enthusiasm': 0.2,
                'technical_depth': 0.9,
                'brevity': -0.3
            },
            preferred_response_length="detailed",
            topic_preferences={},
            clarification_frequency=0.1,
            last_updated=datetime.now()
        )
        
        base_response = "I can't help with that right now."
        adapted = await adapter.adapt_response_style(base_response, profile)
        
        # Should be more formal
        assert "cannot" in adapted or "I cannot" in adapted

if __name__ == "__main__":
    # Run a simple test manually
    async def main():
        analyzer = IntentAnalyzer()
        
        # Test clear intent
        clear_result = await analyzer.analyze_intent(
            "Please create a Python function to calculate fibonacci numbers"
        )
        print(f"Clear intent score: {clear_result.clarity_score}")
        
        # Test ambiguous intent
        ambiguous_result = await analyzer.analyze_intent(
            "help me with this"
        )
        print(f"Ambiguous intent score: {ambiguous_result.clarity_score}")
        print(f"Suggestions: {ambiguous_result.suggested_clarifications}")
        
        # Test style analysis
        style_adapter = StyleAdapter()
        formal_messages = [
            "Could you please assist me with this matter?",
            "Thank you for your consideration.",
            "I would appreciate your guidance on this issue."
        ]
        
        style = await style_adapter.analyze_user_style(formal_messages)
        print(f"Style analysis: {style}")
    
    asyncio.run(main())
