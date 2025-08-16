from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Dict, Any
import json
import base64
from models import Message, ChatRequest
from utils import run_tool, save_chat_message, CHATS_DIR, client, APIConnectionError, APIStatusError

router = APIRouter()

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

@router.post("/chat")
async def chat_endpoint(chat_req: ChatRequest) -> StreamingResponse:
    async def event_stream():
        try:
            if chat_req.tool:
                tool_input = chat_req.tool_input if chat_req.tool_input is not None else ""
                result = run_tool(chat_req.tool, tool_input)
                yield f"[Tool:{chat_req.tool}] {result}"
                if chat_req.chat:
                    save_chat_message(chat_req.chat, {"role": "tool", "content": result, "tool": chat_req.tool})
                return
            from typing import Any
            user_content: list[dict[str, Any]] = [{"type": "text", "text": chat_req.message}]
            if chat_req.image_base64:
                user_content.append({"type": "image_url", "image_url": {"url": f"data:image/png;base64,{chat_req.image_base64}"}})
            messages: List[Message] = [Message.model_validate(msg) for msg in chat_req.history]
            messages.append(Message(role="user", content=user_content))
            def to_message_param(msg):
                if msg.role == "user":
                    return {"role": "user", "content": msg.content}
                elif msg.role == "assistant":
                    return {"role": "assistant", "content": msg.content}
                elif msg.role == "system":
                    return {"role": "system", "content": msg.content}
                elif msg.role == "tool":
                    return {"role": "tool", "content": msg.content, "tool_call_id": getattr(msg, "tool_call_id", None)}
                else:
                    raise ValueError(f"Unknown message role: {msg.role}")
            messages_param = [to_message_param(m) for m in messages]  # type: ignore
            if chat_req.chat:
                save_chat_message(chat_req.chat, {"role": "user", "content": user_content})
            stream = client.chat.completions.create(
                messages=messages_param,  # type: ignore
                model="Llama-4-Maverick-17B-128E-Instruct-FP8",
                temperature=chat_req.temperature,
                max_completion_tokens=chat_req.max_completion_tokens,
                repetition_penalty=chat_req.repetition_penalty,
                top_k=chat_req.top_k,
                user=chat_req.user,
                stream=True,
            )
            full_response = ""
            for chunk in stream:
                if hasattr(chunk, "event") and hasattr(chunk.event, "delta"):
                    text = getattr(chunk.event.delta, "text", None)
                    if text is not None:
                        full_response += text
                        yield text
            if chat_req.chat:
                save_chat_message(chat_req.chat, {"role": "assistant", "content": full_response})
        except APIConnectionError:
            yield "[Error: Could not connect to Llama API]"
        except APIStatusError as e:
            yield f"[Error: Llama API returned status {e.status_code}]"
        except Exception as e:
            yield f"[Error: {str(e)}]"
    return StreamingResponse(event_stream(), media_type="text/plain")
