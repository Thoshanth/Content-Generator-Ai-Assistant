# Follow-Up Questions - Quick Setup Guide

## 🚀 Quick Start

### 1. Backend Setup (AI Service)

The follow-up questions feature has been integrated into the AI service. No additional setup required!

**Files Added/Modified:**
- ✅ `ai-service/routers/followup.py` - New router for follow-up questions
- ✅ `ai-service/services/followup_service.py` - Already exists
- ✅ `ai-service/main.py` - Updated to include followup router

**Start the AI Service:**
```bash
cd ai-service
python main.py
```

The service will run on `http://localhost:8000`

### 2. Frontend Setup

**Files Added/Modified:**
- ✅ `frontend/src/components/chat/FollowUpQuestions.jsx` - New component
- ✅ `frontend/src/pages/ChatPage.jsx` - Updated with follow-up logic
- ✅ `frontend/src/services/api.js` - Updated API method

**Start the Frontend:**
```bash
cd frontend
npm install  # If not already done
npm run dev
```

The frontend will run on `http://localhost:5173`

### 3. Test the Integration

**Option A: Manual Testing**
1. Open browser to `http://localhost:5173`
2. Login to your account
3. Navigate to Chat page
4. Select a content type (e.g., "Resume")
5. You should see follow-up questions appear below the chat window
6. Click any question to auto-fill and send

**Option B: API Testing**
```bash
cd ai-service
python test_followup_endpoint.py
```

This will test all content types and verify the API is working.

## 📋 Verification Checklist

### Backend Verification
- [ ] AI service starts without errors
- [ ] Navigate to `http://localhost:8000/docs` (FastAPI docs)
- [ ] See `/followup/questions` endpoint listed
- [ ] See `/followup/templates/{content_type}` endpoint listed

### Frontend Verification
- [ ] Frontend starts without errors
- [ ] No console errors in browser
- [ ] Follow-up questions component renders
- [ ] Questions appear when content type is selected
- [ ] Questions disappear when message is sent
- [ ] Clicking a question sends it as a message

## 🎨 How It Works

### User Flow
```
1. User selects content type (e.g., "Resume")
   ↓
2. Frontend calls: POST /followup/questions
   {
     "content_type": "resume",
     "initial_prompt": "",
     "user_id": "user123"
   }
   ↓
3. Backend generates 5-8 contextual questions
   ↓
4. Questions appear in elegant card layout
   ↓
5. User clicks a question
   ↓
6. Question auto-fills input and sends
   ↓
7. Questions disappear, AI responds
```

### When Questions Appear
- ✅ Chat is empty (no messages)
- ✅ Only one user message exists
- ✅ Content type is NOT "general"
- ❌ After AI has responded
- ❌ During active conversation

## 🎯 Content Types Supported

| Content Type | Questions | Example |
|-------------|-----------|---------|
| Resume | 8 questions | Name, email, education, skills, experience |
| Cover Letter | 5 questions | Company, position, qualifications, motivation |
| Blog Post | 5 questions | Topic, audience, key points, tone |
| Email | 5 questions | Recipient, purpose, action, context |
| Social Media | 5 questions | Platform, message, audience, hashtags |
| General | 5 questions | Topic, purpose, audience, key points |

## 🔧 Troubleshooting

### Questions Not Appearing

**Problem:** Follow-up questions don't show up

**Solutions:**
1. Check content type is not "general"
2. Verify chat is empty or has only one message
3. Open browser console and check for errors
4. Verify AI service is running: `curl http://localhost:8000/health`

### API Errors

**Problem:** 500 error when loading questions

**Solutions:**
1. Check AI service logs for errors
2. Verify at least one AI provider is configured
3. Test endpoint directly:
```bash
curl -X POST http://localhost:8000/followup/questions \
  -H "Content-Type: application/json" \
  -d '{"content_type":"resume","initial_prompt":"","user_id":"test"}'
```

### Styling Issues

**Problem:** Questions look broken or unstyled

**Solutions:**
1. Clear browser cache
2. Verify Tailwind CSS is working
3. Check framer-motion is installed: `npm list framer-motion`
4. Rebuild frontend: `npm run build`

## 🎨 Customization

### Add New Content Type Questions

Edit `ai-service/services/followup_service.py`:

```python
FOLLOWUP_TEMPLATES = {
    "your_new_type": [
        "Question 1?",
        "Question 2?",
        "Question 3?",
        "Question 4?",
        "Question 5?",
    ]
}
```

### Modify Question Styling

Edit `frontend/src/components/chat/FollowUpQuestions.jsx`:

```jsx
// Change colors
className="bg-surface-raised border-peach/50"

// Change animations
transition={{ delay: index * 0.1 }}

// Change grid layout
className="grid grid-cols-1 md:grid-cols-3 gap-3"
```

### Change Number of Questions

Edit `ai-service/services/followup_service.py`:

```python
# Show more/fewer questions
return template_questions[:8]  # Change from 5 to 8
```

## 📊 Testing Results

Run the test script to verify everything works:

```bash
cd ai-service
python test_followup_endpoint.py
```

**Expected Output:**
```
🚀 Starting Follow-Up Questions Tests

============================================================
Testing Follow-Up Questions Endpoint
============================================================

────────────────────────────────────────────────────────────
Test: Resume - No initial prompt
────────────────────────────────────────────────────────────
✅ Success!
Content Type: resume
Number of Questions: 8

Questions:
  1. What is your full name?
  2. What is your email address and phone number?
  3. What is your current education level and institution?
  ...
```

## 🎉 Success Indicators

You'll know it's working when:
1. ✅ No errors in AI service console
2. ✅ No errors in frontend console
3. ✅ Questions appear when selecting content type
4. ✅ Questions have smooth animations
5. ✅ Clicking questions sends them as messages
6. ✅ Questions disappear after sending
7. ✅ AI responds to the question

## 📚 Additional Resources

- **Full Documentation:** `FOLLOWUP_QUESTIONS_INTEGRATION.md`
- **API Docs:** `http://localhost:8000/docs`
- **Component Code:** `frontend/src/components/chat/FollowUpQuestions.jsx`
- **Backend Service:** `ai-service/services/followup_service.py`

## 🆘 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review browser console for errors
3. Check AI service logs
4. Verify all dependencies are installed
5. Ensure both services are running

## 🎯 Next Steps

After setup is complete:
1. Test with different content types
2. Customize questions for your use case
3. Adjust styling to match your brand
4. Add analytics to track question usage
5. Implement multi-turn question flows

---

**Setup Time:** ~5 minutes  
**Difficulty:** Easy  
**Prerequisites:** AI service and frontend already running

Happy coding! 🚀
