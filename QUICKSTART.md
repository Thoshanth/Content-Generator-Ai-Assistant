# ⚡ Quick Start Guide - AI Content Generator

Get the application running in 15 minutes!

## Prerequisites Checklist

- [ ] Node.js 18+ installed
- [ ] Java 17+ installed
- [ ] Python 3.10+ installed
- [ ] Git installed

## Step-by-Step Setup

### 1️⃣ Get OpenRouter API Key (2 minutes)

1. Go to https://openrouter.ai
2. Click "Sign Up" (free, no credit card)
3. After login, go to "Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-or-...`)

### 2️⃣ Setup Supabase Database (5 minutes)

1. Go to https://supabase.com
2. Sign up (free, no credit card)
3. Click "New Project"
   - Name: `ai-content-gen`
   - Password: Create strong password (SAVE IT!)
   - Region: Choose closest
4. Wait 2-3 minutes for setup
5. Go to "SQL Editor" → "New query"
6. Copy entire content from `database/schema.sql`
7. Paste and click "Run"
8. Go to "Settings" → "Database"
9. Copy these values:
   ```
   Host: db.xxxxx.supabase.co
   Password: (your password from step 3)
   ```

### 3️⃣ Start Python AI Service (3 minutes)

```bash
# Navigate to ai-service folder
cd ai-service

# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "OPENROUTER_API_KEY=your_key_from_step_1" > .env

# Start service
uvicorn main:app --reload --port 8000
```

✅ You should see: `Application startup complete`

Keep this terminal open!

### 4️⃣ Start Spring Boot Backend (3 minutes)

Open a NEW terminal:

```bash
# Navigate to backend folder
cd backend

# Edit application.properties
# Open: src/main/resources/application.properties
# Update these lines:
spring.datasource.url=jdbc:postgresql://db.xxxxx.supabase.co:5432/postgres
spring.datasource.password=your_supabase_password

# Start backend
./mvnw spring-boot:run
```

✅ You should see: `Started ContentGeneratorApplication`

Keep this terminal open!

### 5️⃣ Test Everything (2 minutes)

Open a NEW terminal:

```bash
# Test Python service
curl http://localhost:8000/health

# Should return: {"status":"healthy"}

# Test Spring Boot
curl http://localhost:8080/api/auth/validate

# Should return: {"valid":false} (expected, no token provided)
```

### 6️⃣ Create Test User

```bash
# Register a user
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "fullName": "Test User"
  }'

# Login and get token
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

Copy the `token` from the response!

### 7️⃣ Send Your First AI Message

```bash
# Replace YOUR_TOKEN with the token from step 6
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a short professional email about a meeting",
    "contentType": "email"
  }'
```

🎉 **You should get an AI-generated email!**

## Verify Database

1. Go to Supabase dashboard
2. Click "Table Editor"
3. Check `users` table - you should see your test user
4. Check `chat_sessions` table - you should see a session
5. Check `chat_messages` table - you should see 2 messages (user + AI)

## What's Running?

| Service | Port | URL |
|---------|------|-----|
| Python AI Service | 8000 | http://localhost:8000 |
| Spring Boot API | 8080 | http://localhost:8080 |
| API Documentation | 8000 | http://localhost:8000/docs |

## Common Issues

### Python service fails to start
```bash
# Make sure you're in virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Spring Boot can't connect to database
```bash
# Check your application.properties file
# Make sure:
# 1. URL has correct Supabase host
# 2. Password is correct
# 3. No extra spaces in the values
```

### "Daily limit reached" error
```bash
# Reset your daily count in Supabase:
# 1. Go to Table Editor → users
# 2. Find your user
# 3. Set daily_message_count to 0
```

## Next Steps

✅ Backend is running!
✅ Database is set up!
✅ AI service is working!

Now you can:
1. Build the React frontend (coming soon)
2. Test all API endpoints
3. Customize content types
4. Deploy to production

## Testing Different Content Types

```bash
# Blog Post
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write about AI in healthcare","contentType":"blog_post"}'

# Social Media Post
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"LinkedIn post about productivity","contentType":"social_media"}'

# Ad Copy
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Ad for a fitness app","contentType":"ad_copy"}'
```

## Rate Limiting

Free users get **10 messages per day**. To change this:

1. Edit `backend/src/main/resources/application.properties`
2. Change `rate.limit.daily=10` to your desired limit
3. Restart Spring Boot

## Stopping Services

```bash
# Stop Python service: Ctrl+C in its terminal
# Stop Spring Boot: Ctrl+C in its terminal
```

## Need Help?

- Check `README.md` for detailed documentation
- Check `backend/README.md` for API details
- Check `ai-service/README.md` for AI service details
- Check `database/SUPABASE_SETUP.md` for database help

---

**🎉 Congratulations! Your AI Content Generator is running!**
