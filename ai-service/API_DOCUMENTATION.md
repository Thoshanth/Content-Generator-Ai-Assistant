# AI Service API Documentation

Base URL: `http://localhost:8000`

## Table of Contents
- [Chat Endpoints](#chat-endpoints)
- [Generate Endpoints](#generate-endpoints)
- [Tools Endpoints](#tools-endpoints)
- [Error Responses](#error-responses)
- [Streaming Format](#streaming-format)

---

## Chat Endpoints

### 1. Stream Chat Response

**Endpoint:** `POST /chat/stream`

**Description:** Generate AI content with streaming response (Server-Sent Events)

**Request Body:**
```json
{
  "prompt": "Write a professional email to reschedule a meeting",
  "content_type": "email",
  "tone": "professional",
  "length": "medium",
  "language": "English",
  "user_id": "user123",
  "regenerate": false,
  "custom_instructions": "Keep it brief",
  "uploaded_text": null,
  "conversation_history": []
}
```

**Request Fields:**
- `prompt` (string, required): User's input prompt (1-4000 chars)
- `content_type` (enum): Type of content to generate
  - `general`, `blog_post`, `email`, `social_media`, `ad_copy`, `tweet_thread`
  - `resume`, `cover_letter`, `youtube_script`, `product_desc`, `essay`, `code_explainer`
- `tone` (enum): Tone of response
  - `professional`, `casual`, `formal`, `persuasive`, `friendly`, `witty`, `empathetic`
- `length` (enum): Desired output length
  - `short` (100-300 words), `medium` (300-800 words), `long` (800+ words), `auto`
- `language` (enum): Output language
  - `English`, `Hindi`, `Telugu`, `Spanish`, `French`, `German`, `Portuguese`, `Arabic`, `Japanese`, `Chinese (Simplified)`, `Korean`
- `user_id` (string): User ID for tracking
- `regenerate` (boolean): If true, use higher temperature for variety
- `custom_instructions` (string): Additional instructions
- `uploaded_text` (string): Text from uploaded document
- `conversation_history` (array): Previous messages for context

**Response Format:** Server-Sent Events (SSE)

```
data: {"provider": "Gemini", "model": "gemini-1.5-flash", "attempt": 1}

data: {"delta": "Subject: "}

data: {"delta": "Request to Reschedule Meeting"}

data: {"delta": "\n\nDear [Name],\n\n"}

...

data: {"done": true, "word_count": 150, "char_count": 892}
```

**Response Events:**
- `provider`: Provider name and model used
- `delta`: Streamed text chunk
- `done`: Completion signal with statistics
- `error`: Error message if generation fails
- `info`: Informational messages (e.g., provider switching)

**cURL Example:**
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a professional email to reschedule a meeting",
    "content_type": "email",
    "tone": "professional",
    "user_id": "user123"
  }'
```

**JavaScript Example:**
```javascript
const eventSource = new EventSource(
  'http://localhost:8000/chat/stream?prompt=...&content_type=email&tone=professional'
)

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  if (data.delta) {
    console.log(data.delta)
  } else if (data.done) {
    console.log(`Done! Words: ${data.word_count}, Chars: ${data.char_count}`)
    eventSource.close()
  }
}

eventSource.onerror = (error) => {
  console.error('Stream error:', error)
  eventSource.close()
}
```

---

### 2. Get Available Providers

**Endpoint:** `GET /chat/providers`

**Description:** Get status of all AI providers

**Response (200 OK):**
```json
{
  "providers": [
    {
      "name": "Gemini",
      "model": "gemini-1.5-flash",
      "available": true
    },
    {
      "name": "Groq",
      "model": "llama-3.1-8b-instant",
      "available": true
    },
    {
      "name": "Together AI",
      "model": "meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
      "available": true
    },
    {
      "name": "DeepSeek",
      "model": "deepseek-chat",
      "available": true
    }
  ],
  "total_providers": 4,
  "available_providers": 4
}
```

**cURL Example:**
```bash
curl http://localhost:8000/chat/providers
```

---

## Generate Endpoints

Convenience endpoints for each content type. Pre-sets content_type automatically.

### Blog Post

**Endpoint:** `POST /generate/blog-post`

**Request Body:**
```json
{
  "prompt": "Write about AI trends in 2024",
  "tone": "professional",
  "length": "long",
  "language": "English"
}
```

### Email

**Endpoint:** `POST /generate/email`

### Social Media

**Endpoint:** `POST /generate/social-media`

### Ad Copy

**Endpoint:** `POST /generate/ad-copy`

### Tweet Thread

**Endpoint:** `POST /generate/tweet-thread`

### Resume

**Endpoint:** `POST /generate/resume`

### Cover Letter

**Endpoint:** `POST /generate/cover-letter`

### YouTube Script

**Endpoint:** `POST /generate/youtube-script`

### Product Description

**Endpoint:** `POST /generate/product-description`

### Essay

**Endpoint:** `POST /generate/essay`

### Code Explainer

**Endpoint:** `POST /generate/code-explainer`

---

## Tools Endpoints

### 1. Export Content

**Endpoint:** `POST /tools/export`

**Description:** Convert AI markdown output to different formats

**Request Body:**
```json
{
  "content": "# Blog Post Title\n\n## Introduction\n\nLorem ipsum...",
  "format": "plain_text",
  "content_type": "blog_post"
}
```

**Request Fields:**
- `content` (string): Markdown content to export
- `format` (enum): Export format
  - `plain_text`: Remove all markdown symbols
  - `html`: Convert to HTML
  - `markdown`: Return as-is
- `content_type` (enum): Type of content

**Response (200 OK):**
```json
{
  "content": "Blog Post Title\n\nIntroduction\n\nLorem ipsum...",
  "format": "plain_text",
  "word_count": 150,
  "char_count": 892
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/tools/export \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Title\n\nContent here",
    "format": "plain_text",
    "content_type": "blog_post"
  }'
```

---

### 2. Export as PDF

**Endpoint:** `POST /tools/export-pdf`

**Description:** Convert markdown to PDF (for Resume and Cover Letter)

**Request Body:**
```json
{
  "content": "# John Doe\n\n## Experience\n\n...",
  "content_type": "resume",
  "candidate_name": "John Doe"
}
```

**Request Fields:**
- `content` (string): Markdown content
- `content_type` (enum): `resume` or `cover_letter`
- `candidate_name` (string): Name for PDF filename

**Response:** PDF file (binary)

**Response Headers:**
```
Content-Type: application/pdf
Content-Disposition: attachment; filename="John_Doe_resume.pdf"
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/tools/export-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# John Doe\n\n## Experience\n\n...",
    "content_type": "resume",
    "candidate_name": "John Doe"
  }' \
  --output resume.pdf
```

**JavaScript Example:**
```javascript
async function downloadPdf(content, contentType, candidateName) {
  const response = await fetch('http://localhost:8000/tools/export-pdf', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content,
      content_type: contentType,
      candidate_name: candidateName
    })
  })
  
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${candidateName}_${contentType}.pdf`
  a.click()
  URL.revokeObjectURL(url)
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid request format"
}
```

### 429 Too Many Requests

```json
{
  "detail": "Rate limit exceeded. Please try again later."
}
```

### 500 Internal Server Error

```json
{
  "detail": "All AI providers are currently unavailable. Please try again in a moment."
}
```

---

## Streaming Format

### SSE Event Structure

Each event is a JSON object sent as Server-Sent Events:

```
data: {json_object}\n\n
```

### Event Types

**1. Provider Metadata (First Event)**
```json
{
  "provider": "Gemini",
  "model": "gemini-1.5-flash",
  "attempt": 1
}
```

**2. Content Delta (Streaming)**
```json
{
  "delta": "This is a chunk of text"
}
```

**3. Completion (Final Event)**
```json
{
  "done": true,
  "word_count": 150,
  "char_count": 892
}
```

**4. Error Event**
```json
{
  "error": "Provider error message",
  "done": true
}
```

**5. Info Event (Provider Switching)**
```json
{
  "info": "Gemini rate limited, switching provider..."
}
```

---

## Content Type Routing

Each content type is routed to the optimal provider:

| Content Type | Primary | Fallback 1 | Fallback 2 | Final Fallback |
|---|---|---|---|---|
| general | Groq | Gemini | Together | DeepSeek |
| blog_post | Gemini | Groq | Together | DeepSeek |
| email | Gemini | Groq | DeepSeek | Together |
| social_media | Groq | Gemini | Together | DeepSeek |
| ad_copy | Groq | Gemini | DeepSeek | Together |
| tweet_thread | Groq | Gemini | Together | DeepSeek |
| resume | Together | DeepSeek | Gemini | Groq |
| cover_letter | Gemini | Together | DeepSeek | Groq |
| youtube_script | Gemini | Groq | Together | DeepSeek |
| product_desc | Groq | Gemini | Together | DeepSeek |
| essay | Gemini | Together | DeepSeek | Groq |
| code_explainer | Together | DeepSeek | Gemini | Groq |

---

## Environment Variables

Required `.env` file:

```env
# Groq
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.1-8b-instant

# Gemini
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxx
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai
GEMINI_MODEL=gemini-1.5-flash

# Together AI
TOGETHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
TOGETHER_BASE_URL=https://api.together.xyz/v1
TOGETHER_MODEL=meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo

# DeepSeek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
DEEPSEEK_MODEL=deepseek-chat
```

---

## Rate Limiting

- Groq: 30 requests/minute (free tier)
- Gemini: 60 requests/minute (free tier)
- Together AI: 100 requests/minute (free tier)
- DeepSeek: 60 requests/minute (free tier)

When a provider is rate limited, the system automatically switches to the next provider in the fallback chain.

---

## Health Check

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "service": "ai-content-generator"
}
```
