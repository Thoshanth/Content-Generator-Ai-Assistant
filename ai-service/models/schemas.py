from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="User's input prompt")
    content_type: str = Field(default="general", description="Type of content to generate")
    conversation_history: Optional[List[Dict[str, str]]] = Field(
        default=None,
        description="Previous conversation messages for context"
    )
    user_id: Optional[str] = Field(default=None, description="User ID for tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a professional email to reschedule a meeting",
                "content_type": "email",
                "conversation_history": [],
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }

class ChatResponse(BaseModel):
    content: str = Field(..., description="Generated AI content")
    model_used: str = Field(..., description="Model that generated the content")
    tokens_used: int = Field(..., description="Number of tokens consumed")

    class Config:
        protected_namespaces = ()  # Fix Pydantic warning
        json_schema_extra = {
            "example": {
                "content": "Subject: Request to Reschedule Meeting\n\nDear [Name],\n\nI hope this email finds you well...",
                "model_used": "meta-llama/llama-3.2-3b-instruct:free",
                "tokens_used": 342
            }
        }
