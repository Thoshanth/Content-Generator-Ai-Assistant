from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from enum import Enum

# ── Content Types ──────────────────────────────────────────────────────────
class ContentType(str, Enum):
    general         = "general"
    blog_post       = "blog_post"
    email           = "email"
    social_media    = "social_media"
    ad_copy         = "ad_copy"
    resume          = "resume"
    cover_letter    = "cover_letter"
    youtube_script  = "youtube_script"
    code_explainer  = "code_explainer"
    product_desc    = "product_desc"
    essay           = "essay"
    tweet_thread    = "tweet_thread"

# ── Tone Options ──────────────────────────────────────────────────────────
class Tone(str, Enum):
    professional = "professional"
    casual       = "casual"
    formal       = "formal"
    persuasive   = "persuasive"
    friendly     = "friendly"
    witty        = "witty"
    empathetic   = "empathetic"

# ── Output Length ──────────────────────────────────────────────────────────
class OutputLength(str, Enum):
    short  = "short"
    medium = "medium"
    long   = "long"
    auto   = "auto"

# ── Export Formats ────────────────────────────────────────────────────────
class ExportFormat(str, Enum):
    plain_text = "plain_text"
    markdown   = "markdown"
    html       = "html"

# ── Languages ─────────────────────────────────────────────────────────────
class Language(str, Enum):
    english    = "English"
    hindi      = "Hindi"
    telugu     = "Telugu"
    spanish    = "Spanish"
    french     = "French"
    german     = "German"
    portuguese = "Portuguese"
    arabic     = "Arabic"
    japanese   = "Japanese"
    chinese    = "Chinese (Simplified)"
    korean     = "Korean"

# ── Message History ───────────────────────────────────────────────────────
class MessageHistory(BaseModel):
    role: Literal["user", "assistant"]
    content: str

# ── Chat Request ──────────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000, description="User's input prompt")
    content_type: ContentType = Field(default=ContentType.general, description="Type of content to generate")
    tone: Tone = Field(default=Tone.professional, description="Tone of the response")
    length: OutputLength = Field(default=OutputLength.auto, description="Desired output length")
    language: Language = Field(default=Language.english, description="Output language")
    conversation_history: Optional[List[MessageHistory]] = Field(
        default=None,
        description="Previous conversation messages for context"
    )
    uploaded_text: Optional[str] = Field(None, max_length=15000, description="Text from uploaded document")
    user_id: Optional[str] = Field(default=None, description="User ID for tracking")
    regenerate: bool = Field(default=False, description="Regenerate with higher temperature")
    custom_instructions: Optional[str] = Field(None, max_length=1000, description="Additional custom instructions")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Write a professional email to reschedule a meeting",
                "content_type": "email",
                "tone": "professional",
                "length": "medium",
                "language": "English",
                "conversation_history": [],
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }

# ── Chat Response ─────────────────────────────────────────────────────────
class ChatResponse(BaseModel):
    content: str = Field(..., description="Generated AI content")
    provider: str = Field(..., description="Provider used (Groq, Gemini, NVIDIA NIM, Cerebras)")
    model: str = Field(..., description="Model that generated the content")
    word_count: int = Field(default=0, description="Number of words in response")
    char_count: int = Field(default=0, description="Number of characters in response")

    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "content": "Subject: Request to Reschedule Meeting\n\nDear [Name],\n\nI hope this email finds you well...",
                "provider": "Gemini",
                "model": "gemini-1.5-flash",
                "word_count": 150,
                "char_count": 850
            }
        }

# ── Generate Request (convenience endpoint) ───────────────────────────────
class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=4000)
    content_type: ContentType
    tone: Tone = Field(default=Tone.professional)
    length: OutputLength = Field(default=OutputLength.medium)
    language: Language = Field(default=Language.english)
    custom_instructions: Optional[str] = None
    uploaded_text: Optional[str] = None
    user_id: str

# ── Export Request ────────────────────────────────────────────────────────
class ExportRequest(BaseModel):
    content: str
    format: ExportFormat
    content_type: ContentType

# ── Export Response ───────────────────────────────────────────────────────
class ExportResponse(BaseModel):
    content: str
    format: ExportFormat
    word_count: int
    char_count: int

# ── PDF Export Request ────────────────────────────────────────────────────
class PdfExportRequest(BaseModel):
    content: str
    content_type: Literal["resume", "cover_letter"]
    candidate_name: Optional[str] = "Document"

# ── Follow-up Questions Request ───────────────────────────────────────────
class FollowUpRequest(BaseModel):
    content: str
    content_type: ContentType
    user_id: str

# ── Follow-up Questions Response ──────────────────────────────────────────
class FollowUpResponse(BaseModel):
    questions: List[str] = Field(..., description="List of 3-5 follow-up questions")
    content_type: ContentType

# ── Image Generation ──────────────────────────────────────────────────────
class ImageStyle(str, Enum):
    realistic = "realistic"
    artistic = "artistic"
    anime = "anime"
    digital_art = "digital_art"
    oil_painting = "oil_painting"
    watercolor = "watercolor"
    sketch = "sketch"
    cyberpunk = "cyberpunk"

class ImageRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=1000, description="Description of the image to generate")
    negative_prompt: Optional[str] = Field(None, max_length=500, description="What to avoid in the image")
    width: int = Field(default=512, ge=64, le=1024, description="Image width (must be multiple of 64)")
    height: int = Field(default=512, ge=64, le=1024, description="Image height (must be multiple of 64)")
    steps: int = Field(default=30, ge=10, le=50, description="Number of inference steps")
    guidance_scale: float = Field(default=7.5, ge=1.0, le=20.0, description="How closely to follow the prompt")
    style: Optional[ImageStyle] = Field(None, description="Style preset to apply")
    user_id: Optional[str] = Field(None, description="User ID for tracking")

    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "A beautiful sunset over mountains, peaceful landscape",
                "negative_prompt": "blurry, low quality, distorted",
                "width": 768,
                "height": 512,
                "steps": 30,
                "guidance_scale": 7.5,
                "style": "realistic",
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }

class ImageResponse(BaseModel):
    imageUrl: str = Field(..., description="URL to the generated image")
    prompt: str = Field(..., description="Prompt used for generation")
    modelUsed: str = Field(..., description="Model that generated the image")
    generationTime: float = Field(..., description="Time taken to generate in seconds")
    seed: Optional[int] = Field(None, description="Seed used for generation")
    parameters: Dict = Field(..., description="Generation parameters used")

    class Config:
        protected_namespaces = ()
        json_schema_extra = {
            "example": {
                "imageUrl": "/api/images/123e4567-e89b-12d3-a456-426614174000.png",
                "prompt": "A beautiful sunset over mountains, peaceful landscape, photorealistic, high quality",
                "modelUsed": "stable-diffusion-xl-1024-v1-0",
                "generationTime": 8.5,
                "seed": 42,
                "parameters": {
                    "width": 768,
                    "height": 512,
                    "steps": 30,
                    "guidance_scale": 7.5,
                    "style": "realistic"
                }
            }
        }
