# AI Service v5.0 - Testing Guide

## Overview

This guide covers all testing for the AI Service v5.0, including new features, streaming, format conversion, and multi-provider routing.

---

## Quick Start

### Run All Tests
```bash
cd ai-service
python tests/run_all_tests.py
```

### Run Individual Tests
```bash
# v5.0 Features Test
python tests/test_v5_features.py

# Four Emails Test
python tests/test_four_emails.py

# Fallback Mechanism Test
python tests/test_fallback.py

# Intelligent Routing Test
python tests/test_intelligent_routing.py

# Service Test
python tests/test_service.py
```

---

## Test Files

### 1. test_v5_features.py ⭐ NEW
Comprehensive test suite for all v5.0 features.

**Tests:**
- ✅ Streaming Response (SSE)
- ✅ Format Conversion (markdown → plain text/HTML)
- ✅ PDF Export (resume, cover letter)
- ✅ Tone Customization (7 tones)
- ✅ Length Customization (short, medium, long)
- ✅ Language Support (11 languages)
- ✅ Content Type Routing (12 types)
- ✅ Generate Endpoints (12 convenience endpoints)
- ✅ Provider Status

**Run:**
```bash
python tests/test_v5_features.py
```

**Expected Output:**
```
✅ Streaming Response - PASS
✅ Format Conversion - PASS
✅ PDF Export - PASS
✅ Tone Customization - PASS
✅ Length Customization - PASS
✅ Language Support - PASS
✅ Content Type Routing - PASS
✅ Generate Endpoints - PASS
✅ Provider Status - PASS

All 9 tests passed! 🎉
```

---

### 2. test_four_emails.py (Updated)
Tests 4 different email scenarios with streaming.

**Tests:**
- Business Meeting Email (professional tone)
- Client Follow-up Email (professional tone)
- HR Vacation Request (formal tone)
- Welcome/Onboarding Email (friendly tone)

**Features Tested:**
- Streaming response with SSE
- Tone customization
- Length customization
- Provider routing
- Multi-provider fallback

**Run:**
```bash
python tests/test_four_emails.py
```

**Expected Output:**
```
EMAIL 1: Business Meeting Email
🔄 Streaming response...
🤖 Provider: Gemini | Model: gemini-1.5-flash (Attempt 1)
Subject: Meeting Request...
✅ SUCCESS (2.34s)
📊 Stats: 150 words, 892 chars

...

📊 TEST SUMMARY
✅ Successful: 4/4
❌ Failed: 0/4

🤖 Providers Used:
  Gemini: Email 1, Email 2, Email 4
  Groq: Email 3

🎉 All email generation tests passed!
```

---

### 3. test_fallback.py (Updated)
Tests multi-provider fallback mechanism.

**Tests:**
- Provider availability check
- Individual provider testing
- Forced fallback scenario
- Fallback chain validation

**Features Tested:**
- Provider routing
- Fallback chain
- Error handling
- Rate limit handling

**Run:**
```bash
python tests/test_fallback.py
```

**Expected Output:**
```
MULTI-PROVIDER FALLBACK MECHANISM TEST

Configured providers:
  Groq: ✅ Available (3 models)
  Gemini: ✅ Available (2 models)
  Together: ✅ Available (4 models)
  DeepSeek: ✅ Available (1 model)

Testing with simple prompt...
✓ SUCCESS!
  Provider/Model used: gemini-1.5-flash
  Tokens: 42

✓ Successfully used provider: Gemini

TESTING EACH PROVIDER INDIVIDUALLY
🔄 Testing Groq...
   ✓ SUCCESS - 45 tokens
...

✓ Multi-provider fallback mechanism is working!
```

---

### 4. test_intelligent_routing.py
Tests smart routing for different content types.

**Tests:**
- Content type to provider mapping
- Optimal provider selection
- Routing table validation
- Complexity-based routing

**Run:**
```bash
python tests/test_intelligent_routing.py
```

---

### 5. test_service.py
Tests basic service functionality.

**Tests:**
- Service health check
- Endpoint availability
- Request/response format
- Error handling

**Run:**
```bash
python tests/test_service.py
```

---

### 6. run_all_tests.py ⭐ NEW
Master test runner that executes all tests.

**Features:**
- Runs all test suites
- Provides comprehensive report
- Shows pass/fail summary
- Measures total duration
- Color-coded output

**Run:**
```bash
python tests/run_all_tests.py
```

**Expected Output:**
```
AI Service v5.0 - Complete Test Suite

Available Tests:
  1. v5.0 Features Test
  2. Four Emails Test
  3. Fallback Mechanism Test
  4. Intelligent Routing Test
  5. Service Test

Running Tests...
🧪 Running: v5.0 Features Test
✅ v5.0 Features Test PASSED

🧪 Running: Four Emails Test
✅ Four Emails Test PASSED

...

Test Summary
Total Tests: 5
Passed: 5
Failed: 0
Duration: 45.2s

🎉 All tests passed!
```

---

## Test Coverage

### Features Tested

| Feature | Test File | Status |
|---|---|---|
| Streaming Response | test_v5_features.py | ✅ |
| Format Conversion | test_v5_features.py | ✅ |
| PDF Export | test_v5_features.py | ✅ |
| Tone Customization | test_v5_features.py | ✅ |
| Length Customization | test_v5_features.py | ✅ |
| Language Support | test_v5_features.py | ✅ |
| Content Type Routing | test_v5_features.py | ✅ |
| Generate Endpoints | test_v5_features.py | ✅ |
| Provider Status | test_v5_features.py | ✅ |
| Multi-provider Fallback | test_fallback.py | ✅ |
| Email Generation | test_four_emails.py | ✅ |
| Intelligent Routing | test_intelligent_routing.py | ✅ |
| Service Health | test_service.py | ✅ |

---

## Prerequisites

### 1. Service Running
```bash
cd ai-service
python main.py
```

Service should be running on `http://localhost:8000`

### 2. API Keys Configured
```bash
# ai-service/.env
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIzaSy...
TOGETHER_API_KEY=...
DEEPSEEK_API_KEY=sk-...
```

At least one API key must be configured.

### 3. Dependencies Installed
```bash
pip install -r requirements.txt
```

---

## Test Scenarios

### Scenario 1: Basic Streaming
**Test:** test_v5_features.py → Streaming Response

**Steps:**
1. Send streaming request to `/chat/stream`
2. Receive SSE events
3. Verify provider metadata
4. Verify content delta
5. Verify completion stats

**Expected:** ✅ PASS

---

### Scenario 2: Format Conversion
**Test:** test_v5_features.py → Format Conversion

**Steps:**
1. Send markdown content to `/tools/export`
2. Request plain_text format
3. Verify markdown symbols removed
4. Request HTML format
5. Verify HTML tags present
6. Request markdown format
7. Verify content unchanged

**Expected:** ✅ PASS

---

### Scenario 3: PDF Export
**Test:** test_v5_features.py → PDF Export

**Steps:**
1. Send resume content to `/tools/export-pdf`
2. Verify PDF bytes returned
3. Send cover letter content
4. Verify PDF bytes returned
5. Verify file size > 0

**Expected:** ✅ PASS

---

### Scenario 4: Tone Customization
**Test:** test_v5_features.py → Tone Customization

**Steps:**
1. Generate email with "professional" tone
2. Generate email with "casual" tone
3. Generate email with "formal" tone
4. Generate email with "friendly" tone
5. Verify all succeed

**Expected:** ✅ PASS

---

### Scenario 5: Multi-provider Fallback
**Test:** test_fallback.py

**Steps:**
1. Check provider availability
2. Send request to primary provider
3. If rate limited, verify fallback to next provider
4. Verify final response received
5. Verify provider chain used

**Expected:** ✅ PASS

---

### Scenario 6: Email Generation
**Test:** test_four_emails.py

**Steps:**
1. Generate business meeting email
2. Generate client follow-up email
3. Generate HR vacation request
4. Generate welcome email
5. Verify all succeed with streaming
6. Verify different tones applied

**Expected:** ✅ PASS

---

## Troubleshooting

### Issue: "Connection refused"
**Solution:**
```bash
# Make sure service is running
cd ai-service
python main.py
```

### Issue: "No providers available"
**Solution:**
```bash
# Check .env file has API keys
cat ai-service/.env

# Add missing API keys
GROQ_API_KEY=gsk_...
GEMINI_API_KEY=AIzaSy...
```

### Issue: "All tests failed"
**Solution:**
1. Verify service is running
2. Verify API keys are valid
3. Check network connectivity
4. Check provider API status

### Issue: "Timeout"
**Solution:**
- Increase timeout in test file
- Check provider response time
- Verify network speed

---

## Performance Benchmarks

### Expected Response Times

| Test | Expected Time | Timeout |
|---|---|---|
| Streaming Response | 2-5s | 90s |
| Format Conversion | < 1s | 30s |
| PDF Export | 2-3s | 60s |
| Tone Test | 2-5s | 90s |
| Length Test | 2-5s | 90s |
| Language Test | 2-5s | 90s |
| Content Type Test | 2-5s | 90s |
| Generate Endpoints | 2-5s | 90s |
| Provider Status | < 1s | 30s |

---

## Continuous Integration

### GitHub Actions Example
```yaml
name: AI Service Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      
      - name: Install dependencies
        run: |
          cd ai-service
          pip install -r requirements.txt
      
      - name: Start service
        run: |
          cd ai-service
          python main.py &
          sleep 5
      
      - name: Run tests
        run: |
          cd ai-service
          python tests/run_all_tests.py
```

---

## Test Results Template

```
AI Service v5.0 - Test Results
Date: 2024-12-15
Time: 14:30:00

Environment:
- Python: 3.11.0
- OS: Ubuntu 22.04
- Service: Running on http://localhost:8000

Test Summary:
- Total Tests: 5
- Passed: 5
- Failed: 0
- Duration: 45.2s

Detailed Results:
✅ v5.0 Features Test - PASS (12.3s)
✅ Four Emails Test - PASS (15.4s)
✅ Fallback Mechanism Test - PASS (8.2s)
✅ Intelligent Routing Test - PASS (5.1s)
✅ Service Test - PASS (4.2s)

Conclusion:
All tests passed successfully! ✅
```

---

## Best Practices

### 1. Run Tests Regularly
```bash
# After each code change
python tests/run_all_tests.py
```

### 2. Check Provider Status First
```bash
# Verify providers are available
curl http://localhost:8000/chat/providers
```

### 3. Monitor Performance
- Track response times
- Monitor token usage
- Check error rates

### 4. Test Different Scenarios
- Different content types
- Different tones/lengths
- Different languages
- Different providers

### 5. Document Results
- Keep test logs
- Track performance trends
- Document failures

---

## Support

For issues or questions:
1. Check troubleshooting section
2. Review test output
3. Check API keys
4. Verify service is running
5. Check provider API status

---

**Last Updated:** April 28, 2026
**Version:** 5.0.0
