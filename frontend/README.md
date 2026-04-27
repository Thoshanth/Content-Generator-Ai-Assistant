# AI Content Generator - React Frontend

Modern React frontend with TailwindCSS, streaming AI responses, and complete API integration.

## Features

- ✅ User authentication (Login/Register)
- ✅ Real-time streaming AI responses
- ✅ Multiple content types (Blog, Email, Social, Ad Copy)
- ✅ Chat session management
- ✅ Message history
- ✅ User profile management
- ✅ Rate limiting display
- ✅ Responsive design
- ✅ Blue & white theme with SF Pro font

## Prerequisites

- Node.js 18+ and npm
- Backend API running on port 8080
- Python AI service running on port 8000

## Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

Create `.env` file:

```bash
cp .env.example .env
```

Edit `.env`:

```
VITE_API_BASE_URL=http://localhost:8080/api
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at: http://localhost:5173

## Build for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── ChatWindow.jsx       # Main chat display
│   │   │   ├── MessageBubble.jsx    # Individual messages
│   │   │   ├── InputBar.jsx         # Message input
│   │   │   ├── Sidebar.jsx          # Session list
│   │   │   └── ContentTypeSelector.jsx
│   │   └── ProtectedRoute.jsx       # Auth guard
│   ├── pages/
│   │   ├── LandingPage.jsx          # Home page
│   │   ├── LoginPage.jsx            # Login
│   │   ├── RegisterPage.jsx         # Registration
│   │   ├── ChatPage.jsx             # Main chat interface
│   │   └── ProfilePage.jsx          # User profile
│   ├── context/
│   │   ├── AuthContext.jsx          # Auth state management
│   │   └── ChatContext.jsx          # Chat state management
│   ├── services/
│   │   ├── api.js                   # Axios instance
│   │   ├── authService.js           # Auth API calls
│   │   ├── chatService.js           # Chat API calls
│   │   └── userService.js           # User API calls
│   ├── App.jsx                      # Main app component
│   ├── main.jsx                     # Entry point
│   └── index.css                    # Global styles
├── index.html
├── package.json
├── vite.config.js
└── tailwind.config.js
```

## API Integration

### Authentication

All API calls automatically include JWT token from localStorage:

```javascript
// Login
await authService.login(email, password)

// Register
await authService.register(data)

// Logout
authService.logout()
```

### Chat Operations

```javascript
// Send message (non-streaming)
await chatService.sendMessage(prompt, contentType, sessionId)

// Send message (streaming)
await chatService.sendMessageStream(prompt, contentType, sessionId, onChunk)

// Get sessions
await chatService.getSessions()

// Get session with messages
await chatService.getSession(sessionId)

// Delete session
await chatService.deleteSession(sessionId)
```

### User Operations

```javascript
// Get profile
await userService.getProfile()

// Update profile
await userService.updateProfile(fullName, avatarUrl)

// Change password
await userService.changePassword(oldPassword, newPassword)

// Get stats
await userService.getStats()
```

## Features Explained

### Streaming Responses

The chat uses Server-Sent Events (SSE) for real-time streaming:

```javascript
await chatService.sendMessageStream(prompt, contentType, sessionId, (chunk) => {
  // Handle each chunk as it arrives
  console.log(chunk.content)
})
```

### Rate Limiting

Free users are limited to 10 messages per day. The UI displays:
- Current usage count
- Warning when limit is reached
- Automatic reset at midnight

### Content Types

- **General**: Open-ended conversations
- **Blog Post**: SEO-optimized articles with headings
- **Email**: Professional emails with subject lines
- **Social Media**: Platform-specific posts
- **Ad Copy**: Conversion-focused advertising

### Session Management

- Create new chat sessions
- View all past sessions
- Load previous conversations
- Delete individual sessions
- Delete all sessions

## Styling

### Theme Colors

```css
--primary: #1D6CF2
--primary-dark: #0F4DC9
--primary-light: #E8F0FE
--surface: #F7F9FC
--text-primary: #1A1A2E
--text-secondary: #5F6B7A
```

### Font

SF Pro Display/Text (Apple system font)

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Import repository in Vercel
3. Set environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api
   ```
4. Deploy

### Netlify

1. Build the project: `npm run build`
2. Deploy `dist/` folder
3. Set environment variable in Netlify dashboard

## Troubleshooting

### API Connection Issues

- Verify backend is running on port 8080
- Check CORS configuration in backend
- Ensure `.env` file has correct API URL

### Streaming Not Working

- Check browser console for errors
- Verify Python service is running
- Test with non-streaming first

### Authentication Issues

- Clear localStorage: `localStorage.clear()`
- Check JWT token expiration (24 hours)
- Verify backend auth endpoints

## Development Tips

### Hot Reload

Vite provides instant hot module replacement. Changes appear immediately without full page reload.

### API Proxy

Vite is configured to proxy `/api` requests to `http://localhost:8080` in development.

### State Management

- `AuthContext`: User authentication state
- `ChatContext`: Chat sessions and messages

## Testing

### Manual Testing

1. Register a new user
2. Login
3. Send a message
4. Check streaming works
5. Test all content types
6. Verify session management
7. Test profile updates

### API Testing

Use browser DevTools Network tab to inspect:
- Request/response payloads
- Status codes
- Headers (Authorization)
- Streaming events

## License

MIT
