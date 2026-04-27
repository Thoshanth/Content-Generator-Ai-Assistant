# 🚀 Complete Setup Guide - AI Content Generator

## Overview

This guide will help you set up and run the complete AI Content Generator application with all three services connected.

---

## Prerequisites

- ✅ Node.js 18+ and npm
- ✅ Java 17+
- ✅ Python 3.10+
- ✅ PostgreSQL (Supabase account)
- ✅ OpenRouter API key

---

## Step 1: Database Setup (5 minutes)

### Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up
2. Click "New Project"
3. Fill in:
   - Name: `ai-content-generator`
   - Password: (create strong password - SAVE IT!)
   - Region: Choose closest
4. Wait 2-3 minutes for setup

### Run Database Schema

1. In Supabase dashboard, go to "SQL Editor"
2. Click "New query"
3. Copy entire content from `database/schema.sql`
4. Paste and click "Run"
5. Verify tables created in "Table Editor"

### Get Connection Details

1. Go to Settings → Database
2. Note these values:
   ```
   Host: db.xxxxx.supabase.co
   Database: postgres
   Port: 5432
   User: postgres
   Password: (your password from step 3)
   ```

---

## Step 2: Python AI Service (3 minutes)

### Setup

```bash
cd ai-service

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Configure

Create `.env` file:

```bash
OPENROUTER_API_KEY=your_openrouter_key_here
```

**Get OpenRouter API Key:**
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up (free, no credit card)
3. Go to Keys section
4. Create new key

### Run

```bash
uvicorn main:app --reload --port 8000
```

✅ Service running at: http://localhost:8000

**Test it:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

---

## Step 3: Spring Boot Backend (5 minutes)

### Configure

Edit `backend/src/main/resources/application.properties`:

```properties
# Database (use your Supabase details)
spring.datasource.url=jdbc:postgresql://db.xxxxx.supabase.co:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=your_supabase_password

# JWT Secret (change this!)
jwt.secret=your-super-secret-256-bit-key-change-this-in-production

# AI Service URL
ai.service.url=http://localhost:8000

# Rate Limiting
rate.limit.daily=10
rate.limit.enabled=true

# CORS
cors.allowed.origins=http://localhost:5173
```

### Run

```bash
cd backend
./mvnw spring-boot:run
```

✅ Service running at: http://localhost:8080

**Test it:**
```bash
curl http://localhost:8080/api/auth/validate
# Should return: {"valid":false}
```

---

## Step 4: React Frontend (3 minutes)

### Setup

```bash
cd frontend

# Install dependencies
npm install
```

### Configure

Create `.env` file:

```bash
VITE_API_BASE_URL=http://localhost:8080/api
```

### Run

```bash
npm run dev
```

✅ App running at: http://localhost:5173

---

## Step 5: Test Complete Flow (5 minutes)

### 1. Open Browser

Go to: http://localhost:5173

### 2. Register Account

1. Click "Get Started" or "Register"
2. Fill in:
   - Full Name: Test User
   - Username: testuser
   - Email: test@example.com
   - Password: password123
3. Click "Create Account"

### 3. Login

1. Go to Login page
2. Enter:
   - Email: test@example.com
   - Password: password123
3. Click "Sign In"

### 4. Send First Message

1. You'll be redirected to Chat page
2. Select content type (e.g., "Email")
3. Type: "Write a professional email about a meeting"
4. Press Enter or click Send
5. Watch the AI response stream in real-time!

### 5. Verify Database

1. Go to Supabase dashboard
2. Click "Table Editor"
3. Check tables:
   - `users` - should have your user
   - `chat_sessions` - should have 1 session
   - `chat_messages` - should have 2 messages (user + AI)

---

## Verification Checklist

- [ ] Python service responds to `/health`
- [ ] Spring Boot responds to `/api/auth/validate`
- [ ] Frontend loads at localhost:5173
- [ ] Can register new user
- [ ] Can login
- [ ] Can send message
- [ ] AI response streams word-by-word
- [ ] Message saved to database
- [ ] Can see chat history in sidebar
- [ ] Can view profile
- [ ] Rate limit shows (X/10 messages)

---

## Common Issues & Solutions

### Python Service Won't Start

**Error**: `ModuleNotFoundError`

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

### Spring Boot Can't Connect to Database

**Error**: `Connection refused`

**Solution**:
1. Verify Supabase credentials
2. Check if database is running
3. Test connection:
   ```bash
   psql "postgresql://postgres:PASSWORD@db.xxxxx.supabase.co:5432/postgres"
   ```

### Frontend Can't Connect to Backend

**Error**: `Network Error` or `CORS`

**Solution**:
1. Verify backend is running on port 8080
2. Check CORS configuration in `application.properties`
3. Clear browser cache
4. Check `.env` file has correct API URL

### Streaming Not Working

**Error**: Messages appear all at once

**Solution**:
1. Check Python service is running
2. Verify OpenRouter API key is valid
3. Test non-streaming first
4. Check browser console for errors

### Rate Limit Not Resetting

**Solution**:
```sql
-- Run in Supabase SQL Editor
UPDATE users SET daily_message_count = 0 WHERE email = 'test@example.com';
```

---

## Architecture Overview

```
┌─────────────────────┐
│  React Frontend     │  Port 5173
│  (Vite + Tailwind)  │
└──────────┬──────────┘
           │ HTTP/REST + JWT
           ↓
┌─────────────────────┐
│  Spring Boot API    │  Port 8080
│  (Java + JPA)       │
└──────┬──────────┬───┘
       │          │
       │          └──→ Python FastAPI  Port 8000
       │               (OpenRouter)
       ↓
┌─────────────────────┐
│  PostgreSQL DB      │  Supabase
│  (Users, Sessions,  │
│   Messages)         │
└─────────────────────┘
```

---

## API Endpoints Summary

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login (get JWT)
- `GET /api/auth/validate` - Validate token

### Chat
- `POST /api/chat/message` - Send message (non-streaming)
- `POST /api/chat/message/stream` - Send message (streaming)
- `GET /api/chat/sessions` - Get all sessions
- `GET /api/chat/sessions/{id}` - Get session with messages
- `DELETE /api/chat/sessions/{id}` - Delete session

### User
- `GET /api/user/profile` - Get profile
- `PUT /api/user/profile` - Update profile
- `PUT /api/user/password` - Change password
- `GET /api/user/stats` - Get usage stats

### AI Service
- `POST /chat/` - Generate content
- `POST /chat/stream` - Generate content (streaming)
- `GET /health` - Health check

---

## Next Steps

1. ✅ All services running
2. ✅ Can send messages
3. ✅ Data persists to database
4. 🚀 Ready to deploy!

See `DEPLOYMENT.md` for production deployment guide.

---

## Support

- **Backend Issues**: Check `backend/README.md`
- **Frontend Issues**: Check `frontend/README.md`
- **AI Service Issues**: Check `ai-service/README.md`
- **Database Issues**: Check `database/SUPABASE_SETUP.md`

---

**🎉 Congratulations! Your AI Content Generator is fully operational!**
