from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Dict, Any, Optional
import json
import base64
import uuid
from datetime import datetime
from models import Message, ChatRequest
from utils import run_tool, save_chat_message, CHATS_DIR, client, APIConnectionError, APIStatusError
from intent_analyzer import IntentAnalyzer
from context_manager import ContextManager
from style_adapter import StyleAdapter
from conversation_models import ConversationState, UserProfile, EnhancedMessage, IntentClarity

router = APIRouter()

# Initialize the conversation understanding modules
intent_analyzer = IntentAnalyzer()
context_manager = ContextManager()
style_adapter = StyleAdapter()

# Add new utility functions
async def load_conversation_state(chat_id: str) -> Optional[ConversationState]:
    """Load conversation state from storage."""
    state_path = CHATS_DIR / f"{chat_id}_state.json"
    if state_path.exists():
        data = json.loads(state_path.read_text(encoding="utf-8"))
        return ConversationState.model_validate(data)
    return None

async def save_conversation_state(state: ConversationState):
    """Save conversation state to storage."""
    state_path = CHATS_DIR / f"{state.chat_id}_state.json"
    CHATS_DIR.mkdir(exist_ok=True)
    state_path.write_text(json.dumps(state.model_dump(), default=str), encoding="utf-8")

async def load_user_profile(user_id: str) -> Optional[UserProfile]:
    """Load user profile from storage."""
    profile_path = CHATS_DIR / f"profile_{user_id}.json"
    if profile_path.exists():
        data = json.loads(profile_path.read_text(encoding="utf-8"))
        return UserProfile.model_validate(data)
    return None

async def save_user_profile(profile: UserProfile):
    """Save user profile to storage."""
    profile_path = CHATS_DIR / f"profile_{profile.user_id}.json"
    CHATS_DIR.mkdir(exist_ok=True)
    profile_path.write_text(json.dumps(profile.model_dump(), default=str), encoding="utf-8")

@router.get("/list_chats")
async def list_chats():
    if not CHATS_DIR.exists():
        return {"chats": []}
    return {"chats": [f.stem for f in CHATS_DIR.glob("*.json") if f.is_file()]}

@router.get("/get_chat")
async def get_chat(chat: str):
    chat_path = CHATS_DIR / f"{chat}.json"
    if not chat_path.exists():
        return {"messages": []}
    data = json.loads(chat_path.read_text(encoding="utf-8"))
    return {"messages": data.get("messages", [])}

@router.post("/upload_image")
async def upload_image(file: UploadFile = File(...)):
    content = await file.read()
    return {"base64": base64.b64encode(content).decode("utf-8")}

@router.post("/create_chat")
async def create_chat(chat_name: str = Form(...)) -> JSONResponse:
    chat_path = CHATS_DIR / f"{chat_name}.json"
    CHATS_DIR.mkdir(exist_ok=True)
    chat_path.write_text(json.dumps({"messages": []}), encoding="utf-8")
    return JSONResponse(content={"status": "ok", "chat": chat_name}, media_type="application/json")

@router.post("/clarify")
async def clarify_intent(chat_req: ChatRequest) -> JSONResponse:
    """Analyze message for intent clarity and return clarification if needed."""
    
    # Load conversation history for context
    history = []
    if chat_req.chat:
        chat_path = CHATS_DIR / f"{chat_req.chat}.json"
        if chat_path.exists():
            data = json.loads(chat_path.read_text(encoding="utf-8"))
            history = [msg.get("content", "") for msg in data.get("messages", [])]
    
    # Analyze intent
    intent_clarity = await intent_analyzer.analyze_intent(chat_req.message, history[-5:])
    
    return JSONResponse(content={
        "clarity_score": intent_clarity.clarity_score,
        "needs_clarification": intent_clarity.clarity_score < 0.6,
        "suggested_clarifications": intent_clarity.suggested_clarifications,
        "ambiguous_elements": intent_clarity.ambiguous_elements
    })

@router.post("/chat")
async def enhanced_chat_endpoint(chat_req: ChatRequest) -> StreamingResponse:
    async def enhanced_event_stream():
        try:
            # Step 1: Intent Analysis
            conversation_history = []
            if chat_req.chat:
                chat_path = CHATS_DIR / f"{chat_req.chat}.json"
                if chat_path.exists():
                    data = json.loads(chat_path.read_text(encoding="utf-8"))
                    conversation_history = [msg.get("content", "") for msg in data.get("messages", [])]
            
            intent_clarity = await intent_analyzer.analyze_intent(
                chat_req.message, 
                conversation_history[-5:]
            )
            
            # Step 2: Check if clarification is needed
            if intent_clarity.clarity_score < 0.6 and len(intent_clarity.suggested_clarifications) > 0:
                yield f"I want to make sure I understand correctly. {intent_clarity.suggested_clarifications[0]}"
                return
            
            # Step 3: Load conversation state and user profile
            user_id = chat_req.user or "default_user"
            conversation_state = await load_conversation_state(chat_req.chat) if chat_req.chat else None
            user_profile = await load_user_profile(user_id)
            
            # Step 4: Create enhanced message
            message_id = str(uuid.uuid4())
            enhanced_message = EnhancedMessage(
                role="user",
                content=chat_req.message,
                timestamp=datetime.now(),
                message_id=message_id,
                importance_score=min(1.0, intent_clarity.clarity_score + 0.2),
                intent_clarity=intent_clarity
            )
            
            # Step 5: Update conversation state
            if chat_req.chat:
                conversation_state = await context_manager.update_conversation_state(
                    chat_req.chat, user_id, enhanced_message, conversation_state
                )
                await save_conversation_state(conversation_state)
            
            # Step 6: Handle tool usage (existing logic)
            if chat_req.tool:
                tool_input = chat_req.tool_input if chat_req.tool_input is not None else ""
                result = run_tool(chat_req.tool, tool_input)
                yield f"[Tool:{chat_req.tool}] {result}"
                if chat_req.chat:
                    save_chat_message(chat_req.chat, {"role": "tool", "content": result, "tool": chat_req.tool})
                return
            
            # Step 7: Prepare enhanced context for LLM
            from typing import Any
            user_content: List[Dict[str, Any]] = [{"type": "text", "text": chat_req.message}]
            if chat_req.image_base64:
                user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{chat_req.image_base64}"}})
            
            # Load full message history as EnhancedMessage objects
            full_history = []
            if chat_req.chat and conversation_history:
                for i, msg_content in enumerate(conversation_history):
                    full_history.append(EnhancedMessage(
                        role="assistant" if i % 2 == 1 else "user",
                        content=msg_content,
                        timestamp=datetime.now(),
                        message_id=str(uuid.uuid4()),
                        importance_score=0.5
                    ))
            
            # Get relevant context
            relevant_context = []
            if conversation_state and full_history:
                relevant_context = await context_manager.get_relevant_context(
                    conversation_state, chat_req.message, full_history
                )
            
            # Prepare messages for LLM with enhanced context
            messages = []
            
            # Add system message with conversation context
            if conversation_state:
                system_prompt = f"""You are a helpful assistant. 
                
Conversation context:
- Topic: {conversation_state.topic_summary}
- Stage: {conversation_state.conversation_stage}
- Key entities: {', '.join(conversation_state.key_entities)}

User communication style: {user_profile.communication_style if user_profile else 'Unknown'}
"""
                messages.append({"role": "system", "content": system_prompt})
            
            # Add relevant context messages
            for ctx_msg in relevant_context[-5:]:  # Last 5 relevant messages
                if ctx_msg.role == "user":
                    messages.append({"role": "user", "content": str(ctx_msg.content)})
                elif ctx_msg.role == "assistant":
                    messages.append({"role": "assistant", "content": str(ctx_msg.content)})
            
            # Add current message
            messages.append({"role": "user", "content": user_content})
            
            # Step 8: Generate response
            if chat_req.chat:
                save_chat_message(chat_req.chat, {"role": "user", "content": user_content})
            
            # Handle case where no API client is available (development mode)
            if client is None:
                yield "Hello! I'm running in development mode without an API key. "
                yield "The conversation understanding protocol has been successfully implemented with the following features:\n\n"
                yield f"📊 Intent Analysis: Your message clarity score is {intent_clarity.clarity_score:.2f}\n"
                yield f"💬 Conversation Stage: {conversation_state.conversation_stage if conversation_state else 'opening'}\n"
                yield f"🎯 Key Entities: {', '.join(conversation_state.key_entities) if conversation_state else 'None detected'}\n"
                yield f"🎨 User Style: {user_profile.communication_style if user_profile else 'Being analyzed'}\n\n"
                yield "To enable full AI responses, please set your LLAMA_API_KEY or OPENAI_API_KEY environment variable."
                return
            
            stream = client.chat.completions.create(
                messages=messages,
                model="gpt-3.5-turbo",  # Use standard model for better compatibility
                temperature=chat_req.temperature,
                max_tokens=chat_req.max_completion_tokens,
                user=chat_req.user,
                stream=True,
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if hasattr(delta, 'content') and delta.content is not None:
                        full_response += delta.content
                        yield delta.content
            
            # Step 9: Apply style adaptation
            if user_profile:
                adapted_response = await style_adapter.adapt_response_style(
                    full_response, user_profile, conversation_state.topic_summary if conversation_state else ""
                )
                
                # If significantly different, yield the adaptation
                if len(adapted_response) != len(full_response):
                    yield f"\n\n[Adapted to your style: {adapted_response[len(full_response):]}]"
            
            # Step 10: Update user profile based on interaction
            if user_profile is None:
                user_profile = UserProfile(
                    user_id=user_id,
                    communication_style=await style_adapter.analyze_user_style([chat_req.message]),
                    preferred_response_length="adaptive",
                    topic_preferences={},
                    clarification_frequency=1.0 if intent_clarity.clarity_score < 0.6 else 0.0,
                    last_updated=datetime.now()
                )
            else:
                # Update style analysis
                user_messages = [chat_req.message] + [msg for i, msg in enumerate(conversation_history) if i % 2 == 0]
                user_profile.communication_style = await style_adapter.analyze_user_style(user_messages[-10:])
                user_profile.last_updated = datetime.now()
            
            await save_user_profile(user_profile)
            
            # Save assistant response
            if chat_req.chat:
                save_chat_message(chat_req.chat, {"role": "assistant", "content": full_response})
                
        except Exception as e:
            if "APIConnectionError" in str(type(e)):
                yield "[Error: Could not connect to API]"
            elif hasattr(e, 'status_code'):
                yield f"[Error: API returned status {getattr(e, 'status_code', 'unknown')}]"
            else:
                yield f"[Error: {str(e)}]"
    
    return StreamingResponse(enhanced_event_stream(), media_type="text/plain")
