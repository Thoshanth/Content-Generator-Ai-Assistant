# Authentication Issue Debug Guide

## Problem
The image generation endpoint is receiving anonymous authentication instead of the JWT token.

## Debug Steps

### 1. Check if User is Logged In
Open browser console (F12) and run:
```javascript
console.log('Token:', localStorage.getItem('token'));
console.log('User:', localStorage.getItem('user'));
```

**Expected**: Should show a JWT token and user data
**If null**: User needs to log in first

### 2. Check Network Request
1. Open browser DevTools (F12)
2. Go to Network tab
3. Click the image generation button
4. Look for the `/api/images/generate` request
5. Check the **Request Headers** section
6. Look for: `Authorization: Bearer <token>`

**If missing**: The frontend is not sending the token
**If present but still failing**: The token might be expired or invalid

### 3. Test Token Validity
In browser console:
```javascript
const token = localStorage.getItem('token');
fetch('http://localhost:8080/api/user/profile', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(r => r.json())
.then(d => console.log('Profile:', d))
.catch(e => console.error('Error:', e));
```

**Expected**: Should return user profile
**If 401**: Token is expired or invalid - need to log in again

### 4. Check Token Expiration
JWT tokens expire after 15 minutes (900000ms). If you logged in more than 15 minutes ago, you need to:
- Log out and log in again
- Or implement token refresh (already available in backend)

## Quick Fixes

### Fix 1: Log Out and Log In Again
1. Click logout in the app
2. Log in with your credentials
3. Try image generation again

### Fix 2: Clear Storage and Re-login
In browser console:
```javascript
localStorage.clear();
location.reload();
```
Then log in again.

### Fix 3: Check if ImageGenerator Component is Getting Token
The issue might be in how the ImageGenerator component fetches data. Let me check the code...

## Code Review

### ImageGenerator.jsx - Lines 28-40
```javascript
const fetchStyles = async () => {
  try {
    const response = await fetch('http://localhost:8080/api/images/styles', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    })
    // ...
  }
}
```

This looks correct. The token should be sent.

### ChatPage.jsx - Lines 93-102
```javascript
const response = await fetch('http://localhost:8080/api/images/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${localStorage.getItem('token')}`
  },
  body: JSON.stringify(imageRequest)
})
```

This also looks correct.

## Most Likely Causes

1. **User Not Logged In**: The most common cause
2. **Token Expired**: JWT tokens expire after 15 minutes
3. **Token Not Saved**: Login might have failed to save token
4. **CORS Issue**: Browser might be blocking the request

## Solution

### Immediate Fix
**Log out and log in again** - This will get a fresh token.

### Long-term Fix
We should add better error handling in the frontend to:
1. Check if token exists before making requests
2. Redirect to login if token is missing
3. Show clear error messages
4. Implement automatic token refresh

## Testing

After logging in, test with this in browser console:
```javascript
// Test image generation
const token = localStorage.getItem('token');
console.log('Token exists:', !!token);
console.log('Token length:', token?.length);

// Test API call
fetch('http://localhost:8080/api/images/usage', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(r => r.json())
.then(d => console.log('Usage:', d))
.catch(e => console.error('Error:', e));
```

## Backend Logs to Check

The backend logs show:
```
No user ID extracted or authentication already exists
Current authentication: null
Set SecurityContextHolder to anonymous SecurityContext
```

This confirms the token is either:
- Not being sent
- Invalid format
- Expired
- Not being parsed correctly

## Next Steps

1. **Verify you're logged in** - Check if you see your username in the UI
2. **Check browser console** for any errors
3. **Try logging out and back in**
4. **Check Network tab** to see if Authorization header is present
5. **If still failing**, we may need to add token refresh logic
