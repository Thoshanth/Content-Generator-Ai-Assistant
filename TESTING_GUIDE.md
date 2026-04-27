# 🧪 Testing Guide - AI Content Generator

Complete guide to test all components of the application.

## 📋 Testing Overview

This guide covers:
1. Python AI Service testing
2. Spring Boot Backend testing
3. Database testing
4. Integration testing
5. Load testing

---

## 1️⃣ Python AI Service Testing

### Prerequisites
```bash
cd ai-service
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload --port 8000
```

### Test 1: Health Check
```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "ai-content-generator"
}
```

### Test 2: Non-Streaming Chat
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short professional email about a meeting",
    "content_type": "email",
    "conversation_history": [],
    "user_id": "test-user-123"
  }'
```

**Expected Response**:
```json
{
  "content": "Subject: Meeting Request\n\nDear [Name],\n\n...",
  "model_used": "nvidia/llama-3.1-nemotron-70b-instruct:free",
  "tokens_used": 150
}
```

### Test 3: Streaming Chat
```bash
curl -X POST "http://localhost:8000/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a blog post intro about AI",
    "content_type": "blog_post"
  }'
```

**Expected Response**: Server-Sent Events stream
```
data: {"content": "Artificial", "model": "nvidia/..."}
data: {"content": " Intelligence", "model": "nvidia/..."}
...
data: {"done": true}
```

### Test 4: Different Content Types

**Blog Post**:
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write about the future of AI in healthcare",
    "content_type": "blog_post"
  }'
```

**Social Media**:
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "LinkedIn post about productivity tips",
    "content_type": "social_media"
  }'
```

**Ad Copy**:
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Ad for a new fitness app",
    "content_type": "ad_copy"
  }'
```

### Test 5: Conversation History
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Can you make it more casual?",
    "content_type": "email",
    "conversation_history": [
      {"role": "user", "content": "Write a professional email"},
      {"role": "assistant", "content": "Dear Sir/Madam..."}
    ]
  }'
```

---

## 2️⃣ Spring Boot Backend Testing

### Prerequisites
```bash
cd backend
./mvnw spring-boot:run
```

### Test 1: Register User
```bash
curl -X POST "http://localhost:8080/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "password123",
    "fullName": "Test User"
  }'
```

**Expected Response**:
```json
{
  "message": "User registered successfully",
  "userId": "uuid-here",
  "email": "testuser@example.com",
  "username": "testuser"
}
```

### Test 2: Login
```bash
curl -X POST "http://localhost:8080/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "password123"
  }'
```

**Expected Response**:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "message": "Login successful"
}
```

**Save the token for next tests!**

### Test 3: Get Profile
```bash
# Replace YOUR_TOKEN with actual token from login
curl -X GET "http://localhost:8080/api/user/profile" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
{
  "id": "uuid",
  "email": "testuser@example.com",
  "username": "testuser",
  "fullName": "Test User",
  "plan": "free",
  "totalSessions": 0,
  "totalMessages": 0,
  "dailyMessageCount": 0
}
```

### Test 4: Send Chat Message
```bash
curl -X POST "http://localhost:8080/api/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short email about project update",
    "contentType": "email",
    "sessionTitle": "Project Updates"
  }'
```

**Expected Response**:
```json
{
  "sessionId": "uuid",
  "content": "Subject: Project Update\n\n...",
  "modelUsed": "nvidia/llama-3.1-nemotron-70b-instruct:free",
  "tokensUsed": 120,
  "messageId": "uuid"
}
```

### Test 5: Get All Sessions
```bash
curl -X GET "http://localhost:8080/api/chat/sessions" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
[
  {
    "id": "uuid",
    "userId": "uuid",
    "title": "Project Updates",
    "contentType": "email",
    "createdAt": "2024-01-01T10:00:00",
    "updatedAt": "2024-01-01T10:00:00"
  }
]
```

### Test 6: Get Session with Messages
```bash
# Replace SESSION_ID with actual session ID
curl -X GET "http://localhost:8080/api/chat/sessions/SESSION_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
{
  "id": "uuid",
  "title": "Project Updates",
  "contentType": "email",
  "messages": [
    {
      "id": "uuid",
      "role": "user",
      "content": "Write a short email about project update",
      "createdAt": "2024-01-01T10:00:00"
    },
    {
      "id": "uuid",
      "role": "assistant",
      "content": "Subject: Project Update...",
      "modelUsed": "nvidia/...",
      "tokensUsed": 120,
      "createdAt": "2024-01-01T10:00:01"
    }
  ]
}
```

### Test 7: Update Profile
```bash
curl -X PUT "http://localhost:8080/api/user/profile" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "Updated Name",
    "avatarUrl": "https://example.com/avatar.jpg"
  }'
```

### Test 8: Change Password
```bash
curl -X PUT "http://localhost:8080/api/user/password" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "oldPassword": "password123",
    "newPassword": "newpassword456"
  }'
```

### Test 9: Get User Stats
```bash
curl -X GET "http://localhost:8080/api/user/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Response**:
```json
{
  "totalSessions": 1,
  "totalMessages": 2,
  "userMessages": 1,
  "dailyMessageCount": 1,
  "lastMessageDate": "2024-01-01T10:00:00"
}
```

### Test 10: Delete Session
```bash
curl -X DELETE "http://localhost:8080/api/chat/sessions/SESSION_ID" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 11: Rate Limiting
Send 11 messages in a row to test rate limiting:

```bash
# This script sends 11 messages
for i in {1..11}; do
  echo "Message $i:"
  curl -X POST "http://localhost:8080/api/chat/message" \
    -H "Authorization: Bearer YOUR_TOKEN" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\":\"Test message $i\",\"contentType\":\"general\"}"
  echo "\n"
done
```

**Expected**: First 10 succeed, 11th returns:
```json
{
  "error": "Daily message limit reached",
  "limit": 10
}
```

---

## 3️⃣ Database Testing

### Connect to Supabase

**Using psql**:
```bash
psql "postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres"
```

### Test Queries

**Check users**:
```sql
SELECT id, email, username, plan, daily_message_count 
FROM users 
ORDER BY created_at DESC;
```

**Check sessions**:
```sql
SELECT 
    cs.id,
    cs.title,
    u.username,
    COUNT(cm.id) as message_count
FROM chat_sessions cs
JOIN users u ON u.id = cs.user_id
LEFT JOIN chat_messages cm ON cm.session_id = cs.id
GROUP BY cs.id, u.username
ORDER BY cs.updated_at DESC;
```

**Check messages**:
```sql
SELECT 
    cm.role,
    LEFT(cm.content, 50) as content_preview,
    cm.model_used,
    cm.tokens_used,
    cm.created_at
FROM chat_messages cm
WHERE cm.session_id = 'YOUR_SESSION_ID'
ORDER BY cm.created_at ASC;
```

**Check rate limiting**:
```sql
SELECT 
    email,
    daily_message_count,
    last_message_date,
    CASE 
        WHEN DATE(last_message_date) = CURRENT_DATE THEN 'Today'
        ELSE 'Old'
    END as status
FROM users;
```

**Reset rate limit for testing**:
```sql
UPDATE users 
SET daily_message_count = 0 
WHERE email = 'testuser@example.com';
```

---

## 4️⃣ Integration Testing

### Full Flow Test

This tests the complete flow from user registration to AI response:

```bash
#!/bin/bash

echo "=== AI Content Generator Integration Test ==="

# 1. Register user
echo "\n1. Registering user..."
REGISTER_RESPONSE=$(curl -s -X POST "http://localhost:8080/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "integration@test.com",
    "username": "integrationtest",
    "password": "test123",
    "fullName": "Integration Test"
  }')
echo $REGISTER_RESPONSE

# 2. Login
echo "\n2. Logging in..."
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8080/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "integration@test.com",
    "password": "test123"
  }')
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token')
echo "Token: $TOKEN"

# 3. Get profile
echo "\n3. Getting profile..."
curl -s -X GET "http://localhost:8080/api/user/profile" \
  -H "Authorization: Bearer $TOKEN" | jq

# 4. Send message
echo "\n4. Sending chat message..."
MESSAGE_RESPONSE=$(curl -s -X POST "http://localhost:8080/api/chat/message" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short email",
    "contentType": "email"
  }')
echo $MESSAGE_RESPONSE | jq

SESSION_ID=$(echo $MESSAGE_RESPONSE | jq -r '.sessionId')

# 5. Get sessions
echo "\n5. Getting all sessions..."
curl -s -X GET "http://localhost:8080/api/chat/sessions" \
  -H "Authorization: Bearer $TOKEN" | jq

# 6. Get session with messages
echo "\n6. Getting session with messages..."
curl -s -X GET "http://localhost:8080/api/chat/sessions/$SESSION_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

# 7. Get stats
echo "\n7. Getting user stats..."
curl -s -X GET "http://localhost:8080/api/user/stats" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "\n=== Integration Test Complete ==="
```

Save as `integration-test.sh` and run:
```bash
chmod +x integration-test.sh
./integration-test.sh
```

---

## 5️⃣ Load Testing

### Using Apache Bench

**Test authentication endpoint**:
```bash
ab -n 100 -c 10 -p register.json -T application/json \
  http://localhost:8080/api/auth/register
```

**Test chat endpoint** (requires token):
```bash
ab -n 50 -c 5 -p chat.json -T application/json \
  -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8080/api/chat/message
```

### Using k6

Create `load-test.js`:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  // Register
  let registerRes = http.post('http://localhost:8080/api/auth/register', 
    JSON.stringify({
      email: `user${__VU}@test.com`,
      username: `user${__VU}`,
      password: 'test123'
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(registerRes, { 'register status 200': (r) => r.status === 200 });
  
  // Login
  let loginRes = http.post('http://localhost:8080/api/auth/login',
    JSON.stringify({
      email: `user${__VU}@test.com`,
      password: 'test123'
    }),
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  let token = loginRes.json('token');
  
  // Send message
  let chatRes = http.post('http://localhost:8080/api/chat/message',
    JSON.stringify({
      prompt: 'Write a short email',
      contentType: 'email'
    }),
    { headers: { 
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    }}
  );
  
  check(chatRes, { 'chat status 200': (r) => r.status === 200 });
  
  sleep(1);
}
```

Run:
```bash
k6 run load-test.js
```

---

## 6️⃣ Error Testing

### Test Invalid Inputs

**Invalid email**:
```bash
curl -X POST "http://localhost:8080/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"invalid","username":"test","password":"test123"}'
```

**Short password**:
```bash
curl -X POST "http://localhost:8080/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"test","password":"123"}'
```

**Invalid token**:
```bash
curl -X GET "http://localhost:8080/api/user/profile" \
  -H "Authorization: Bearer invalid_token"
```

**Empty prompt**:
```bash
curl -X POST "http://localhost:8080/api/chat/message" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"","contentType":"email"}'
```

---

## ✅ Testing Checklist

### Python AI Service
- [ ] Health check works
- [ ] Non-streaming chat works
- [ ] Streaming chat works
- [ ] All content types work
- [ ] Conversation history works
- [ ] Model fallback works
- [ ] Error handling works

### Spring Boot Backend
- [ ] User registration works
- [ ] User login works
- [ ] JWT validation works
- [ ] Profile management works
- [ ] Chat message creation works
- [ ] Session management works
- [ ] Rate limiting works
- [ ] Database operations work
- [ ] CORS works
- [ ] Error handling works

### Database
- [ ] All tables created
- [ ] Indexes work
- [ ] Foreign keys work
- [ ] Triggers work
- [ ] Cascade delete works
- [ ] Queries perform well

### Integration
- [ ] Full user flow works
- [ ] Services communicate correctly
- [ ] Data persists correctly
- [ ] Rate limiting enforced
- [ ] Errors handled gracefully

---

## 📊 Expected Performance

### Response Times (Local)
- Health check: < 10ms
- User registration: < 100ms
- User login: < 100ms
- Chat message (non-streaming): 2-5 seconds
- Chat message (streaming): Starts in < 1 second
- Database queries: < 50ms

### Response Times (Production)
- Add 200-500ms for network latency
- First request after sleep: 30-60 seconds (free tier)
- Subsequent requests: Normal times

---

## 🐛 Common Issues

### "Connection refused"
- Service not running
- Wrong port
- Firewall blocking

### "Unauthorized"
- Invalid or expired token
- Token not in Authorization header
- Wrong token format

### "Daily limit reached"
- Reset in database: `UPDATE users SET daily_message_count = 0`
- Or wait until midnight

### "All models failed"
- Invalid OpenRouter API key
- OpenRouter service down
- Network issues

---

**Testing Complete! 🎉**

All tests passing means your application is production-ready!
