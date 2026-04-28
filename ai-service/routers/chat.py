from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from models.schemas import ChatRequest, ChatResponse
from services.streaming import stream_response
from services.model_router import get_provider_chain
from services.ai_client import generate_content
from services.followup_service import should_ask_followup_questions, generate_bot_followup_questions
import json

router = APIRouter()


@router.post("/")
async def chat(request: ChatRequest):
    """
    Generate AI content with non-streaming response.
    Returns complete response at once.
    
    Supports:
    - Multiple AI providers with intelligent fallback
    - Conversation history context
    - Tone, length, and language customization
    - File uploads and custom instructions
    - Automatic follow-up questions when needed
    """
    try:
        history = []
        if request.conversation_history:
            history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ]
        
        # Check if bot should ask follow-up questions
        should_ask_followup = await should_ask_followup_questions(
            content_type=request.content_type.value,
            user_message=request.prompt,
            conversation_history=history
        )
        
        # If bot should ask follow-up questions, generate them instead of regular content
        if should_ask_followup:
            followup_message = await generate_bot_followup_questions(
                content_type=request.content_type.value,
                user_message=request.prompt,
                conversation_history=history,
                user_id=request.user_id or ""
            )
            
            return ChatResponse(
                content=followup_message,
                provider="followup_service",
                model="question_generator",
                word_count=len(followup_message.split()),
                char_count=len(followup_message)
            )
        
        # Generate regular content using AI client
        result = await generate_content(
            prompt=request.prompt,
            content_type=request.content_type.value,
            tone=request.tone.value,
            length=request.length.value,
            language=request.language.value,
            history=history,
            uploaded_text=request.uploaded_text,
            custom_instructions=request.custom_instructions,
            user_id=request.user_id or "",
            regenerate=request.regenerate
        )
        
        return ChatResponse(
            content=result["content"],
            provider=result["provider"],
            model=result["model"],
            word_count=result.get("word_count", 0),
            char_count=result.get("char_count", 0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def chat_stream(request: ChatRequest):
    """
    Generate AI content with streaming response (word-by-word).
    Returns Server-Sent Events (SSE) stream.
    
    Supports:
    - Multiple AI providers with intelligent fallback
    - Conversation history context
    - Tone, length, and language customization
    - File uploads and custom instructions
    - Automatic follow-up questions when needed
    """
    try:
        async def event_generator():
            try:
                history = []
                if request.conversation_history:
                    history = [
                        {"role": msg.role, "content": msg.content}
                        for msg in request.conversation_history
                    ]
                
                # Check if bot should ask follow-up questions
                should_ask_followup = await should_ask_followup_questions(
                    content_type=request.content_type.value,
                    user_message=request.prompt,
                    conversation_history=history
                )
                
                # If bot should ask follow-up questions, stream them
                if should_ask_followup:
                    followup_message = await generate_bot_followup_questions(
                        content_type=request.content_type.value,
                        user_message=request.prompt,
                        conversation_history=history,
                        user_id=request.user_id or ""
                    )
                    
                    # Stream the follow-up message word by word
                    words = followup_message.split()
                    for i, word in enumerate(words):
                        chunk_data = {
                            "content": word + " ",
                            "provider": "followup_service",
                            "model": "question_generator",
                            "done": i == len(words) - 1
                        }
                        yield f"data: {json.dumps(chunk_data)}\n\n"
                    
                    # Send final completion event
                    final_data = {
                        "content": "",
                        "provider": "followup_service",
                        "model": "question_generator",
                        "done": True,
                        "word_count": len(words),
                        "char_count": len(followup_message)
                    }
                    yield f"data: {json.dumps(final_data)}\n\n"
                    return
                
                # Stream regular content
                async for chunk in stream_response(
                    prompt=request.prompt,
                    content_type=request.content_type.value,
                    tone=request.tone.value,
                    length=request.length.value,
                    language=request.language.value,
                    history=history,
                    uploaded_text=request.uploaded_text,
                    custom_instructions=request.custom_instructions,
                    user_id=request.user_id or "",
                    regenerate=request.regenerate
                ):
                    yield chunk
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
        provider_chain = get_provider_chain("general")
        providers = [
            {
                "name": p.name,
                "model": p.model,
                "available": bool(p.api_key)
            }
            for p in provider_chain
        ]
        return {
            "providers": providers,
            "total_providers": len(providers),
            "available_providers": len([p for p in providers if p["available"]])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
