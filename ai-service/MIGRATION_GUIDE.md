# Migration Guide: OpenRouter to Multi-Provider System

This guide helps you migrate from the OpenRouter-only system to the new multi-provider AI service.

## 🔄 What Changed

### Before (OpenRouter Only)
- Single provider: OpenRouter
- Limited to OpenRouter's free models
- Rate limits could block entire service
- Single point of failure

### After (Multi-Provider)
- Multiple providers: Groq, Gemini, TogetherAI, DeepSeek
- Automatic fallback between providers
- Better rate limit handling
- Improved reliability and performance

## 📋 Migration Steps

### 1. Update Environment Variables

**Old `.env`:**
```env
OPENROUTER_API_KEY=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
SERVICE_PORT=8000
SERVICE_HOST=0.0.0.0
```

**New `.env`:**
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

### 2. Get New API Keys

#### Groq (Recommended - Fast & Free)
1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for free account
3. Navigate to API Keys
4. Create new key
5. Add to `.env` as `GROQ_API_KEY`

#### Google Gemini (Recommended - Powerful)
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Create API key
4. Add to `.env` as `GEMINI_API_KEY`

#### TogetherAI (Optional - Diverse Models)
1. Visit [Together Console](https://api.together.xyz/)
2. Sign up for account
3. Get API key from dashboard
4. Add to `.env` as `TOGETHER_API_KEY`

#### DeepSeek (Optional - Coding Focused)
1. Visit [DeepSeek Platform](https://platform.deepseek.com/)
2. Create account
3. Generate API key
4. Add to `.env` as `DEEPSEEK_API_KEY`

### 3. Code Changes

**No code changes needed!** The API endpoints remain the same:
- `POST /chat/` - Generate content
- `POST /chat/stream` - Streaming generation
- Same request/response format

### 4. Test the Migration

```bash
# Test the new system
python test_providers.py

# Check provider status
curl http://localhost:8000/chat/providers

# Test content generation
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a test email",
    "content_type": "email"
  }'
```

## 🆚 Feature Comparison

| Feature | OpenRouter Only | Multi-Provider |
|---------|----------------|----------------|
| **Providers** | 1 (OpenRouter) | 4 (Groq, Gemini, Together, DeepSeek) |
| **Fallback** | Model-level only | Provider + Model level |
| **Speed** | Variable | Optimized (Groq first) |
| **Reliability** | Single point of failure | Multiple fallbacks |
| **Rate Limits** | Blocks entire service | Automatic provider switching |
| **API Keys** | 1 required | At least 1 required |
| **Models** | 5 free models | 10+ models across providers |

## 🎯 Benefits of Migration

### 1. **Improved Reliability**
- If one provider is down, others continue working
- No more complete service outages

### 2. **Better Performance**
- Groq provides very fast inference
- Automatic selection of fastest available provider

### 3. **More Models**
- Access to latest models from multiple providers
- Specialized models (DeepSeek for coding, Gemini for reasoning)

### 4. **Rate Limit Resilience**
- Automatic switching when rate limited
- Better distribution of requests

### 5. **Future-Proof**
- Easy to add new providers
- Not locked into single vendor

## 🔧 Configuration Options

### Minimum Setup (1 Provider)
```env
GROQ_API_KEY=your_groq_key_here
```

### Recommended Setup (2 Providers)
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
```

### Full Setup (All Providers)
```env
GROQ_API_KEY=your_groq_key_here
GEMINI_API_KEY=your_gemini_key_here
TOGETHER_API_KEY=your_together_key_here
DEEPSEEK_API_KEY=your_deepseek_key_here
```

## 🚨 Troubleshooting

### Issue: "No providers available"
**Solution**: Set at least one API key in `.env`

### Issue: "All providers failing"
**Solutions**:
1. Check API key validity
2. Verify internet connection
3. Check provider service status
4. Try different provider

### Issue: "Slower than before"
**Solutions**:
1. Ensure Groq API key is set (fastest provider)
2. Check network latency
3. Use streaming for better perceived performance

### Issue: "Different response format"
**Solution**: Response format is identical - no changes needed

## 📊 Monitoring Migration

### Check Provider Status
```bash
curl http://localhost:8000/chat/providers
```

### Monitor Logs
```bash
python main.py
# Watch for provider selection logs:
# ✅ Successfully used: groq/llama-3.1-70b-versatile
```

### Test Each Provider
```bash
# Test with different prompts to trigger different providers
python test_providers.py
```

## 🔄 Rollback Plan

If you need to rollback to OpenRouter:

1. **Keep old files**: Don't delete `services/openrouter.py`
2. **Revert imports**: Change back to `from services.openrouter`
3. **Restore old .env**: Use OpenRouter API key
4. **Update router**: Import from openrouter service

## 📈 Performance Expectations

### Response Times (Typical)
- **Groq**: 1-3 seconds
- **Gemini**: 2-5 seconds  
- **TogetherAI**: 3-7 seconds
- **DeepSeek**: 2-6 seconds

### Fallback Behavior
1. Try Groq (fastest)
2. If fails, try TogetherAI
3. If fails, try DeepSeek
4. If fails, try Gemini
5. If all fail, return helpful fallback message

## ✅ Migration Checklist

- [ ] Get at least one new API key (Groq recommended)
- [ ] Update `.env` file with new keys
- [ ] Remove old OpenRouter key (optional)
- [ ] Test with `python test_providers.py`
- [ ] Verify API endpoints still work
- [ ] Check provider status endpoint
- [ ] Monitor logs for successful provider usage
- [ ] Update documentation/deployment configs
- [ ] Inform team of new provider system

## 🎉 You're Done!

Your AI service now has:
- ✅ Multiple provider fallbacks
- ✅ Improved reliability
- ✅ Better performance
- ✅ Future-proof architecture

The migration maintains full API compatibility while providing significant improvements in reliability and performance.