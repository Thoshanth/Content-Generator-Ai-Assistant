# AI Service — Full Implementation Plan (v5.0)
## Python FastAPI · Smart Model Routing · 4 Providers · Streaming · PDF Export · Dynamic Follow-ups

---

## What's New in v5.0

| Feature | Details |
|---|---|
| 4 AI Providers | Groq, Gemini, Together AI, DeepSeek |
| Smart Model Routing | Each content type gets its best-fit model |
| DeepSeek Universal Fallback | Final fallback for ALL content types |
| Per-provider free models | Specific free-tier model IDs listed |
| PDF Export (Client-side) | html2pdf.js — Resume + Cover Letter |
| PDF Export (Server-side) | Python WeasyPrint endpoint as backup |
| Resume PDF Template | Professionally styled HTML → PDF |
| Dynamic Follow-up Questions | Auto-generated after every response + manual refresh |

---

## Model Provider Overview

| Provider | Best At | Free Model | API Base |
|---|---|---|---|
| **Groq** | Speed, casual/creative content, chat | `llama-3.1-8b-instant` | `https://api.groq.com/openai/v1` |
| **Gemini** | Structured long-form, emails, essays | `gemini-1.5-flash` | `https://generativelanguage.googleapis.com/v1beta/openai` |
| **Together AI** | Technical, resume, code, reasoning | `meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo` | `https://api.together.xyz/v1` |
| **DeepSeek** | Deep reasoning, universal fallback | `deepseek-chat` | `https://api.deepseek.com/v1` |

> All 4 providers expose an **OpenAI-compatible API** — same request format, just different base URLs and keys. This makes the client code clean and unified.

---

## Smart Model Routing Table

This is the core of v4.0 — every content type gets a primary model + ordered fallback chain based on what that content type needs.

```
Content Type       Primary      Fallback 1    Fallback 2    Final Fallback
─────────────────────────────────────────────────────────────────────────
general            Groq         Gemini        Together      DeepSeek
blog_post          Gemini       Groq          Together      DeepSeek
email              Gemini       Groq          DeepSeek      Together
social_media       Groq         Gemini        Together      DeepSeek
ad_copy            Groq         Gemini        DeepSeek      Together
tweet_thread       Groq         Gemini        Together      DeepSeek
resume             Together     DeepSeek      Gemini        Groq
cover_letter       Gemini       Together      DeepSeek      Groq
youtube_script     Gemini       Groq          Together      DeepSeek
product_desc       Groq         Gemini        Together      DeepSeek
essay              Gemini       Together      DeepSeek      Groq
code_explainer     Together     DeepSeek      Gemini        Groq
```

### Routing Logic Explained

**Groq (Primary for: general, social, ad copy, tweet thread, product desc)**
- Fastest response time — ideal for short, punchy content
- Low latency streaming feels most "real-time" to the user
- Free tier: generous RPM limits
- `llama-3.1-8b-instant` is strong at creative, conversational output

**Gemini (Primary for: blog post, email, cover letter, YouTube script, essay)**
- Excellent at structured, multi-section long-form content
- Follows formatting instructions reliably
- Strong at professional writing tone
- `gemini-1.5-flash` handles long outputs without truncation

**Together AI (Primary for: resume, code explainer)**
- Best free reasoning model for structured technical content
- Resume requires precise formatting + ATS-awareness
- Code explanation needs accurate technical understanding
- Handles complex multi-part output well

**DeepSeek (Universal Final Fallback)**
- Most capable reasoning of the 4 free tiers
- Never used as primary (save capacity for when others fail)
- Handles any content type reliably
- `deepseek-chat` is free tier with solid context window

---

## Full Folder Structure

```
ai-service/
├── main.py
├── routers/
│   ├── chat.py                      # /chat/stream
│   ├── generate.py                  # /generate/* convenience endpoints
│   └── tools.py                     # /tools/export, /tools/export-pdf
├── services/
│   ├── model_router.py              # ★ NEW — smart routing logic
│   ├── ai_client.py                 # ★ NEW — unified multi-provider client
│   ├── streaming.py                 # ★ NEW — streaming handler (replaces openrouter.py)
│   ├── post_processor.py            # Clean/format raw LLM output
│   ├── file_extractor.py            # Extract text from PDF/DOCX/TXT
│   ├── pdf_exporter.py              # ★ NEW — server-side PDF via WeasyPrint
│   └── export_service.py            # plain text / HTML / markdown conversion
├── prompts/
│   ├── templates.py                 # System prompts per content type
│   ├── tone_modifiers.py            # Tone + length injectors
│   └── pdf_templates.py             # ★ NEW — HTML templates for PDF export
├── models/
│   └── schemas.py                   # All Pydantic models
├── utils/
│   └── text_utils.py
├── requirements.txt
├── .env
└── Dockerfile
```

---

## SECTION 1 — Environment Variables (`.env`)

```env
# ── Groq ──────────────────────────────
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.1-8b-instant

# ── Gemini ────────────────────────────
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
GEMINI_MODEL=gemini-1.5-flash

# ── Together AI ───────────────────────
TOGETHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
TOGETHER_BASE_URL=https://api.together.xyz/v1
TOGETHER_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo

# ── DeepSeek ──────────────────────────
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat

# ── App ───────────────────────────────
YOUR_SITE_URL=http://localhost:5173
FRONTEND_URL=https://your-app.vercel.app
BACKEND_URL=https://your-backend.onrender.com
```

---

## SECTION 2 — Model Router (`services/model_router.py`)

This is the brain of the routing system. Given a content type, it returns the ordered list of providers to try.

```python
from dataclasses import dataclass
from typing import List
import os

@dataclass
class ProviderConfig:
    name: str           # Human label for logs
    api_key: str
    base_url: str
    model: str

# ── Load all 4 provider configs from env ──────────────────────────────────────
def _load_providers() -> dict[str, ProviderConfig]:
    return {
        "groq": ProviderConfig(
            name="Groq",
            api_key=os.getenv("GROQ_API_KEY", ""),
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        ),
        "gemini": ProviderConfig(
            name="Gemini",
            api_key=os.getenv("GEMINI_API_KEY", ""),
            base_url=os.getenv("GEMINI_BASE_URL",
                               "https://generativelanguage.googleapis.com/v1beta/openai"),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        ),
        "together": ProviderConfig(
            name="Together AI",
            api_key=os.getenv("TOGETHER_API_KEY", ""),
            base_url=os.getenv("TOGETHER_BASE_URL", "https://api.together.xyz/v1"),
            model=os.getenv("TOGETHER_MODEL",
                            "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo")
        ),
        "deepseek": ProviderConfig(
            name="DeepSeek",
            api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            base_url=os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"),
            model=os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        ),
    }

# ── Routing table — content type → ordered provider keys ─────────────────────
#    First = primary, Last = final fallback (always deepseek)
ROUTING_TABLE: dict[str, List[str]] = {
    "general":        ["groq",    "gemini",  "together", "deepseek"],
    "blog_post":      ["gemini",  "groq",    "together", "deepseek"],
    "email":          ["gemini",  "groq",    "deepseek", "together"],
    "social_media":   ["groq",    "gemini",  "together", "deepseek"],
    "ad_copy":        ["groq",    "gemini",  "deepseek", "together"],
    "tweet_thread":   ["groq",    "gemini",  "together", "deepseek"],
    "resume":         ["together","deepseek","gemini",   "groq"    ],
    "cover_letter":   ["gemini",  "together","deepseek", "groq"    ],
    "youtube_script": ["gemini",  "groq",    "together", "deepseek"],
    "product_desc":   ["groq",    "gemini",  "together", "deepseek"],
    "essay":          ["gemini",  "together","deepseek", "groq"    ],
    "code_explainer": ["together","deepseek","gemini",   "groq"    ],
}

def get_provider_chain(content_type: str) -> List[ProviderConfig]:
    """
    Returns ordered list of ProviderConfig for the given content type.
    Always ends with DeepSeek as the universal final fallback.
    """
    providers = _load_providers()
    order = ROUTING_TABLE.get(content_type, ROUTING_TABLE["general"])
    return [providers[key] for key in order if providers[key].api_key]
```

---

## SECTION 3 — Unified AI Client (`services/ai_client.py`)

All 4 providers use the OpenAI-compatible format. One client, 4 providers.

```python
import httpx
import json
from typing import AsyncGenerator
from services.model_router import ProviderConfig


async def stream_from_provider(
    provider: ProviderConfig,
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 2500
) -> AsyncGenerator[str, None]:
    """
    Stream from a single provider using OpenAI-compatible /chat/completions.
    Yields raw SSE lines as strings.
    Raises exception on HTTP error or connection failure (caller tries next provider).
    """
    headers = {
        "Authorization": f"Bearer {provider.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": provider.model,
        "messages": messages,
        "stream": True,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
    }

    async with httpx.AsyncClient(timeout=90.0) as client:
        async with client.stream(
            "POST",
            f"{provider.base_url}/chat/completions",
            headers=headers,
            json=payload
        ) as response:

            if response.status_code == 429:
                raise RateLimitError(f"{provider.name} rate limited")
            if response.status_code != 200:
                body = await response.aread()
                raise ProviderError(
                    f"{provider.name} HTTP {response.status_code}: {body.decode()[:200]}"
                )

            async for line in response.aiter_lines():
                yield line


class RateLimitError(Exception):
    pass

class ProviderError(Exception):
    pass
```

---

## SECTION 4 — Streaming Orchestrator (`services/streaming.py`)

Replaces the old `openrouter.py`. Orchestrates provider chain, fallback logic, and SSE output.

```python
import json
from typing import AsyncGenerator
from services.model_router import get_provider_chain
from services.ai_client import stream_from_provider, RateLimitError, ProviderError
from prompts.templates import get_system_prompt
from prompts.tone_modifiers import build_modifiers


def build_messages(
    prompt: str, content_type: str, tone: str, length: str,
    language: str, history: list,
    uploaded_text: str = None,
    custom_instructions: str = None
) -> list:
    system = get_system_prompt(content_type)
    modifiers = build_modifiers(tone, length, language)
    full_system = f"{system}\n\n---\n{modifiers}"

    if custom_instructions:
        full_system += f"\n\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}"

    messages = [{"role": "system", "content": full_system}]

    # Last 5 exchanges = 10 messages kept as context window
    recent = history[-10:] if len(history) > 10 else history
    for msg in recent:
        messages.append({"role": msg.role, "content": msg.content})

    user_content = prompt
    if uploaded_text:
        user_content = (
            f"Document provided by user:\n\n"
            f"--- DOCUMENT START ---\n{uploaded_text[:12000]}\n--- DOCUMENT END ---\n\n"
            f"User request: {prompt}"
        )

    messages.append({"role": "user", "content": user_content})
    return messages


async def stream_response(
    prompt: str,
    content_type: str,
    tone: str = "professional",
    length: str = "auto",
    language: str = "English",
    history: list = None,
    uploaded_text: str = None,
    custom_instructions: str = None,
    user_id: str = "",
    regenerate: bool = False
) -> AsyncGenerator[str, None]:

    if history is None:
        history = []

    messages = build_messages(
        prompt, content_type, tone, length,
        language, history, uploaded_text, custom_instructions
    )

    temperature = 0.9 if regenerate else 0.7
    provider_chain = get_provider_chain(content_type)

    for attempt, provider in enumerate(provider_chain):
        try:
            full_content = ""

            # Yield provider metadata as first SSE event
            yield f"data: {json.dumps({'provider': provider.name, 'model': provider.model, 'attempt': attempt + 1})}\n\n"

            async for line in stream_from_provider(provider, messages, temperature):
                if not line.startswith("data: "):
                    continue
                data = line[6:].strip()

                if data == "[DONE]":
                    # Final metadata event: word + char count
                    yield f"data: {json.dumps({'done': True, 'word_count': len(full_content.split()), 'char_count': len(full_content)})}\n\n"
                    return

                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        full_content += delta
                        yield f"data: {json.dumps({'delta': delta})}\n\n"
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

            # Stream ended without [DONE] — treat as success
            if full_content:
                yield f"data: {json.dumps({'done': True, 'word_count': len(full_content.split()), 'char_count': len(full_content)})}\n\n"
                return

        except RateLimitError:
            print(f"[{provider.name}] Rate limited — trying next provider")
            yield f"data: {json.dumps({'info': f'{provider.name} rate limited, switching provider...'})}\n\n"
            continue

        except ProviderError as e:
            print(f"[{provider.name}] Provider error: {e}")
            continue

        except Exception as e:
            print(f"[{provider.name}] Unexpected error: {e}")
            continue

    # All providers exhausted
    yield f"data: {json.dumps({'error': 'All AI providers are currently unavailable. Please try again in a moment.', 'done': True})}\n\n"
```

---

## SECTION 5 — PDF Templates (`prompts/pdf_templates.py`)

HTML templates used by both client-side (html2pdf.js) and server-side (WeasyPrint) PDF export.

```python
RESUME_PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Georgia', 'Times New Roman', serif;
    font-size: 11pt;
    color: #1a1a1a;
    line-height: 1.5;
    padding: 40px 50px;
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
  }}
  h1 {{
    font-size: 22pt;
    font-weight: bold;
    color: #1D3557;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}
  .contact-line {{
    font-size: 9pt;
    color: #555;
    margin-bottom: 18px;
    border-bottom: 2px solid #1D3557;
    padding-bottom: 10px;
  }}
  h2 {{
    font-size: 11pt;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #1D3557;
    border-bottom: 1px solid #1D3557;
    padding-bottom: 3px;
    margin-top: 18px;
    margin-bottom: 8px;
  }}
  h3 {{
    font-size: 10.5pt;
    font-weight: bold;
    color: #1a1a1a;
    margin-bottom: 1px;
  }}
  .job-meta {{
    font-size: 9.5pt;
    color: #555;
    font-style: italic;
    margin-bottom: 4px;
  }}
  ul {{
    padding-left: 16px;
    margin-bottom: 8px;
  }}
  li {{
    margin-bottom: 3px;
    font-size: 10.5pt;
  }}
  p {{
    font-size: 10.5pt;
    margin-bottom: 6px;
  }}
  .skills-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
    font-size: 10.5pt;
  }}
  strong {{ color: #1D3557; }}
</style>
</head>
<body>
{content}
</body>
</html>
"""

COVER_LETTER_PDF_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    color: #1a1a1a;
    line-height: 1.8;
    padding: 60px 70px;
    max-width: 800px;
    margin: 0 auto;
    background: #fff;
  }}
  .header {{
    margin-bottom: 30px;
  }}
  .sender-info {{
    font-size: 10pt;
    color: #444;
    margin-bottom: 20px;
  }}
  .date {{
    color: #666;
    margin-bottom: 20px;
    font-size: 10.5pt;
  }}
  .recipient {{
    margin-bottom: 25px;
    font-size: 10.5pt;
  }}
  p {{
    margin-bottom: 16px;
    font-size: 11pt;
  }}
  .salutation {{
    font-weight: bold;
    margin-bottom: 16px;
  }}
  .closing {{
    margin-top: 24px;
  }}
  strong {{ color: #1D3557; }}
  hr {{
    border: none;
    border-top: 1px solid #ddd;
    margin: 20px 0;
  }}
</style>
</head>
<body>
{content}
</body>
</html>
"""

def get_pdf_template(content_type: str) -> str:
    templates = {
        "resume": RESUME_PDF_TEMPLATE,
        "cover_letter": COVER_LETTER_PDF_TEMPLATE,
    }
    return templates.get(content_type, COVER_LETTER_PDF_TEMPLATE)
```

---

## SECTION 6 — PDF Exporter Service (`services/pdf_exporter.py`)

Server-side PDF generation using WeasyPrint. Called by `/tools/export-pdf` endpoint.

```python
import markdown as md
from weasyprint import HTML, CSS
from prompts.pdf_templates import get_pdf_template
from io import BytesIO


def markdown_to_pdf_bytes(markdown_content: str, content_type: str) -> bytes:
    """
    Convert markdown AI output → styled HTML → PDF bytes.
    Returns raw PDF bytes for streaming to client.
    """
    # Step 1: markdown → HTML body
    html_body = md.markdown(
        markdown_content,
        extensions=["extra", "nl2br", "sane_lists"]
    )

    # Step 2: Inject into styled template
    template = get_pdf_template(content_type)
    full_html = template.format(content=html_body)

    # Step 3: WeasyPrint renders HTML → PDF
    pdf_bytes = BytesIO()
    HTML(string=full_html).write_pdf(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.read()
```

---

## SECTION 7 — Tools Router with PDF Endpoint (`routers/tools.py`)

```python
from fastapi import APIRouter
from fastapi.responses import Response
from models.schemas import ExportRequest, ExportResponse, PdfExportRequest
from services.export_service import to_plain_text, to_html, to_markdown
from services.pdf_exporter import markdown_to_pdf_bytes
from utils.text_utils import word_count, char_count

router = APIRouter(prefix="/tools", tags=["tools"])


@router.post("/export", response_model=ExportResponse)
async def export_content(req: ExportRequest):
    """Convert AI markdown output to requested text format."""
    if req.format == "plain_text":
        converted = to_plain_text(req.content)
    elif req.format == "html":
        converted = to_html(req.content)
    else:
        converted = to_markdown(req.content)

    return ExportResponse(
        content=converted,
        format=req.format,
        word_count=word_count(converted),
        char_count=char_count(converted)
    )


@router.post("/export-pdf")
async def export_pdf(req: PdfExportRequest):
    """
    Convert AI markdown output to a downloadable PDF.
    Used for Resume and Cover Letter.
    Returns PDF bytes with correct headers for browser download.
    """
    pdf_bytes = markdown_to_pdf_bytes(req.content, req.content_type)

    filename_map = {
        "resume":       "resume.pdf",
        "cover_letter": "cover_letter.pdf",
    }
    filename = filename_map.get(req.content_type, "document.pdf")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
            "Content-Length": str(len(pdf_bytes))
        }
    )
```

---

## SECTION 8 — Updated Schemas (`models/schemas.py`)

```python
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum

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

class Tone(str, Enum):
    professional = "professional"
    casual       = "casual"
    formal       = "formal"
    persuasive   = "persuasive"
    friendly     = "friendly"
    witty        = "witty"
    empathetic   = "empathetic"

class OutputLength(str, Enum):
    short  = "short"
    medium = "medium"
    long   = "long"
    auto   = "auto"

class ExportFormat(str, Enum):
    plain_text = "plain_text"
    markdown   = "markdown"
    html       = "html"

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

class MessageHistory(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    prompt: str                    = Field(..., min_length=1, max_length=4000)
    content_type: ContentType      = ContentType.general
    tone: Tone                     = Tone.professional
    length: OutputLength           = OutputLength.auto
    language: Language             = Language.english
    conversation_history: List[MessageHistory] = []
    uploaded_text: Optional[str]   = Field(None, max_length=15000)
    user_id: str
    regenerate: bool               = False
    custom_instructions: Optional[str] = None

class GenerateRequest(BaseModel):
    prompt: str                    = Field(..., min_length=1, max_length=4000)
    content_type: ContentType
    tone: Tone                     = Tone.professional
    length: OutputLength           = OutputLength.medium
    language: Language             = Language.english
    custom_instructions: Optional[str] = None
    uploaded_text: Optional[str]   = None
    user_id: str

class ExportRequest(BaseModel):
    content: str
    format: ExportFormat
    content_type: ContentType

# ★ NEW — for PDF export
class PdfExportRequest(BaseModel):
    content: str
    content_type: Literal["resume", "cover_letter"]
    candidate_name: Optional[str] = "Document"   # used in PDF filename

class ExportResponse(BaseModel):
    content: str
    format: ExportFormat
    word_count: int
    char_count: int
```

---

## SECTION 9 — React PDF Download (Client-side)

Two approaches in the frontend — both implemented, user gets the best one available.

### Approach A — Client-side html2pdf.js (Primary)

Fast, no server round-trip. Works offline. Renders exactly what user sees.

```javascript
// src/hooks/usePdfExport.js
import html2pdf from 'html2pdf.js'

export function usePdfExport() {
  const [exporting, setExporting] = useState(false)

  const downloadAsPdf = async (markdownContent, contentType, candidateName = 'document') => {
    setExporting(true)
    try {
      // Convert markdown to HTML first
      const { marked } = await import('marked')
      const htmlBody = marked.parse(markdownContent)

      // Style based on content type
      const styles = contentType === 'resume'
        ? RESUME_STYLES
        : COVER_LETTER_STYLES

      const fullHtml = `
        <div style="${styles}">
          ${htmlBody}
        </div>
      `

      const element = document.createElement('div')
      element.innerHTML = fullHtml
      document.body.appendChild(element)

      await html2pdf()
        .set({
          margin: [15, 20, 15, 20],        // top, right, bottom, left (mm)
          filename: `${candidateName.replace(/\s+/g, '_')}_${contentType}.pdf`,
          image: { type: 'jpeg', quality: 0.98 },
          html2canvas: { scale: 2, useCORS: true },
          jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
        })
        .from(element)
        .save()

      document.body.removeChild(element)
    } finally {
      setExporting(false)
    }
  }

  return { exporting, downloadAsPdf }
}

// Inline styles injected into PDF
const RESUME_STYLES = `
  font-family: Georgia, 'Times New Roman', serif;
  font-size: 11pt;
  color: #1a1a1a;
  line-height: 1.5;
  padding: 0;
  max-width: 100%;
`

const COVER_LETTER_STYLES = `
  font-family: -apple-system, Helvetica Neue, Arial, sans-serif;
  font-size: 11pt;
  color: #1a1a1a;
  line-height: 1.8;
  padding: 0;
`
```

### Approach B — Server-side WeasyPrint (Fallback / Higher Quality)

Called when user wants higher-fidelity PDF with exact template styling.

```javascript
// In the Download button component
const downloadServerPdf = async (content, contentType, candidateName) => {
  setExporting(true)
  try {
    const { data: { session } } = await supabase.auth.getSession()

    const response = await fetch(`${API_BASE}/tools/export-pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.access_token}`
      },
      body: JSON.stringify({
        content,
        content_type: contentType,
        candidate_name: candidateName
      })
    })

    // Stream PDF bytes → trigger browser download
    const blob = await response.blob()
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${candidateName}_${contentType}.pdf`
    a.click()
    URL.revokeObjectURL(url)
  } finally {
    setExporting(false)
  }
}
```

### Download Button UI (Resume / Cover Letter responses only)

```jsx
// Shown only when content_type is resume or cover_letter
{(contentType === 'resume' || contentType === 'cover_letter') && (
  <div className="flex gap-2 mt-3">

    {/* Primary: client-side fast download */}
    <button
      onClick={() => downloadAsPdf(content, contentType, userName)}
      disabled={exporting}
      className="flex items-center gap-2 px-4 py-2 bg-primary-500
                 text-white rounded-lg text-sm font-medium
                 hover:bg-primary-600 transition-colors"
    >
      {exporting
        ? <Spinner size="sm" />
        : <DownloadIcon size={14} />
      }
      Download PDF
    </button>

    {/* Secondary: server-side higher quality */}
    <button
      onClick={() => downloadServerPdf(content, contentType, userName)}
      className="flex items-center gap-2 px-4 py-2 border border-primary-500
                 text-primary-500 rounded-lg text-sm font-medium
                 hover:bg-primary-50 transition-colors"
    >
      <FileTextIcon size={14} />
      High Quality PDF
    </button>

  </div>
)}
```

---

## SECTION 10 — Clipboard Copy (ChatGPT / Claude Style)

### 3 Copy Buttons on Every AI Response

```
┌────────────────────────────────────────────────────┐
│  AI Response Bubble                                │
│  ──────────────────────────────────────────────   │
│  # Blog Post Title                                 │
│  ## Introduction                                   │
│  Lorem ipsum...                                    │
│                                                    │
│  [📋 Copy]  [📄 Plain Text]  [🌐 Rich Copy]       │
│  [🔊 Read Aloud]  [🔄 Regenerate]                 │
│                                                    │
│  📊 Words: 482  •  Chars: 2,841  •  via Gemini    │
└────────────────────────────────────────────────────┘
```

### Copy Hook (`src/hooks/useClipboard.js`)

```javascript
export function useClipboard() {
  const [copiedId, setCopiedId] = useState(null)

  // ── Copy 1: Raw markdown (default — like ChatGPT)
  // Pastes into Notion, VS Code, GitHub — preserves # ** etc.
  const copyMarkdown = async (content, id) => {
    await navigator.clipboard.writeText(content)
    flash(id)
  }

  // ── Copy 2: Plain text (strips all markdown symbols)
  // Pastes into WhatsApp, SMS, plain email body — no symbols
  const copyPlainText = async (content, contentType, id) => {
    const res = await apiPost('/tools/export', {
      content, format: 'plain_text', content_type: contentType
    })
    await navigator.clipboard.writeText(res.content)
    flash(id + '-plain')
  }

  // ── Copy 3: Rich HTML copy (like Claude's copy button)
  // Pastes into Gmail / Outlook / Notion with FULL formatting:
  // bold subject lines, bullet points, headings — everything preserved
  // Uses ClipboardItem to write text/html + text/plain simultaneously
  const copyRichHtml = async (content, contentType, id) => {
    const res = await apiPost('/tools/export', {
      content, format: 'html', content_type: contentType
    })

    try {
      // Modern API — writes both html and plaintext
      // So paste works in rich editors AND plain text fields
      const item = new ClipboardItem({
        'text/html':  new Blob([res.content], { type: 'text/html' }),
        'text/plain': new Blob([content],     { type: 'text/plain' })
      })
      await navigator.clipboard.write([item])
    } catch {
      // Fallback for browsers that don't support ClipboardItem
      await navigator.clipboard.writeText(content)
    }
    flash(id + '-html')
  }

  const flash = (id) => {
    setCopiedId(id)
    setTimeout(() => setCopiedId(null), 2000)
  }

  return { copiedId, copyMarkdown, copyPlainText, copyRichHtml }
}
```

### Read Aloud (Free — Browser Web Speech API)

```javascript
// src/hooks/useTextToSpeech.js
export function useTextToSpeech() {
  const [speaking, setSpeaking] = useState(false)

  const speak = (markdownText) => {
    // Strip markdown before reading aloud
    const plain = markdownText
      .replace(/#{1,6}\s/g, '')       // remove headers
      .replace(/\*\*(.+?)\*\*/g, '$1') // remove bold
      .replace(/\*(.+?)\*/g, '$1')     // remove italic
      .replace(/`(.+?)`/g, '$1')       // remove inline code
      .replace(/```[\s\S]*?```/g, '')  // remove code blocks
      .replace(/\[(.+?)\]\(.+?\)/g, '$1') // remove links
      .replace(/[-*]{3,}/g, '')        // remove hr
      .replace(/\n+/g, ' ')
      .trim()

    const utterance = new SpeechSynthesisUtterance(plain)
    utterance.rate  = 0.95
    utterance.pitch = 1.0
    utterance.lang  = 'en-US'

    utterance.onstart = () => setSpeaking(true)
    utterance.onend   = () => setSpeaking(false)
    utterance.onerror = () => setSpeaking(false)

    window.speechSynthesis.cancel() // stop any current speech
    window.speechSynthesis.speak(utterance)
  }

  const stop = () => {
    window.speechSynthesis.cancel()
    setSpeaking(false)
  }

  return { speaking, speak, stop }
}
```

---

## SECTION 11 — Provider Info on Every Response

The frontend receives the provider name + model in the first SSE event. Show it as a small badge on the response bubble.

```javascript
// SSE first event contains:
// { "provider": "Gemini", "model": "gemini-1.5-flash", "attempt": 1 }

// If fallback was used:
// { "provider": "DeepSeek", "model": "deepseek-chat", "attempt": 3 }
// Also: { "info": "Gemini rate limited, switching provider..." }
```

```jsx
// Provider badge on response bubble
<span className="text-xs text-gray-400 flex items-center gap-1">
  <SparklesIcon size={10} />
  {providerName} · {modelName}
  {attempt > 1 && (
    <span className="text-orange-400 ml-1">
      (fallback #{attempt})
    </span>
  )}
</span>
```

---

## SECTION 12 — Complete API Endpoint Reference

| Method | Endpoint | Provider Used | Description |
|---|---|---|---|
| GET | `/health` | — | Service status |
| POST | `/chat/stream` | Smart routing | Main chat with history |
| POST | `/generate/blog-post` | Gemini primary | Blog generation |
| POST | `/generate/email` | Gemini primary | Email generation |
| POST | `/generate/social-media` | Groq primary | All 4 platforms |
| POST | `/generate/ad-copy` | Groq primary | Multi-version ads |
| POST | `/generate/resume` | Together primary | Resume writing |
| POST | `/generate/cover-letter` | Gemini primary | Cover letter |
| POST | `/generate/youtube-script` | Gemini primary | Full YT script |
| POST | `/generate/tweet-thread` | Groq primary | Twitter thread |
| POST | `/generate/product-description` | Groq primary | Product copy |
| POST | `/generate/essay` | Gemini primary | Academic essay |
| POST | `/generate/code-explainer` | Together primary | Code docs |
| POST | `/tools/export` | — | Format conversion |
| POST | `/tools/export-pdf` | — | Resume/CL → PDF |

---

## SECTION 13 — Requirements (`requirements.txt`)

```
fastapi==0.111.0
uvicorn[standard]==0.30.0
httpx==0.27.0
pydantic==2.7.0
python-dotenv==1.0.1
PyPDF2==3.0.1
python-docx==1.1.2
python-multipart==0.0.9
markdown==3.6
weasyprint==62.3
```

> **WeasyPrint system dependencies** (needed on Ubuntu/Render):
> ```bash
> apt-get install -y libpango-1.0-0 libpangoft2-1.0-0 libpangocairo-1.0-0 \
>   libcairo2 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
> ```
> Add a `render.yaml` or `Dockerfile` with these apt installs for deployment.

---

## SECTION 14 — Feature Summary

| Feature | Implementation | Free? |
|---|---|---|
| 12 content types | Per-type system prompts + structured output | ✅ |
| Smart model routing | 4 providers, per-type primary + fallback chain | ✅ |
| DeepSeek universal fallback | Always last resort for all types | ✅ |
| Word-by-word streaming | SSE, all 4 providers | ✅ |
| Tone selector (7 options) | Prompt injection modifier | ✅ |
| Length control (4 options) | Prompt injection modifier | ✅ |
| 11 languages | Prompt injection modifier | ✅ |
| Regenerate response | Higher temperature re-run | ✅ |
| Copy as markdown | navigator.clipboard.writeText | ✅ |
| Copy as plain text | Strip markdown via /tools/export | ✅ |
| Copy as rich HTML | ClipboardItem text/html + text/plain | ✅ |
| Read aloud | Browser Web Speech API | ✅ |
| File upload (PDF/DOCX/TXT) | PyPDF2 + python-docx extraction | ✅ |
| Resume PDF download | html2pdf.js client-side | ✅ |
| Resume PDF (high quality) | WeasyPrint server-side | ✅ |
| Cover letter PDF | Same as resume | ✅ |
| Provider badge on response | First SSE event metadata | ✅ |
| Fallback notification | SSE info event shown in UI | ✅ |
| Word + char count | Sent in done SSE event | ✅ |
| Post-processor | Clean markdown output before stream | ✅ |
| Dynamic follow-up questions | Auto after response + manual refresh, 3 chips | ✅ |

---

## SECTION 15 — Dynamic Follow-up Questions

### How It Works

```
User sends prompt → AI streams response
                          ↓
            Response streaming completes (done: true)
                          ↓
        Frontend fires /chat/followups (non-blocking)
        Groq generates 3 contextual follow-up questions
        based on: content_type + original prompt + AI response
                          ↓
        3 clickable chips appear below the response bubble
        + a 🔄 refresh icon to generate 3 new ones
                          ↓
        User clicks chip → auto-fills input bar → sends as new message
```

### Why Groq for Follow-ups

- Groq (`llama-3.1-8b-instant`) is the fastest provider — sub-second response
- Follow-up generation is a lightweight task — no big model needed
- Runs in parallel after streaming completes — no delay for user
- Uses a strict JSON-only system prompt so parsing is reliable

---

### Backend — Follow-up Schema (add to `models/schemas.py`)

```python
class FollowupRequest(BaseModel):
    original_prompt: str           # what the user originally asked
    ai_response: str               # the full AI response (truncated to 1000 chars)
    content_type: ContentType      # blog_post, email, resume, etc.
    user_id: str

class FollowupResponse(BaseModel):
    questions: List[str]           # always exactly 3 strings
```

---

### Backend — Follow-up Prompts (`prompts/followup_prompts.py`)

Each content type gets a tailored instruction so follow-ups are genuinely useful,
not generic. The model is forced to return pure JSON — no markdown, no preamble.

```python
# Base system prompt — strict JSON output
FOLLOWUP_SYSTEM = """You are a helpful AI assistant that suggests follow-up actions.

Given a user's original request and an AI-generated response, suggest exactly 3
short follow-up questions or actions the user might want to do next.

RULES:
- Each question must be SHORT — under 12 words
- Questions must be directly relevant to what was just generated
- Questions should feel like natural next steps, not generic
- Make them feel like they come from a smart colleague
- Return ONLY valid JSON. No explanation, no markdown, no preamble.

OUTPUT FORMAT (strict):
{"questions": ["question 1", "question 2", "question 3"]}"""


# Per content type example follow-ups (shown to model as few-shot examples)
FOLLOWUP_EXAMPLES: dict[str, list[str]] = {
    "blog_post": [
        "Turn this into a LinkedIn post",
        "Write a shorter summary version",
        "Add an FAQ section at the end",
        "Make it more SEO optimized",
        "Create a tweet thread from this blog",
        "Add statistics and data points",
    ],
    "email": [
        "Make this more formal",
        "Add an apology paragraph",
        "Write a follow-up if no reply in 3 days",
        "Make the subject line more compelling",
        "Shorten this to under 100 words",
        "Add a meeting scheduling request",
    ],
    "social_media": [
        "Make the LinkedIn version longer",
        "Generate 3 alternative hook lines",
        "Add more relevant hashtags",
        "Rewrite for a younger audience",
        "Create a story/reel caption version",
        "Make the Twitter version more punchy",
    ],
    "ad_copy": [
        "Write a version targeting seniors",
        "Make a more urgent version",
        "Create a Black Friday variant",
        "Write a Google Ads version",
        "Generate 3 alternative headlines",
        "Make a softer, trust-building version",
    ],
    "resume": [
        "Improve the professional summary",
        "Make bullets more achievement-focused",
        "Write a matching cover letter",
        "Optimize this for ATS systems",
        "Add more quantified achievements",
        "Tailor this for a senior role",
    ],
    "cover_letter": [
        "Make this more concise",
        "Add a stronger opening hook",
        "Write a version for a career change",
        "Make it sound more confident",
        "Generate a follow-up email version",
        "Tailor this for a startup company",
    ],
    "youtube_script": [
        "Write a shorter 3-minute version",
        "Generate a video description for YouTube",
        "Create a thumbnail text and title",
        "Write a pinned comment for this video",
        "Generate 10 tags for this video",
        "Make the hook more dramatic",
    ],
    "tweet_thread": [
        "Make the hook tweet more shocking",
        "Add one more tweet with a case study",
        "Write a LinkedIn post from this thread",
        "Create a shorter 5-tweet version",
        "Add a tweet with actionable tips",
        "Rewrite for a business audience",
    ],
    "product_desc": [
        "Write a version for Amazon listing",
        "Make it target a younger demographic",
        "Add more emotional trigger words",
        "Create a shorter product card version",
        "Write a comparison vs competitors",
        "Make it more luxury/premium sounding",
    ],
    "essay": [
        "Add more supporting evidence",
        "Write a counter-argument section",
        "Make the conclusion more powerful",
        "Summarize this into an abstract",
        "Add citations in APA format",
        "Make the thesis statement stronger",
    ],
    "code_explainer": [
        "Explain potential performance issues",
        "Show a real-world use case example",
        "Write unit tests for this code",
        "Explain how to handle edge cases",
        "Convert this explanation to a README",
        "Suggest refactoring improvements",
    ],
    "general": [
        "Tell me more about this",
        "Give me a practical example",
        "Summarize the key points",
        "What are the common mistakes here?",
        "How can I apply this immediately?",
        "Give me a checklist version",
    ],
}


def get_followup_user_prompt(
    original_prompt: str,
    ai_response: str,
    content_type: str
) -> str:
    """
    Build the user message sent to Groq for follow-up generation.
    Includes few-shot examples for the specific content type.
    """
    examples = FOLLOWUP_EXAMPLES.get(content_type, FOLLOWUP_EXAMPLES["general"])
    examples_str = "\n".join(f'- "{q}"' for q in examples[:4])

    # Truncate AI response to keep token usage low
    response_preview = ai_response[:800] + "..." if len(ai_response) > 800 else ai_response

    return f"""Content Type: {content_type.replace('_', ' ').title()}

Original user request:
"{original_prompt}"

AI response preview:
"{response_preview}"

Example follow-ups for this content type (for reference only):
{examples_str}

Now generate exactly 3 follow-up questions/actions for THIS specific content.
Make them relevant to what was actually generated, not generic.
Return ONLY JSON: {{"questions": ["...", "...", "..."]}}"""
```

---

### Backend — Follow-up Service (`services/followup_service.py`)

```python
import httpx
import json
import os
from prompts.followup_prompts import FOLLOWUP_SYSTEM, get_followup_user_prompt

# Always use Groq for follow-ups — fastest, sufficient for this task
GROQ_BASE_URL = os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1")
GROQ_API_KEY  = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL    = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

# Fallback questions if Groq fails — shown instead of empty chips
GENERIC_FALLBACKS = [
    "Can you improve this further?",
    "Make this shorter and more concise",
    "Give me an alternative version"
]


async def generate_followups(
    original_prompt: str,
    ai_response: str,
    content_type: str
) -> list[str]:
    """
    Call Groq to generate 3 contextual follow-up questions.
    Returns list of 3 strings.
    Falls back to generic questions on any failure.
    """
    user_prompt = get_followup_user_prompt(
        original_prompt, ai_response, content_type
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": FOLLOWUP_SYSTEM},
            {"role": "user",   "content": user_prompt}
        ],
        "stream": False,          # NOT streaming — we need the full JSON at once
        "max_tokens": 150,        # 3 short questions fit easily in 150 tokens
        "temperature": 0.8,       # slight creativity so refresh gives different results
        "response_format": {"type": "json_object"}  # Groq supports forced JSON mode
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                f"{GROQ_BASE_URL}/chat/completions",
                headers=headers,
                json=payload
            )

            if response.status_code != 200:
                return GENERIC_FALLBACKS

            data = response.json()
            raw = data["choices"][0]["message"]["content"]

            # Parse JSON response
            parsed = json.loads(raw)
            questions = parsed.get("questions", [])

            # Validate: must be list of 3 non-empty strings
            questions = [
                str(q).strip()
                for q in questions
                if isinstance(q, str) and q.strip()
            ][:3]

            # Pad with fallbacks if model returned fewer than 3
            while len(questions) < 3:
                questions.append(GENERIC_FALLBACKS[len(questions)])

            return questions

    except (httpx.TimeoutException, httpx.ConnectError):
        return GENERIC_FALLBACKS
    except (json.JSONDecodeError, KeyError, ValueError):
        return GENERIC_FALLBACKS
    except Exception:
        return GENERIC_FALLBACKS
```

---

### Backend — Follow-up Router (`routers/followups.py`)

```python
from fastapi import APIRouter
from models.schemas import FollowupRequest, FollowupResponse
from services.followup_service import generate_followups

router = APIRouter(prefix="/chat", tags=["followups"])

@router.post("/followups", response_model=FollowupResponse)
async def get_followups(req: FollowupRequest):
    """
    Generate 3 contextual follow-up questions after an AI response.
    Called automatically by frontend after streaming completes.
    Also called when user clicks the refresh icon on chips.

    Always returns exactly 3 questions — never fails visibly to user.
    """
    questions = await generate_followups(
        original_prompt=req.original_prompt,
        ai_response=req.ai_response,
        content_type=req.content_type
    )
    return FollowupResponse(questions=questions)
```

---

### Register Router in `main.py`

```python
# Add to main.py imports
from routers import chat, generate, tools, followups

# Add to app.include_router calls
app.include_router(followups.router)
```

---

### Frontend — Follow-up Service (`src/services/followupService.js`)

```javascript
import api from './api'   // axios instance with JWT interceptor

/**
 * Fetch 3 follow-up questions from the AI service.
 * Called after streaming completes or when user clicks refresh.
 *
 * @param {string} originalPrompt  — what the user typed
 * @param {string} aiResponse      — full AI response text
 * @param {string} contentType     — blog_post, email, resume, etc.
 * @returns {Promise<string[]>}    — array of 3 question strings
 */
export async function fetchFollowups(originalPrompt, aiResponse, contentType, userId) {
  try {
    const { data } = await api.post('/chat/followups', {
      original_prompt: originalPrompt,
      ai_response: aiResponse.slice(0, 800),   // truncate to save bandwidth
      content_type: contentType,
      user_id: userId
    })
    return data.questions   // ["question 1", "question 2", "question 3"]
  } catch {
    return []   // silently fail — chips just won't show
  }
}
```

---

### Frontend — Follow-up Hook (`src/hooks/useFollowups.js`)

```javascript
import { useState, useCallback } from 'react'
import { fetchFollowups } from '../services/followupService'

export function useFollowups() {
  const [questions, setQuestions]   = useState([])   // current 3 chips
  const [loading, setLoading]       = useState(false) // refresh spinner
  const [visible, setVisible]       = useState(false) // chips visible?

  // Called automatically after streaming completes
  const generateAuto = useCallback(async (prompt, response, contentType, userId) => {
    setVisible(false)
    setLoading(true)
    const qs = await fetchFollowups(prompt, response, contentType, userId)
    setQuestions(qs)
    setVisible(qs.length > 0)
    setLoading(false)
  }, [])

  // Called when user clicks the 🔄 refresh icon — gets 3 NEW questions
  // temperature: 0.8 on backend means refresh gives different results
  const refresh = useCallback(async (prompt, response, contentType, userId) => {
    setLoading(true)
    const qs = await fetchFollowups(prompt, response, contentType, userId)
    setQuestions(qs)
    setLoading(false)
  }, [])

  const hide = () => setVisible(false)

  return { questions, loading, visible, generateAuto, refresh, hide }
}
```

---

### Frontend — Follow-up Chips Component (`src/components/chat/FollowupChips.jsx`)

```jsx
import { RefreshCw, Sparkles } from 'lucide-react'

/**
 * Renders 3 clickable follow-up question chips below an AI response bubble.
 *
 * Props:
 *   questions   string[]    — 3 follow-up strings from the hook
 *   loading     boolean     — shows spinner during refresh
 *   onSelect    (q) => void — called when chip is clicked
 *   onRefresh   () => void  — called when refresh icon clicked
 */
export function FollowupChips({ questions, loading, onSelect, onRefresh }) {
  if (!questions.length && !loading) return null

  return (
    <div className="mt-3 ml-1">

      {/* Label row */}
      <div className="flex items-center gap-2 mb-2">
        <Sparkles size={12} className="text-primary-500" />
        <span className="text-xs text-gray-400 font-medium">
          Follow-up suggestions
        </span>

        {/* Refresh button — spins while loading */}
        <button
          onClick={onRefresh}
          disabled={loading}
          className="ml-auto p-1 rounded hover:bg-gray-100
                     text-gray-400 hover:text-primary-500
                     transition-colors disabled:opacity-40"
          title="Get new suggestions"
        >
          <RefreshCw
            size={12}
            className={loading ? 'animate-spin' : ''}
          />
        </button>
      </div>

      {/* Chip row */}
      {loading ? (
        // Skeleton placeholders while loading
        <div className="flex flex-wrap gap-2">
          {[1, 2, 3].map(i => (
            <div
              key={i}
              className="h-8 rounded-full bg-gray-100 animate-pulse"
              style={{ width: `${100 + i * 40}px` }}
            />
          ))}
        </div>
      ) : (
        <div className="flex flex-wrap gap-2">
          {questions.map((q, idx) => (
            <button
              key={idx}
              onClick={() => onSelect(q)}
              className="px-3 py-1.5 rounded-full text-sm
                         bg-primary-50 text-primary-700
                         border border-primary-200
                         hover:bg-primary-100 hover:border-primary-400
                         transition-all duration-150
                         text-left leading-snug
                         max-w-xs truncate"
              title={q}   /* tooltip shows full text if truncated */
            >
              {q}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
```

---

### Frontend — Wiring Into Chat Page (`src/pages/ChatPage.jsx`)

```jsx
import { useFollowups } from '../hooks/useFollowups'
import { FollowupChips } from '../components/chat/FollowupChips'

export function ChatPage() {
  const [inputValue, setInputValue] = useState('')
  const { questions, loading, visible, generateAuto, refresh } = useFollowups()

  // Called when streaming finishes (done: true SSE event)
  const handleStreamComplete = (fullResponse, originalPrompt, contentType) => {
    // Fire follow-up generation — non-blocking, runs in background
    generateAuto(originalPrompt, fullResponse, contentType, userId)
  }

  // Called when user clicks a chip
  const handleChipClick = (question) => {
    setInputValue(question)           // fills the input bar
    inputRef.current?.focus()         // focuses the input
    // Optional: auto-send immediately instead of just filling
    // handleSend(question)
  }

  // Called when user clicks 🔄 refresh
  const handleRefresh = () => {
    refresh(lastPrompt, lastResponse, contentType, userId)
  }

  return (
    <div>
      {/* ... messages list ... */}

      {/* Render chips below the LAST assistant message only */}
      {visible && (
        <FollowupChips
          questions={questions}
          loading={loading}
          onSelect={handleChipClick}
          onRefresh={handleRefresh}
        />
      )}

      {/* ... input bar ... */}
    </div>
  )
}
```

---

### UI Flow — What User Sees

```
User: "Write a professional email to reschedule a meeting"

AI Response (streaming word by word):
  ---
  Subject: Request to Reschedule Our Meeting

  Hi [Name],

  I hope this message finds you well. I wanted to reach out
  regarding our upcoming meeting scheduled for...
  ---
  Words: 124 · Chars: 712 · via Gemini

  [📋 Copy] [📄 Plain Text] [🌐 Rich Copy] [🔊 Read] [🔄 Regen]

  ✨ Follow-up suggestions              [🔄]
  ┌──────────────────────┐ ┌───────────────────────┐ ┌─────────────────────────┐
  │ Make this more formal│ │Add an apology paragraph│ │ Write a follow-up email │
  │                      │ │                        │ │  if no reply in 3 days  │
  └──────────────────────┘ └───────────────────────┘ └─────────────────────────┘

User clicks "Make this more formal"
  → Input bar fills with "Make this more formal"
  → User hits send
  → New message sent with full context
```

---

### Skeleton Loading State (while Groq generates follow-ups)

Chips appear as animated grey pill skeletons for ~0.5–1 second, then fade into real questions. This matches the loading pattern used by ChatGPT and Perplexity.

```jsx
// Tailwind skeleton pill
<div className="h-8 w-32 rounded-full bg-gray-100 animate-pulse" />
```

---

### Follow-up Behavior Rules

| Situation | Behavior |
|---|---|
| After every AI response | Auto-generate 3 chips (non-blocking) |
| User clicks 🔄 refresh | Fetch 3 new chips (different due to temp=0.8) |
| User clicks a chip | Fills input bar + focuses it |
| Groq fails / times out | No chips shown (silent fail — not an error) |
| User sends next message | Previous chips disappear, new ones generate after |
| Streaming in progress | Chips from previous message hidden during stream |
| Resume / Cover Letter | Follow-ups include "Download as PDF" as a chip option |

---

### Endpoint Summary (Follow-ups)

| Method | Endpoint | Provider | Description |
|---|---|---|---|
| POST | `/chat/followups` | Groq (always) | Generate 3 follow-up questions |

---

*AI Service Plan v5.0 · 4 Providers · Smart Routing · PDF Export · Dynamic Follow-ups · April 2026*
