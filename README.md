# 🤖 AI Content Generator - Full Stack Application

A modern, full-stack AI-powered content generation web application with React frontend, Java Spring Boot backend, Python FastAPI AI service, and PostgreSQL database.

![Tech Stack](https://img.shields.io/badge/React-18-blue)
![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2-green)
![Python](https://img.shields.io/badge/Python-3.10+-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)

## ✨ Features

- 🎨 **Multiple Content Types**: Blog posts, emails, social media posts, ad copy
- 🔐 **Secure Authentication**: JWT-based auth with bcrypt password hashing
- 💬 **Chat Interface**: Conversational AI with message history
- 📊 **User Dashboard**: Profile management, usage statistics
- ⚡ **Streaming Responses**: Real-time word-by-word AI generation
- 🎯 **Rate Limiting**: 10 messages/day for free users
- 🗄️ **Persistent Storage**: All chats saved to PostgreSQL database
- 🔄 **AI Fallback**: Automatic fallback across 3 free LLM models
- 🎭 **Modern UI**: Blue & white theme with SF Pro font

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │ (Port 5173)
│   (Vite + Tailwind)
└────────┬────────┘
         │ HTTP/REST + JWT
         ↓
┌─────────────────┐
│ Spring Boot API │ (Port 8080)
│  (Java 17 + JPA)
└────────┬────────┘
         │
         ├─→ PostgreSQL (Supabase)
         │   └─ Users, Sessions, Messages
         │
         └─→ Python FastAPI (Port 8000)
             └─ OpenRouter LLM API
                 ├─ meta-llama/llama-3.2-3b-instruct:free
                 ├─ google/gemini-flash-1.5:free
                 └─ qwen/qwen-2-7b-instruct:free
```

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Java** 17+
- **Maven** 3.6+
- **Python** 3.10+
- **PostgreSQL** (Supabase free tier)
- **OpenRouter API Key** (free at [openrouter.ai](https://openrouter.ai))

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <your-repo-url>
cd ai-content-generator
```

### 2. Setup Database

Follow the complete guide: [`database/SUPABASE_SETUP.md`](database/SUPABASE_SETUP.md)

**Quick steps:**
1. Create free account at [supabase.com](https://supabase.com)
2. Create new project
3. Run `database/schema.sql` in SQL Editor
4. Copy connection details

### 3. Setup Python AI Service

```bash
cd ai-service

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your OpenRouter API key

# Run service
uvicorn main:app --reload --port 8000
```

**Get OpenRouter API Key:**
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up (free, no credit card)
3. Create API key in dashboard

### 4. Setup Spring Boot Backend

```bash
cd backend

# Configure database connection
# Edit src/main/resources/application.properties
# Add your Supabase credentials

# Run application
./mvnw spring-boot:run
```

### 5. Setup React Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure API endpoint
# Create .env file:
echo "VITE_API_BASE_URL=http://localhost:8080/api" > .env

# Run development server
npm run dev
```

### 6. Access Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **AI Service**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📁 Project Structure

```
ai-content-generator/
├── ai-service/                 # Python FastAPI AI Service
│   ├── main.py                # FastAPI entry point
│   ├── routers/
│   │   └── chat.py           # Chat endpoints (streaming & non-streaming)
│   ├── services/
│   │   └── openrouter.py     # OpenRouter client with fallback
│   ├── models/
│   │   └── schemas.py        # Pydantic models
│   ├── prompts/
│   │   └── templates.py      # Content-type specific prompts
│   └── requirements.txt
│
├── backend/                    # Java Spring Boot Backend
│   ├── src/main/java/com/contentgen/
│   │   ├── controllers/      # REST API endpoints
│   │   │   ├── AuthController.java
│   │   │   ├── UserController.java
│   │   │   └── ChatController.java
│   │   ├── services/         # Business logic + DB operations
│   │   │   ├── AuthService.java
│   │   │   ├── UserService.java
│   │   │   ├── ChatService.java
│   │   │   └── AIProxyService.java
│   │   ├── repositories/     # Database access layer
│   │   │   ├── UserRepository.java
│   │   │   ├── ChatSessionRepository.java
│   │   │   └── ChatMessageRepository.java
│   │   ├── models/           # JPA entities
│   │   │   ├── User.java
│   │   │   ├── ChatSession.java
│   │   │   └── ChatMessage.java
│   │   ├── security/         # JWT authentication
│   │   │   ├── JwtUtil.java
│   │   │   └── JwtFilter.java
│   │   └── config/           # Spring configuration
│   └── pom.xml
│
├── frontend/                   # React Frontend (Coming next)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── context/
│   └── package.json
│
└── database/
    ├── schema.sql             # PostgreSQL schema
    └── SUPABASE_SETUP.md      # Database setup guide
```

## 🔑 Environment Variables

### Python AI Service (`.env`)
```bash
OPENROUTER_API_KEY=your_key_here
SERVICE_PORT=8000
```

### Spring Boot Backend (`application.properties`)
```properties
spring.datasource.url=jdbc:postgresql://db.<project-ref>.supabase.co:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=your_password
jwt.secret=your-secret-key
ai.service.url=http://localhost:8000
rate.limit.daily=10
```

### React Frontend (`.env`)
```bash
VITE_API_BASE_URL=http://localhost:8080/api
```

## 🎯 Content Types

| Type | Description | Use Case |
|------|-------------|----------|
| **Blog Post** | SEO-optimized articles with headings | Content marketing, thought leadership |
| **Email** | Professional emails with subject lines | Business communication |
| **Social Media** | Platform-specific posts | LinkedIn, Twitter, Instagram, Facebook |
| **Ad Copy** | Conversion-focused copy with CTA | Marketing campaigns, ads |
| **General** | Open-ended content generation | Any other use case |

## 🔒 Security Features

- ✅ JWT token authentication
- ✅ BCrypt password hashing
- ✅ CORS configuration
- ✅ SQL injection prevention (JPA)
- ✅ Input validation
- ✅ Rate limiting
- ✅ Secure password requirements

## 📊 Database Schema

### Users Table
- User authentication and profile data
- Daily message count tracking
- Plan management (free/premium)

### Chat Sessions Table
- Conversation grouping
- Content type tracking
- Timestamps for sorting

### Chat Messages Table
- User and AI messages
- Model and token tracking
- Full conversation history

See [`database/schema.sql`](database/schema.sql) for complete schema.

## 🧪 Testing

### Test Python AI Service
```bash
curl -X POST "http://localhost:8000/chat/" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a short email","content_type":"email"}'
```

### Test Spring Boot Backend
```bash
# Register
curl -X POST "http://localhost:8080/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123"}'

# Login
curl -X POST "http://localhost:8080/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'
```

## 🚢 Deployment

### Free Hosting Options

| Service | Component | Free Tier |
|---------|-----------|-----------|
| **Vercel** | React Frontend | Unlimited |
| **Render** | Spring Boot | 750 hrs/month |
| **Render** | Python FastAPI | 750 hrs/month |
| **Supabase** | PostgreSQL | 500 MB |

### Deployment Guides

- **Frontend**: See `frontend/README.md` (coming soon)
- **Backend**: See `backend/README.md`
- **AI Service**: See `ai-service/README.md`
- **Database**: See `database/SUPABASE_SETUP.md`

## 📚 API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get JWT token
- `GET /api/auth/validate` - Validate token

### User Management
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `PUT /api/user/password` - Change password
- `GET /api/user/stats` - Get usage statistics
- `DELETE /api/user/account` - Delete account

### Chat
- `POST /api/chat/message` - Send message (non-streaming)
- `POST /api/chat/message/stream` - Send message (streaming)
- `GET /api/chat/sessions` - Get all sessions
- `GET /api/chat/sessions/{id}` - Get session with messages
- `POST /api/chat/sessions` - Create new session
- `DELETE /api/chat/sessions/{id}` - Delete session

Full API documentation: http://localhost:8000/docs (Python service)

## 🛠️ Development

### Run All Services

```bash
# Terminal 1: Python AI Service
cd ai-service && uvicorn main:app --reload

# Terminal 2: Spring Boot Backend
cd backend && ./mvnw spring-boot:run

# Terminal 3: React Frontend
cd frontend && npm run dev
```

### Database Migrations

When updating schema:
1. Modify `database/schema.sql`
2. Run in Supabase SQL Editor
3. Update JPA entities in `backend/src/main/java/com/contentgen/models/`

## 🐛 Troubleshooting

### Python Service Won't Start
- Check OpenRouter API key in `.env`
- Verify Python 3.10+ installed
- Install dependencies: `pip install -r requirements.txt`

### Spring Boot Connection Error
- Verify Supabase credentials
- Check database is running
- Test connection with psql

### Frontend Can't Connect
- Check backend is running on port 8080
- Verify CORS configuration
- Check `.env` file has correct API URL

### Rate Limit Issues
- Check `rate.limit.enabled` in application.properties
- Verify user's `daily_message_count` in database
- Limit resets at midnight

## 📝 License

MIT License - feel free to use this project for learning or commercial purposes.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📧 Support

- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions
- **Email**: your-email@example.com

## 🎉 Acknowledgments

- OpenRouter for free LLM access
- Supabase for free PostgreSQL hosting
- Spring Boot and FastAPI communities

---

**Built with ❤️ using React, Spring Boot, FastAPI, and PostgreSQL**

**Status**: ✅ Backend Complete | ✅ Frontend Complete | 🚀 Ready to Deploy
