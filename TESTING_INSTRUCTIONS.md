# Testing Instructions - Chat History Integration

## Current Status
✅ Frontend UI upgraded with animations and date grouping
✅ Backend API endpoints working
✅ Authentication flow working
⏳ Need to verify data integration

## How to Test Chat History

### Step 1: Ensure Services are Running

**Backend:**
```bash
cd backend
./run.bat  # Should be running on port 8080
```

**Frontend:**
```bash
cd frontend
npm run dev  # Should be running on port 5173
```

### Step 2: Open Browser
1. Open http://localhost:5173
2. Open DevTools (F12)
3. Go to Console tab

### Step 3: Login or Register
1. If you don't have an account:
   - Click "Sign In" → "Create Account"
   - Fill in details and register
   
2. If you have an account:
   - Click "Sign In"
   - Enter email and password
   - Click "Login"

### Step 4: Check Console Logs
After login, you should see in console:
```
ChatPage: Loading sessions for authenticated user
ChatContext: Fetching sessions from API...
ChatContext: Received sessions data: [...]
ChatContext: Setting X sessions
Sidebar: Sessions updated: X [...]
```

### Step 5: Create First Session (If Empty)
If you see "Setting 0 sessions", you need to create a session:

1. In the chat input, type any message (e.g., "Hello")
2. Click Send button
3. Wait for AI response
4. Check sidebar - you should now see a session appear

### Step 6: Verify Session Appears
After sending a message:
- Sidebar should show the session under "Today"
- Session title should be visible
- Clicking the session should load messages

### Step 7: Test Features

**Search:**
- Type in search box to filter sessions

**Refresh:**
- Click refresh icon to reload sessions

**Delete:**
- Hover over a session
- Click trash icon to delete

**Date Grouping:**
- Sessions should be grouped by:
  - Today
  - Yesterday  
  - This Week
  - This Month
  - Older

## Troubleshooting

### Issue: "Setting 0 sessions"
**Cause:** No sessions exist yet
**Solution:** Send a message to create first session

### Issue: Console shows error "Failed to load sessions"
**Possible causes:**
1. Backend not running
2. Not logged in
3. Token expired
4. CORS issue

**Check:**
```javascript
// In browser console
localStorage.getItem('accessToken')  // Should return a token
```

**Solution:**
- Logout and login again
- Restart backend
- Check backend logs for errors

### Issue: Sessions not grouped by date
**Cause:** Invalid timestamp format
**Check console for:** "ChatContext: Received sessions data"
**Look for:** `updatedAt` field with `seconds` property

### Issue: Network error
**Check:**
1. Backend running: http://localhost:8080
2. Frontend .env file: `VITE_API_BASE_URL=http://localhost:8080/api`
3. Network tab in DevTools for failed requests

## Expected Behavior

### On Login:
1. ✅ Redirects to /chat
2. ✅ Sidebar opens automatically
3. ✅ Calls loadSessions()
4. ✅ Displays sessions or empty state

### On Send Message:
1. ✅ Message appears in chat
2. ✅ AI responds
3. ✅ Session created (if new)
4. ✅ Session appears in sidebar
5. ✅ Session grouped by date

### On Refresh:
1. ✅ Loading indicator shows
2. ✅ Sessions reload from API
3. ✅ Sidebar updates

### On Delete:
1. ✅ Confirmation dialog
2. ✅ Session removed from sidebar
3. ✅ If current session, clears chat

## Console Commands for Testing

### Check Authentication:
```javascript
localStorage.getItem('accessToken')
```

### Manually Trigger Session Load:
```javascript
// This won't work directly, but you can click the refresh button in sidebar
```

### Check Current Sessions State:
```javascript
// Open React DevTools
// Find ChatContext
// Check sessions state
```

## API Testing

### Test Sessions Endpoint Directly:
```bash
# Get your token from localStorage first
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/chat/sessions
```

Expected response:
```json
[
  {
    "id": "session-id",
    "userId": "user-id",
    "title": "Chat title",
    "contentType": "general",
    "createdAt": { "seconds": 1234567890, "nanos": 0 },
    "updatedAt": { "seconds": 1234567890, "nanos": 0 },
    "messages": null
  }
]
```

## Success Criteria

✅ After login, console shows "Loading sessions"
✅ After sending message, session appears in sidebar
✅ Sessions are grouped by date (Today, Yesterday, etc.)
✅ Search filters sessions
✅ Delete removes session
✅ Refresh reloads sessions
✅ Daily reset indicator shows countdown
✅ Animations are smooth

## What to Report

If it's not working, please provide:

1. **Console logs** (copy all logs starting with "ChatPage:" or "ChatContext:")
2. **Network tab** (screenshot of /chat/sessions request)
3. **Steps taken** (what you clicked/typed)
4. **Expected vs Actual** (what should happen vs what happened)

## Quick Test Scenario

1. ✅ Open http://localhost:5173
2. ✅ Login with credentials
3. ✅ Open console (F12)
4. ✅ Look for "Loading sessions" log
5. ✅ Type "Hello" and send
6. ✅ Wait for response
7. ✅ Check sidebar for new session
8. ✅ Verify session appears under "Today"
9. ✅ Click refresh icon
10. ✅ Verify session still there

## Notes

- First time users will have 0 sessions (this is normal)
- Sessions are created when you send your first message
- The backend automatically creates a session if none exists
- Session title is auto-generated from first message
- Daily message count resets at midnight
- History persists indefinitely

---

**If everything works:** You should see your chat sessions organized by date in the sidebar! 🎉

**If something doesn't work:** Check the troubleshooting section and provide the requested information.
