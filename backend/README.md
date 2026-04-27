# AI Content Generator - Spring Boot Backend

Java Spring Boot REST API backend with JWT authentication, PostgreSQL database integration, and AI service proxy.

## Features

- ✅ JWT-based authentication
- ✅ User registration and login
- ✅ PostgreSQL database with JPA/Hibernate
- ✅ Chat session management
- ✅ Message history storage
- ✅ Rate limiting (10 messages/day for free users)
- ✅ AI service proxy (calls Python FastAPI)
- ✅ Streaming and non-streaming responses
- ✅ CORS configuration
- ✅ RESTful API design

## Prerequisites

- Java 17 or higher
- Maven 3.6+
- PostgreSQL database (Supabase recommended)
- Python AI service running (see `ai-service/README.md`)

## Setup

### 1. Database Setup

Follow the complete guide in `database/SUPABASE_SETUP.md` to:
1. Create free Supabase account
2. Create new project
3. Run database schema
4. Get connection details

### 2. Configure Application

Create `src/main/resources/application-local.properties`:

```properties
# Database Configuration
spring.datasource.url=jdbc:postgresql://db.<your-project-ref>.supabase.co:5432/postgres
spring.datasource.username=postgres
spring.datasource.password=<your-database-password>

# JWT Configuration
jwt.secret=your-256-bit-secret-key-change-this-in-production-make-it-long
jwt.expiration=86400000

# Python AI Service
ai.service.url=http://localhost:8000

# Rate Limiting
rate.limit.daily=10
rate.limit.enabled=true

# CORS
cors.allowed.origins=http://localhost:5173,http://localhost:3000
```

### 3. Install Dependencies

```bash
./mvnw clean install
```

### 4. Run Application

```bash
./mvnw spring-boot:run
```

Or with specific profile:

```bash
./mvnw spring-boot:run -Dspring-boot.run.profiles=local
```

The API will be available at: http://localhost:8080

## API Endpoints

### Authentication Endpoints

#### Register
```bash
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "johndoe",
  "password": "password123",
  "fullName": "John Doe"
}
```

#### Login
```bash
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "message": "Login successful"
}
```

#### Validate Token
```bash
GET /api/auth/validate
Authorization: Bearer <token>
```

### User Endpoints

#### Get Profile
```bash
GET /api/user/profile
Authorization: Bearer <token>
```

#### Update Profile
```bash
PUT /api/user/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "fullName": "John Updated",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

#### Change Password
```bash
PUT /api/user/password
Authorization: Bearer <token>
Content-Type: application/json

{
  "oldPassword": "password123",
  "newPassword": "newpassword456"
}
```

#### Get User Stats
```bash
GET /api/user/stats
Authorization: Bearer <token>
```

#### Delete Account
```bash
DELETE /api/user/account
Authorization: Bearer <token>
```

### Chat Endpoints

#### Send Message (Non-Streaming)
```bash
POST /api/chat/message
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Write a blog post about AI in healthcare",
  "contentType": "blog_post",
  "sessionId": "optional-existing-session-id",
  "sessionTitle": "Healthcare AI Blog"
}

Response:
{
  "sessionId": "uuid",
  "content": "Generated content...",
  "modelUsed": "nvidia/llama-3.1-nemotron-70b-instruct:free",
  "tokensUsed": 342,
  "messageId": "uuid"
}
```

#### Send Message (Streaming)
```bash
POST /api/chat/message/stream
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "Write an email",
  "contentType": "email",
  "sessionId": "optional-session-id"
}

Response: Server-Sent Events (SSE) stream
```

#### Get All Sessions
```bash
GET /api/chat/sessions
Authorization: Bearer <token>
```

#### Get Session with Messages
```bash
GET /api/chat/sessions/{sessionId}
Authorization: Bearer <token>
```

#### Create New Session
```bash
POST /api/chat/sessions
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "My New Chat",
  "contentType": "general"
}
```

#### Delete Session
```bash
DELETE /api/chat/sessions/{sessionId}
Authorization: Bearer <token>
```

#### Delete All Sessions
```bash
DELETE /api/chat/sessions
Authorization: Bearer <token>
```

## Database Operations

All services interact with the database using Spring Data JPA repositories:

### UserService
- `getUserById()` - Fetch user from database by ID
- `getUserByEmail()` - Fetch user from database by email
- `updateUserProfile()` - Update user data in database
- `changePassword()` - Update password hash in database
- `deleteUserAccount()` - Delete user and cascade delete sessions/messages
- `hasReachedDailyLimit()` - Check rate limit from database
- `incrementDailyMessageCount()` - Update message count in database

### ChatService
- `createSession()` - Insert new session into database
- `getUserSessions()` - Fetch all user sessions from database
- `getSessionById()` - Fetch session from database with ownership check
- `getSessionWithMessages()` - Fetch session and all messages from database
- `saveUserMessage()` - Insert user message into database
- `saveAssistantMessage()` - Insert AI response into database
- `getLastNMessages()` - Fetch last N messages for context from database
- `deleteSession()` - Delete session and messages from database
- `deleteAllUserSessions()` - Delete all user sessions from database

### AuthService
- `register()` - Insert new user into database
- `login()` - Authenticate user from database and generate JWT

## Rate Limiting

Free users are limited to 10 messages per day. The limit resets at midnight.

- Limit is stored in database (`users.daily_message_count`)
- Automatically resets when date changes
- Returns 429 status when limit reached

## Security

- Passwords hashed with BCrypt
- JWT tokens for stateless authentication
- CORS configured for frontend origins
- SQL injection prevention via JPA
- Input validation with Jakarta Validation

## Testing

### Test with cURL

```bash
# Register
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","fullName":"Test User"}'

# Login
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Get Profile (replace <token>)
curl -X GET http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer <token>"

# Send Message
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"Write a short email","contentType":"email"}'
```

## Project Structure

```
backend/
├── src/main/java/com/contentgen/
│   ├── ContentGeneratorApplication.java    # Main application
│   ├── config/
│   │   ├── SecurityConfig.java            # Security & CORS
│   │   ├── WebClientConfig.java           # WebClient bean
│   │   └── CustomUserDetailsService.java  # User details loader
│   ├── controllers/
│   │   ├── AuthController.java            # Auth endpoints
│   │   ├── UserController.java            # User endpoints
│   │   └── ChatController.java            # Chat endpoints
│   ├── services/
│   │   ├── AuthService.java               # Auth logic + DB
│   │   ├── UserService.java               # User logic + DB
│   │   ├── ChatService.java               # Chat logic + DB
│   │   └── AIProxyService.java            # Python service proxy
│   ├── repositories/
│   │   ├── UserRepository.java            # User DB operations
│   │   ├── ChatSessionRepository.java     # Session DB operations
│   │   └── ChatMessageRepository.java     # Message DB operations
│   ├── models/
│   │   ├── User.java                      # User entity
│   │   ├── ChatSession.java               # Session entity
│   │   └── ChatMessage.java               # Message entity
│   ├── dto/
│   │   ├── LoginRequest.java
│   │   ├── RegisterRequest.java
│   │   ├── ChatRequest.java
│   │   ├── ChatResponse.java
│   │   ├── UserProfileDTO.java
│   │   └── ...
│   └── security/
│       ├── JwtUtil.java                   # JWT generation/validation
│       └── JwtFilter.java                 # JWT authentication filter
└── src/main/resources/
    └── application.properties             # Configuration
```

## Deployment

### Render (Free Tier)

1. Create new Web Service on Render
2. Connect your GitHub repository
3. Configure:
   - **Build Command**: `./mvnw clean package -DskipTests`
   - **Start Command**: `java -jar target/ai-content-generator-1.0.0.jar`
4. Add environment variables:
   ```
   SUPABASE_HOST=db.<project-ref>.supabase.co
   SUPABASE_PASSWORD=<your-password>
   JWT_SECRET=<your-secret>
   AI_SERVICE_URL=<python-service-url>
   ```

### Railway (Free Tier)

1. Create new project on Railway
2. Connect repository
3. Railway auto-detects Java/Maven
4. Add environment variables (same as above)

## Troubleshooting

### Database Connection Failed
- Verify Supabase credentials
- Check if database is accessible
- Test connection with psql or DBeaver

### JWT Token Invalid
- Check JWT secret is configured
- Verify token format: `Bearer <token>`
- Token expires after 24 hours

### AI Service Connection Failed
- Ensure Python service is running on port 8000
- Check `ai.service.url` configuration
- Verify network connectivity

### Rate Limit Not Working
- Check `rate.limit.enabled=true`
- Verify database updates are working
- Check user's `daily_message_count` in database

## License

MIT
