# Testing the Resume Generation Fix

## Quick Start

### 1. Start AI Service
```bash
cd ai-service
python main.py
```

Expected output:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 2. Start Backend
```bash
cd backend
./run.bat    # Windows
# or
./run.sh     # Linux/Mac
```

Expected output:
```
Started ContentGeneratorApplication in X.XXX seconds
```

### 3. Test Resume Generation

#### Option A: Using Frontend
1. Open browser: `http://localhost:3000`
2. Login to your account
3. In chat, type: "Generate a resume for me"
4. Should see:
   - Provider badge (NVIDIA NIM or Cerebras)
   - Complete resume content
   - No 404 error

#### Option B: Using Test Script
```bash
cd ai-service
python tests/test_non_streaming_endpoint.py
```

Expected output:
```
✓ Success!
Provider: NVIDIA NIM
Model: nvidia/llama-3.1-nemotron-70b-instruct
Word Count: 250
Char Count: 1500
```

#### Option C: Using cURL
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Generate a resume for a software engineer",
    "content_type": "resume",
    "tone": "professional",
    "length": "medium",
    "language": "English",
    "user_id": "test-123"
  }'
```

Expected response:
```json
{
  "content": "...",
  "provider": "NVIDIA NIM",
  "model": "nvidia/llama-3.1-nemotron-70b-instruct",
  "word_count": 250,
  "char_count": 1500
}
```

## Troubleshooting

### Still Getting 404?

1. **Check AI Service is Running**
   ```bash
   curl http://localhost:8000/health
   ```
   Should return: `{"status": "healthy"}`

2. **Check Endpoint Exists**
   ```bash
   curl http://localhost:8000/docs
   ```
   Look for `POST /chat/` in the API docs

3. **Check Backend Configuration**
   In `backend/src/main/resources/application.properties`:
   ```properties
   ai.service.url=http://localhost:8000
   ```

4. **Check Backend Logs**
   Look for:
   ```
   Calling AI service: POST http://localhost:8000/chat/
   ```

### Provider Errors?

If you see provider errors in AI service logs:

1. **Check .env File**
   ```bash
   cd ai-service
   cat .env
   ```
   Verify all 4 API keys are set:
   - `GROQ_API_KEY`
   - `GEMINI_API_KEY`
   - `NVIDIA_API_KEY`
   - `CEREBRAS_API_KEY`

2. **Test Individual Providers**
   ```bash
   cd ai-service
   python tests/test_all_providers.py
   ```

3. **Check Provider Status**
   ```bash
   curl http://localhost:8000/chat/providers
   ```

### Backend Compilation Errors?

If backend won't compile:

1. **Clean and Rebuild**
   ```bash
   cd backend
   mvn clean install -DskipTests
   ```

2. **Check Java Version**
   ```bash
   java -version
   ```
   Should be Java 17 or higher

3. **Check Maven Version**
   ```bash
   mvn -version
   ```
   Should be Maven 3.6 or higher

## Verification Checklist

- [ ] AI service starts without errors
- [ ] Backend starts without errors
- [ ] `/chat/` endpoint exists (check http://localhost:8000/docs)
- [ ] All 4 providers configured in .env
- [ ] Resume generation works via test script
- [ ] Resume generation works via frontend
- [ ] Provider badge shows correct provider
- [ ] Word count and char count are displayed
- [ ] No 404 errors in browser console or backend logs

## Expected Provider for Resume

Based on routing table:
1. **Primary**: NVIDIA NIM (if API key valid)
2. **Fallback 1**: Cerebras (if NVIDIA fails)
3. **Fallback 2**: Gemini (if both fail)
4. **Final**: Groq (if all others fail)

## Success Indicators

✅ **AI Service Logs**:
```
INFO: 127.0.0.1:XXXXX - "POST /chat/ HTTP/1.1" 200 OK
```

✅ **Backend Logs**:
```
AI Response received: provider=NVIDIA NIM, model=nvidia/llama-3.1-nemotron-70b-instruct
```

✅ **Frontend**:
- Resume content displayed
- Provider badge shows "NVIDIA NIM" or "Cerebras"
- Export buttons work (Copy, HTML, PDF)
- No error messages

## Common Issues

### Issue: "All AI providers are currently unavailable"
**Solution**: Check .env file has valid API keys for at least one provider

### Issue: Backend can't connect to AI service
**Solution**: Verify AI service is running on port 8000 and not blocked by firewall

### Issue: Resume content is empty
**Solution**: Check AI service logs for provider errors, may need to add credits to provider account

### Issue: Wrong provider being used
**Solution**: Check routing table in `ai-service/services/model_router.py`, resume should use NVIDIA NIM first

## Need Help?

1. Check logs in both AI service and backend
2. Run test script to isolate the issue
3. Verify all environment variables are set
4. Check API provider dashboards for rate limits/credits
5. Review `404_FIX_SUMMARY.md` for technical details
