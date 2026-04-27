# Backend API Documentation

Base URL: `http://localhost:8080`

## Table of Contents
- [Authentication APIs](#authentication-apis)
- [User APIs](#user-apis)
- [Chat APIs](#chat-apis)
- [Error Responses](#error-responses)

---

## Authentication APIs

### 1. Register User

**Endpoint:** `POST /api/auth/register`

**Description:** Register a new user account

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123",
  "fullName": "John Doe"
}
```

**Response (200 OK):**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": "cBRkOSJRLiVs4fDunwe2",
    "email": "user@example.com",
    "username": "username",
    "fullName": "John Doe",
    "plan": "free",
    "dailyMessageCount": 0,
    "createdAt": "2024-12-15T10:30:00"
  }
}
```

**Error Responses:**
- `400 Bad Request` - Email or username already exists
- `400 Bad Request` - Invalid input data

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "username",
    "password": "password123",
    "fullName": "John Doe"
  }'
```

---

### 2. Login User

**Endpoint:** `POST /api/auth/login`

**Description:** Login and get JWT access and refresh tokens

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "message": "Login successful",
  "expiresIn": 900
}
```

**Token Details:**
- `accessToken`: Short-lived token (15 minutes) for API access
- `refreshToken`: Long-lived token (7 days) for refreshing access tokens
- `expiresIn`: Access token expiration time in seconds

**Error Responses:**
- `401 Unauthorized` - Invalid credentials
- `400 Bad Request` - Missing email or password

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

---

### 3. Refresh Access Token

**Endpoint:** `POST /api/auth/refresh`

**Description:** Get a new access token using refresh token

**Request Body:**
```json
{
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Response (200 OK):**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "type": "Bearer",
  "message": "Token refreshed successfully",
  "expiresIn": 900
}
```

**Error Responses:**
- `400 Bad Request` - Invalid or expired refresh token
- `400 Bad Request` - Missing refresh token

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{
    "refreshToken": "your-refresh-token-here"
  }'
```

---

### 4. Validate Token

**Endpoint:** `GET /api/auth/validate`

**Description:** Validate current access token

**Headers:**
```
Authorization: Bearer <access-token>
```

**Response (200 OK):**
```json
{
  "valid": true,
  "userId": "cBRkOSJRLiVs4fDunwe2"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8080/api/auth/validate \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## User APIs

**Authentication Required:** All user APIs require JWT access token in Authorization header

**Header Format:**
```
Authorization: Bearer <your-access-token>
```

---

### 5. Get User Profile

**Endpoint:** `GET /api/user/profile`

**Description:** Get current user's profile with statistics

**Response (200 OK):**
```json
{
  "id": "cBRkOSJRLiVs4fDunwe2",
  "email": "user@example.com",
  "username": "username",
  "fullName": "John Doe",
  "avatarUrl": "https://example.com/avatar.jpg",
  "plan": "free",
  "createdAt": "2024-12-15T10:30:00",
  "totalSessions": 5,
  "totalMessages": 42,
  "dailyMessageCount": 10
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

### 4. Update User Profile

**Endpoint:** `PUT /api/user/profile`

**Description:** Update user's profile information

**Request Body:**
```json
{
  "fullName": "John Smith",
  "avatarUrl": "https://example.com/new-avatar.jpg"
}
```

**Response (200 OK):**
```json
{
  "message": "Profile updated successfully",
  "user": {
    "id": "cBRkOSJRLiVs4fDunwe2",
    "email": "user@example.com",
    "username": "username",
    "fullName": "John Smith",
    "avatarUrl": "https://example.com/new-avatar.jpg",
    "plan": "free"
  }
}
```

**cURL Example:**
```bash
curl -X PUT http://localhost:8080/api/user/profile \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "fullName": "John Smith",
    "avatarUrl": "https://example.com/new-avatar.jpg"
  }'
```

---

### 5. Change Password

**Endpoint:** `PUT /api/user/password`

**Description:** Change user's password

**Request Body:**
```json
{
  "oldPassword": "password123",
  "newPassword": "newpassword456"
}
```

**Response (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

**Error Responses:**
- `400 Bad Request` - Current password is incorrect

**cURL Example:**
```bash
curl -X PUT http://localhost:8080/api/user/password \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "oldPassword": "password123",
    "newPassword": "newpassword456"
  }'
```

---

### 6. Get User Statistics

**Endpoint:** `GET /api/user/stats`

**Description:** Get detailed user statistics

**Response (200 OK):**
```json
{
  "totalSessions": 5,
  "totalMessages": 42,
  "userMessages": 21,
  "dailyMessageCount": 10,
  "lastMessageDate": "2024-12-15T14:30:00"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8080/api/user/stats \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 7. Delete User Account

**Endpoint:** `DELETE /api/user/account`

**Description:** Delete user account and all associated data

**Response (200 OK):**
```json
{
  "message": "Account deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8080/api/user/account \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Chat APIs

**Authentication Required:** All chat APIs require JWT token

---

### 8. Send Message (Non-Streaming)

**Endpoint:** `POST /api/chat/message`

**Description:** Send a message and get AI response

**Request Body:**
```json
{
  "prompt": "Write a blog post about AI",
  "sessionId": "xYz9AbC123dEf456",
  "contentType": "blog",
  "sessionTitle": "AI Blog Post"
}
```

**Fields:**
- `prompt` (required): The user's message
- `sessionId` (optional): Existing session ID, creates new if not provided
- `contentType` (optional): Type of content (general, blog, social, email, code, creative)
- `sessionTitle` (optional): Title for new session

**Response (200 OK):**
```json
{
  "sessionId": "xYz9AbC123dEf456",
  "content": "Here's a blog post about AI...",
  "modelUsed": "nvidia/llama-3.1-nemotron-70b-instruct:free",
  "tokensUsed": 450,
  "messageId": "pQr7StU890vWx123"
}
```

**Error Responses:**
- `429 Too Many Requests` - Daily message limit reached (if rate limiting enabled)
- `400 Bad Request` - Invalid request

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/chat/message \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a blog post about AI",
    "contentType": "blog"
  }'
```

---

### 9. Send Message (Streaming)

**Endpoint:** `POST /api/chat/message/stream`

**Description:** Send a message and get AI response as Server-Sent Events (SSE)

**Request Body:** Same as non-streaming endpoint

**Response:** Server-Sent Events stream

**Content-Type:** `text/event-stream`

**Event Format:**
```
data: {"chunk": "Here's"}
data: {"chunk": " a"}
data: {"chunk": " blog"}
data: {"chunk": " post"}
data: [DONE]
```

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/chat/message/stream \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Write a blog post about AI",
    "contentType": "blog"
  }'
```

**JavaScript Example:**
```javascript
const eventSource = new EventSource(
  'http://localhost:8080/api/chat/message/stream',
  {
    headers: {
      'Authorization': 'Bearer YOUR_JWT_TOKEN'
    }
  }
);

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data === '[DONE]') {
    eventSource.close();
  } else {
    console.log(data.chunk);
  }
};
```

---

### 10. Get All Chat Sessions

**Endpoint:** `GET /api/chat/sessions`

**Description:** Get all chat sessions for the current user

**Response (200 OK):**
```json
[
  {
    "id": "xYz9AbC123dEf456",
    "userId": "cBRkOSJRLiVs4fDunwe2",
    "title": "AI Blog Post",
    "contentType": "blog",
    "createdAt": "2024-12-15T10:30:00",
    "updatedAt": "2024-12-15T14:30:00"
  },
  {
    "id": "aBc1DeF234gHi567",
    "userId": "cBRkOSJRLiVs4fDunwe2",
    "title": "Social Media Content",
    "contentType": "social",
    "createdAt": "2024-12-14T09:00:00",
    "updatedAt": "2024-12-14T09:45:00"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:8080/api/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 11. Get Session with Messages

**Endpoint:** `GET /api/chat/sessions/{sessionId}`

**Description:** Get a specific session with all its messages

**Path Parameters:**
- `sessionId`: The session ID

**Response (200 OK):**
```json
{
  "id": "xYz9AbC123dEf456",
  "userId": "cBRkOSJRLiVs4fDunwe2",
  "title": "AI Blog Post",
  "contentType": "blog",
  "createdAt": "2024-12-15T10:30:00",
  "updatedAt": "2024-12-15T14:30:00",
  "messages": [
    {
      "id": "msg1",
      "sessionId": "xYz9AbC123dEf456",
      "role": "user",
      "content": "Write a blog post about AI",
      "modelUsed": null,
      "tokensUsed": null,
      "createdAt": "2024-12-15T10:30:00"
    },
    {
      "id": "msg2",
      "sessionId": "xYz9AbC123dEf456",
      "role": "assistant",
      "content": "Here's a blog post about AI...",
      "modelUsed": "nvidia/llama-3.1-nemotron-70b-instruct:free",
      "tokensUsed": 450,
      "createdAt": "2024-12-15T10:30:15"
    }
  ]
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8080/api/chat/sessions/xYz9AbC123dEf456 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 12. Create New Chat Session

**Endpoint:** `POST /api/chat/sessions`

**Description:** Create a new empty chat session

**Request Body:**
```json
{
  "title": "My New Chat",
  "contentType": "general"
}
```

**Response (200 OK):**
```json
{
  "id": "newSessionId123",
  "userId": "cBRkOSJRLiVs4fDunwe2",
  "title": "My New Chat",
  "contentType": "general",
  "createdAt": "2024-12-15T15:00:00",
  "updatedAt": "2024-12-15T15:00:00"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8080/api/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Chat",
    "contentType": "general"
  }'
```

---

### 13. Delete Chat Session

**Endpoint:** `DELETE /api/chat/sessions/{sessionId}`

**Description:** Delete a specific chat session and all its messages

**Path Parameters:**
- `sessionId`: The session ID to delete

**Response (200 OK):**
```json
{
  "message": "Session deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8080/api/chat/sessions/xYz9AbC123dEf456 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

### 14. Delete All Chat Sessions

**Endpoint:** `DELETE /api/chat/sessions`

**Description:** Delete all chat sessions for the current user

**Response (200 OK):**
```json
{
  "message": "All sessions deleted successfully"
}
```

**cURL Example:**
```bash
curl -X DELETE http://localhost:8080/api/chat/sessions \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Content Types

Available content types for chat sessions:

| Type | Description |
|------|-------------|
| `general` | General conversation |
| `blog` | Blog post generation |
| `social` | Social media content |
| `email` | Email writing |
| `code` | Code generation |
| `creative` | Creative writing |

---

## Error Responses

### Standard Error Format

```json
{
  "error": "Error message description"
}
```

### HTTP Status Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `400` | Bad Request - Invalid input |
| `401` | Unauthorized - Invalid or missing token |
| `403` | Forbidden - Access denied |
| `404` | Not Found - Resource doesn't exist |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error |

---

## Authentication Flow

### 1. Register or Login
```bash
# Register
POST /api/auth/register
# or Login
POST /api/auth/login
```

### 2. Save JWT Tokens
```javascript
const response = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ email, password })
});
const { accessToken, refreshToken } = await response.json();
localStorage.setItem('accessToken', accessToken);
localStorage.setItem('refreshToken', refreshToken);
```

### 3. Use Access Token in Requests
```javascript
const accessToken = localStorage.getItem('accessToken');
fetch('/api/user/profile', {
  headers: {
    'Authorization': `Bearer ${accessToken}`
  }
});
```

### 4. Handle Token Refresh
```javascript
// Automatic refresh when access token expires
const refreshAccessToken = async () => {
  const refreshToken = localStorage.getItem('refreshToken');
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refreshToken })
  });
  const { accessToken: newAccessToken, refreshToken: newRefreshToken } = await response.json();
  localStorage.setItem('accessToken', newAccessToken);
  localStorage.setItem('refreshToken', newRefreshToken);
  return newAccessToken;
};
```

---

## Rate Limiting

Rate limiting is **disabled by default** but can be enabled in configuration.

**Configuration:**
```properties
rate.limit.enabled=true
rate.limit.daily=1000
```

**When enabled:**
- Free users: 1000 messages per day
- Returns `429 Too Many Requests` when limit exceeded

**Response when limit reached:**
```json
{
  "error": "Daily message limit reached",
  "limit": 1000
}
```

---

## Testing with Postman

### Import Collection

1. Create a new collection in Postman
2. Add environment variables:
   - `baseUrl`: `http://localhost:8080`
   - `token`: (will be set after login)

### Example Workflow

1. **Register User**
   - POST `{{baseUrl}}/api/auth/register`
   - Save response

2. **Login**
   - POST `{{baseUrl}}/api/auth/login`
   - Save token from response
   - Set `token` environment variable

3. **Get Profile**
   - GET `{{baseUrl}}/api/user/profile`
   - Header: `Authorization: Bearer {{token}}`

4. **Send Message**
   - POST `{{baseUrl}}/api/chat/message`
   - Header: `Authorization: Bearer {{token}}`
   - Body: `{ "prompt": "Hello", "contentType": "general" }`

---

## WebSocket / SSE Support

The streaming endpoint uses **Server-Sent Events (SSE)** for real-time streaming responses.

**Browser Support:**
- Chrome: ✅
- Firefox: ✅
- Safari: ✅
- Edge: ✅

**Example Implementation:**
```javascript
const sendStreamingMessage = async (prompt) => {
  const response = await fetch('/api/chat/message/stream', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ prompt, contentType: 'general' })
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    
    const chunk = decoder.decode(value);
    console.log(chunk);
  }
};
```

---

## CORS Configuration

CORS is configured to allow requests from:
- `http://localhost:5173` (Vite dev server)
- `http://localhost:3000` (React dev server)

**To add more origins:**
Edit `application.properties`:
```properties
cors.allowed.origins=http://localhost:5173,http://localhost:3000,https://yourdomain.com
```

---

## API Versioning

Current version: **v1** (implicit in `/api/` prefix)

Future versions will use: `/api/v2/`, `/api/v3/`, etc.

---

## Support

For issues or questions:
1. Check error response messages
2. Review logs in console
3. Verify JWT token is valid
4. Ensure Firebase is configured correctly

---

**Last Updated:** Firebase Migration - December 2024
