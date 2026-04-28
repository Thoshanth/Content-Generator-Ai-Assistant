"""
Follow-up Questions Router
Handles bot-initiated follow-up questions where the AI asks the user for more information.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from services.followup_service import (
    should_ask_followup_questions,
    generate_bot_followup_questions,
    generate_followup_questions  # Keep for backward compatibility
)

router = APIRouter()


class FollowUpCheckRequest(BaseModel):
    """Request to check if bot should ask follow-up questions."""
    content_type: str
    user_message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    user_id: Optional[str] = ""


class FollowUpCheckResponse(BaseModel):
    """Response indicating if bot should ask follow-up questions."""
    should_ask: bool
    content_type: str
    reason: Optional[str] = ""


class BotFollowUpRequest(BaseModel):
    """Request for bot to generate follow-up questions to ask the user."""
    content_type: str
    user_message: str
    conversation_history: Optional[List[Dict[str, str]]] = []
    user_id: Optional[str] = ""


class BotFollowUpResponse(BaseModel):
    """Response with bot's follow-up message containing questions."""
    message: str
    content_type: str
    has_questions: bool


class FollowUpRequest(BaseModel):
    """Legacy request model for backward compatibility."""
    content_type: str
    initial_prompt: Optional[str] = ""
    user_id: Optional[str] = ""


class FollowUpResponse(BaseModel):
    """Legacy response model for backward compatibility."""
    questions: List[str]
    content_type: str


@router.post("/check", response_model=FollowUpCheckResponse)
async def check_should_ask_followup(request: FollowUpCheckRequest):
    """
    Check if the bot should ask follow-up questions based on user's message.
    
    This endpoint determines whether the AI should proactively ask for more information
    to create better content.
    
    Args:
        request: FollowUpCheckRequest with user message and context
    
    Returns:
        FollowUpCheckResponse indicating if bot should ask questions
    
    Example:
        POST /followup/check
        {
            "content_type": "resume",
            "user_message": "I need a resume",
            "conversation_history": [],
            "user_id": "user123"
        }
        
        Response:
        {
            "should_ask": true,
            "content_type": "resume",
            "reason": "Message is too brief for resume creation"
        }
    """
    try:
        should_ask = await should_ask_followup_questions(
            content_type=request.content_type,
            user_message=request.user_message,
            conversation_history=request.conversation_history
        )
        
        reason = ""
        if should_ask:
            if len(request.user_message.strip()) < 50:
                reason = "Message is too brief for detailed content creation"
            elif request.content_type in ['resume', 'cover_letter', 'blog_post']:
                reason = f"{request.content_type.replace('_', ' ').title()} requires detailed information"
            else:
                reason = "More information needed for quality content"
        else:
            reason = "Sufficient information provided or general chat"
        
        return FollowUpCheckResponse(
            should_ask=should_ask,
            content_type=request.content_type,
            reason=reason
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check follow-up requirements: {str(e)}"
        )


@router.post("/generate", response_model=BotFollowUpResponse)
async def generate_bot_followup(request: BotFollowUpRequest):
    """
    Generate follow-up questions that the bot will ask the user.
    
    This endpoint creates a conversational message where the AI asks the user
    specific questions to gather information for content creation.
    
    Args:
        request: BotFollowUpRequest with user message and context
    
    Returns:
        BotFollowUpResponse with formatted message containing questions
    
    Example:
        POST /followup/generate
        {
            "content_type": "resume",
            "user_message": "I need help with my resume",
            "conversation_history": [],
            "user_id": "user123"
        }
        
        Response:
        {
            "message": "I'd be happy to help you create a professional resume! To make sure I create the best possible resume for you, I need to gather some specific information:\n\n1. What is your full name and contact information?\n2. What is your current education level?\n...",
            "content_type": "resume",
            "has_questions": true
        }
    """
    try:
        message = await generate_bot_followup_questions(
            content_type=request.content_type,
            user_message=request.user_message,
            conversation_history=request.conversation_history,
            user_id=request.user_id
        )
        
        # Check if message contains questions (numbered items)
        has_questions = any(
            line.strip() and (line.strip()[0].isdigit() or line.strip().startswith('-'))
            for line in message.split('\n')
        )
        
        return BotFollowUpResponse(
            message=message,
            content_type=request.content_type,
            has_questions=has_questions
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate bot follow-up questions: {str(e)}"
        )


# Legacy endpoint for backward compatibility
@router.post("/questions", response_model=FollowUpResponse)
async def get_followup_questions(request: FollowUpRequest):
    """
    LEGACY: Generate follow-up questions (backward compatibility).
    
    This endpoint is kept for backward compatibility but is deprecated.
    Use /followup/generate for new implementations.
    """
    try:
        questions = await generate_followup_questions(
            content_type=request.content_type,
            initial_prompt=request.initial_prompt,
            user_id=request.user_id
        )
        
        return FollowUpResponse(
            questions=questions,
            content_type=request.content_type
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate follow-up questions: {str(e)}"
        )


@router.get("/templates/{content_type}")
async def get_question_templates(content_type: str):
    """
    Get template questions for a specific content type.
    
    Args:
        content_type: Type of content (resume, cover_letter, blog_post, etc.)
    
    Returns:
        Dictionary with content_type and list of template questions
    """
    from services.followup_service import generate_template_followup_message
    
    try:
        # Generate template message
        template_message = generate_template_followup_message(content_type, "")
        
        # Extract questions from template
        questions = []
        for line in template_message.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                question = line.lstrip('0123456789.-) ').strip()
                if question and len(question) > 10:
                    questions.append(question)
        
        return {
            "content_type": content_type,
            "questions": questions,
            "full_message": template_message
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get templates: {str(e)}"
        )
