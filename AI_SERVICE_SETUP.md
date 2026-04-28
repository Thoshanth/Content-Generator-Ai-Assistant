# AI Service Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
cd ai-service
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create or update `.env` file in `ai-service/` directory:

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
```

### 3. Get API Keys

#### Groq
1. Visit https://console.groq.com
2. Sign up or login
3. Create API key
4. Copy to `GROQ_API_KEY`

#### Gemini
1. Visit https://aistudio.google.com/app/apikey
2. Create API key
3. Copy to `GEMINI_API_KEY`

#### Together AI
1. Visit https://www.together.ai
2. Sign up or login
3. Create API key
4. Copy to `TOGETHER_API_KEY`

#### DeepSeek
1. Visit https://platform.deepseek.com
2. Sign up or login
3. Create API key
4. Copy to `DEEPSEEK_API_KEY`

### 4. Run AI Service

```bash
python main.py
```

Service will start on `http://localhost:8000`

### 5. Verify Installation

```bash
# Check health
curl http://localhost:8000/health

# Get available providers
curl http://localhost:8000/chat/providers
```

---

## Frontend Configuration

Update `frontend/.env`:

```env
VITE_AI_SERVICE_URL=http://localhost:8000
VITE_API_BASE_URL=http://localhost:8080/api
```

---

## Testing Endpoints

### Test Streaming

```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a professional email to reschedule a meeting",
    "content_type": "email",
    "tone": "professional",
    "user_id": "test-user"
  }'
```

### Test Export

```bash
curl -X POST http://localhost:8000/tools/export \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# Blog Post\n\n## Introduction\n\nThis is a test.",
    "format": "plain_text",
    "content_type": "blog_post"
  }'
```

### Test PDF Export

```bash
curl -X POST http://localhost:8000/tools/export-pdf \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# John Doe\n\n## Experience\n\nSoftware Engineer at Company",
    "content_type": "resume",
    "candidate_name": "John Doe"
  }' \
  --output resume.pdf
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "GROQ_API_KEY not found"

**Solution:**
1. Check `.env` file exists in `ai-service/` directory
2. Verify API key is set correctly
3. Restart the service

### Issue: "Connection refused" when calling endpoints

**Solution:**
1. Verify service is running: `python main.py`
2. Check port 8000 is not in use
3. Verify firewall settings

### Issue: "All AI providers are currently unavailable"

**Solution:**
1. Check all API keys are valid
2. Verify internet connection
3. Check provider API status
4. Wait a moment and retry (rate limit)

### Issue: "PDF export service not available"

**Solution:**
```bash
pip install weasyprint
```

Note: WeasyPrint requires system dependencies. On Windows, you may need to install GTK+ separately.

---

## Production Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Build and run:
```bash
docker build -t ai-service .
docker run -p 8000:8000 --env-file .env ai-service
```

### Environment Variables (Production)

Use secure secret management:
- AWS Secrets Manager
- Google Cloud Secret Manager
- HashiCorp Vault
- Environment variables from deployment platform

### CORS Configuration

Update `main.py` for production:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)
```

---

## Performance Optimization

### 1. Enable Caching
```python
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Cache provider status for 5 minutes
@cached(expire=300)
async def get_providers():
    ...
```

### 2. Add Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/chat/stream")
@limiter.limit("30/minute")
async def chat_stream(request: ChatRequest):
    ...
```

### 3. Connection Pooling
```python
# In ai_client.py
async with httpx.AsyncClient(
    limits=httpx.Limits(max_connections=100, max_keepalive_connections=20)
) as client:
    ...
```

---

## Monitoring

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info(f"[{provider.name}] Streaming response")
logger.error(f"[{provider.name}] Provider error: {e}")
```

### Metrics

Track:
- Request count per provider
- Response time per provider
- Error rate per provider
- User count
- Content type distribution

---

## Security Checklist

- [ ] API keys stored in `.env` (never in code)
- [ ] `.env` added to `.gitignore`
- [ ] CORS configured for specific domains
- [ ] Input validation on all endpoints
- [ ] Rate limiting enabled
- [ ] HTTPS enabled in production
- [ ] Logging configured
- [ ] Error messages don't leak sensitive info

---

## Support Resources

- **API Documentation**: `ai-service/API_DOCUMENTATION.md`
- **Implementation Details**: `AI_IMPLEMENTATION_COMPLETE.md`
- **Provider Documentation**:
  - Groq: https://console.groq.com/docs
  - Gemini: https://ai.google.dev/docs
  - Together AI: https://docs.together.ai
  - DeepSeek: https://platform.deepseek.com/docs

---

## Next Steps

1. ✅ Install dependencies
2. ✅ Configure API keys
3. ✅ Run AI service
4. ✅ Test endpoints
5. ✅ Integrate with frontend
6. ✅ Deploy to production

---

**Setup Complete!** 🎉

Your AI Service is ready to generate content with intelligent provider routing.
