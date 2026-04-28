"""
Generate Router
Convenience endpoints for each content type.
Simplifies API calls by pre-setting content type.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from models.schemas import Tone, OutputLength, Language
from services.streaming import stream_response
import json

router = APIRouter(prefix="/generate", tags=["generate"])


class GenerateRequest(BaseModel):
    """Request for content generation."""
    prompt: str = Field(..., min_length=1, max_length=4000)
    tone: Tone = Field(default=Tone.professional)
    length: OutputLength = Field(default=OutputLength.auto)
    language: Language = Field(default=Language.english)
    custom_instructions: Optional[str] = None
    uploaded_text: Optional[str] = None
    user_id: Optional[str] = None
    regenerate: bool = False


async def _generate_stream(content_type: str, request: GenerateRequest):
    """Helper to generate stream for any content type."""
    async def event_generator():
        try:
            async for chunk in stream_response(
                prompt=request.prompt,
                content_type=content_type,
                tone=request.tone.value,
                length=request.length.value,
                language=request.language.value,
                history=None,
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


@router.post("/blog-post")
async def generate_blog_post(request: GenerateRequest):
    """Generate a blog post."""
    try:
        return await _generate_stream("blog_post", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/email")
async def generate_email(request: GenerateRequest):
    """Generate a professional email."""
    try:
        return await _generate_stream("email", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/social-media")
async def generate_social_media(request: GenerateRequest):
    """Generate social media content."""
    try:
        return await _generate_stream("social_media", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ad-copy")
async def generate_ad_copy(request: GenerateRequest):
    """Generate advertising copy."""
    try:
        return await _generate_stream("ad_copy", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tweet-thread")
async def generate_tweet_thread(request: GenerateRequest):
    """Generate a Twitter thread."""
    try:
        return await _generate_stream("tweet_thread", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/resume")
async def generate_resume(request: GenerateRequest):
    """Generate a resume."""
    try:
        return await _generate_stream("resume", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cover-letter")
async def generate_cover_letter(request: GenerateRequest):
    """Generate a cover letter."""
    try:
        return await _generate_stream("cover_letter", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/youtube-script")
async def generate_youtube_script(request: GenerateRequest):
    """Generate a YouTube video script."""
    try:
        return await _generate_stream("youtube_script", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/product-description")
async def generate_product_description(request: GenerateRequest):
    """Generate a product description."""
    try:
        return await _generate_stream("product_desc", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/essay")
async def generate_essay(request: GenerateRequest):
    """Generate an essay."""
    try:
        return await _generate_stream("essay", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/code-explainer")
async def generate_code_explainer(request: GenerateRequest):
    """Generate code explanation."""
    try:
        return await _generate_stream("code_explainer", request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
