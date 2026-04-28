# Chat History Debugging Guide

## Issue
Chat history not appearing in sidebar after login.

## Changes Made

### 1. Fixed ChatContext.jsx
- Added `useCallback` to `loadSessions` to prevent unnecessary re-renders
- Added comprehensive console logging for debugging
- Better error handling with detailed error messages

### 2. Fixed ChatPage.jsx
- Added `loadSessions` to useEffect dependency array
- Added error handling with toast notifications
- Added console logging for debugging

### 3. Fixed Sidebar.jsx
- Added `useEffect` import
- Added debug logging to track sessions updates
- Sessions are properly grouped by date

## How to Debug

### Step 1: Check Browser Console
Open browser DevTools (F12) and look for these logs:

```
ChatPage: Loading sessions for authenticated user
ChatContext: Fetching sessions from API...
ChatContext: Received sessions data: [...]
ChatContext: Setting X sessions
Sidebar: Sessions updated: X [...]
```

### Step 2: Check Authentication
Run this in browser console:
```javascript
localStorage.getItem('accessToken')
```

Should return a JWT token. If null, user is not logged in.

### Step 3: Test API Directly
1. Open `frontend/test-api.html` in browser
2. Click "Test Auth" to verify token exists
3. Click "Test Get Sessions" to see raw API response

### Step 4: Check Backend
Verify backend is running on `http://localhost:8080`

Test endpoint directly:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/chat/sessions
```

### Step 5: Check Network Tab
1. Open DevTools → Network tab
2. Filter by "sessions"
3. Look for GET request to `/api/chat/sessions`
4. Check:
   - Status code (should be 200)
   - Response body (should be array of sessions)
   - Request headers (should include Authorization)

## Expected API Response Format

```json
[
  {
    "id": "session-id-123",
    "userId": "user-id-456",
    "title": "My Chat Session",
    "contentType": "general",
    "createdAt": {
      "seconds": 1714262400,
      "nanos": 0
    },
    "updatedAt": {
      "seconds": 1714262400,
      "nanos": 0
    },
    "messages": []
  }
]
```

## Common Issues & Solutions

### Issue 1: Empty Array Returned
**Symptom**: API returns `[]`
**Cause**: User has no chat sessions yet
**Solution**: Send a message to create first session

### Issue 2: 401 Unauthorized
**Symptom**: API returns 401 status
**Cause**: Token expired or invalid
**Solution**: 
- Logout and login again
- Check token refresh logic in `api.js`

### Issue 3: CORS Error
**Symptom**: Console shows CORS policy error
**Cause**: Backend CORS not configured for frontend URL
**Solution**: Check `SecurityConfig.java` CORS settings

### Issue 4: Network Error
**Symptom**: "Failed to fetch" or network error
**Cause**: Backend not running or wrong URL
**Solution**: 
- Verify backend is running: `http://localhost:8080`
- Check `.env` file: `VITE_API_BASE_URL=http://localhost:8080/api`

### Issue 5: Sessions Not Grouping
**Symptom**: Sessions appear but not grouped by date
**Cause**: Invalid timestamp format
**Solution**: Check `updatedAt` field has `seconds` property

## Testing Checklist

- [ ] Backend running on port 8080
- [ ] Frontend running on port 5173
- [ ] User is logged in (token in localStorage)
- [ ] Console shows "Loading sessions" log
- [ ] Console shows "Received sessions data" log
- [ ] Network tab shows 200 response for /sessions
- [ ] Sessions array is not empty
- [ ] Sidebar shows sessions grouped by date

## Manual Test Steps

1. **Start Backend**
   ```bash
   cd backend
   ./run.bat  # or ./run.sh on Linux/Mac
   ```

2. **Start Frontend**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Login**
   - Go to http://localhost:5173
   - Click "Sign In"
   - Enter credentials
   - Should redirect to /chat

4. **Check Sidebar**
   - Sidebar should be open on left
   - Should show "Creo" header
   - Should show search bar
   - Should show sessions grouped by date

5. **Send Test Message**
   - Type a message in input bar
   - Click send
   - Wait for response
   - Refresh page
   - Session should appear in sidebar

## Code Flow

```
User Login
  ↓
AuthContext sets user
  ↓
ChatPage useEffect detects isAuthenticated
  ↓
Calls loadSessions()
  ↓
ChatContext.loadSessions()
  ↓
chatService.getSessions()
  ↓
api.get('/chat/sessions')
  ↓
Backend ChatController.getSessions()
  ↓
Returns List<ChatSessionDTO>
  ↓
ChatContext sets sessions state
  ↓
Sidebar receives sessions via useChat()
  ↓
Sidebar groups sessions by date
  ↓
Renders session list
```

## Environment Variables

Ensure `.env` file exists in `frontend/` directory:

```env
VITE_API_BASE_URL=http://localhost:8080/api
VITE_AI_SERVICE_URL=http://localhost:8000
```

## Backend Configuration

Check `backend/.env`:

```env
SPRING_PROFILES_ACTIVE=dev
SERVER_PORT=8080
```

Check `backend/src/main/resources/application.properties`:

```properties
server.port=8080
```

## Quick Fix Commands

### Clear localStorage (if token is corrupted)
```javascript
localStorage.clear()
location.reload()
```

### Force reload sessions
```javascript
// In browser console
window.location.reload()
```

### Check if sessions exist in database
Look at Firebase Console → Firestore → `chat_sessions` collection

## Success Indicators

✅ Console shows: "ChatContext: Setting X sessions" (where X > 0)
✅ Sidebar shows date groups (Today, Yesterday, etc.)
✅ Sessions are clickable
✅ Clicking session loads messages
✅ Search filters sessions
✅ Delete button appears on hover

## Still Not Working?

1. Check all console errors
2. Check Network tab for failed requests
3. Verify backend logs for errors
4. Test with test-api.html
5. Try creating a new session by sending a message
6. Check Firebase Firestore directly

## Contact

If issue persists after following this guide, provide:
- Browser console logs
- Network tab screenshot
- Backend logs
- Environment details (OS, Node version, Java version)
