# Start AI Service with New Providers

## Quick Start

### Option 1: Start Service (Recommended)
```bash
cd ai-service
python main.py
```

### Option 2: Start with Auto-reload (Development)
```bash
cd ai-service
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## After Starting

### 1. Verify Service is Running
Open browser: http://localhost:8000

Expected response:
```json
{"message": "AI Content Generator Service is running"}
```

### 2. Check Provider Status
```bash
curl http://localhost:8000/chat/providers
```

Expected response:
```json
{
  "providers": [
    {"name": "Groq", "model": "llama-3.1-8b-instant"},
    {"name": "Gemini", "model": "gemini-1.5-flash"},
    {"name": "NVIDIA NIM", "model": "meta/llama-3.3-70b-instruct"},
    {"name": "Cerebras", "model": "llama-3.3-70b"}
  ]
}
```

### 3. Run Tests
```bash
# In a new terminal
cd ai-service
python tests/test_all_providers.py
```

---

## Expected Output

```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Then restart
cd ai-service
python main.py
```

### Import Errors
```bash
cd ai-service
pip install -r requirements.txt
```

---

## Test Commands

### Quick Test
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Hello\",\"content_type\":\"general\"}"
```

### Test Resume (NVIDIA Primary)
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Create resume summary\",\"content_type\":\"resume\"}"
```

### Test Code (NVIDIA Primary)
```bash
curl -X POST http://localhost:8000/chat/stream \
  -H "Content-Type: application/json" \
  -d "{\"prompt\":\"Explain async\",\"content_type\":\"code_explainer\"}"
```

---

**Start the service and run the tests!** 🚀
