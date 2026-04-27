# AI Content Generator Service

A FastAPI-based service for AI content generation using multiple providers with automatic fallback.

## 🚀 Features

- **Multi-Provider Support**: Groq, Gemini, TogetherAI, DeepSeek
- **Automatic Fallback**: Seamlessly switches between providers if one fails
- **Streaming Support**: Real-time content generation
- **Content Types**: Email, blog posts, social media, general content
- **Rate Limit Handling**: Automatic retry with exponential backoff
- **Conversation History**: Context-aware responses

## 🔧 Supported Providers

### 1. Groq (Fast Inference)
- **Models**: llama-3.1-70b-versatile, llama-3.1-8b-instant, mixtral-8x7b-32768, gemma2-9b-it
- **Strengths**: Very fast inference, good for real-time applications
- **API Key**: Get from [Groq Console](https://console.groq.com/)

### 2. TogetherAI (Diverse Models)
- **Models**: Meta-Llama-3.1-70B-Instruct-Turbo, Meta-Llama-3.1-8B-Instruct-Turbo, Mixtral-8x7B-Instruct-v0.1
- **Strengths**: Wide variety of models, competitive pricing
- **API Key**: Get from [Together Console](https://api.together.xyz/)

### 3. DeepSeek (Specialized Models)
- **Models**: deepseek-chat, deepseek-coder
- **Strengths**: Excellent for coding and technical content
- **API Key**: Get from [DeepSeek Platform](https://platform.deepseek.com/)

### 4. Google Gemini (Google's AI)
- **Models**: gemini-1.5-flash, gemini-1.5-pro
- **Strengths**: Strong reasoning, multimodal capabilities
- **API Key**: Get from [Google AI Studio](https://aistudio.google.com/)

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   cd ai-service
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Set API Keys** in `.env`:
   ```env
   # AI Provider API Keys (set at least one)
   GROQ_API_KEY=your_groq_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   TOGETHER_API_KEY=your_together_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here

   # Service Configuration
   SERVICE_PORT=8000
   SERVICE_HOST=0.0.0.0
   ```

## 🏃‍♂️ Running the Service

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Using Docker
```bash
docker build -t ai-service .
docker run -p 8000:8000 --env-file .env ai-service
```

## 🧪 Testing

### Test All Providers
```bash
python test_providers.py
```

### Test Specific Functionality
```bash
python test_service.py
```

### Test Fallback Mechanism
```bash
python test_fallback.py
```

## 📡 API Endpoints

### 1. Generate Content (Non-streaming)
```http
POST /chat/
Content-Type: application/json

{
  "prompt": "Write a professional email about scheduling a meeting",
  "content_type": "email",
  "conversation_history": [],
  "user_id": "optional-user-id"
}
```

**Response**:
```json
{
  "content": "Subject: Meeting Schedule Request...",
  "model_used": "groq/llama-3.1-70b-versatile",
  "tokens_used": 245
}
```

### 2. Generate Content (Streaming)
```http
POST /chat/stream
Content-Type: application/json

{
  "prompt": "Write a blog post about AI",
  "content_type": "blog"
}
```

**Response**: Server-Sent Events (SSE)
```
data: {"content": "# The Future", "model": "groq/llama-3.1-70b-versatile"}
data: {"content": " of Artificial", "model": "groq/llama-3.1-70b-versatile"}
data: {"done": true}
```

### 3. Check Provider Status
```http
GET /chat/providers
```

**Response**:
```json
{
  "providers": [
    {
      "name": "groq",
      "available": true,
      "models": ["llama-3.1-70b-versatile", "llama-3.1-8b-instant"]
    }
  ],
  "total_providers": 4,
  "available_providers": 2
}
```

## 🎯 Content Types

- **email**: Professional emails, newsletters
- **blog**: Blog posts, articles, long-form content
- **social**: Social media posts, tweets, captions
- **general**: General purpose content, Q&A

## 🔄 Fallback Logic

The service tries providers in this order:
1. **Groq** (fastest)
2. **TogetherAI** (diverse models)
3. **DeepSeek** (specialized)
4. **Gemini** (Google's AI)

If all providers fail, returns a helpful fallback message.

## 🛠️ Configuration

### Environment Variables
- `GROQ_API_KEY`: Groq API key
- `GEMINI_API_KEY`: Google Gemini API key
- `TOGETHER_API_KEY`: TogetherAI API key
- `DEEPSEEK_API_KEY`: DeepSeek API key
- `SERVICE_PORT`: Service port (default: 8000)
- `SERVICE_HOST`: Service host (default: 0.0.0.0)

### Provider Priority
Edit `PROVIDERS` list in `services/ai_providers.py` to change fallback order.

## 📊 Monitoring

### Health Check
```http
GET /health
```

### Service Status
```http
GET /
```

### Provider Status
```http
GET /chat/providers
```

## 🚨 Error Handling

- **Rate Limits**: Automatic retry with backoff
- **API Errors**: Graceful fallback to next provider
- **Network Issues**: Timeout handling and retry logic
- **Invalid Keys**: Skip provider and continue with others

## 🔒 Security

- API keys stored in environment variables
- CORS configured for frontend integration
- Request validation with Pydantic models
- Error messages sanitized

## 📈 Performance

- **Async/Await**: Non-blocking operations
- **Connection Pooling**: Efficient HTTP client usage
- **Streaming**: Real-time content delivery
- **Caching**: Response caching (optional)

## 🤝 Integration

### Frontend Integration
```javascript
// Non-streaming
const response = await fetch('/chat/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    prompt: 'Write an email',
    content_type: 'email'
  })
});

// Streaming
const eventSource = new EventSource('/chat/stream', {
  method: 'POST',
  body: JSON.stringify({ prompt: 'Write a blog post' })
});
```

### Backend Integration
```python
import httpx

async def call_ai_service(prompt: str, content_type: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/chat/",
            json={"prompt": prompt, "content_type": content_type}
        )
        return response.json()
```

## 📝 Migration from OpenRouter

If migrating from the old OpenRouter-only system:

1. **Update imports**: Change `from services.openrouter` to `from services.ai_providers`
2. **Add API keys**: Set new provider keys in `.env`
3. **Test providers**: Run `python test_providers.py`
4. **Update frontend**: No changes needed (same API)

## 🐛 Troubleshooting

### Common Issues

1. **No providers available**
   - Check API keys in `.env`
   - Verify key format and permissions

2. **All requests failing**
   - Check internet connection
   - Verify provider service status
   - Check rate limits

3. **Slow responses**
   - Try different providers
   - Check network latency
   - Consider using streaming

### Debug Mode
```bash
export LOG_LEVEL=DEBUG
python main.py
```

## 📚 API Documentation

Start the service and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤖 Example Usage

```python
import asyncio
from services.ai_providers import generate_content

async def example():
    content, model, tokens = await generate_content(
        prompt="Write a welcome email for new users",
        content_type="email"
    )
    print(f"Generated by {model}: {content}")

asyncio.run(example())
```