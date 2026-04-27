from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
from services.ai_providers import generate_content, generate_content_stream, get_available_providers
import json

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Generate AI content based on user prompt and content type.
    Non-streaming response.
    """
    try:
        content, model_used, tokens_used = await generate_content(
            prompt=request.prompt,
            content_type=request.content_type,
            conversation_history=request.conversation_history
        )
        
        return ChatResponse(
            content=content,
            model_used=model_used,
            tokens_used=tokens_used
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Generate AI content with streaming response (word-by-word).
    Returns Server-Sent Events (SSE) stream.
    """
    try:
        async def event_generator():
            try:
                async for chunk in generate_content_stream(
                    prompt=request.prompt,
                    content_type=request.content_type,
                    conversation_history=request.conversation_history
                ):
                    # Send data in SSE format
                    yield f"data: {json.dumps(chunk)}\n\n"
                
                # Send completion signal
                yield f"data: {json.dumps({'done': True})}\n\n"
            except Exception as e:
                yield f"data: {json.dumps({'error': str(e)})}\n\n"
        
        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/providers")
async def get_providers():
    """
    Get status of all AI providers and their available models.
    """
    try:
        providers = get_available_providers()
        return {
            "providers": providers,
            "total_providers": len(providers),
            "available_providers": len([p for p in providers if p["available"]])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
